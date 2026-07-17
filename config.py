import os
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    # Secret key used by Flask to sign session cookies.
    # Loaded from the .env file; the hard-coded fallback exists only so the
    # test suite can run without a .env. Never use the fallback in production.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # WTF_CSRF_SECRET_KEY - used by flask-wtf to sign CSRF tokens
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY', SECRET_KEY)

    # Database file location (SQLite for development)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'deicms.db'))

    # Disable modification tracking to save memory (we don't need it)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Folder where uploaded evidence files will be saved
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

    # Maximum file size for uploads: 500 MB
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024

    # API key for the AI assistant (NVIDIA NIM, OpenAI-compatible endpoint).
    # Set NVIDIA_API_KEY in the .env file; without a valid key the assistant
    # falls back to a context-aware mock response.
    NVIDIA_API_KEY = os.environ.get('NVIDIA_API_KEY', '')

    # AI assistant tuning. The 8B model answers in a few seconds; the larger
    # 70B model is more capable but took 1-2 minutes for this workload.
    # Override via .env if you prefer the larger model.
    AI_MODEL = os.environ.get('AI_MODEL', 'meta/llama-3.1-8b-instruct')
    AI_MAX_TOKENS = int(os.environ.get('AI_MAX_TOKENS', 700))
    AI_REQUEST_TIMEOUT = int(os.environ.get('AI_REQUEST_TIMEOUT', 60))

    # Allowed file extensions for evidence uploads
    ALLOWED_EXTENSIONS = {
        'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff',  # Images
        'pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx',  # Documents
        'mp4', 'avi', 'mov', 'mkv',                    # Videos
        'mp3', 'wav',                                  # Audio
        'csv', 'json', 'xml', 'log', 'db', 'sqlite'   # Data files
    }

    #  Security settings 
    # Account lockout: how many consecutive failures trigger a lockout
    MAX_LOGIN_ATTEMPTS = 5
    # How long the account stays locked (minutes)
    LOCKOUT_MINUTES = 15

    # Session cookie security
    SESSION_COOKIE_HTTPONLY = True   # JS cannot read the session cookie
    SESSION_COOKIE_SAMESITE = 'Lax'  # Protects against CSRF on cross-origin navigations
    # Only send the session cookie over HTTPS connections (TLS).
    # The app runs over HTTPS in development, so this can stay enabled.
    SESSION_COOKIE_SECURE = True

    # Idle session timeout: log a user out after this many minutes of inactivity.
    from datetime import timedelta as _timedelta
    PERMANENT_SESSION_LIFETIME = _timedelta(minutes=30)
    IDLE_TIMEOUT_MINUTES = 30

    # Master secret used to derive the keys that encrypt private keys and
    # evidence files at rest.
    KEY_ENCRYPTION_SECRET = os.environ.get('KEY_ENCRYPTION_SECRET') or 'dev-encryption-secret-change-in-production'

    # Minimum length enforced by the password-strength policy.
    PASSWORD_MIN_LENGTH = 12

    # Flask-Limiter storage. The in-memory store is fine for single-process
    # development, but it resets on restart and is NOT shared across worker
    # processes, so limits are not enforced consistently under a multi-worker
    # production server (gunicorn/uWSGI). In production set RATELIMIT_STORAGE_URI
    # to a shared backend, e.g. 'redis://localhost:6379'.
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')

    # 
    # Magic-byte MIME type -> allowed extension mapping
    # Used by the file upload validator to verify the real file type
    MIME_TO_EXTENSIONS = {
        'image/png':       ['.png'],
        'image/jpeg':      ['.jpg', '.jpeg'],
        'image/gif':       ['.gif'],
        'image/bmp':       ['.bmp'],
        'image/tiff':      ['.tiff'],
        'application/pdf': ['.pdf'],
        'application/msword':                                              ['.doc'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
        'application/vnd.ms-excel':                                        ['.xls'],
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
        'text/plain':      ['.txt', '.log', '.csv'],
        'text/csv':        ['.csv'],
        'application/json': ['.json'],
        'application/xml':  ['.xml'],
        'text/xml':         ['.xml'],
        'video/mp4':        ['.mp4'],
        'video/x-msvideo':  ['.avi'],
        'video/quicktime':  ['.mov'],
        'video/x-matroska': ['.mkv'],
        'audio/mpeg':       ['.mp3'],
        'audio/wav':        ['.wav'],
        'application/x-sqlite3': ['.db', '.sqlite'],
        'application/zip':  ['.zip'],   # kept for zip files only
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # In production, use PostgreSQL instead of SQLite
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/deicms'

    # Enforce strict secrets in production (crashes on startup if missing)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    KEY_ENCRYPTION_SECRET = os.environ.get('KEY_ENCRYPTION_SECRET')
    NVIDIA_API_KEY = os.environ.get('NVIDIA_API_KEY')


# Known-weak fallback values that must never be used in production.
_INSECURE_DEFAULTS = {
    'dev-secret-key-change-in-production',
    'dev-encryption-secret-change-in-production',
}

# Select the active config from the environment (APP_ENV or FLASK_ENV);
# defaults to development so existing local setups keep working unchanged.
# Set APP_ENV=production to activate the strict production profile.
_env = (os.environ.get('APP_ENV') or os.environ.get('FLASK_ENV') or 'development').lower()
config = ProductionConfig if _env in ('production', 'prod') else DevelopmentConfig

if config is ProductionConfig:
    # Fail fast: production must not boot without real, non-default secrets.
    for key in ['SECRET_KEY', 'KEY_ENCRYPTION_SECRET', 'NVIDIA_API_KEY']:
        value = getattr(config, key)
        if not value:
            raise ValueError(
                f"FATAL: Missing required environment variable for production: {key}")
        if value in _INSECURE_DEFAULTS:
            raise ValueError(
                f"FATAL: {key} is set to a known insecure default value in production.")
else:
    # Development: don't crash (existing data may have been encrypted with the
    # fallback), but warn loudly so the weak secret is never mistaken for safe.
    import warnings
    for key in ['SECRET_KEY', 'KEY_ENCRYPTION_SECRET']:
        if getattr(config, key) in _INSECURE_DEFAULTS:
            warnings.warn(
                f"SECURITY: {key} is using an insecure development default. "
                f"Set it in your .env before any real deployment "
                f"(and never rotate KEY_ENCRYPTION_SECRET after data exists, "
                f"or encrypted files and private keys become unrecoverable).",
                stacklevel=2)