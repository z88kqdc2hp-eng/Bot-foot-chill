import urllib.request
import json
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def job_soiree():
    maintenant = datetime.utcnow()
    # On cible les matchs qui commencent après 17h00 UTC (18h00/19h00 en France)
    limite_soir = maintenant.replace(hour=17, minute=0, second=0)
    aujourdhui = maintenant.strftime("%Y-%m-%d")
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    
                    # FILTRE : Uniquement les matchs de ce soir qui n'ont pas commencé
                    if date_m > maintenant and aujourdhui in m['commence_time']:
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        h2h = bk[0]['outcomes']
                        cote_h = next(o['price'] for o in h2h if o['name'] == home)
                        cote_n = next(o['price'] for o in h2h if o['name'] == 'Draw')

                        # Calculs
                        prob_v = int((1 / cote_h) * 100)
                        prob_n = int((1 / cote_n) * 100)
                        fiab_s = int(prob_v + (prob_n * 0.7))

                        # On accepte des matchs un peu moins "évidents" pour avoir plus de choix
                        if fiab_s >= 65:
                            heure_fr = (date_m + timedelta(hours=1)).strftime("%H:%M")
                            msg = (
                                f"🌙 **SCANNER DE SOIRÉE : {home.upper()}**\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"⏰ **Coup d'envoi** : {heure_fr}\n"
                                f"🏟️ **Match** : {home} vs {away}\n"
                                f"📊 **Fiabilité Victoire** : {prob_v}%\n"
                                f"🛡️ **Sécurité (V ou N)** : {fiab_s}%\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"🎯 **CONSEIL SOIRÉE** :\n"
                                f"👉 Pari : **{home} ou Nul**\n"
                                f"━━━━━━━━━━━━━━━━━━"
                            )
                            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}&parse_mode=Markdown"
                            urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    job_soiree()
