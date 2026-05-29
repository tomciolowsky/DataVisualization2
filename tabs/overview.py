from dash import html
from styles import *

title = 'Overview'
desc = 'A high-level view of the gaming market.'
layout = html.Div([
    html.Div([
        html.H2(title, style={"fontSize": "1.8rem", "fontWeight": "600", "margin": "0", "color": TEXT_PRIMARY}),
        html.Div(desc, style={"color": TEXT_SECONDARY, "fontSize": "0.95rem", "marginTop": "4px"})
    ], style={"marginBottom": "2rem"}),
    
    html.Div([
        html.Div(style=CARD_STYLE, children=[
            html.Div("Total Games Tracked", style={"color": TEXT_SECONDARY, "fontSize": "0.85rem", "fontWeight": "500", "marginBottom": "8px"}),
            html.Div("122,611", style={"fontSize": "2rem", "fontWeight": "600", "color": TEXT_PRIMARY})
        ]),
        html.Div(style=CARD_STYLE, children=[
            html.Div("Avg Price (USD)", style={"color": TEXT_SECONDARY, "fontSize": "0.85rem", "fontWeight": "500", "marginBottom": "8px"}),
            html.Div("$14.99", style={"fontSize": "2rem", "fontWeight": "600", "color": TEXT_PRIMARY})
        ]),
        html.Div(style=CARD_STYLE, children=[
            html.Div("Peak Concurrent Users", style={"color": TEXT_SECONDARY, "fontSize": "0.85rem", "fontWeight": "500", "marginBottom": "8px"}),
            html.Div("32.4M", style={"fontSize": "2rem", "fontWeight": "600", "color": TEXT_PRIMARY})
        ])
    ], style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(240px, 1fr))", "gap": "1.5rem", "marginBottom": "2rem"}),
    
    html.Div(style={**CARD_STYLE, "minHeight": "400px", "display": "flex", "alignItems": "center", "justifyContent": "center"}, children=[
        html.Div([
            html.I(className="fa-regular fa-chart-bar", style={"fontSize": "2.5rem", "color": "#cbd5e1", "marginBottom": "1rem"}),
            html.Div("Data visualizations will be displayed here", style={"color": TEXT_SECONDARY, "fontSize": "0.95rem"})
        ], style={"textAlign": "center"})
    ])
])