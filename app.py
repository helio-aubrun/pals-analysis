import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def set_page_config():
    st.set_page_config(page_title="Base Stat Pals", layout="wide")

def load_data():
    df = pd.read_csv('csv/Palworld_Data--Palu combat attribute table.csv', skiprows=[0])
    df_job = pd.read_csv('csv/Palworld_Data-Palu Job Skills Table.csv', skiprows=[0])
    return df, df_job

def create_sidebar(df, df_job=None):
    options_radio = ["generally"]
    options_multiselect = df["Element 1"].unique().tolist()
    options_multiselect.pop(0)
    
    with st.sidebar:
        choice_type = st.radio("Type:", options_radio + [f"{i}" for i in options_multiselect])
        
        # Ajout du filtre pour les statistiques ici
        stat_choice = st.sidebar.multiselect(
            "Sélectionnez une ou plusieurs statistique :",
            options=["HP","melee attack","Remote attack","defense"],
            default=["HP","melee attack","Remote attack","defense"]
        )
        
        if choice_type == "Autre":
            selected_option_type = st.selectbox("Sélectionnez une option spécifique:", options_multiselect)
        else:
            selected_option_type = choice_type.replace("Autre ", "")
        
        choice_job = st.radio("Job:", ["Make a fire"] + [f"{i}" for i in options_multiselect])
        
        if choice_job == "Autre":
            selected_option_job = st.selectbox("Sélectionnez une option spécifique pour le job:", options_multiselect)
        else:
            selected_option_job = choice_job.replace("Autre ", "")
    
    return selected_option_type, stat_choice, selected_option_job

def filter_and_summarize_data(df, selected_option, stat_choice):
    pals_with_selected_option = df[(df['Element 1'] == selected_option) | (df['Element 2'] == selected_option)]
    filtered_df_sum = pals_with_selected_option[pals_with_selected_option[stat_choice].notnull().any(axis=1)]
    
    summed_columns = ['sum_' + col for col in stat_choice]
    for col in stat_choice:
        filtered_df_sum['sum_' + col] = filtered_df_sum.groupby(level=0)[col].transform('sum')
    
    filtered_df_sum['Total_Sum'] = filtered_df_sum[summed_columns].sum(axis=1)
    top_10_sorted_sum = filtered_df_sum.nlargest(10, 'Total_Sum').sort_values(by='Total_Sum', ascending=True)
    
    return top_10_sorted_sum

def create_top_10_bar_chart(top_10_sorted_sum):
    fig_sum = px.bar(
        top_10_sorted_sum,
        x=top_10_sorted_sum['Total_Sum'],
        y=top_10_sorted_sum['Name'],
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
    
    return fig_sum

def create_pie_chart(df):
    element1_counts = df['Element 1'].value_counts()
    element2_counts = df['Element 2'].value_counts()
    counts_total = element1_counts.add(element2_counts, fill_value=0)
    counts_total_percentage = counts_total / counts_total.sum() * 100
    
    labels = counts_total_percentage.index
    values = counts_total_percentage.values
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
    fig.update_layout(title_text="Répartition des types",
                      height=600,
                      width=800,
                      legend=dict(font_size=16))
    
    return fig

def display_image(image_path):
    st.image(image_path)

def sort_and_select_top_riding(df):
    riding_df = df.loc[:, ["Name", "Riding sprint speed"]]
    sorted_riding_df = riding_df.sort_values(by="Riding sprint speed", ascending=False)
    top_10_riding = sorted_riding_df.head(10)
    sorted_riding_df_reverse = top_10_riding.sort_values(by="Riding sprint speed", ascending=True)
    sorted_riding_df_reverse.set_index("Name", inplace=True)
    
    return sorted_riding_df_reverse

def create_riding_speed_chart(sorted_riding_df_reverse):
    fig_riding = px.bar(
        sorted_riding_df_reverse,
        x="Riding sprint speed",
        y=sorted_riding_df_reverse.index,
        orientation='h',
        title="Top 10 des montures les plus rapides",
        labels={"index": "Name"},
        text="Riding sprint speed"
    )
    
    fig_riding.update_traces(marker_color='darkblue', textposition='outside')
    fig_riding.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    fig_riding.update_xaxes(visible=False)
    fig_riding.update_yaxes(title="")
    
    return fig_riding

def filter_by_job(df_job, selected_option_job):
    filtered_df_job = df_job.dropna(subset=[selected_option_job])
    sorted_selected_columns_job = filtered_df_job.sort_values(by=selected_option_job, ascending=False)
    top_5_sorted_job = sorted_selected_columns_job.head(5)
    sorted_selected_columns_reverse_job = top_5_sorted_job.sort_values(by=selected_option_job, ascending=True)
    sorted_selected_columns_reverse_job.set_index("English name", inplace=True)
    
    return sorted_selected_columns_reverse_job

def create_job_skill_chart(sorted_selected_columns_reverse_job, selected_option_job):
    fig_job = px.bar(
        sorted_selected_columns_reverse_job,
        y=selected_option_job,
        x=sorted_selected_columns_reverse_job.index,
        orientation='v',
        title=f"Top 5 des pals par {selected_option_job}",
        labels={"index": "English name"},
        text=selected_option_job
    )
    
    fig_job.update_traces(marker_color='darkblue', textposition='outside')
    fig_job.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    fig_job.update_yaxes(visible=False)
    fig_job.update_xaxes(title="")
    
    return fig_job

def main():
    set_page_config()
    df, df_job = load_data()
    selected_option_type, stat_choice, selected_option_job = create_sidebar(df, df_job)
    top_10_sorted_sum = filter_and_summarize_data(df, selected_option_type, stat_choice)
    fig_sum = create_top_10_bar_chart(top_10_sorted_sum)
    st.plotly_chart(fig_sum)
    
    pie_fig = create_pie_chart(df)
    st.plotly_chart(pie_fig)
    display_image('image/type.jpg')
    
    sorted_riding_df_reverse = sort_and_select_top_riding(df)
    fig_riding = create_riding_speed_chart(sorted_riding_df_reverse)
    st.plotly_chart(fig_riding)
    
    if selected_option_job:
        sorted_selected_columns_reverse_job = filter_by_job(df_job, selected_option_job)
        fig_job = create_job_skill_chart(sorted_selected_columns_reverse_job, selected_option_job)
        st.plotly_chart(fig_job)

if __name__ == "__main__":
    main()