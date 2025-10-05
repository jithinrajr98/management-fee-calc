from pathlib import Path
import os

DB_TIMEOUT = 5000  # milliseconds
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "mfc_database.db"
CSV_PATH = BASE_DIR / "data" / "input" / "Inputs.xlsm"
CSV_SAVED_PATH = BASE_DIR / "data" / "input" 
GROQ_MODEL = "groq/gemma2-9b-it"

