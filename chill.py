import urllib.request, json, urllib.parse
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

# PAYS AUTORISÉS
PAYS_CIBLES = ["France", "England", "Spain", "Italy", "Germany", "Portugal"]

def run_chill_full_scan():
    now = datetime.utcnow()
    # 1. On récupère d'abord TOUTES les ligues disponibles
    leagues_url = f"https://api.the-odds-api.com/v4/sports/?apiKey={API_KEY}"
    matchs_analyses = 0
    
    try:
        with urllib.request.urlopen(leagues_url) as resp:
            all_sports = json.loads(resp.read().decode())
            # On ne garde que le foot (soccer) des pays cibles
            target_leagues = [s['key'] for s in all_sports if s['group'] == 'Soccer' and any(p in s['title'] for p in PAYS_CIBLES)]
            
            for league in target_leagues:
                url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
                try:
                    with urllib.request.urlopen(url) as response:
                        data = json.loads(response.read().decode())
                        for m in data:
                            date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                            # Scan des matchs dans les prochaines 24h
                            if now < date_m <= now + timedelta(hours=24):
                                home, away = m['home_team'], m['away_team']
                                bk = m['bookmakers'][0]['markets']
                                
                                # Extraction Cotes 1N2
                                h2h = next(mk for mk in bk if mk['key'] == 'h2h')['outcomes']
                                c_h = next(o['price'] for o in h2h if o['name'] == home)
                                c_a = next(o['price'] for o in h2h if o['name'] == away)
                                
                                # Analyse Dynamique des Buts
                                totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                                o15_c = 1.30
                                if totals:
                                    o15_c = next((o['price'] for o in totals['outcomes'] if o['point'] == 1.5 and o['name'] == 'Over'), 1.30)

                                # Logique de verdict Data
                                conseil = f"{home} ou Nul" if c_h <= c_a else f"{away} ou Nul"

                                matchs_analyses += 1
                                report = (
                                    f"🔥 **CHILL DATA : {m['sport_title'].upper()}**\n"
                                    f"🏟️ {home} vs {away}\n"
                                    f"━━━━━━━━━━━━━━━━━━\n"
                                    f"📊 **ANALYSE STATISTIQUE**\n"
                                    f"• Victoire {home} : {c_h}\n"
                                    f"• Victoire {away} : {c_a}\n"
                                    f"• Potentiel Buts : {'🚀 Élevé' if o15_c < 1.25 else '⚖️ Normal'}\n"
                                    f"━━━━━━━━━━━━━━━━━━\n"
                                    f"🎯 **VERDICT CHILL**\n"
                                    f"👉 Pari : {conseil}\n"
                                    f"👉 Sécurité : +1.5 buts\n"
                                    f"━━━━━━━━━━━━━━━━━━"
                                )
                                api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                                urllib.request.urlopen(api_url)
                except: continue
    except Exception as e:
        print(f"Erreur Scan : {e}")

    if matchs_analyses == 0:
        msg = "✅ Scan terminé : Aucun match trouvé pour les 6 pays cibles."
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}"
        urllib.request.urlopen(api_url)

if __name__ == "__main__":
    run_chill_full_scan()
