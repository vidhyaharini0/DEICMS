from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from app import limiter
from app.logic.ai_assistant import AIInvestigationAssistant

assistant_bp = Blueprint('assistant', __name__, url_prefix='/assistant')

# One shared instance (stateless - all state is in the session or passed in)
_assistant = AIInvestigationAssistant()


def _load_history():
    """
    Return the current user's chat history, discarding any history that
    belongs to a different user. The history is tagged with the owner's ID
    so a session left over from a previous login (same browser) can never
    leak one investigator's conversation to the next.
    """
    stored = session.get('assistant_history')
    if not isinstance(stored, dict) or stored.get('user_id') != current_user.id:
        return []
    return stored.get('turns', [])


def _save_history(turns):
    session['assistant_history'] = {
        'user_id': current_user.id,
        'turns': turns[-10:]}  # keep last 10 turns = 5 exchanges


@assistant_bp.route('/')
@login_required
def chat_page():
    history = _load_history()
    return render_template('assistant/chat.html', history=history)


@assistant_bp.route('/chat', methods=['POST'])
@login_required
@limiter.limit('20 per minute')  # LLM calls are the most expensive endpoint
def chat():
    data = request.get_json(force=True)
    user_message = (data.get('message') or '').strip()
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    # Per-user conversation history (never another user's turns)
    history = _load_history()
    # Scope the answer to the logged-in investigator's identity and access
    response = _assistant.answer(
        user_message, conversation_history=history, user=current_user)

    history.append({'role': 'user',      'content': user_message})
    history.append({'role': 'assistant', 'content': response.reply})
    _save_history(history)

    return jsonify({
        'reply':               response.reply,
        'intent':              response.intent,
        'context_used':        response.context_used,
        'validation_passed':   response.validation_passed,
        'warning':             response.warning,
        'hallucination_flags': response.hallucination_flags})


@assistant_bp.route('/clear', methods=['POST'])
@login_required
def clear():
    session.pop('assistant_history', None)
    return jsonify({'status': 'cleared'})
