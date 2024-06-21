import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Base Stat Pals", layout="wide")

df = pd.read_csv('Palworld_Data--Palu combat attribute table.csv')
df_job = pd.read_csv('Palworld_Data-Palu Job Skills Table.csv')

# Sidebar pour filtrer par type
# Définir les options pour la radio et la multiselect
options_radio = ["generally"]
options_multiselect = df["Element1"].unique().tolist()
options_multiselect.pop(0)
# Utiliser sidebar pour placer le choix dans la sidebar
with st.sidebar:
    choice = st.radio("Type:", options_radio + [f"{i}" for i in options_multiselect])

if choice == "Autre":
    # Si l'utilisateur choisit "Autre", afficher la liste déroulante pour sélectionner une option spécifique
    selected_option = st.selectbox("Sélectionnez une option spécifique:", options_multiselect)
else:
    # Si l'utilisateur choisit "generally" ou toute autre option non "Autre", procéder avec cette sélection
    selected_option = choice.replace("Autre ", "")

# Début du grahique Top 10 des pals ayant le plus de statistique par types
# Filtrer le dataframe pour le top 10 des pals avec le plus de stats hp, def, atk
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
    title="Top 10 des pals ayant le plus de statistique par types",
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
fig.update_xaxes(visible=False)
fig.update_yaxes(title="")

# Afficher le graphique avec Streamlit
st.plotly_chart(fig)
# Fin du grahique Top 10 des pals ayant le plus de statistique par types

# Début du graphique Répartition des types
element1_counts = df['Element1'].value_counts()
element2_counts = df['Element2'].value_counts()

# Fusionner les comptages pour avoir un seul ensemble de données
counts_total = element1_counts.add(element2_counts, fill_value=0)

# Convertir les comptages en pourcentages
counts_total_percentage = counts_total / counts_total.sum() * 100

# Préparer les labels pour le diagramme
labels = counts_total_percentage.index
values = counts_total_percentage.values

fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
fig.update_layout(title_text="Répartition des types",
                height=600,  # Hauteur de la figure en pixels
                width=800,  # Largeur de la figure en pixels
                legend=dict(
                    font_size=16,  # Taille de la police de la légende
    )
)

st.plotly_chart(fig)
# Fin du graphique Répartition des types

# Afficher l'image dans votre application Streamlit
image_path = 'image/type.jpg'
st.image(image_path)


# Début du graphique Top 10 des montures les plus rapides
riding_df = df.loc[:, ["Name", "Riding_sprint_speed"]]
sorted_riding_df = riding_df.sort_values(by="Riding_sprint_speed", ascending=False)
top_10_riding = sorted_riding_df.head(10)
sorted_riding_df_reverse = top_10_riding.sort_values(by="Riding_sprint_speed", ascending=True)
sorted_riding_df_reverse.set_index("Name", inplace=True)

# Créer le graphique à barres horizontales avec Plotly
fig_riding = px.bar(
    sorted_riding_df_reverse,
    x="Riding_sprint_speed",
    y=sorted_riding_df_reverse.index,
    orientation='h',
    title="Top 10 des montures les plus rapides",
    labels={"index": "Name"},
    text="Riding_sprint_speed"
)

# Mettre à jour les couleurs et le style du graphique
fig_riding.update_traces(marker_color='darkblue', textposition='outside')
fig_riding.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white'
)
fig_riding.update_xaxes(visible=False)
fig_riding.update_yaxes(title="")

# Afficher le graphique avec Streamlit
st.plotly_chart(fig_riding)
# Fin du graphique Top 10 des montures les plus rapides

# Sidebar pour filtrer par job
# Définir les options pour la radio et la multiselect
options_radio = ["Make a fire"]
options_multiselect = ["watering","planting","generate electricity","manual","collection","logging","Mining","pharmaceutical","cool down","pasture","carry","Handling speed"]
# Utiliser sidebar pour placer le choix dans la sidebar
with st.sidebar:
    choice = st.radio("Job:", options_radio + [f"{i}" for i in options_multiselect])

if choice == "Autre":
    # Si l'utilisateur choisit "Autre", afficher la liste déroulante pour sélectionner une option spécifique
    selected_option_job = st.selectbox("Sélectionnez une option spécifique:", options_multiselect)
else:
    # Si l'utilisateur choisit "generally" ou toute autre option non "Autre", procéder avec cette sélection
    selected_option_job = choice.replace("Autre ", "")

# Début du graphique Top 5 des pals par job
filtered_df_job = df_job[df_job[selected_option_job]]
selected_columns_job = filtered_df_job.loc[:, ["English name", selected_option_job]]
sorted_selected_columns_job = selected_columns_job.sort_values(by=selected_option_job, ascending=False)
top_5_sorted_job = sorted_selected_columns_job.head(5)
sorted_selected_columns_reverse_job = top_5_sorted_job.sort_values(by=selected_option_job, ascending=True)

sorted_selected_columns_reverse_job.set_index("English name", inplace=True)

# Créer le graphique à barres horizontales avec Plotly
fig_job = px.bar(
    sorted_selected_columns_reverse,
    x=selected_option_job,
    y=sorted_selected_columns_reverse.index,
    orientation='h',
    title="Top 5 des pals par job",
    labels={"index": "English name"},
    text=selected_option_job
)

# Mettre à jour les couleurs et le style du graphique
fig_job.update_traces(marker_color='darkblue', textposition='outside')
fig_job.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white'
)
fig_job.update_xaxes(visible=False)
fig_job.update_yaxes(title="")

# Afficher le graphique avec Streamlit
st.plotly_chart(fig_job)
# Fin du graphique Top 5 des pals par job