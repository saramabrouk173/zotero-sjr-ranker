# Smart Zotero Journal Tagger (SJR Integration) 🚀

## 🎯 Overview
This Python-based automation tool is designed for researchers and data scientists to streamline their literature review process. It creates a **direct connection** between your **Zotero** library and the **SCImago Journal Rank (SJR)** database.

Instead of manually checking the quality of every paper, this script automatically identifies the journal ranking (Q1, Q2, Q3, or Q4) and applies the corresponding tag directly to your Zotero items. This allows for instant filtering of high-impact research.

## ✨ Key Features
* **Direct Cloud Integration:** Connects via Zotero API to update your library in real-time.
* **Automated Rank Tagging:** Instantly labels papers with [Q1], [Q2], [Q3], or [Q4].
* **Fuzzy Matching Logic:** Smartly identifies journal names even if there are slight variations in spelling or formatting.
* **Enhanced Workflow:** Helps researchers prioritize reading by focusing on top-tier publications first.

## 🛠️ Prerequisites
To use this script, you will need:
1.  **SJR Data File:** Download the latest journal rankings CSV from [SCImagoJR](https://www.scimagojr.com/journalrank.php) and place it on your **Desktop**. 
    *(Note: A sample CSV file is provided in this repository for testing purposes).*
2.  **Zotero API Credentials:**
    * Your **UserID** (found in Zotero settings).
    * A **Secret API Key** (generated via Zotero.org account settings under *Feeds/API*).


## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/saramabrouk173/zotero-sjr-ranker.git
```
### 2. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 3. Configuration

Open the `zotero_tagger_rank.py` file and replace the placeholders with your actual credentials:

```python
LIBRARY_ID = 'YOUR_ZOTERO_ID'
API_KEY = 'YOUR_ZOTERO_API_KEY'
```

### 4. Run the Automation

```bash
python zotero_tagger_rank.py
```

---

## 📂 How It Works (Step-by-Step)

* **Detection:** The script automatically scans your Desktop for the Scimago CSV file.
* **Data Processing:** It loads the journal rankings using `pandas` and cleans the data for matching.
* **API Sync:** It fetches all journal articles from your Zotero library.
* **Tagging:** It matches each article to its SJR rank and pushes the new tags back to Zotero's servers.
* **Final Result:** Open your Zotero Desktop app, click Sync, and watch your library organize itself!

---

## 📝 License

This project is licensed under the MIT License - feel free to use and modify it!

---

## 👩‍🔬 Author

Developed by a researcher and data engineer focused on merging Chemical Sciences with Data Engineering to optimize scientific research.

Connect with me on [LinkedIn](https://www.linkedin.com/in/sarah-m-8402833a2)



