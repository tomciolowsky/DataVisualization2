from dash import html
from styles import *

title = 'Explore Data'
desc = 'Dive deeper into the dataset.'
layout = html.Div([
    html.Div([
        html.H2(title, style={"fontSize": "1.8rem", "fontWeight": "600", "margin": "0", "color": TEXT_PRIMARY}),
        html.Div(desc, style={"color": TEXT_SECONDARY, "fontSize": "0.95rem", "marginTop": "4px"})
    ], style={"marginBottom": "2rem"}),
    
    html.Div(style={**CARD_STYLE, "minHeight": "400px", "display": "flex", "alignItems": "center", "justifyContent": "center"}, children=[
        html.Div("Module currently under construction", style={"color": TEXT_SECONDARY, "fontSize": "0.95rem"})
    ])
])
         
        