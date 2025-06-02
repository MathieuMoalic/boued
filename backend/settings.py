import os
from pathlib import Path
import secrets

DATABASE_URL = os.environ["DATABASE_URL"]
FIRST_USER_NAME = os.environ["FIRST_USER_NAME"]
FIRST_USER_PASSWORD = os.environ["FIRST_USER_PASSWORD"]

SECRET_KEY_FILE = os.environ["SECRET_KEY_FILE"]
SECRET_FILE = Path(SECRET_KEY_FILE)
if SECRET_FILE.exists():
    SECRET_KEY = SECRET_FILE.read_text().strip()
else:
    SECRET_KEY = secrets.token_urlsafe(32)
    SECRET_FILE.write_text(SECRET_KEY)

