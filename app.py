"""Tableau de bord descriptif Auto MPG — lancement : streamlit run app.py."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Exploration des données automobiles", page_icon="🚗", layout="wide")
SOURCE = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
COLORS = {"europe": "#0068c9", "japan": "#83c9ff", "usa": "#ff2b2b"}


@st.cache_data
def load_data():
    # Une copie locale peut être utilisée pour travailler sans connexion.
    local_file = Path(__file__).with_name("mpg.csv")
    df = pd.read_csv(local_file if local_file.exists() else SOURCE)
    df["horsepower"] = pd.to_numeric(df["horsepower"], errors="coerce")
    df["year"] = df["model_year"] + 1900
    # MPG américain : litres / 100 km = 235,214583 / MPG.
    df["consumption_l_100km"] = 235.214583 / df["mpg"].where(df["mpg"] > 0)
    df["weight_kg"] = df["weight"] * 0.45359237
    return df


try:
    data = load_data()
except Exception:
    st.error("Impossible de charger les données. Vérifiez la connexion ou placez mpg.csv à côté de app.py.")
    st.stop()

st.title("🚗 Exploration des données automobiles")
st.caption("Dataset historique Auto MPG · copie CSV publique du dépôt Seaborn")
st.info("mpg élevé = meilleure efficacité. L/100 km faible = consommation moindre. Analyse descriptive, sans modèle IA ni prédiction.")

with st.sidebar:
    st.header("Filtres")
    origin = st.selectbox("Origine", ["Toutes"] + sorted(data["origin"].unique()))
    cylinder_options = sorted(data["cylinders"].unique().tolist())
    cylinders = st.multiselect("Nombre de cylindres", cylinder_options, default=cylinder_options)
    year_min, year_max = int(data["year"].min()), int(data["year"].max())
    years = st.slider("Année du modèle", year_min, year_max, (year_min, year_max))
    minimum_mpg = st.slider("Efficacité minimale (mpg)", float(data["mpg"].min()), float(data["mpg"].max()), float(data["mpg"].min()), step=0.1)

mask = (data["cylinders"].isin(cylinders)
        & data["year"].between(*years)
        & data["mpg"].ge(minimum_mpg))
if origin != "Toutes":
    mask &= data["origin"].eq(origin)
filtered = data.loc[mask].copy()
columns = ["name", "origin", "year", "cylinders", "mpg", "consumption_l_100km", "horsepower", "weight_kg", "acceleration"]

st.header("1 — Indicateurs et données filtrées")
st.write(f"{len(filtered)} observations sur {len(data)}")
if filtered.empty:
    st.warning("Aucun véhicule ne correspond aux filtres. Sélectionnez des cylindres ou élargissez les critères.")
    st.stop()

first, second, third = st.columns(3)
first.metric("Efficacité moyenne", f"{filtered['mpg'].mean():.1f} mpg")
second.metric("Consommation moyenne", f"{filtered['consumption_l_100km'].mean():.1f} L/100 km")
power = filtered["horsepower"].mean()
third.metric("Puissance moyenne", "Non disponible" if pd.isna(power) else f"{power:.1f} hp")
st.caption("Les moyennes ignorent les valeurs manquantes. La consommation moyenne est la moyenne des conversions individuelles, pas la conversion du mpg moyen.")
st.dataframe(filtered[columns].round(2), use_container_width=True, height=350)
st.download_button("Télécharger les données filtrées (CSV)", filtered[columns].to_csv(index=False).encode("utf-8-sig"), "automobiles_filtrees.csv", "text/csv")

st.header("2 — Choisir un véhicule")
# L'index distingue les véhicules dont le nom et l'année sont identiques.
vehicle = st.selectbox("Véhicule", filtered.index.tolist(), format_func=lambda i: f"{data.at[i, 'name']} — {data.at[i, 'year']} (ligne {i + 1})")
st.dataframe(filtered.loc[[vehicle], columns].round(2), use_container_width=True)

st.header("3 — Comparaisons graphiques")
counts = filtered.groupby("origin").size().reset_index(name="Nombre")
fig = px.bar(counts, x="origin", y="Nombre", color="origin", color_discrete_map=COLORS,
             category_orders={"origin": ["europe", "japan", "usa"]},
             title="Nombre d’observations par origine", labels={"origin": "Origine"})
fig.update_layout(template="plotly_white", height=430)
st.plotly_chart(fig, use_container_width=True)

with st.expander("Graphiques complémentaires"):
    scatter = px.scatter(filtered, x="weight_kg", y="mpg", color="origin", hover_name="name",
                         color_discrete_map=COLORS, labels={"weight_kg": "Poids (kg)", "mpg": "Efficacité (mpg)", "origin": "Origine"},
                         title="Poids et efficacité énergétique")
    st.plotly_chart(scatter, use_container_width=True)
    trend = filtered.groupby(["year", "origin"], as_index=False)["mpg"].mean()
    st.plotly_chart(px.line(trend, x="year", y="mpg", color="origin", markers=True,
                           color_discrete_map=COLORS, labels={"year": "Année", "mpg": "Efficacité moyenne (mpg)", "origin": "Origine"},
                           title="Évolution de l’efficacité moyenne"), use_container_width=True)

st.caption("Source : " + SOURCE + " · L’accélération correspond au temps pour atteindre 60 mph (en secondes). Ces données historiques ne représentent pas le marché actuel.")
