from dash import Dash, html, dcc, register_page, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
#from app import df

df = pd.read_csv("data/cohorte_combattants_ufcmaster.csv")

#register_page(__name__, path='/', name='Home')
app = Dash(__name__)

VARIABLES = [
    'taille_cm',
    'allonge_cm',
    'poids_kg',
    'nb_combats_total',
    'frappes_sig_moy_apres3',
    'precision_frappes_apres3',
    'takedowns_moy_apres3',
    'soumissions_tent_moy_apres3',
]

categories = sorted(df['categorie_debut'].dropna().unique())

app.layout = html.Div([

    dbc.Row([
        dbc.Col([
            html.Label('Catégorie(s)'),
            dcc.Dropdown(
                id='dd-categorie',
                options=[{'label': c, 'value': c} for c in categories],
                value=None,
                multi=True,
                placeholder='Toutes les catégories',
            ),
        ], md=12, className='mb-3'),
    ]),

    dbc.Row([
        dbc.Col([
            html.Label('Axe X'),
            dcc.Dropdown(
                id='dd-x',
                options=[{'label': v, 'value': v} for v in VARIABLES],
                value=VARIABLES[0],
                clearable=False,
            ),
        ], md=6, className='mb-3'),

        dbc.Col([
            html.Label('Axe Y'),
            dcc.Dropdown(
                id='dd-y',
                options=[{'label': v, 'value': v} for v in VARIABLES],
                value=VARIABLES[1],
                clearable=False,
            ),
        ], md=6, className='mb-3'),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='scatter-plot'),
        ]),
    ]),

], className='p-4')


@callback(
    Output('scatter-plot', 'figure'),
    Input('dd-categorie', 'value'),
    Input('dd-x', 'value'),
    Input('dd-y', 'value'),
)
def update_graph(categories_sel, x_col, y_col):
    dff = df.copy()
    if categories_sel:
        dff = dff[dff['categorie_debut'].isin(categories_sel)]

    fig = px.scatter(
        dff,
        x=x_col,
        y=y_col,
        color='categorie_debut',
        size='nb_combats_total',
        hover_name='combattant',
        labels={'categorie_debut': 'Catégorie'},
    )
    fig.update_layout(margin=dict(t=30, b=10))
    return fig

if __name__ == '__main__':
    app.run(debug=True)