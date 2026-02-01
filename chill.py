import urllib.request
import json
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def run_advanced_scout():
    maintenant = datetime.utcnow()
    aujourdhui = maintenant.strftime("%Y-%m-%d")
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        # On extrait les cotes vainqueur et totaux de buts
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    
                    # FILTRE : Uniquement les vrais matchs restants aujourd'hui
                    if date_m > maintenant and aujourdhui in m['commence_time']:
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        
                        # 1. ANALYSE DES COTES RÉELLES
                        h2h = next(mk for mk in bk if mk['key'] == 'h2h')['outcomes']
                        cote_h = next(o['price'] for o in h2h if o['name'] == home)
                        cote_a = next(o['price'] for o in h2h if o['name'] == away)
                        cote_n = next(o['price'] for o in h2h if o['name'] == 'Draw')
                        
                        # 2. CALCUL DES PROBABILITÉS (Rigueur Statistique)
                        prob_h = int((1/cote_h) * 100)
                        prob_n = int((1/cote_n) * 100)
                        fiabilite_securisee = min(99, prob_h + int(prob_n * 0.75))

                        # 3. ANALYSE DYNAMIQUE DES BUTS
                        totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                        over_25_cote = 2.0
                        if totals:
                            over_25_cote = next((o['price'] for o in totals['outcomes'] if o['point'] == 2.5), 2.0)
                        
                        # On varie la fenêtre de but selon l'intensité
                        fenetre = "75'-90' (Fatigue adverse)" if over_25_cote < 1.9 else "45'-60' (Retour vestiaire)"
                        tendance = "🚀 Match Ouvert (+2.5)" if over_25_cote < 1.85 else "🛡️ Tactique (-2.5)"

                        # 4. MISE EN FORME PROPRE
                        heure_fr = (date_m + timedelta(hours=1)).strftime("%H:%M")
                        report = (
                            f"🕵️ **SCOUTING : {home.upper()} vs {away.upper()}**\n"
                            f"⏰ **Coup d'envoi** : {heure_fr}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"📊 **RATIOS & ENJEUX**\n"
                            f"• Probabilité Victoire : {prob_h}%\n"
                            f"• Sécurité (V ou N) : {fiabilite_securisee}%\n"
                            f"• Risque de Nul : {'Élevé' if cote_n < 3.5 else 'Faible'}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"⚽ **STATS AVANCÉES**\n"
                            f"• Style attendu : {tendance}\n"
                            f"• Fenêtre de but probable : {fenetre}\n"
                            f"• Penalty / Minute clé : {'Possible 80' if over_25_cote < 1.7 else 'Faible'}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🎯 **VERDICT IA**\n"
                            f"👉 Pari conseillé : {'Victoire' if prob_h > 65 else 'Double Chance ' + home}\n"
                            f"👉 Option Buteur : Star offensive de {home}\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                        urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    run_advanced_scout()
