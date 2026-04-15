from pyzotero import zotero
import pandas as pd
import os
import time

# --- 1. Authentication Setup ---
# Insert your Zotero User ID and API Key here
# You can find these in your Zotero account settings (Feeds/API)
LIBRARY_ID = 'YOUR_ZOTERO_ID' 
API_KEY = 'YOUR_ZOTERO_API_KEY'
LIBRARY_TYPE = 'user' # or 'group'

zot = zotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, API_KEY)

# --- 2. Locating the SJR Ranking File (CSV) ---
# The script looks for a file starting with 'scimagojr' on the Desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
sjr_file = None

for file in os.listdir(desktop_path):
    if file.startswith('scimagojr') and file.endswith('.csv'):
        sjr_file = os.path.join(desktop_path, file)
        break

if not sjr_file:
    print("❌ Error: SJR CSV file not found on Desktop. Please download it from ScimagoJR.")
    exit()

print(f"✅ Found Journal Database: {os.path.basename(sjr_file)}")

# --- 3. Loading Rankings into Memory ---
try:
    # Attempting to read with semicolon separator (default for SJR)
    sjr_df = pd.read_csv(sjr_file, sep=';')
except:
    sjr_df = pd.read_csv(sjr_file, sep=',')

# Clean journal titles for better matching
sjr_df['Title_Clean'] = sjr_df['Title'].str.lower().str.strip()
journal_rank_map = dict(zip(sjr_df['Title_Clean'], sjr_df['SJR Best Quartile']))

print("🚀 Scanning Zotero library and applying tags...")

# --- 4. Fetching and Processing Zotero Items ---
all_items = zot.everything(zot.items())
updated_count = 0

for item in all_items:
    try:
        # Check if the item is a journal article
        if item['data'].get('itemType') == 'journalArticle':
            journal_name = item['data'].get('publicationTitle', '').lower().strip()
            item_title = item['data'].get('title', '')[:50]
            
            if not journal_name: 
                continue

            # Look for exact or partial rank match
            rank = journal_rank_map.get(journal_name)
            
            # Fuzzy matching if exact match fails
            if not rank:
                for sjr_title, sjr_rank in journal_rank_map.items():
                    if journal_name in sjr_title or sjr_title in journal_name:
                        rank = sjr_rank
                        break
            
            if rank:
                # Check current tags to avoid duplicates
                current_tags = [t.get('tag') for t in item['data'].get('tags', [])]
                
                if rank not in current_tags:
                    # Apply the rank as a new tag
                    zot.add_tags(item, rank)
                    updated_count += 1
                    print(f"✅ Tagged [{rank}] -> {item_title}...")
                    
                    # Small delay to respect API rate limits
                    time.sleep(0.3) 
    except Exception as e:
        print(f"⚠️ Could not process item: {e}")
        continue

print(f"\n✨ Automation Complete! {updated_count} items updated.")
print("Sync your Zotero desktop app to see the changes.")