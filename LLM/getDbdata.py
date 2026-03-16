import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Load .env from the same directory as this file
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Read Supabase connection info from environment
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError('SUPABASE_URL and SUPABASE_KEY must be set in the environment')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_raw_scrapes(limit: int = 50):
    """
    Fetch latest raw scrapes from Supabase.
    Returns a list of JSON objects directly.
    """
    try:
        response = (
            supabase.table("raw_scrapes")
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )

        if response.data:
            return response.data
        else:
            return []

    except Exception as e:
        print("❌ Error fetching from Supabase:", e)
        return []