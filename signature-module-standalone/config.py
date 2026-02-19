import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "change-me-in-production")
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

    GOOGLE_SCOPES = ["https://www.googleapis.com/auth/gmail.settings.basic"]
    GOOGLE_SERVICE_ACCOUNT_FILE = os.environ.get(
        "GOOGLE_SERVICE_ACCOUNT_FILE",
        "data/credentials.json",
    )

    BASE_DIR = Path(__file__).resolve().parent
