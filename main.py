import os
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread

app = Flask(__name__)

# కొత్త RRB Unified Portal అధికారిక లింక్
URL = "https://rrb.indianrailways.gov.in"

def monitor_website():
    print("RRB పోర్టల్ మానిటరింగ్ స్టార్ట్ అయింది...")
    last_content = ""
    
    while True:
        try:
            # వెబ్‌సైట్ డేటాను రిక్వెస్ట్ చేయడం
            response = requests.get(URL, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # ఇక్కడ వెబ్‌సైట్‌లోని లేటెస్ట్ నోటీసుల టెక్స్ట్‌ను తీసుకుంటుంది
                # గమనిక: సైట్ స్ట్రక్చర్ బట్టి ట్యాగ్స్ మారవచ్చు, ప్రస్తుతానికి బాడీ టెక్స్ట్ చెక్ చేస్తున్నాం
                current_content = soup.get_text()
                
                if last_content == "":
                    last_content = current_content
                    print("మొదటిసారి వెబ్‌సైట్ డేటా సేవ్ అయింది. మానిటరింగ్ యాక్టివ్‌గా ఉంది.")
                elif current_content != last_content:
                    print("🚨 అలర్ట్: New RRB Portal లో కొత్త అప్‌డేట్ వచ్చింది! 🚨")
                    # టెలిగ్రామ్ లేదా నోటిఫికేషన్ కోడ్ ఇక్కడ యాడ్ చేసుకోవచ్చు
                    last_content = current_content
                else:
                    print("వెబ్‌సైట్ చెక్ చేసాము: ఎలాంటి కొత్త అప్‌డేట్ లేదు.")
            else:
                print(f"Error: వెబ్‌సైట్ రెస్పాన్స్ ఇవ్వడం లేదు. Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        
        # ప్రతి 15 సెకన్లకు ఒకసారి రన్ అవ్వడానికి
        time.sleep(15)

@app.route('/')
def home():
    return "RRB Unified Portal Bot is Running Live!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # బ్యాక్‌గ్రౌండ్‌లో మానిటరింగ్ నిరంతరాయంగా రన్ అవ్వడానికి థ్రెడ్ స్టార్ట్ చేస్తున్నాం
    t = Thread(target=monitor_website)
    t.daemon = True
    t.start()
    run()
