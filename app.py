import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Base Stat Pals", layout="wide")

df = pd.read_csv('Palworld_Data--Palu combat attribute table.csv', skiprows=[0])
df_job = pd.read_csv('Palworld_Data-Palu Job Skills Table.csv', skiprows=[0])

# Sidebar pour filtrer par type
# Définir les options pour la radio et la multiselect
options_radio = ["generally"]
options_multiselect = df["Element 1"].unique().tolist()
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

stat_choice = st.sidebar.multiselect(
    "Sélectionnez une ou plusieurs statistique :",
    options=["HP","melee attack","Remote attack","defense"],
    default=["HP","melee attack","Remote attack","defense"]
)

# Début du grahique Top 10 des pals ayant le plus de statistique par types
pals_with_selected_option = df[(df['Element 1'] == selected_option) | (df['Element 2'] == selected_option)]
# Filtrer le dataframe pour le top 10 des pals avec le plus de stats hp, def, atk
# Étape 1 & 2: Filtrer le DataFrame pour ne conserver que les lignes où au moins une des colonnes spécifiées dans stat_choice est présente
filtered_df_sum = pals_with_selected_option[pals_with_selected_option[stat_choice].notnull().any(axis=1)]

# Étape 1: Calculer la somme des valeurs pour chaque pal selon les colonnes spécifiées dans stat_choice
summed_columns = ['sum_' + col for col in stat_choice]
for col in stat_choice:
    filtered_df_sum['sum_' + col] = filtered_df_sum.groupby(level=0)[col].transform('sum')

# Étape 2: Calculer la somme totale pour chaque pal
filtered_df_sum['Total_Sum'] = filtered_df_sum[summed_columns].sum(axis=1)

# Étape 3: Trier le DataFrame pour obtenir le top 10 des pals avec la somme la plus élevée selon les colonnes spécifiées
top_10_sorted_sum = filtered_df_sum.nlargest(10, 'Total_Sum')
top_10_sorted_sum_reverse = top_10_sorted_sum.sort_values(by='Total_Sum', ascending=True)
# Étape 4: Créer et afficher le graphique à barres horizontales
fig_sum = px.bar(
    top_10_sorted_sum,
    x=top_10_sorted_sum_reverse['Total_Sum'],
    y=top_10_sorted_sum_reverse['Name'],
    orientation='h',
    title="Top 10 des pals avec la somme la plus élevée selon les statistiques choisies",
    labels={"x": "Somme totale", "y": "Nom"}
)

fig_sum.update_traces(marker_color='darkblue', textposition='outside')
fig_sum.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white'
)
fig_sum.update_xaxes(visible=False)
fig_sum.update_yaxes(title="")

st.plotly_chart(fig_sum)
# Fin du grahique Top 10 des pals ayant le plus de statistique par types

# Début du graphique Répartition des types
element1_counts = df['Element 1'].value_counts()
element2_counts = df['Element 2'].value_counts()

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
riding_df = df.loc[:, ["Name", "Riding sprint speed"]]
sorted_riding_df = riding_df.sort_values(by="Riding sprint speed", ascending=False)
top_10_riding = sorted_riding_df.head(10)
sorted_riding_df_reverse = top_10_riding.sort_values(by="Riding sprint speed", ascending=True)
sorted_riding_df_reverse.set_index("Name", inplace=True)

# Créer le graphique à barres horizontales avec Plotly
fig_riding = px.bar(
    sorted_riding_df_reverse,
    x="Riding sprint speed",
    y=sorted_riding_df_reverse.index,
    orientation='h',
    title="Top 10 des montures les plus rapides",
    labels={"index": "Name"},
    text="Riding sprint speed"
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
filtered_df_job = df_job.dropna(subset=[selected_option_job])

# Sort the filtered DataFrame by the selected column in descending order
sorted_selected_columns_job = filtered_df_job.sort_values(by=selected_option_job, ascending=False)

# Select the top 5 entries
top_5_sorted_job = sorted_selected_columns_job.head(5)
sorted_selected_columns_reverse_job = top_5_sorted_job.sort_values(by=selected_option_job, ascending=True)

# Set the index to the English name column for better visualization
sorted_selected_columns_reverse_job.set_index("English name", inplace=True)

# Create the horizontal bar chart with Plotly
fig_job = px.bar(
    sorted_selected_columns_reverse_job,
    y=selected_option_job,
    x=sorted_selected_columns_reverse_job.index,
    orientation='v',
    title=f"Top 5 des pals par {selected_option_job}",
    labels={"index": "English name"},
    text=selected_option_job
)

# Update the colors and style of the chart
fig_job.update_traces(marker_color='darkblue', textposition='outside')
fig_job.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white'
)
fig_job.update_yaxes(visible=False)
fig_job.update_xaxes(title="")

# Display the chart with Streamlit
st.plotly_chart(fig_job)