# Import des bibliothèques nécessaires
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# 1. Chargement des données SpaceX (Utilisation du dataset nettoyé par IBM)
spacex_df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# 2. Initialisation de l'application Dash
app = dash.Dash(__name__)

# 3. Définition de la mise en page (Layout)
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-family': 'Arial', 'fontSize': 40}),

    # TASK 1: Menu déroulant (Dropdown) pour la sélection du site de lancement
    html.Div([
        html.Label("Select a Launch Site:", style={'fontSize': 20, 'font-family': 'Arial'}),
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
            ],
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True,
            style={'width': '100%', 'padding': '3px', 'fontSize': '20px', 'textAlign': 'left'}
        ),
    ]),
    html.Br(),

    # TASK 2: Graphique en secteurs (Pie Chart) pour les taux de réussite
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3: Curseur (Range Slider) pour filtrer la masse de charge utile (Payload)
    html.P("Payload Mass (Kg):", style={'fontSize': 20, 'font-family': 'Arial'}),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: f'{i}' for i in range(0, 10001, 2500)},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4: Graphique de dispersion (Scatter Chart) pour la charge utile vs. résultat
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# ==============================================================================
# CALLBACKS INTERACTIFS
# ==============================================================================

# TASK 2: Callback pour mettre à jour le Pie Chart selon le site sélectionné
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(
            filtered_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches by Site',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        return fig
    else:
        # Filtrer pour le site spécifique et compter les succès (1) et échecs (0)
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        site_counts = site_df['class'].value_counts().reset_index()
        site_counts.columns = ['class', 'count']
        fig = px.pie(
            site_counts,
            values='count',
            names='class',
            title=f'Total Success Launches for site {entered_site}',
            labels={'class': 'Launch Status (0=Fail, 1=Success)'},
            color_discrete_map={0: 'red', 1: 'green'}
        )
        return fig


# TASK 4: Callback pour mettre à jour le Scatter Chart selon le site et le curseur
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]

    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df, x="Payload Mass (kg)", y="class",
            color="Booster Version Category",
            title="Correlation between Payload and Success for all Sites"
        )
        return fig
    else:
        site_mask_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            site_mask_df, x="Payload Mass (kg)", y="class",
            color="Booster Version Category",
            title=f"Correlation between Payload and Success for site {entered_site}"
        )
        return fig


# 4. Lancement du serveur local
if __name__ == '__main__':
    app.run(debug=True, port=8050)