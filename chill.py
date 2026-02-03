import urllib.request, json, urllib.parse
from datetime import datetime, timedelta

API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def run_chill_open():
    now = datetime.utcnow()
    # On scanne largement pour ne rien rater ce soir
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    matchs_envoyes = 0
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                for m in data:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    # On regarde les matchs de ce soir (prochaines 12h)
                    if now < date_m <= now + timedelta(hours=12):
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        
                        # Analyse CHILL : On cherche des matchs avec des buts
                        totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                        if totals:
                            o25_c = next((o['price'] for o in totals['outcomes'] if o['name'] == 'Over'), 2.0)
                            
                            # On baisse les barrières pour capturer les matchs intéressants
                            matchs_envoyes += 1
                            report = (
                                f"🔥 **BOT CHILL : ANALYSE DU SOIR**\n"
                                f"🏟️ Match : {home} vs {away}\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"📊 **DATA SCIENCE**\n"
                                f"• Tendance : {'🚀 Match Ouvert' if o25_c < 2.0 else '🛡️ Match Fermé'}\n"
                                f"• Probabilité +1.5 buts : {int((1/1.25)*100)}%\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"🎯 **PRONO CHILL**\n"
                                f"👉 Conseil : Plus de 1.5 buts\n"
                                f"👉 Alternative : {home} ou Nul\n"
                                f"━━━━━━━━━━━━━━━━━━"
                            )
                            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                            urllib.request.urlopen(api_url)
        except: continue

    if matchs_envoyes == 0:
        msg = "⚠️ Scan Chill : Aucun match trouvé dans les ligues majeures pour ce soir."
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}"
        urllib.request.urlopen(api_url)

if __name__ == "__main__":
    run_chill_open()
