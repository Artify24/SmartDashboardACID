import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Load .env from the same directory as this file
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Read Supabase connection info from environment for security
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError('SUPABASE_URL and SUPABASE_KEY must be set in the environment')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_llm_text(llm_type, content):
    """
    Save plain text output from LLM to Supabase.
    llm_type: 'competitor_summary', 'our_summary', 'comparison_report', 'final_strategy'
    content: plain text string from LLM
    """
    response = supabase.table("llm_outputs").insert({
        "type": llm_type,
        "content": content
    }).execute()

    if response.data:
        print(f"✅ Saved {llm_type}")
    else:
        print(f"❌ Failed to save {llm_type}: {response}")
