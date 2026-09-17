# Chapter 17 — Deployment and Operation

---

## 17.1 Development Environment

Deployment is the process of making a system available for use. This chapter documents the environment in which DEICMS runs, how it is configured and started, and what would be required to move it from a development deployment to a production one. The physical topology is given in Figure 8.11.

**Table 17.1 — Runtime environment**

| Element | Development configuration | Production target |
|---|---|---|
| Runtime | Python 3 | Python 3 |
| Web server | Werkzeug development server | gunicorn or uWSGI behind a reverse proxy |
| Transport | HTTPS on port 5001 with a self-signed certificate | HTTPS with a certificate from a recognised authority |
| Database | SQLite file, WAL journaling mode | PostgreSQL |
| File storage | Local `uploads/` directory, AES-256-GCM encrypted | Encrypted volume or object store |
| Configuration | `.env` file loaded at startup | Environment variables injected by the platform |
| External service | NVIDIA NIM inference endpoint over HTTPS | Unchanged, or a self-hosted equivalent |
| Debug mode | Enabled — the server restarts on file save | **Disabled** |

Three of these rows are deliberate compromises rather than oversights, and each is recorded as a limitation in Section 13.5: the self-signed certificate, the single-file database and the development server. The fourth row that matters is debug mode, which must never be enabled in a real deployment because it exposes an interactive debugger to anyone who can trigger an exception.

**Table 17.2 — Dependencies**

| Group | Packages |
|---|---|
| Web framework and extensions | flask, flask-sqlalchemy, flask-login, flask-wtf, flask-limiter, python-dotenv |
| Cryptography | cryptography (Ed25519, AES-GCM, X.509); SHA-256 via the standard library `hashlib` |
| File metadata and type validation | pillow; python-magic-bin on Windows, python-magic elsewhere |
| AI assistant | openai — the NVIDIA NIM endpoint is OpenAI-compatible |
| Anomaly detection | scikit-learn |
| Reporting | reportlab |
| Two-factor authentication | pyotp, qrcode |
| Testing | pytest, pytest-cov |

The platform-conditional dependency in the third group is worth noting as a portability detail: `python-magic` requires a native library, supplied by a different package on Windows. This is the one place where the system is not platform-neutral, and it is the reason one content-validation test passes on the development machine and is skipped in a bare container (Section 12.9).

## 17.2 Configuration Management

Configuration is separated from code entirely. No secret, path or tunable value is hard-coded in a module; all are read from the environment through a single configuration class, with `.env` excluded from version control.

**Table 17.3 — Configuration values**

| Setting | Purpose | Default |
|---|---|---|
| `SECRET_KEY` | Signs session cookies | Development placeholder — **warned about at startup** |
| `WTF_CSRF_SECRET_KEY` | Signs CSRF tokens | Falls back to `SECRET_KEY` |
| `KEY_ENCRYPTION_SECRET` | Derives the key protecting private keys and evidence files | Development placeholder — **warned about at startup** |
| `DATABASE_URL` | Database connection | SQLite file in the project root |
| `UPLOAD_FOLDER` | Encrypted evidence storage | `uploads/` |
| `MAX_CONTENT_LENGTH` | Upload size ceiling | 500 MB |
| `NVIDIA_API_KEY` | Inference endpoint credential | Empty — the assistant falls back to the mock |
| `AI_MODEL` | Model identifier | A current catalogue model; overridable |
| `AI_REQUEST_TIMEOUT` | Per-model timeout | 20 s |
| `AI_TOTAL_BUDGET` | Total budget across fallback candidates | 60 s |
| `AI_MAX_TOKENS` | Response length ceiling | 700 |
| `MAX_LOGIN_ATTEMPTS` / `LOCKOUT_MINUTES` | Account lockout policy | 5 attempts / 15 minutes |
| `IDLE_TIMEOUT_MINUTES` | Sliding session timeout | 30 minutes |
| `PASSWORD_MIN_LENGTH` | Password policy | 12 characters |
| `RATELIMIT_STORAGE_URI` | Rate-limit backend | In-memory — **not suitable for multi-worker production** |

Two profiles are provided. **DevelopmentConfig** enables debug mode and permits the placeholder secrets, emitting a loud startup warning for each. **ProductionConfig** disables debug and **refuses to start** if `SECRET_KEY`, `KEY_ENCRYPTION_SECRET` or `NVIDIA_API_KEY` is missing, or if either secret matches a known insecure default. The profile is selected by an environment variable and defaults to development, so an existing local setup keeps working unchanged.

This fail-fast behaviour in the production profile is the practical answer to the configuration-management threat category of Table 2.2. A system that boots happily with a known default key is one misconfiguration away from being unprotected; one that refuses to boot cannot be deployed insecurely by accident.

## 17.3 Database Setup and Seeding

**Table 17.4 — Database operations**

| Operation | Mechanism | Notes |
|---|---|---|
| Schema creation | Performed by the application factory on first run | Creates all six tables from the model declarations |
| Schema migration | Lightweight startup routine inspecting existing columns and adding any missing | Added columns only; limits stated in Section 10.2 |
| Seeding | `seed.py` | Creates investigator accounts with genuine Ed25519 key pairs, cases, access grants, evidence items, and **genuinely signed** custody records |
| WAL checkpoint | `flush_db.py` | Folds pending writes from `deicms.db-wal` back into the main file so the live trail is visible in an external browser |

The seeding script deserves a note because it is a source of subtle error in systems of this kind. Once signing became mandatory, a seed script that created custody records without signatures would produce a database in which **every item fails integrity verification** — which looks like an algorithm defect and is not. The seed script therefore constructs the canonical payload by the same definition used by the custody route and the verifier, and signs it with the seeded investigator's private key. The three implementations produce identical bytes, which is the practical meaning of the "formal" classification in Table 3.3.

The WAL checkpoint utility exists because SQLite in write-ahead-log mode keeps recent writes in side files. Opening `deicms.db` in an external browser while or just after the application has run therefore shows stale contents, which is confusing rather than harmful; `flush_db.py` performs a full checkpoint and prints row counts and the five most recent audit events so that the live trail can be confirmed.

## 17.4 Running the System

**Table 17.5 — Operational commands**

| Task | Command | Notes |
|---|---|---|
| Install dependencies | `pip install -r requirements.txt` | A virtual environment is assumed |
| Generate the TLS certificate | Automatic on first run via `generate_cert.py` | Produces `cert.pem` and `key.pem` |
| Seed demonstration data | `python seed.py` | Creates accounts, cases and signed custody records |
| Start the application | `python run.py` | Serves over HTTPS on port 5001 |
| Run the test suite | `pytest` | 172 tests; no network access required |
| Run with coverage | `pytest --cov=app` | Produces the figures in Table 12.12 |
| Checkpoint the database for inspection | `python flush_db.py` | Run with the server stopped |

The browser will warn about the self-signed certificate on first connection; this is expected in development and is the visible consequence of the limitation recorded in Table 13.5.

## 17.5 Path to Production

Moving DEICMS from a development deployment to an operational one requires no application code changes, only configuration and infrastructure changes. This is the portability requirement NFR-09 realised, and it is worth setting out as a concrete checklist rather than a claim.

**Table 17.6 — Production readiness checklist**

| # | Step | Why | Currently |
|---|---|---|---|
| 1 | Set `APP_ENV=production` | Activates the strict profile that refuses insecure defaults | Development profile |
| 2 | Supply real `SECRET_KEY` and `KEY_ENCRYPTION_SECRET` | The placeholders are publicly known | Placeholders, warned about |
| 3 | Point `DATABASE_URL` at PostgreSQL | SQLite does not support concurrent writers | SQLite |
| 4 | Replace the self-signed certificate | Provides identity assurance, not just encryption | Self-signed |
| 5 | Run behind gunicorn or uWSGI with a reverse proxy | The development server is single-threaded and not hardened | Werkzeug |
| 6 | Set `RATELIMIT_STORAGE_URI` to a shared backend such as Redis | In-memory limits are per-worker and reset on restart | In-memory |
| 7 | Disable debug mode | An interactive debugger must never be reachable | Enabled |
| 8 | Move evidence storage to an encrypted volume with backup | Local disk has no redundancy | Local `uploads/` |
| 9 | Tighten the Content-Security-Policy to a nonce-based form | The current policy permits inline scripts and styles | Inline permitted |
| 10 | Conduct load and penetration testing | Behaviour under attack and under volume is unverified | Not performed |

Steps 1 to 7 are configuration and infrastructure only. Step 9 requires refactoring the templates to remove embedded scripts and styles, which is the one item on the list that touches application code. Step 10 is an activity rather than a change.

**A caution that belongs with this checklist.** The `KEY_ENCRYPTION_SECRET` must be set **before any data exists** and must never be rotated afterwards, because every encrypted evidence file and every encrypted private key is protected under a key derived from it. Rotating it renders that data permanently unrecoverable. There is no key-rotation procedure, and this is recorded as an inherent limitation in Table 13.5 rather than as an oversight — designing one would require re-encrypting the whole store under a new key while retaining the old, which is a substantial feature in its own right.

## 17.6 A Note on DevOps

The steps above describe a manual path to production, and it is worth naming what a DevOps approach would change, since the course treats it.

DevOps aims to shorten the path from a committed change to a running system by automating it and by making development and operations a single concern rather than two handoffs. Its characteristic practices are **continuous integration** (every commit builds and runs the test suite automatically), **continuous delivery** (every change that passes is deployable), **infrastructure as code** (the environment is defined in version-controlled files rather than configured by hand), and **monitoring** (the running system reports its own health).

DEICMS has one of these and not the others. It has a fast, deterministic, network-free test suite — the single hardest prerequisite for continuous integration, and the reason the project *could* adopt it with little further work. It has no automated pipeline, no infrastructure definition and no monitoring, because a single-developer academic project deploys to one machine and has no operational phase to monitor.

The honest assessment is therefore that the project is **CI-ready but not CI-practising**. Stating it that way is more useful than either claiming a DevOps practice that does not exist or omitting the topic: the prerequisite that usually blocks adoption — a trustworthy, fast test suite — is the one thing the project does have.

## 17.7 Summary

This chapter documented how DEICMS is deployed and operated. The development environment was set out beside its production target, with three deliberate compromises identified as such. Configuration was shown to be fully separated from code, with two profiles — a development profile that warns about placeholder secrets and a production profile that refuses to start without real ones, which is the practical defence against insecure deployment by accident.

Database setup, the lightweight startup migration, seeding and the WAL checkpoint utility were described, with a note on why the seed script must construct signed custody records by the same canonical definition as the application. Operational commands were listed. A ten-step production readiness checklist was given, with the observation that seven of the ten steps are configuration and infrastructure only and just one touches application code — which is the portability claim made concrete rather than asserted. The key-rotation caution was stated alongside it.

Finally, the project's position relative to DevOps was assessed honestly as CI-ready but not CI-practising. The next chapter shows the system in operation.

---

\newpage
