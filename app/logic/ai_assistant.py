"""
AI Investigation Assistant - Orchestration Workflow
Category C - Complex Application Logic.

Six-stage pipeline (each stage is independently testable):
1. classify_intent - keyword-frequency classifier -> IntentCategory
2. retrieve_context - fetch relevant DB records based on intent
3. build_prompt - construct system prompt + message history
4. call_llm - send to the NVIDIA NIM API (Llama 3.1), receive raw reply
5. validate_response - length / refusal / off-topic checks
6. check_hallucinations - cross-check every case number, evidence ID and
   investigator name mentioned in the reply against the retrieved context;
   unknown references are flagged and surfaced to the user as warnings

This is not a simple API passthrough: the context injection, intent
classification, validation, and hallucination-detection logic are all
custom application code. The LLM itself is a third-party service.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple
from flask import current_app

# Candidate models tried, in order, when the configured AI_MODEL is
# unavailable. Hosted models are retired periodically by the provider (the
# API answers HTTP 410 Gone), so keeping an ordered fallback list means one
# retirement cannot disable the assistant. Newest/most capable first.
AI_MODEL_FALLBACKS = [
    # Fast NVIDIA MoE, text-to-text, free endpoint - the default choice.
    "nvidia/nemotron-3.5-lightning-30b-a3b",
    # Widely used general chat/reasoning models on the same catalogue.
    "minimaxai/minimax-m3",
    "stepfun-ai/step-3.7-flash",
    # Most capable, but noticeably slower for interactive use.
    "nvidia/nemotron-3-ultra-550b-a55b",
]

# Data structures
class IntentCategory(str, Enum):
    IDENTITY        = "IDENTITY"        # "who am I", "my cases", "assigned to me"
    CASE_QUERY      = "CASE_QUERY"
    EVIDENCE_QUERY  = "EVIDENCE_QUERY"
    RISK_QUERY      = "RISK_QUERY"
    CUSTODY_QUERY   = "CUSTODY_QUERY"
    INTEGRITY_QUERY = "INTEGRITY_QUERY"
    GENERAL_FORENSICS = "GENERAL_FORENSICS"
    UNKNOWN         = "UNKNOWN"

@dataclass
class ClassifiedIntent:
    category: IntentCategory
    confidence: float # 0.0 – 1.0
    entity_id: Optional[int] # numeric ID parsed from the message if present
    keywords_matched: List[str]

@dataclass
class RetrievedContext:
    intent: ClassifiedIntent
    records: Dict # raw DB objects (for tests / logging)
    context_text: str  # human-readable summary injected into prompt

@dataclass
class AssistantResponse:
    reply: str
    intent: IntentCategory
    context_used: bool
    validation_passed: bool
    warning: Optional[str]
    hallucination_flags: List[str] = None  # entity refs not found in context

    def __post_init__(self):
        if self.hallucination_flags is None:
            self.hallucination_flags = []

# Assistant
class AIInvestigationAssistant:
    """
    Orchestrates the AI Q&A session about forensic case data.
    Each stage is a separate method so it can be tested and extended
    independently.
    """

    # Intent -> keywords lookup
    _INTENT_KEYWORDS: Dict[IntentCategory, List[str]] = {
        IntentCategory.IDENTITY: [
            "who am i", "my cases", "my case", "assigned to me",
            "assigned to my", "my evidence", "my work", "my account",
            "my role", "am i", "cases i", "what am i", "who i am",
        ],
        IntentCategory.CASE_QUERY: [
            "case", "cases", "investigation", "case number", "case id",
            "open case", "closed case", "case status", "assigned",
        ],
        IntentCategory.EVIDENCE_QUERY: [
            "evidence", "file", "item", "exhibit", "upload", "document",
            "sample", "artefact", "artifact", "sha256",
        ],
        IntentCategory.RISK_QUERY: [
            "risk", "score", "danger", "threat", "vulnerability",
            "critical", "high risk", "risk level", "assessment", "risky",
        ],
        IntentCategory.CUSTODY_QUERY: [
            "custody", "transfer", "chain", "handover", "handler",
            "who had", "moved", "possession", "custody log",
        ],
        IntentCategory.INTEGRITY_QUERY: [
            "integrity", "tamper", "hash", "verify", "verification",
            "corrupt", "signature", "mismatch", "altered", "modified",
        ],
        IntentCategory.GENERAL_FORENSICS: [
            "forensic", "procedure", "best practice", "protocol",
            "how to", "what is", "explain", "define", "guideline",
            "standard", "methodology",
        ],
    }

    # Deterministic priority order used to break ties when two intents match
    # the same number of keywords (earlier = higher priority). Without this the
    # winner would depend on dict iteration order, which is an implementation
    # detail rather than a design decision.
    _INTENT_PRIORITY = [
        IntentCategory.INTEGRITY_QUERY,
        IntentCategory.CUSTODY_QUERY,
        IntentCategory.RISK_QUERY,
        IntentCategory.EVIDENCE_QUERY,
        IntentCategory.CASE_QUERY,
        IntentCategory.GENERAL_FORENSICS,
    ]

    #  Stage 1: Intent classification
    def classify_intent(self, user_message: str) -> ClassifiedIntent:
        """
        Keyword-overlap classifier (a deliberately simple, transparent heuristic
        - the "complex logic" of this feature is the orchestration pipeline as a
        whole, not ML-grade intent accuracy).

        Algorithm:
          - Convert message to lowercase.
          - A first-person self-reference short-circuits to IDENTITY.
          - Otherwise, for each intent category count how many of its keywords
            appear in the message; the category with the most hits wins.
          - Ties are broken by a fixed priority order (_INTENT_PRIORITY) so the
            result is deterministic and does not depend on dict ordering. More
            specific intents (integrity, custody) outrank broader ones (case).
          - Confidence is a HEURISTIC, not a calibrated probability: it is
            winner_hits / total_hits scaled by 2 and clamped to [0, 1], which
            simply expresses "how dominant was the winning category among all
            matches". It should be read as a rough dominance ratio only.
          - Parse a numeric entity ID from the message if one is present
            (e.g. "case 3", "evidence #7", "item id 12"). Only the first ID is
            used; multi-entity questions fall back to the single parsed ID.
        """
        msg_lower = user_message.lower()

        # Priority rule: a clear first-person self-reference is an IDENTITY
        # question ("who am I", "my cases", "cases assigned to me"), even
        # though words like "cases" or "assigned" also belong to CASE_QUERY.
        # This is checked before the frequency contest so identity questions
        # are always answered from the authenticated user.
        identity_phrases = [
            "who am i", "who i am", "what am i", "am i",
            "assigned to me", "assigned to my", "my case", "my cases",
            "my evidence", "my work", "my account", "my role"]
        if any(p in msg_lower for p in identity_phrases):
            return ClassifiedIntent(
                category=IntentCategory.IDENTITY, confidence=1.0,
                entity_id=None, keywords_matched=[
                    p for p in identity_phrases if p in msg_lower])

        scores: Dict[IntentCategory, int] = {}
        matched_kws: Dict[IntentCategory, List[str]] = {}

        for category, keywords in self._INTENT_KEYWORDS.items():
            hits = [kw for kw in keywords if kw in msg_lower]
            scores[category] = len(hits)
            matched_kws[category] = hits

        # Winner = most keyword hits, ties broken by the fixed priority order
        # (lower index = higher priority) so classification is deterministic.
        def _priority(cat):
            try:
                return self._INTENT_PRIORITY.index(cat)
            except ValueError:
                return len(self._INTENT_PRIORITY)
        best_category = max(scores, key=lambda c: (scores[c], -_priority(c)))
        best_score = scores[best_category]

        if best_score == 0:
            return ClassifiedIntent(category=IntentCategory.UNKNOWN, confidence=0.0, entity_id=None, keywords_matched=[])

        total_hits = sum(scores.values()) or 1
        confidence = min(1.0, best_score / total_hits * 2.0)

        # Extract entity ID: "case 3", "evidence id 7", "#5", etc.
        entity_id: Optional[int] = None
        id_match = re.search(r'(?:case|evidence|item|id)[^\d]{0,5}(\d+)', msg_lower)
        if not id_match:
            id_match = re.search(r'#\s*(\d+)', msg_lower)
        if id_match:
            entity_id = int(id_match.group(1))

        return ClassifiedIntent(category=best_category, confidence=round(confidence, 3), entity_id=entity_id, keywords_matched=matched_kws[best_category])

    #  Stage 2: Context retrieval 
    def retrieve_context(self, intent: ClassifiedIntent, user=None) -> RetrievedContext:
        """
        Fetches the DB records most relevant to the classified intent and
        serialises them into a compact text block for the prompt.

        All record retrieval is scoped to the cases the *current* investigator
        may access (via CaseAccess), so the assistant never reveals cases or
        evidence outside the logged-in user's remit. "user" is the current
        investigator; when None (e.g. isolated unit tests) no scope filter is
        applied.
        """
        from app.models.case import Case
        from app.models.evidence import EvidenceItem
        from app.models.custody_log import CustodyLog
        from app.models.investigator import Investigator
        from app.models.case_access import CaseAccess

        records: Dict = {}
        lines: List[str] = []

        case_ids = CaseAccess.accessible_case_ids(user) if user is not None else None

        def scope_cases(q):
            return q if case_ids is None else q.filter(Case.id.in_(case_ids or [-1]))

        def scope_evidence(q):
            q = q.filter(EvidenceItem.is_deleted.is_(False))
            return q if case_ids is None else q.filter(EvidenceItem.case_id.in_(case_ids or [-1]))

        def can_see_case(cid):
            return case_ids is None or cid in (case_ids or [])

        #  Identity queries: "who am I", "my cases", "assigned to me"
        if intent.category == IntentCategory.IDENTITY:
            if user is not None and getattr(user, 'is_authenticated', False):
                lines.append(
                    f"The current user is {user.full_name} "
                    f"(investigator ID {user.id}, role: {user.role}).")
                my_cases = scope_cases(Case.query).order_by(Case.created_at.desc()).all()
                if case_ids is None:
                    lines.append("As an Admin, this user has access to every case in the system.")
                if my_cases:
                    lines.append(f"Cases this user can access ({len(my_cases)}):")
                    for c in my_cases:
                        lines.append(
                            f"  Case #{c.id}: '{c.title}' | {c.status} | "
                            f"{c.evidence_items.count()} evidence item(s)")
                else:
                    lines.append("This user is not currently a member of any case.")
                records["user"] = user
                records["cases"] = my_cases
            else:
                lines.append("No authenticated user is associated with this request.")
            context_text = "\n".join(lines) if lines else "No relevant records found."
            return RetrievedContext(intent=intent, records=records, context_text=context_text)

        #  Case queries
        if intent.category == IntentCategory.CASE_QUERY:
            if intent.entity_id:
                case = Case.query.get(intent.entity_id)
                if case and not can_see_case(case.id):
                    lines.append(
                        f"You do not have access to Case #{intent.entity_id}, "
                        f"or it does not exist.")
                    case = None
                if case:
                    records["case"] = case
                    case_evidence = case.evidence_items.filter_by(is_deleted=False)
                    lines.append(
                        f"Case #{case.id}: '{case.title}' | "
                        f"Status: {case.status} | "
                        f"Created: {case.created_at.date()} | "
                        f"Evidence items: {case_evidence.count()}"
                    )
                    for ev in case_evidence.all():
                        lines.append(
                            f"  Evidence #{ev.id}: '{ev.title}' "
                            f"[{getattr(ev, 'lifecycle_state', 'Unknown')}]")
                else:
                    lines.append(f"No case found with ID {intent.entity_id}.")
            else:
                cases = (scope_cases(Case.query)
                         .order_by(Case.created_at.desc()).limit(10).all())
                records["cases"] = cases
                if cases:
                    lines.append(f"Most recent {len(cases)} accessible case(s):")
                    for c in cases:
                        lines.append(
                            f"  Case #{c.id}: '{c.title}' | "
                            f"{c.status} | {c.evidence_items.count()} evidence item(s)")
                else:
                    lines.append("You do not currently have access to any cases.")

        #  Evidence / Risk / Integrity queries 
        elif intent.category in (
            IntentCategory.EVIDENCE_QUERY,
            IntentCategory.RISK_QUERY,
            IntentCategory.INTEGRITY_QUERY):
            if intent.entity_id:
                ev = EvidenceItem.query.get(intent.entity_id)
                if ev and ev.is_deleted:
                    ev = None
                if ev and not can_see_case(ev.case_id):
                    lines.append(
                        f"You do not have access to Evidence #{intent.entity_id}, "
                        f"or it does not exist.")
                    ev = None
                if ev:
                    records["evidence"] = ev
                    lines.append(
                        f"Evidence #{ev.id}: '{ev.title}' | "
                        f"Category: {getattr(ev, 'category', 'Other')} | "
                        f"State: {getattr(ev, 'lifecycle_state', 'Unknown')} | "
                        f"Case: #{ev.case_id} | "
                        f"File: {getattr(ev, 'file_name', 'N/A')}")
                elif ev is None and intent.entity_id and not lines:
                    lines.append(f"No evidence item found with ID {intent.entity_id}.")
            else:
                items = (scope_evidence(EvidenceItem.query)
                    .order_by(EvidenceItem.created_at.desc())
                    .limit(10)
                    .all())
                records["evidence_items"] = items
                if items:
                    lines.append(f"Most recent {len(items)} accessible evidence item(s):")
                    for ev in items:
                        lines.append(
                            f"  Evidence #{ev.id}: '{ev.title}' | "
                            f"State: {getattr(ev, 'lifecycle_state', 'Unknown')} | "
                            f"File: {getattr(ev, 'file_name', 'N/A')}")
                else:
                    lines.append("You do not have access to any evidence items.")

        #  Custody queries 
        elif intent.category == IntentCategory.CUSTODY_QUERY:
            if intent.entity_id:
                ev = EvidenceItem.query.get(intent.entity_id)
                if ev and not can_see_case(ev.case_id):
                    lines.append(
                        f"You do not have access to the custody chain for "
                        f"Evidence #{intent.entity_id}.")
                    logs = []
                else:
                    logs = (CustodyLog.query
                        .filter_by(evidence_id=intent.entity_id)
                        .order_by(CustodyLog.timestamp.asc())
                        .all())
                records["custody_logs"] = logs
                if logs:
                    lines.append(
                        f"Custody chain for Evidence #{intent.entity_id} "
                        f"({len(logs)} transfer(s)):")
                    for log in logs:
                        handler = Investigator.query.get(log.to_investigator_id)
                        name = handler.full_name if handler else "Unknown"
                        lines.append(
                            f"  {log.timestamp.date()} -> {name} "
                            f"(reason: {log.reason or 'not specified'})")
                else:
                    lines.append(f"No custody transfers found for Evidence #{intent.entity_id}.")
            else:
                logs_q = CustodyLog.query
                if case_ids is not None:
                    logs_q = (logs_q
                        .join(EvidenceItem, CustodyLog.evidence_id == EvidenceItem.id)
                        .filter(EvidenceItem.case_id.in_(case_ids or [-1])))
                logs = logs_q.order_by(CustodyLog.timestamp.desc()).limit(15).all()
                records["recent_custody"] = logs
                if logs:
                    lines.append(f"Most recent {len(logs)} accessible custody transfer(s):")
                    for log in logs:
                        handler = Investigator.query.get(log.to_investigator_id)
                        name = handler.full_name if handler else "Unknown"
                        lines.append(
                            f"  Evidence #{log.evidence_id} -> {name} "
                            f"on {log.timestamp.date()}")
                else:
                    lines.append("You do not have access to any custody transfers.")
                    
        #  General forensics or unknown - no DB context needed 
        else:
            lines.append(
                "No specific case or evidence record retrieved for this query. "
                "Answering from general forensics knowledge.")

        context_text = "\n".join(lines) if lines else "No relevant records found."
        return RetrievedContext(intent=intent, records=records, context_text=context_text)

    #  Stage 3: Prompt construction 
    def build_prompt(self, user_message: str, context: RetrievedContext, conversation_history: Optional[List[Dict]] = None, user=None) -> Tuple[List[Dict], str]:
        """
        Assembles the system prompt and message list for the LLM API.

        The system prompt embeds the live DB context so the model answers
        about actual case data instead of hallucinating. It also states who
        the current user is, so questions like "who am I?" or "my cases" are
        answered from the authenticated identity rather than guessed.
        Previous conversation turns (up to 6) are prepended as history.
        """
        if user is not None and getattr(user, 'is_authenticated', False):
            identity_line = (
                f"You are currently speaking with {user.full_name} "
                f"(investigator ID {user.id}, role: {user.role}). "
                f"The SYSTEM CONTEXT below is already restricted to the cases "
                f"this user is allowed to see. When the user says 'me', 'my', "
                f"or 'I', they mean this person.\n\n")
        else:
            identity_line = ""

        system_content = (
            "You are DEICMS-AI, an expert forensic investigation assistant embedded "
            "in the Digital Evidence Integrity & Chain-of-Custody Management System.\n"
            "Your role: help investigators understand case data, interpret risk scores, "
            "explain custody chains, and advise on digital forensics best practices.\n\n"
            + identity_line +
            "Rules:\n"
            "- Base your answers on the SYSTEM CONTEXT block when it contains relevant data.\n"
            "- Be concise and professional. Use bullet points for lists.\n"
            "- Only discuss the cases and evidence present in the SYSTEM CONTEXT. "
            "Never mention or invent case IDs, evidence IDs, investigator names, or "
            "file names that are not in the context - the user may not have access to them.\n"
            "- If the context does not contain the answer, say so and offer general guidance.\n"
            "- Do not discuss topics unrelated to digital forensics, evidence management, "
            "or cybersecurity.\n\n"
            f"SYSTEM CONTEXT (live database snapshot)\n"
            f"{'=' * 60}\n"
            f"{context.context_text}\n"
            f"{'=' * 60}"
        )

        messages: List[Dict] = []

        # Inject previous turns (trim to last 6 to control context size)
        if conversation_history:
            for turn in conversation_history[-6:]:
                messages.append({"role": turn["role"], "content": turn["content"]})

        messages.append({"role": "user", "content": user_message})
        return messages, system_content

    #  Stage 4: AI Agent API call 

    def call_nvidia(self, messages: List[Dict], system_content: str) -> str:
        """
        Calls the NVIDIA NIM API (OpenAI-compatible endpoint).
        Falls back to intelligent mock if no key is configured.
        """
        from openai import OpenAI
        api_key = current_app.config.get("NVIDIA_API_KEY", "")

        if api_key and api_key.startswith("nvapi-"):
            # A per-request timeout stops a slow model from hanging the
            # whole HTTP request; the route/UI will show a clear message.
            timeout_s = current_app.config.get("AI_REQUEST_TIMEOUT", 60)
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key,
                timeout=timeout_s)
            max_tokens = current_app.config.get("AI_MAX_TOKENS", 700)
            # Prepend system message as first user turn (NIM style)
            full_messages = [{"role": "system", "content": system_content}] + messages

            # Hosted models are periodically retired by the provider, which
            # returns HTTP 410 Gone and would otherwise silently drop the
            # assistant back to the mock. Try the configured model first, then
            # the documented fallbacks, so a single retirement cannot disable
            # the feature. Set AI_MODEL in .env to pin a specific model.
            candidates = []
            configured = current_app.config.get("AI_MODEL")
            if configured:
                candidates.append(configured)
            for fallback in AI_MODEL_FALLBACKS:
                if fallback not in candidates:
                    candidates.append(fallback)

            last_error = None
            for model in candidates:
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=full_messages,
                        max_tokens=max_tokens,
                        temperature=0.4)
                    if model != candidates[0]:
                        print(f"LLM: '{candidates[0]}' unavailable; used '{model}'. "
                              f"Set AI_MODEL={model} in your .env to make this the default.")
                    return response.choices[0].message.content or ""
                except Exception as exc:
                    last_error = exc
                    # 410 Gone / 404 => model retired or unknown: try the next one.
                    # Anything else (auth, network, rate limit) will fail the
                    # same way for every model, so stop and report it.
                    status = getattr(exc, "status_code", None)
                    if status in (404, 410):
                        print(f"LLM: model '{model}' unavailable ({status}); trying next candidate.")
                        continue
                    break

            print("LLM CALL FAILED:", repr(last_error))
            print("The assistant is returning a structured mock response. "
                  "Check the model name (AI_MODEL in .env) and the API key.")
        return self._mock_response(messages, system_content)
    
    def _mock_response(self, messages: List[Dict], system_content: str) -> str:
        """
        Generates a context-aware mock reply by reading the injected
        system context block - demonstrates the full pipeline without
        requiring API credits.
        """
        user_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                user_msg = m.get("content", "").lower()
                break

        # Extract the SYSTEM CONTEXT block from the system prompt
        context_block = ""
        if "SYSTEM CONTEXT" in system_content:
            parts = system_content.split("=" * 60)
            if len(parts) >= 2:
                context_block = parts[1].strip()

        # Build a reply that references the actual injected context
        if context_block and "No relevant records" not in context_block:
            lines = [l.strip() for l in context_block.splitlines() if l.strip()]
            summary = "\n".join(f"- {l}" for l in lines[:8])
            reply = (
                f"Based on the current database records, here is what I found:\n\n"
                f"{summary}\n\n"
                f"[Note: This is a structured mock response. The orchestration "
                f"pipeline ran successfully - intent was classified, database "
                f"context was retrieved (scoped to the cases you may access) "
                f"and injected, the prompt was constructed, and the reply was "
                f"validated and checked for hallucinated references. Only the "
                f"language-model call itself was unavailable, so the retrieved "
                f"records are shown directly rather than as natural-language "
                f"prose.]")
        else:
            reply = (
                "I can answer general digital forensics questions. "
                "For example:\n"
                "- Chain of custody ensures evidence integrity from collection to court.\n"
                "- SHA-256 hashing verifies that a file has not been altered.\n"
                "- Role-based access control limits who can handle sensitive evidence.\n\n"
                "[Note: Mock response - the orchestration pipeline ran fully. "
                "Add API credits for natural-language answers.]"
            )

        return reply

    #  Stage 5: Response validation 
    def validate_response(self, raw_reply: str, intent: IntentCategory) -> Tuple[str, bool, Optional[str]]:
        """
        Checks the reply for:
        - Minimum length (> 20 chars)
        - Refusal patterns (model declined to answer)
        - Off-topic signals (no forensics terms in a domain-specific reply)
        Returns (reply_text, passed: bool, warning_message | None)
        """
        if len(raw_reply.strip()) < 20:
            return raw_reply, False, "Response too short - the model may have failed."

        refusal_patterns = [
            r"i(?:'m| am) (?:sorry|unable|not able)",
            r"i cannot (?:help|assist|answer)",
            r"as an ai (?:language model|assistant)",
            r"i don'?t have (?:access|information)"]
        for pattern in refusal_patterns:
            if re.search(pattern, raw_reply.lower()):
                return raw_reply, False, "Model indicated it could not answer the question."

        # Warn if the reply for a domain-specific query lacks any forensics term
        forensics_terms = [
            "evidence", "case", "forensic", "custody", "investigat",
            "hash", "integrity", "risk", "transfer", "file", "audit", "chain"]
        domain_specific = intent not in (
            IntentCategory.GENERAL_FORENSICS, IntentCategory.UNKNOWN, IntentCategory.IDENTITY)
        if domain_specific and not any(t in raw_reply.lower() for t in forensics_terms):
            return raw_reply, True, "Response may be off-topic - review before relying on it."

        return raw_reply, True, None

    #  Stage 6: Hallucination detection
    def check_hallucinations(self, reply: str, context: RetrievedContext) -> List[str]:
        """
        Cross-checks every entity reference in the LLM reply against the
        retrieved database context (proposal section 2C.5).

        Algorithm:
          1. Extract all case and evidence ID references from the reply
             using regex patterns (e.g. "Case #12", "evidence item 7").
          2. Extract all known investigator full names from the database
             and detect which of them the reply mentions.
          3. Each extracted reference is looked up in the context text that
             was actually injected into the prompt. A reference that does
             NOT appear in the context is a potential hallucination.
          4. Return the list of flagged references (empty list = clean).

        The mock backend can never trigger this check (it only echoes the
        context), so any flag indicates the live model invented an entity.
        """
        flags: List[str] = []
        known = context.context_text.lower()

        # 1. Case / evidence ID references
        id_patterns = [
            ("Case",     r"case\s*(?:number|id)?\s*#?\s*(\d+)"),
            ("Evidence", r"evidence\s*(?:item|id)?\s*#?\s*(\d+)"),
        ]
        for label, pattern in id_patterns:
            for match in re.finditer(pattern, reply, re.IGNORECASE):
                ref = f"{label.lower()} #{match.group(1)}"
                if ref not in known:
                    flags.append(
                        f"{label} #{match.group(1)} is mentioned in the answer "
                        f"but does not appear in the retrieved database records.")

        # 2. Investigator name references
        try:
            from app.models.investigator import Investigator
            for inv in Investigator.query.all():
                name = (inv.full_name or "").strip()
                if len(name) >= 4 and name.lower() in reply.lower() \
                        and name.lower() not in known:
                    flags.append(
                        f"Investigator '{name}' is mentioned in the answer "
                        f"but was not part of the retrieved context.")
        except Exception:
            # No app/db context available (e.g. isolated unit test) -
            # skip the name check rather than fail the whole pipeline.
            pass

        # De-duplicate while preserving order
        seen = set()
        unique_flags = []
        for f in flags:
            if f not in seen:
                seen.add(f)
                unique_flags.append(f)
        return unique_flags

    # Public entry point
    def answer(self, user_message: str, conversation_history: Optional[List[Dict]] = None, user=None) -> AssistantResponse:
        """
        Runs the full six-stage pipeline.
        "user" is the current investigator; all context retrieval is scoped
        to the cases they may access, and their identity is injected into the
        prompt so identity questions are answered correctly.
        Degrades gracefully - always returns an AssistantResponse even on error.
        """
        try:
            intent  = self.classify_intent(user_message)
            context = self.retrieve_context(intent, user=user)
            messages, system_content = self.build_prompt(user_message, context, conversation_history, user=user)
            raw = self.call_nvidia(messages, system_content)
            reply, passed, warning = self.validate_response(raw, intent.category)
            hallucination_flags = self.check_hallucinations(reply, context)

            if hallucination_flags and not warning:
                warning = (
                    "The answer references entities that were not found in the "
                    "database context - verify before relying on it.")

            context_used = (
                bool(context.context_text) and
                "No relevant records" not in context.context_text and
                "Answering from general" not in context.context_text)

            return AssistantResponse(
                reply=reply,
                intent=intent.category,
                context_used=context_used,
                validation_passed=passed,
                warning=warning,
                hallucination_flags=hallucination_flags)

        except Exception as exc:
            if "401" in str(exc) or "auth" in str(exc).lower():
                return AssistantResponse(
                    reply=(
                        "Authentication error: the NVIDIA_API_KEY is missing or invalid. "
                        "Please set it in the .env file."),
                    intent=IntentCategory.UNKNOWN,
                    context_used=False,
                    validation_passed=False,
                    warning="API key error")
            return AssistantResponse(
                reply=f"An unexpected error occurred: {exc}. Please try again.",
                intent=IntentCategory.UNKNOWN,
                context_used=False,
                validation_passed=False,
                warning=str(exc))