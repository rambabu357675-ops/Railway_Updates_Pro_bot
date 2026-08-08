import os
import requests
import hashlib

# GitHub Secrets నుండి టోకెన్ మరియు చాట్ ఐడి తీసుకుంటుంది
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
URL = "https://rrb.indianrailways.gov.in/"

HASH_FILE = "last_hash.txt"

def send_telegram_message(text):
    telegram_url = f"https://telegram.org{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(telegram_url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

def check_website():
    if not TOKEN or not CHAT_ID:
        print("Error: TELEGRAM_TOKEN or TELEGRAM_CHAT_ID is missing in GitHub Secrets!")
        return

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=10)
        current_hash = hashlib.sha224(response.content).hexdigest()
        
        old_hash = ""
        if os.path.exists(HASH_FILE):
            with open(HASH_FILE, "r") as f:
                old_hash = f.read().strip()
        
        if old_hash == "":
            with open(HASH_FILE, "w") as f:
                f.write(current_hash)
            print("Initial state captured.")
            
        elif current_hash != old_hash:
            with open(HASH_FILE, "w") as f:
                f.write(current_hash)
            msg = "🔔 *RRB Unified Portal Update!* \n\nవెబ్‌సైట్‌లో కొత్త నోటీస్ వచ్చింది! వెంటనే చెక్ చేయండి:\nhttps://rrb.indianrailways.gov.in/"
            send_telegram_message(msg)
            print("Notification sent to Telegram!")
        else:
            print("No changes detected.")
            
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    check_website()
