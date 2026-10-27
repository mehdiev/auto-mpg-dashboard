# 🚗 Exploration des données automobiles

Tableau de bord pédagogique en français réalisé avec Python, Streamlit, Pandas et Plotly, sur les 398 observations du jeu de données Auto MPG.

## Installation et lancement

Python 3.10 ou plus récent est nécessaire. Depuis le dossier du projet :

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py --global.developmentMode false
```

Ouvrir l'adresse locale affichée par Streamlit, généralement http://localhost:8501.

## Fonctionnalités

- Filtres par origine, cylindres, année et efficacité minimale.
- Moyennes du mpg, de la consommation en L/100 km et de la puissance.
- Tableau interactif et export CSV.
- Sélection d'un véhicule précis.
- Répartition des véhicules par origine.
- Graphiques complémentaires : poids et efficacité, évolution annuelle.

## Données et calculs

Le fichier `mpg.csv` est une copie du [jeu de données public Seaborn](https://github.com/mwaskom/seaborn-data/blob/master/mpg.csv). Consulter ce dépôt pour la provenance et les informations relatives aux données.

- Année : `model_year + 1900`.
- Poids en kg : `weight × 0.45359237`.
- Consommation en L/100 km : `235.214583 / mpg` (gallon américain).
- Les moyennes ignorent les valeurs manquantes.
- La consommation moyenne est calculée sur les conversions individuelles.

Sans filtres restrictifs : 398 véhicules, 23,5 mpg, 11,2 L/100 km et 104,5 hp environ. Les effectifs par origine sont 70 pour l'Europe, 79 pour le Japon et 249 pour les États-Unis.

L'application utilise le fichier local, donc fonctionne sans connexion après installation des bibliothèques. Si le fichier est absent, elle tente un chargement en ligne.

Il s'agit d'une analyse descriptive de données historiques de 1970 à 1982, sans modèle prédictif ni régression.
