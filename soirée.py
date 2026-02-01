import urllib.request
import json
from datetime import datetime

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def scanner_complet():
    maintenant = datetime.utcnow()
    aujourdhui = maintenant.strftime("%Y-%m-%d")
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    
                    # On prend TOUS les matchs d'aujourd'hui qui n'ont pas encore commencé
                    if date_m > maintenant and aujourdhui in m['commence_time']:
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        cote_h = next(o['price'] for o in bk[0]['outcomes'] if o['name'] == home)
                        
                        # Indices de confiance simplifiés
                        fiab = int((1 / cote_h) * 100)
                        
                        msg = (
                            f"🌟 **MATCH DÉTECTÉ : {home.upper()}**\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🏟️ **Match** : {home} vs {away}\n"
                            f"📊 **Fiabilité** : {fiab}%\n"
                            f"🎯 **Pari** : {home} ou Nul\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}&parse_mode=Markdown"
                        urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    scanner_complet()
