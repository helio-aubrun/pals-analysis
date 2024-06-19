import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Base Stat Pals", layout="wide")

df = pd.read_csv('Palworld_Data--Palu combat attribute table.csv')


# Définir les options pour la radio et la multiselect
options_radio = ["generally"]
options_multiselect = df["Element1"].unique().tolist()
options_multiselect.pop(0)
# Utiliser beta_sidebar pour placer le choix dans la sidebar
with st.sidebar:
    choice = st.radio("Type:", options_radio + [f"{i}" for i in options_multiselect])

if choice == "Autre":
    # Si l'utilisateur choisit "Autre", afficher la liste déroulante pour sélectionner une option spécifique
    selected_option = st.selectbox("Sélectionnez une option spécifique:", options_multiselect)
else:
    # Si l'utilisateur choisit "generally" ou toute autre option non "Autre", procéder avec cette sélection
    selected_option = choice.replace("Autre ", "")

# Filtrer le dataframe selon la sélection
filtered_df = df[df['Element1'].isin([selected_option]) | df['Element2'].isin([selected_option])]
selected_columns = filtered_df.loc[:, ["Name", "4Dtotal"]]
sorted_selected_columns = selected_columns.sort_values(by="4Dtotal", ascending=False)
top_10_sorted = sorted_selected_columns.head(10)
sorted_selected_columns_reverse = top_10_sorted.sort_values(by="4Dtotal", ascending=True)

sorted_selected_columns_reverse.set_index("Name", inplace=True)

# Créer le graphique à barres horizontales avec Plotly
fig = px.bar(
    sorted_selected_columns_reverse,
    x="4Dtotal",
    y=sorted_selected_columns_reverse.index,
    orientation='h',
    title="Top 10 Sorted by 4Dtotal",
    labels={"index": "Name"},
    text="4Dtotal"
)

# Mettre à jour les couleurs et le style du graphique
fig.update_traces(marker_color='darkblue', textposition='outside')
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white'
)

# Afficher le graphique avec Streamlit
st.plotly_chart(fig)