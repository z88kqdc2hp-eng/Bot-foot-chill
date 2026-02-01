import urllib.request
import json
from datetime import datetime, timedelta

API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def job_soiree_auto():
    maintenant = datetime.utcnow()
    # On scanne les ligues majeures pour ce soir
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    
                    # FILTRE : Matchs entre 18h et 21h (Heure FR) qui n'ont pas commencé
                    # En UTC, cela correspond environ à 17h - 20h
                    if maintenant < date_m <= maintenant + timedelta(hours=4):
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        cote_h = next(o['price'] for o in bk[0]['outcomes'] if o['name'] == home)
                        
                        # Calcul probabilités et buts
                        prob_v = int((1 / cote_h) * 100)
                        
                        msg = (
                            f"🌙 **SCAN SOIRÉE (18h-21h)**\n"
                            f"🏟️ **Match** : {home} vs {away}\n"
                            f"📊 **Fiabilité Victoire** : {prob_v}%\n"
                            f"✅ **Pari** : {home} ou Nul\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}&parse_mode=Markdown"
                        urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    job_soiree_auto()
