from dash import html, register_page
from app import df

register_page(__name__, path='/', name='Home')

layout = html.Div([

    html.P('Home page')

])