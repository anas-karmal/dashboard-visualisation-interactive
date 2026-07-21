import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Dashboard Titanic", layout="wide")

# Titre
st.title("🚢 Dashboard de Visualisation Interactive - Titanic")
st.write("Analyse dynamique des données des passagers du Titanic")

# Chargement des données
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# Nettoyage basique avec Pandas
df_clean = df.copy()
df_clean["Age"] = df_clean["Age"].fillna(df_clean["Age"].median())
df_clean["Embarked"] = df_clean["Embarked"].fillna(df_clean["Embarked"].mode()[0])
df_clean.drop(columns=["Cabin"], inplace=True, errors="ignore")

# Sidebar - filtres interactifs
st.sidebar.header("Filtres")
sexe = st.sidebar.multiselect(
    "Sexe",
    options=df_clean["Sex"].unique(),
    default=df_clean["Sex"].unique()
)
classe = st.sidebar.multiselect(
    "Classe",
    options=sorted(df_clean["Pclass"].unique()),
    default=sorted(df_clean["Pclass"].unique())
)
age_min, age_max = st.sidebar.slider(
    "Tranche d'âge",
    int(df_clean["Age"].min()), int(df_clean["Age"].max()),
    (int(df_clean["Age"].min()), int(df_clean["Age"].max()))
)

# Application des filtres
df_filtered = df_clean[
    (df_clean["Sex"].isin(sexe)) &
    (df_clean["Pclass"].isin(classe)) &
    (df_clean["Age"].between(age_min, age_max))
]

# Statistiques descriptives
st.subheader("Statistiques générales")
col1, col2, col3 = st.columns(3)
col1.metric("Nombre de passagers", len(df_filtered))
col2.metric("Taux de survie", f"{df_filtered['Survived'].mean()*100:.1f}%")
col3.metric("Âge moyen", f"{df_filtered['Age'].mean():.1f} ans")

# Graphique 1 : Survie par classe
st.subheader("Taux de survie par classe")
fig1, ax1 = plt.subplots()
sns.barplot(data=df_filtered, x="Pclass", y="Survived", ax=ax1)
ax1.set_xlabel("Classe")
ax1.set_ylabel("Taux de survie")
st.pyplot(fig1)

# Graphique 2 : Distribution des âges
st.subheader("Distribution des âges")
fig2, ax2 = plt.subplots()
sns.histplot(df_filtered["Age"], bins=20, kde=True, ax=ax2)
ax2.set_xlabel("Âge")
st.pyplot(fig2)
# Graphique 3 : Survie par sexe
st.subheader("Survie par sexe")
fig3, ax3 = plt.subplots()
sns.countplot(data=df_filtered, x="Sex", hue="Survived", ax=ax3)
ax3.set_xlabel("Sexe")
ax3.legend(title="Survécu", labels=["Non", "Oui"])
st.pyplot(fig3)

# Tableau de données brut
st.subheader("Données détaillées")
st.dataframe(df_filtered)