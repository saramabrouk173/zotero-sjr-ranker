from pyzotero import zotero
import pandas as pd
import os
import re
import time

# --- 1. Credentials (Personal Information Removed) ---
# Replace the values below with your actual Zotero credentials
LIBRARY_ID = 'YOUR_LIBRARY_ID_HERE' 
API_KEY = 'YOUR_API_KEY_HERE'
LIBRARY_TYPE = 'user' # Change to 'group' if using a group library

try:
    zot = zotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
    zot.num_items()
    print("✅ Connection to Zotero established successfully!")
except Exception as e:
    print(f"❌ Connection Error: {e}")
    exit()

# --- 2. Advanced Cleaning Functions ---
def clean_text(text):
    """Removes all non-alphanumeric characters for flexible title matching."""
    if not text: return ""
    return re.sub(r'[^a-z0-9]', '', str(text).lower())

def extract_issns(issn_str):
    """Extracts all 8-character ISSN sequences from a string."""
    if not issn_str: return set()
    found = re.findall(r'([0-9]{4})[- ]?([0-9]{3}[0-9X])', str(issn_str).upper())
    return {f"{p[0]}{p[1]}" for p in found}

# --- 3. Loading SJR Data ---
current_folder = os.path.dirname(os.path.abspath(__file__))
sjr_file = next((os.path.join(current_folder, f) for f in os.listdir(current_folder) 
                 if f.lower().startswith('scimagojr') and f.endswith('.csv')), None)

if not sjr_file:
    print("❌ Error: SJR CSV file not found.")
    exit()

print(f"✅ Processing: {os.path.basename(sjr_file)}")

try:
    df = pd.read_csv(sjr_file, sep=';', low_memory=False)
    df['Clean_Title'] = df['Title'].apply(clean_text)
    df['ISSN_Set'] = df['Issn'].apply(extract_issns)
    
    q_col = 'SJR Best Quartile' if 'SJR Best Quartile' in df.columns else None
    if not q_col:
        print("❌ Error: Could not find Quartile column in CSV.")
        exit()
        
    print(f"✅ Database loaded. Found {len(df)} journals.")
except Exception as e:
    print(f"❌ Parsing Error: {e}")
    exit()

# --- 4. Zotero Processing ---
print("🚀 Fetching items from Zotero...")
items = zot.everything(zot.top()) 
updated_count = 0

print(f"📊 Analyzing {len(items)} items...")

for item in items:
    if item['data'].get('itemType') != 'journalArticle':
        continue

    z_pub = item['data'].get('publicationTitle', '')
    z_issns = extract_issns(item['data'].get('ISSN', ''))
    z_pub_clean = clean_text(z_pub)

    match_row = None

    # Step 1: Match by ISSN
    if z_issns:
        match_mask = df['ISSN_Set'].apply(lambda db_set: not z_issns.isdisjoint(db_set))
        if match_mask.any():
            match_row = df[match_mask].iloc[0]

    # Step 2: Fallback to Title match
    if match_row is None and z_pub_clean:
        title_mask = df['Clean_Title'] == z_pub_clean
        if title_mask.any():
            match_row = df[title_mask].iloc[0]

    # Step 3: Apply Tag (Rank or NOT RANKED)
    new_tag = None
    existing_tags = [t['tag'] for t in item['data'].get('tags', [])]

    if match_row is not None:
        rank = match_row[q_col]
        if pd.notna(rank) and rank != '-':
            new_tag = str(rank).upper()
        else:
            new_tag = "NOT RANKED"
    else:
        new_tag = "NOT RANKED"

    # Add the tag if it's not already there
    if new_tag and new_tag not in existing_tags:
        zot.add_tags(item, new_tag)
        updated_count += 1
        print(f"✨ Tagged: {z_pub[:30]}... -> {new_tag}")
        time.sleep(0.1)

print(f"\n✅ Finished! Successfully tagged {updated_count} items.")
