import urllib.request, json, urllib.parse
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def run_chill_elite_6():
    now = datetime.utcnow()
    # Focus strict sur les 6 nations demandées
    leagues = [
        'soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 
        'soccer_germany_bundesliga', 'soccer_france_ligue_1',
        'soccer_portugal_primeira_liga'
    ]
    
    matchs_analyses = 0
    
    for league in leagues:
        # Requête pour les cotes 1N2 et les Totals de buts
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                for m in data:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    # Analyse des matchs dans une fenêtre de 24h
                    if now < date_m <= now + timedelta(hours=24):
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        
                        # 1. Extraction Data 1N2
                        h2h = next(mk for mk in bk if mk['key'] == 'h2h')['outcomes']
                        c_h = next(o['price'] for o in h2h if o['name'] == home)
                        c_a = next(o['price'] for o in h2h if o['name'] == away)
                        
                        # 2. Analyse de la Probabilité de Buts (Over 1.5)
                        totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                        prob_buts = "Moyenne"
                        if totals:
                            o15_c = next((o['price'] for o in totals['outcomes'] if o['point'] == 1.5 and o['name'] == 'Over'), 1.30)
                            if o15_c < 1.25: prob_buts = "🔥 TRÈS ÉLEVÉE"

                        # 3. Logique de Décision Data-Driven
                        # On ne privilégie le domicile que si la cote est significativement plus basse
                        if c_h < (c_a - 0.50):
                            conseil = f"{home} ou Nul"
                            justification = f"Puissance offensive de {home} supérieure à domicile."
                        elif c_a < (c_h - 0.50):
                            conseil = f"{away} ou Nul"
                            justification = f"L'équipe visiteuse ({away}) est statistiquement favorite."
                        else:
                            conseil = "Match Nul ou +1.5 Buts"
                            justification = "Équilibre des forces détecté, match indécis."

                        matchs_analyses += 1
                        report = (
                            f"🔥 **CHILL EXPERT : {league.replace('soccer_', '').upper()}**\n"
                            f"🏟️ {home} vs {away}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"📊 **STATISTIQUES DU MARCHÉ**\n"
                            f"• Cote Domicile : {c_h}\n"
                            f"• Cote Extérieur : {c_a}\n"
                            f"• Probabilité +1.5 buts : {prob_buts}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🎯 **ANALYSE RATIONNELLE**\n"
                            f"👉 Pari : {conseil}\n"
                            f"💡 Pourquoi : {justification}\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                        urllib.request.urlopen(api_url)
        except:
            continue

    if matchs_analyses == 0:
        msg = "✅ Scan Chill terminé : Aucun match détecté dans les 6 nations pour les prochaines 24h."
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}"
        urllib.request.urlopen(api_url)

if __name__ == "__main__":
    run_chill_elite_6()
