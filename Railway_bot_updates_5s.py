import os
import time
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from flask import Flask
from threading import Thread

# --- QUICK FLASK PORT SYSTEM WEB ENGINE SERVER ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Railway Bot Server Active 24/7 Successfully Connected!"

def run_flask_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- SYSTEM CONFIGURATION AREA ---
TOKEN = "8429420294:AAHyonxcGVdByBXj4vw3bTElut4A62vVU6I"  # Mee original Token variables double quotes "" key text center copy paste string configuration input set list
CHAT_ID = "8429420294"  # Mee numeric Chat ID data block match set integer value format string logic
CHECK_INTERVAL = 5sec
# --------------------------

URL = "https://rrb.indianrailways.gov.in"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

bot = Bot(token=TOKEN)
seen_links = set()

async def check_railway_updates():
    print("Railway central monitoring tracking script background live stream setup loading checking connections parameters status configuration...")
    global seen_links
    
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            seen_links.add(a_tag['href'])
        print(f"Benchmark initialization tracker active. Found {len(seen_links)} data entries tags.")
    except Exception as e:
        print(f"Network benchmark tracking logging trace alert context system setup framework glitch: {e}")

    while True:
        try:
            response = requests.get(URL, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for a_tag in soup.find_all('a', href=True):
                    link = a_tag['href']
                    text = a_tag.get_text().strip()
                    
                    if link not in seen_links and len(text) > 5:
                        full_url = link if link.startswith('http') else f"{URL}{link}"
                        message = f"📢 **Kotha RRB Update Vachindhi!**\n\n📝 {text}\n\n🔗 Website Link: {full_url}\n\n👉 *Dheenni mee channel ki forward cheskondi.*"
                        
                        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
                        print(f"New change event tracking sync continuous: {text}")
                        seen_links.add(link)
        except Exception as e:
            pass
            
        await asyncio.sleep(CHECK_INTERVAL)

def start_bot_loop():
    asyncio.run(check_railway_updates())

if __name__ == "__main__":
    # Start web container instance loop system mapping parameters connection tracking network logic setup
    server_thread = Thread(target=run_flask_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Run central telegram execution context background processing loop parameters 
    start_bot_loop()
