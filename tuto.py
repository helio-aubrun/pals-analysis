import streamlit as st
import pandas as pd

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
filtered_df = df[df["Element1"] == selected_option]
selected_columns = filtered_df.loc[:, ["Name", "4Dtotal"]]
sorted_selected_columns = selected_columns.sort_values(by="4Dtotal", ascending=False)
top_10_sorted = sorted_selected_columns.head(10)
sorted_selected_columns_reverse = top_10_sorted.sort_values(by="4Dtotal", ascending=True)

# Il n'est pas nécessaire de transposer le DataFrame pour un graphique à barres horizontales ; utilisez directement les données triées
top_10_horizontal_bar_chart = sorted_selected_columns_reverse.plot(kind='barh', figsize=(10, 5), legend=False)

# Afficher le graphique avec Streamlit
st.pyplot(top_10_horizontal_bar_chart.figure)