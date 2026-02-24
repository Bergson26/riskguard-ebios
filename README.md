🛡️ RiskGuard - Assistant d'Analyse de Risques Cyber (EBIOS RM)
Développé par Bergson Jean-Michel.

📝 À propos du projet
RiskGuard est un outil interactif d'aide à la décision conçu pour les Responsables de la Sécurité des Systèmes d'Information (RSSI) et les équipes de gouvernance. Il digitalise et simplifie l'évaluation des risques cyber en s'appuyant sur la méthodologie EBIOS Risk Manager, le standard recommandé par l'ANSSI en France.

Ce projet a été réalisé afin de démontrer une double compétence en développement d'outils automatisés et en gouvernance de la sécurité des systèmes d'information, en préparation de mon intégration en cycle Bac+5 en Cybersécurité, Administration, Systèmes et Réseaux dès septembre 2026.

🚀 Fonctionnalités Principales
Inventaire Dynamique des Actifs
Interface permettant de recenser et de catégoriser les valeurs métiers et les biens supports avec leur niveau de sensibilité.

Évaluation des Événements Redoutés (ER)
Moteur de calcul du risque basé sur le croisement classique : Impact x Vraisemblance.

Cartographie des Risques (Heatmap)
Génération instantanée d'une matrice de risques 4x4.

Plan de Traitement Automatisé et Exportabilité
Moteur de règles suggérant des mesures de sécurité proportionnées au risque. Génération d'un rapport complet téléchargeable au format CSV.

🏗️ Architecture et Stack Technique
Interface Web et Logique : Python 3, Streamlit

Manipulation des Données : Pandas

Visualisation Interactive : Plotly Graph Objects

🛠️ Installation et Utilisation en local
Cloner le dépôt :
git clone https://github.com/BErgson26/riskguard-ebios.git
cd riskguard-ebios

Installer les dépendances requises :
pip install -r requirements.txt

Lancer l'application web :
python -m streamlit run src/app.py

L'interface s'ouvrira automatiquement à l'adresse http://localhost:8501.

🔒 Confidentialité des données
Ce projet fonctionne entièrement en local. Aucune donnée saisie n'est envoyée vers des serveurs externes.