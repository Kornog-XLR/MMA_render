import dash
from dash import html, dcc, callback, Input, Output, register_page
import dash_bootstrap_components as dbc
from app import df

register_page(__name__, path='/', name='FIGHTER')

# Liste des combattants pour l'autocomplétion
combattants = df['combattant'].dropna().unique().tolist()
# Combattant par défaut (en dur)
default_fighter = "Jon Jones" if "Jon Jones" in combattants else (combattants[0] if combattants else None)

layout = html.Div([
    html.H2("Profil Combattant", className="mb-4"),
    
    # Input Dropdown avec autocomplétion
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='fighter-dropdown',
                options=[{'label': c, 'value': c} for c in combattants],
                value=default_fighter,
                clearable=False,
                placeholder="Sélectionnez un FIGHTER..."
            )
        ], width=4)
    ], className="mb-4"),
    
    # Grille 4/4/4 qui sera mise à jour par le callback
    dbc.Row(id='fighter-info-grid')
])

@callback(
    Output('fighter-info-grid', 'children'),
    Input('fighter-dropdown', 'value')
)
def update_fighter_info(fighter_name):
    if not fighter_name:
        return []
        
    # Extraire les données du combattant sélectionné
    fighter_data = df[df['combattant'] == fighter_name].iloc[0]
    
    # Colonne 1 : Nom, Age, Poids
    col1 = dbc.Col([
        html.H4(fighter_data['combattant'], className="text-primary"),
        html.Hr(),
        html.P(f"Âge (début) : {fighter_data.get('age_debut', 'N/A')} ans"),
        html.P(f"Poids : {fighter_data.get('poids_kg', 'N/A')} kg")
    ], width=4)
    
    # Colonne 2 : Nombre de combats / victoires
    col2 = dbc.Col([
        html.H4("Palmarès", className="text-success"),
        html.Hr(),
        html.P(f"Nombre total de combats : {fighter_data.get('nb_combats_total', 'N/A')}"),
        html.P(f"Victoires (3 premiers) : {fighter_data.get('victoires_3premiers', 'N/A')}")
    ], width=4)
    
    # Colonne 3 : Autres infos
    col3 = dbc.Col([
        html.H4("Physiologie & Style", className="text-info"),
        html.Hr(),
        html.P(f"Taille : {fighter_data.get('taille_cm', 'N/A')} cm"),
        html.P(f"Allonge : {fighter_data.get('allonge_cm', 'N/A')} cm"),
        html.P(f"Garde : {fighter_data.get('garde', 'N/A')}"),
        html.P(f"Catégorie : {fighter_data.get('categorie_debut', 'N/A')}")
    ], width=4)
    
    return [col1, col2, col3]
