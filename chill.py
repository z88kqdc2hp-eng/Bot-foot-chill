import urllib.request
import json
from datetime import datetime, timedelta

API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def run_dynamic_scout():
    now = datetime.utcnow()
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    
                    # On analyse uniquement les matchs à venir (18h-22h)
                    if now < date_m <= now + timedelta(hours=5):
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        
                        # 1. EXTRACTION DES COTES RÉELLES
                        h2h = next(mk for mk in bk if mk['key'] == 'h2h')['outcomes']
                        cote_h = next(o['price'] for o in h2h if o['name'] == home)
                        cote_a = next(o['price'] for o in h2h if o['name'] == away)
                        
                        # 2. CALCUL DES RATIOS DYNAMIQUES
                        # Plus la cote est basse, plus le ratio de puissance est élevé
                        ratio_h = round(3.0 / cote_h, 2) 
                        ratio_a = round(3.0 / cote_a, 2)
                        prob_v = int((1/cote_h) * 100)

                        # 3. ANALYSE DES BUTS (OVER 2.5)
                        totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                        o25_cote = 2.0
                        if totals:
                            o25_cote = next((o['price'] for o in totals['outcomes'] if o['name'] == 'Over'), 2.0)
                        
                        # 4. GÉNÉRATION DU RAPPORT UNIQUE
                        report = (
                            f"📝 **DOSSIER MATCH : {home.upper()} vs {away.upper()}**\n"
                            f"🏆 **Ligue** : {league.replace('soccer_', '').upper()}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"📊 **STATISTIQUES DE PUISSANCE**\n"
                            f"• Ratio Offensif {home} : {ratio_h}\n"
                            f"• Ratio Défensif {away} : {round(1/ratio_a, 2)}\n"
                            f"• Probabilité Victoire : {prob_v}%\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"⏱️ **CHRONOLOGIE PROBABLE**\n"
                            f"• 0'-30' : {'Pressing haut attendu' if ratio_h > 1.8 else 'Phase d observation'}\n"
                            f"• 75'-90' : {'TRÈS ÉLEVÉE (Fin de match ouverte)' if o25_cote < 1.8 else 'Moyenne (Bloc compact)'}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🎯 **VERDICT SCIENTIFIQUE**\n"
                            f"👉 **Conseil** : {'Victoire Directe' if prob_v > 65 else 'Double Chance ' + home}\n"
                            f"👉 **Pourquoi ?** : Le ratio de puissance de {home} ({ratio_h}) est nettement supérieur au bloc adverse.\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                        urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    run_dynamic_scout()
