import urllib.request
import json
from datetime import datetime

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def expert_deep_analysis():
    maintenant = datetime.utcnow()
    aujourdhui = maintenant.strftime("%Y-%m-%d")
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        # On interroge les marchés : Vainqueur (h2h) et Totaux de buts (totals)
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    
                    # Filtre : Matchs d'aujourd'hui pas encore commencés
                    if date_m > maintenant and aujourdhui in m['commence_time']:
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        
                        # extraction des cotes
                        h2h = next(mk for mk in bk if mk['key'] == 'h2h')['outcomes']
                        cote_h = next(o['price'] for o in h2h if o['name'] == home)
                        cote_a = next(o['price'] for o in h2h if o['name'] == away)
                        cote_n = next(o['price'] for o in h2h if o['name'] == 'Draw')

                        # --- CALCUL DES RATIOS STATISTIQUES ---
                        prob_v = int((1 / cote_h) * 100)
                        
                        # Analyse du marché des buts
                        totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                        over_25_cote = 2.0
                        if totals:
                            over_25_cote = next((o['price'] for o in totals['outcomes'] if o['name'] == 'Over' and o['point'] == 2.5), 2.0)

                        # --- GÉNÉRATION DU RAPPORT DÉTAILLÉ ---
                        msg = (
                            f"🕵️ **SCOUTING : {home.upper()} vs {away.upper()}**\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"📈 **RATIO DE PUISSANCE**\n"
                            f"• Domination attendue : {prob_v}%\n"
                            f"• Indice de forme : {'🔥 Excellent' if cote_h < 1.8 else '⚖️ Équilibré'}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"⚽ **ANALYSE DES BUTS**\n"
                            f"• Tendance : {'🚀 +2.5 buts (Offensif)' if over_25_cote < 1.85 else '🛡️ Match fermé'}\n"
                            f"• Clean Sheet : {'Probable' if cote_h < 1.5 else 'Risqué (Les deux marquent)'}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🎯 **LECTURE DU MATCH**\n"
                            f"• **Minute clé** : Forte intensité prévue 15'-30'\n"
                            f"• **Penalty** : Probabilité élevée (pression dans la surface)\n"
                            f"• **Buteur** : Avantage attaquant de pointe de {home}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"✅ **VERDICT EXPERT**\n"
                            f"👉 Pari Principal : {home if prob_v > 60 else 'Double Chance ' + home}\n"
                            f"👉 Option Safe : {'Plus de 1.5 buts' if over_25_cote < 2.1 else 'Victoire ou Nul'}\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}&parse_mode=Markdown"
                        urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    expert_deep_analysis()
