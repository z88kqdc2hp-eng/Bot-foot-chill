import urllib.request
import json
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def run_real_scout():
    maintenant = datetime.utcnow()
    aujourdhui = maintenant.strftime("%Y-%m-%d")
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    # FILTRE TEMPS RÉEL : Uniquement les matchs à venir
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    if date_m < maintenant: continue
                    
                    home, away = m['home_team'], m['away_team']
                    bk = m['bookmakers'][0]['markets']
                    
                    # Extraction des cotes réelles
                    h2h = next(mk for mk in bk if mk['key'] == 'h2h')['outcomes']
                    cote_h = next(o['price'] for o in h2h if o['name'] == home)
                    cote_a = next(o['price'] for o in h2h if o['name'] == away)
                    cote_n = next(o['price'] for o in h2h if o['name'] == 'Draw')
                    
                    # Calcul des probabilités de victoire
                    prob_h = int((1/cote_h) * 100)
                    prob_n = int((1/cote_n) * 100)
                    fiabilite_v_n = min(99, prob_h + int(prob_n * 0.7))

                    # Analyse du marché des buts (Over 2.5)
                    totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                    over_25_msg = "Analyse indisponible"
                    if totals:
                        cote_over = next((o['price'] for o in totals['outcomes'] if o['name'] == 'Over'), 2.0)
                        over_25_msg = "🔥 Élevé (+2.5)" if cote_over < 1.85 else "🛡️ Modéré (-2.5)"

                    # Mise en forme ultra-claire
                    heure_fr = (date_m + timedelta(hours=1)).strftime("%H:%M")
                    report = (
                        f"🏟️ **MATCH : {home.upper()} vs {away.upper()}**\n"
                        f"⏰ **Heure** : {heure_fr}\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"📊 **PROBABILITÉS RÉELLES**\n"
                        f"• Victoire {home} : {prob_h}%\n"
                        f"• Match Nul : {prob_n}%\n"
                        f"• Sécurité (V ou N) : {fiabilite_v_n}%\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"⚽ **MARCHÉ DES BUTS**\n"
                        f"• Tendance : {over_25_msg}\n"
                        f"• Clean Sheet {home} : {'Oui' if cote_h < 1.6 else 'Non'}\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"🎯 **VERDICT** : {'Victoire Directe' if prob_h > 65 else 'Victoire ou Nul'}\n"
                        f"━━━━━━━━━━━━━━━━━━"
                    )
                    
                    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                    urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    run_real_scout()
