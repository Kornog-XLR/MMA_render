from dash import html, dcc, callback, Output, Input
from app import df

import pandas as pd

#df = pd.read_csv("data/cohorte_combattants_ufcmaster.csv")
#app = Dash(__name__)

var = df['combattant'].unique()

layout = html.Div([
    html.H1('Fighters Head 2 Head Comparison', style={'textAlign': 'center'}),

    # Section des sélecteurs
    html.Div([
        html.Div([
            html.H4('Choose the first fighter:'),
            dcc.Dropdown(id='fighter_first', options=var, value=var[0]),
        ], style={'width': '45%', 'display': 'inline-block'}),

        html.Div([
            html.H4('Choose the second fighter:'),
            dcc.Dropdown(id='fighter_second', options=var, value=var[1]),
        ], style={'width': '45%', 'display': 'inline-block', 'float': 'right'})
    ], style={'padding': '20px'}),

    # Conteneur dynamique pour les deux colonnes de comparaison
    html.Div(id='h2h-container', style={
        'display': 'flex', 
        'justifyContent': 'space-around', 
        'marginTop': '30px'
    })
])

@callback(
    Output(component_id='h2h-container', component_property='children'),
    Input(component_id='fighter_first', component_property='value'),
    Input(component_id='fighter_second', component_property='value'),
)
def update_comparison(fighter1, fighter2):
    if not fighter1 or not fighter2:
        return "Veuillez sélectionner deux combattants."

    # Récupération des données pour chaque combattant
    f1_data = df[df['combattant'] == fighter1].iloc[0]
    f2_data = df[df['combattant'] == fighter2].iloc[0]

    # Fonction pour créer une carte de statistiques par combattant
    def create_fighter_card(data):
        return html.Div([
            html.H2(data['combattant'], style={'textAlign': 'center'}),
            html.Hr(),
            html.P(f"Âge (début) : {data['age_debut']} ans"),
            html.P(f"Taille : {data['taille_cm']} cm"),
            html.P(f"Allonge : {data['allonge_cm']} cm"),
            html.P(f"Poids : {data['poids_kg']} kg"),
            html.P(f"Catégorie : {data['categorie_debut']}"),
            html.P(f"Garde : {data['garde']}"),
            html.P(f"Nombre de combats total : {data['nb_combats_total']}"),
            html.P(f"Côte début : {data['cote_debut']}")
        ], style={
            'border': '1px solid #ccc',
            'borderRadius': '8px',
            'padding': '20px',
            'width': '40%',
            'backgroundColor': '#f9f9f9',
            'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'
        })

    return [create_fighter_card(f1_data), create_fighter_card(f2_data)]