import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

EXTRACT_DIR = Path(os.getenv("EXTRACT_DIR"))

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

DB_URL = os.getenv("DB_URL")
