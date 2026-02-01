import urllib.request
import json
from datetime import datetime

API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def start():
    now = datetime.utcnow()
    day = now.strftime("%Y-%m-%d")
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    if day in m['commence_time']:
                        home = m['home_team']
                        away = m['away_team']
                        msg = f"🌙 **MATCH CE SOIR** : {home} vs {away}\n✅ Pari : {home} ou Nul"
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}"
                        urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    start()
