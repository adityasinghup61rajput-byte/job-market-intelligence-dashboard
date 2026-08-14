from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
STAGING_DIR = ROOT / "data" / "staging"
CURATED_DIR = ROOT / "data" / "curated"
DB_PATH = ROOT / "data" / "warehouse.db"
LOG_DIR = ROOT / "logs"

for p in [STAGING_DIR, CURATED_DIR, LOG_DIR]:
    p.mkdir(parents=True, exist_ok=True)

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
S3_BUCKET = os.getenv("S3_BUCKET", "")
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "")
GENAI_MODEL = os.getenv("GENAI_MODEL", "")
