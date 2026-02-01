import urllib.request
import json
from datetime import datetime

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def scanner_dimanche():
    maintenant = datetime.utcnow()
    aujourdhui = maintenant.strftime("%Y-%m-%d")
    # On scanne les ligues majeures pour ce soir
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    # On prend les matchs de ce soir (Lyon, Real, etc.)
                    if date_m > maintenant and aujourdhui in m['commence_time']:
                        home = m['home_team']
                        away = m['away_team']
                        cote_h = m['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
                        
                        msg = f"🌙 **MATCH CE SOIR** : {home} vs {away}\n📈 Cote : {cote_h}\n✅ Pari : {home} ou Nul"
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}"
                        urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    scanner_dimanche()
