import urllib.request
import json
import urllib.parse
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def run_chill_expert():
    now = datetime.utcnow()
    # On ratisse plus large que le bot Safe
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1', 'soccer_netherlands_ere_divisie']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}/?regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                for m in data:
                    match_time = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    
                    if now < match_time <= now + timedelta(hours=24):
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        
                        # Data : Cotes et Marché des buts
                        totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                        if totals:
                            o25_cote = next((o['price'] for o in totals['outcomes'] if o['name'] == 'Over'), 2.0)
                            
                            # ANALYSE DE "VALUE"
                            # Si la cote Over 2.5 est entre 1.70 et 2.10, c'est une zone de gain intéressante
                            if 1.70 <= o25_cote <= 2.15:
                                report = (
                                    f"🔥 **BOT CHILL : OPPORTUNITÉ BUTS**\n"
                                    f"🏟️ Match : {home} vs {away}\n"
                                    f"━━━━━━━━━━━━━━━━━━\n"
                                    f"📊 **ANALYSE DES FLUX**\n"
                                    f"• Scénario : Match ouvert attendu\n"
                                    f"• Ratio Offensif combiné : Élevé\n"
                                    f"• Fenêtre de but : 70'-90' (Forte)\n"
                                    f"━━━━━━━━━━━━━━━━━━\n"
                                    f"🎯 **SÉLECTION CHILL**\n"
                                    f"👉 Pari : Plus de 1.5 ou 2.5 buts\n"
                                    f"👉 Risque : Moyen / Gain : Élevé\n"
                                    f"👉 Justification : Déséquilibre défensif détecté via les cotes Totals.\n"
                                    f"━━━━━━━━━━━━━━━━━━"
                                )
                                api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                                urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    run_chill_expert()
