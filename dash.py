import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Titanic",
    page_icon="🚢",
    layout="wide"
)

# Style CSS léger pour un rendu plus pro
st.markdown("""
    <style>
    .block-container {padding-top: 2rem;}
    div[data-testid="stMetric"] {
        background-color: #1e2127;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Chargement des données
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# Nettoyage
df_clean = df.copy()
df_clean["Age"] = df_clean["Age"].fillna(df_clean["Age"].median())
df_clean["Embarked"] = df_clean["Embarked"].fillna(df_clean["Embarked"].mode()[0])
df_clean.drop(columns=["Cabin"], inplace=True, errors="ignore")
df_clean["Survived_label"] = df_clean["Survived"].map({0: "Non", 1: "Oui"})

# En-tête
st.title("🚢 Dashboard Titanic")
st.caption("Analyse dynamique des données des passagers")

# Sidebar - filtres
with st.sidebar:
    st.header("🔍 Filtres")
    sexe = st.multiselect("Sexe", df_clean["Sex"].unique(), default=df_clean["Sex"].unique())
    classe = st.multiselect("Classe", sorted(df_clean["Pclass"].unique()), default=sorted(df_clean["Pclass"].unique()))
    age_min, age_max = st.slider(
        "Tranche d'âge",
        int(df_clean["Age"].min()), int(df_clean["Age"].max()),
        (int(df_clean["Age"].min()), int(df_clean["Age"].max()))
    )

df_filtered = df_clean[
    (df_clean["Sex"].isin(sexe)) &
    (df_clean["Pclass"].isin(classe)) &
    (df_clean["Age"].between(age_min, age_max))
]

# Métriques clés
col1, col2, col3, col4 = st.columns(4)
col1.metric("Passagers", len(df_filtered))
col2.metric("Taux de survie", f"{df_filtered['Survived'].mean()*100:.1f}%")
col3.metric("Âge moyen", f"{df_filtered['Age'].mean():.1f} ans")
col4.metric("Tarif moyen", f"{df_filtered['Fare'].mean():.0f} £")

st.divider()

# Graphiques en grille compacte (2 colonnes)
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Survie par classe")
    fig1 = px.bar(
        df_filtered.groupby("Pclass")["Survived"].mean().reset_index(),
        x="Pclass", y="Survived",
        labels={"Pclass": "Classe", "Survived": "Taux de survie"},
        color="Pclass",
        height=280
    )
    fig1.update_layout(showlegend=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig1, use_container_width=True)

with row1_col2:
    st.subheader("Survie par sexe")
    fig2 = px.histogram(
        df_filtered, x="Sex", color="Survived_label",
        barmode="group",
        labels={"Sex": "Sexe", "count": "Nombre"},
        height=280
    )
    fig2.update_layout(legend_title="Survécu", margin=dict(t=10, b=10))
    st.plotly_chart(fig2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Distribution des âges")
    fig3 = px.histogram(
        df_filtered, x="Age", nbins=20,
        height=280
    )
    fig3.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig3, use_container_width=True)

with row2_col2:
    st.subheader("Répartition des tarifs")
    fig4 = px.box(
        df_filtered, x="Pclass", y="Fare",
        labels={"Pclass": "Classe", "Fare": "Tarif"},
        height=280
    )
    fig4.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Données détaillées (repliable)
with st.expander("📋 Voir les données détaillées"):
    st.dataframe(df_filtered, use_container_width=True)