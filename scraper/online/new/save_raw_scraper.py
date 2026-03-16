import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Load .env from the scraper directory (two levels up from this file)
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")
load_dotenv(dotenv_path=Path(__file__).parent / ".env")  # also check local

# Read Supabase config from environment
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError('SUPABASE_URL and SUPABASE_KEY must be set in the environment')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_raw_scraper(target, is_our_site, raw_json):
    """
    Saves raw JSON data to Supabase table `raw_scrapes`.
    Compatible with supabase-py v2+.
    """
    response = supabase.table("raw_scrapes").insert({
        "target": target,
        "is_our_site": is_our_site,
        "raw_data": raw_json
    }).execute()

    # Check if data was inserted
    if not response.data:
        print("❌ Failed to save. Response:", response)
    else:
        print("✅ Saved successfully:", response.data)

