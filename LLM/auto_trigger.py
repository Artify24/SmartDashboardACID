"""
Auto-trigger: Runs model.ipynb when new scraper data arrives
"""
import time
import subprocess
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load .env from this directory
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from getDbdata import get_raw_scrapes

# Configuration
CHECK_INTERVAL = 60  # Check every 60 seconds
LAST_DATA_COUNT = 0
MIN_NEW_RECORDS = 2  # Trigger if 5+ new records

def get_current_record_count():
    """Get total records in database"""
    try:
        data = get_raw_scrapes(limit=10000)  # Get max records
        return len(data) if data else 0
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return 0

def run_notebook():
    """Execute the notebook using papermill"""
    try:
        print(f"\n🚀 Triggering notebook at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Install papermill if needed
        os.system("pip install papermill -q")
        
        # Run notebook
        result = subprocess.run(
            ["papermill", "model.ipynb", "model_output.ipynb"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            print("✅ Notebook executed successfully")
            return True
        else:
            print(f"❌ Notebook failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running notebook: {e}")
        return False

def monitor_for_new_data():
    """Monitor database and trigger on new data"""
    global LAST_DATA_COUNT
    
    print("🔍 Starting auto-trigger monitor...")
    print(f"   Checking every {CHECK_INTERVAL} seconds")
    print(f"   Minimum {MIN_NEW_RECORDS} new records to trigger\n")
    
    while True:
        try:
            current_count = get_current_record_count()
            new_records = current_count - LAST_DATA_COUNT
            
            if new_records >= MIN_NEW_RECORDS:
                print(f"✨ {new_records} new records detected!")
                run_notebook()
                LAST_DATA_COUNT = current_count
            elif current_count > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Records: {current_count} (waiting for {MIN_NEW_RECORDS - new_records} more...)")
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n⏹️  Monitor stopped")
            break
        except Exception as e:
            print(f"⚠️  Error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_for_new_data()
