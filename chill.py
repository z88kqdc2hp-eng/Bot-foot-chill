import urllib.request, json, urllib.parse
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def run_chill_complete():
    now = datetime.utcnow()
    # On ajoute les compétitions de coupes et les ligues secondaires importantes
    leagues = [
        # Championnats
        'soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 
        'soccer_germany_bundesliga', 'soccer_france_ligue_1', 'soccer_portugal_primeira_liga',
        # Coupes et compétitions additionnelles
        'soccer_fa_cup', 'soccer_england_efl_cup', 'soccer_spain_copa_del_rey',
        'soccer_italy_cup', 'soccer_germany_cup', 'soccer_france_cup'
    ]
    
    matchs_analyses = 0
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                for m in data:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    # Scan large de 24h pour ne rien rater ce soir
                    if now < date_m <= now + timedelta(hours=24):
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        
                        # 1. Extraction Cotes
                        h2h = next(mk for mk in bk if mk['key'] == 'h2h')['outcomes']
                        c_h = next(o['price'] for o in h2h if o['name'] == home)
                        c_a = next(o['price'] for o in h2h if o['name'] == away)
                        
                        # 2. Analyse Buts
                        totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                        o15_c = 1.30
                        if totals:
                            o15_c = next((o['price'] for o in totals['outcomes'] if o['point'] == 1.5 and o['name'] == 'Over'), 1.30)

                        # 3. Verdict Intelligent (Double Chance par défaut)
                        if c_h < c_a:
                            conseil = f"{home} ou Nul"
                        else:
                            conseil = f"{away} ou Nul"

                        matchs_analyses += 1
                        report = (
                            f"🔥 **CHILL EXPERT : {m['sport_title'].upper()}**\n"
                            f"🏟️ {home} vs {away}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"📊 **ANALYSE DATA**\n"
                            f"• Victoire {home} : {c_h}\n"
                            f"• Victoire {away} : {c_a}\n"
                            f"• Indice Buts (+1.5) : {'🚀 Élevé' if o15_c < 1.25 else '⚖️ Normal'}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🎯 **PRONO DU SOIR**\n"
                            f"👉 Pari : {conseil}\n"
                            f"👉 Sécurité : +1.5 buts\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                        urllib.request.urlopen(api_url)
        except:
            continue

    if matchs_analyses == 0:
        msg = "✅ Scan complet : Aucun match trouvé dans les 6 nations (Coupes incluses)."
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}"
        urllib.request.urlopen(api_url)

if __name__ == "__main__":
    run_chill_complete()
