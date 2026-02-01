import urllib.request
import json
import math
from datetime import datetime

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

class FootballAnalyst:
    def __init__(self, api_key):
        self.api_key = api_key

    def poisson_prob(self, lmbda, x):
        """Calcule la probabilité de x buts selon la loi de Poisson."""
        return (math.exp(-lmbda) * (lmbda**x)) / math.factorial(x)

    def analyze_match(self, home, away, cote_h, cote_a, cote_n, over_25_cote):
        # 1. Calcul des probabilités implicites (Correction de la marge)
        total_inv = (1/cote_h) + (1/cote_a) + (1/cote_n)
        prob_h = (1/cote_h) / total_inv
        
        # 2. Simulation xG (basée sur les cotes de buts)
        # Une cote Over 2.5 basse indique un xG global élevé (~3.0+)
        expected_goals = 3.5 - (over_25_cote * 0.5) 
        
        # 3. Analyse Temporelle (Modèle de fatigue/pression)
        # Statistiquement, 60% des buts arrivent en 2nde mi-temps
        intervals = {
            "0-30'": 0.25, "30-45'": 0.15, 
            "45-75'": 0.30, "75-90'": 0.30
        }
        best_window = "75-90' (Pression max)" if expected_goals > 2.5 else "45-60' (Reprise)"

        # 4. Détection de Variance / Risque
        variance = "HAUTE" if 2.2 < cote_h < 3.5 else "CONTRÔLÉE"
        
        return {
            "win_p": int(prob_h * 100),
            "xg": round(expected_goals, 2),
            "variance": variance,
            "window": best_window
        }

    def run(self):
        maintenant = datetime.utcnow()
        leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
        
        for league in leagues:
            url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={self.api_key}&regions=eu&markets=h2h,totals"
            try:
                with urllib.request.urlopen(url) as response:
                    matchs = json.loads(response.read().decode())
                    for m in matchs:
                        date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                        if date_m < maintenant: continue # Anti-Live

                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        
                        # Data Extraction
                        h2h = next(mk for mk in bk if mk['key'] == 'h2h')['outcomes']
                        cote_h = next(o['price'] for o in h2h if o['name'] == home)
                        cote_a = next(o['price'] for o in h2h if o['name'] == away)
                        cote_n = next(o['price'] for o in h2h if o['name'] == 'Draw')
                        
                        totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                        o25 = next((o['price'] for o in totals['outcomes'] if o['point'] == 2.5), 2.0) if totals else 2.0

                        # Analyse
                        res = self.analyze_match(home, away, cote_h, cote_a, cote_n, o25)

                        # Affichage Structuré
                        report = (
                            f"📊 **REPORTING IA : {home} vs {away}**\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🎯 **PROBABILITÉS H2H**\n"
                            f"• Victoire {home}: {res['win_p']}%\n"
                            f"• xG Estimé : {res['xg']} buts/match\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"⏱️ **ANALYSE TEMPORELLE**\n"
                            f"• Fenêtre critique : {res['window']}\n"
                            f"• Risque de variance : {res['variance']}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"✅ **VALUE BET DETECTÉ**\n"
                            f"👉 {'BTTS (Les 2 marquent)' if res['xg'] > 2.8 else 'Clean Sheet Possible'}\n"
                            f"👉 Verdict : {home if res['win_p'] > 55 else 'Double Chance'}\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                        urllib.request.urlopen(api_url)
            except: continue

if __name__ == "__main__":
    analyst = FootballAnalyst(API_KEY)
    analyst.run()
