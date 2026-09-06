import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio

# --- CONFIGURATION AREA ---
TOKEN = "8429420294:AAHyonxcGVdByBXj4vw3bTElut4A62vVU6I"  # Mee original Telegram Bot Token ikkada direct paste cheyyandi
CHAT_ID = "8429420294"  # Mee numeric User ID string ikkada type cheyyandi
CHECK_INTERVAL = 5  # Prathi 5 seconds updates monitor running logic
# --------------------------

URL = "https://rrb.indianrailways.gov.in"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

bot = Bot(token=TOKEN)
seen_links = set()

async def check_railway_updates():
    print("Render Cloud System: Bot completely active and listening 24/7 continuous stream...")
    global seen_links
    
    # Baseline load settings setup initial check parameters verification
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            seen_links.add(a_tag['href'])
        print(f"Initial setup complete logs check. Found {len(seen_links)} links frame tracker database.")
    except Exception as e:
        print(f"Network checking target initial failure tracker trace: {e}")

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
                        print(f"Cloud server dynamic tracking log update pushed text delivery success: {text}")
                        
                        seen_links.add(link)
        except Exception as e:
            print(f"Continuous polling dynamic status server loop warning log parameters trace: {e}")
            
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(check_railway_updates())
