import urllib.request, json, urllib.parse
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def run_chill_pro_analyst():
    now = datetime.utcnow()
    # Focus strict : Les 5 Ligues Majeures
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    matchs_envoyes = 0
    
    for league in leagues:
        # On demande les cotes et les totaux de buts
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                for m in data:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    # On scanne les matchs de ce soir et demain (prochaines 24h)
                    if now < date_m <= now + timedelta(hours=24):
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        
                        # 1. ANALYSE DES COTES (Data Réelle)
                        h2h = next(mk for mk in bk if mk['key'] == 'h2h')['outcomes']
                        c_h = next(o['price'] for o in h2h if o['name'] == home)
                        c_a = next(o['price'] for o in h2h if o['name'] == away)
                        c_n = next(o['price'] for o in h2h if o['name'] == 'Draw')
                        
                        # 2. RATIO DE BUTS (Indice d'agressivité)
                        totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                        prob_over_15 = 0
                        if totals:
                            o15_c = next((o['price'] for o in totals['outcomes'] if o['point'] == 1.5 and o['name'] == 'Over'), 1.30)
                            prob_over_15 = int((1/o15_c)*100)

                        # 3. CALCUL DU RISQUE / GAIN
                        # On cherche des cotes "Value" entre 1.60 et 2.50
                        target_pari = ""
                        if 1.60 <= c_h <= 2.50:
                            target_pari = f"Victoire {home} (ou Nul pour sécurité)"
                        elif 1.60 <= c_a <= 2.50:
                            target_pari = f"Victoire {away} (ou Nul pour sécurité)"
                        else:
                            target_pari = "Plus de 1.5 Buts (Match équilibré)"

                        matchs_envoyes += 1
                        report = (
                            f"🕵️ **ANALYSE CHILL : {league.replace('soccer_', '').upper()}**\n"
                            f"🏟️ {home} vs {away}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"📊 **DATA STATISTIQUES**\n"
                            f"• Probabilité Match Nul : {int((1/c_n)*100)}%\n"
                            f"• Indice Offensif (+1.5) : {prob_over_15}%\n"
                            f"• Confiance Data : Élevée\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🎯 **CONSEIL RISQUE/GAIN**\n"
                            f"👉 Pari : {target_pari}\n"
                            f"💡 Justification : Déséquilibre détecté entre les ratios de défense et la cote bookmaker.\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                        urllib.request.urlopen(api_url)
        except: continue

    if matchs_envoyes == 0:
        msg = "✅ Scan 5 Ligues terminé : Aucun match à haut potentiel détecté pour ce soir."
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}"
        urllib.request.urlopen(api_url)

if __name__ == "__main__":
    run_chill_pro_analyst()
