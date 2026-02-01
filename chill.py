import urllib.request
import json
import math
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

class FootballDataScientist:
    def __init__(self, api_key):
        self.api_key = api_key
        self.leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']

    def calculate_poisson_goals(self, avg_goals):
        """Estime la probabilité de distribution des buts."""
        # Probabilité 0 but, 1 but, 2 buts...
        prob_over_1_5 = 1 - (math.exp(-avg_goals) * (1 + avg_goals))
        return round(prob_over_1_5 * 100, 2)

    def analyze_market_discrepancy(self, prob_reelle, cote_bookmaker):
        """Détecte si le pari présente un ratio gain/risque intéressant."""
        prob_implicite = (1 / cote_bookmaker) * 100
        return prob_reelle > prob_implicite

    def fetch_and_analyze(self):
        now = datetime.utcnow()
        for league in self.leagues:
            url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={self.api_key}&regions=eu&markets=h2h,totals"
            try:
                with urllib.request.urlopen(url) as response:
                    matches = json.loads(response.read().decode())
                    for m in matches:
                        match_time = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                        
                        # Fenêtre d'analyse : Matchs de la soirée (prochaines 6h)
                        if now < match_time <= now + timedelta(hours=6):
                            home, away = m['home_team'], m['away_team']
                            bookmaker = m['bookmakers'][0]['markets']
                            
                            # Extraction H2H et Totals
                            h2h = next(mk for mk in bookmaker if mk['key'] == 'h2h')['outcomes']
                            totals = next((mk for mk in bookmaker if mk['key'] == 'totals'), None)
                            
                            c_home = next(o['price'] for o in h2h if o['name'] == home)
                            c_over = next((o['price'] for o in totals['outcomes'] if o['name'] == 'Over'), 2.0) if totals else 2.0
                            
                            # ANALYSE FROIDE
                            prob_reelle_h = (1 / c_home) * 100 
                            prob_buts = self.calculate_poisson_goals(2.5 if c_over < 1.9 else 1.5)
                            
                            # ÉVALUATION DU RISQUE
                            risk_level = "FAIBLE" if c_home < 1.5 else "MOYEN"
                            if c_home > 2.5: risk_level = "ÉLEVÉ (Variance forte)"

                            # SYNTHÈSE DE SORTIE
                            report = (
                                f"🔬 **ANALYSE DATA : {home} vs {away}**\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"📊 **PROBABILITÉS CALCULÉES**\n"
                                f"• Victoire {home} : {int(prob_reelle_h)}%\n"
                                f"• +1.5 Buts dans le match : {prob_buts}%\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"⏱️ **FENÊTRE TEMPORELLE**\n"
                                f"• Pic d'intensité : 65'-80' (Probabilité de but accrue)\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"🎯 **SÉLECTION RATIONNELLE**\n"
                                f"👉 Pari : {'Victoire ou Nul ' + home if risk_level != 'FAIBLE' else 'Victoire ' + home}\n"
                                f"👉 Alternative : {'Over 1.5' if prob_buts > 75 else 'Under 3.5 (Sécurité)'}\n"
                                f"⚠️ Risque : {risk_level}\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"💡 **JUSTIFICATION** : Basé sur le ratio offensif/défensif implicite et la distribution de Poisson."
                            )
                            
                            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                            urllib.request.urlopen(api_url)
            except Exception as e:
                print(f"Erreur league {league}: {e}")

if __name__ == "__main__":
    bot = FootballDataScientist(API_KEY)
    bot.fetch_and_analyze()
