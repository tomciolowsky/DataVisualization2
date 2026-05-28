import pandas as pd
from dash import Dash, Input, Output, dcc, html

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Game Market Analyzer"


BG_BASE = "#f8fafc"       
BG_SURFACE = "#ffffff"    
BORDER_COLOR = "#e2e8f0"  
TEXT_PRIMARY = "#0f172a"   
TEXT_SECONDARY = "#64748b" 
ACCENT_COLOR = "#3b82f6"   

APP_STYLE = {
    "backgroundColor": BG_BASE,
    "minHeight": "100vh",
    "fontFamily": "'Inter', sans-serif",
    "color": TEXT_PRIMARY,
    "display": "flex"
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "240px",
    "backgroundColor": BG_SURFACE,
    "borderRight": f"1px solid {BORDER_COLOR}",
    "display": "flex",
    "flexDirection": "column",
    "padding": "2rem 0", 
    "zIndex": 1000
}

CONTENT_STYLE = {
    "marginLeft": "240px",
    "flex": "1",
    "padding": "3rem 4rem",
    "minHeight": "100vh",
}

TAB_STYLE = {
    "padding": "10px 16px",
    "color": TEXT_SECONDARY,
    "backgroundColor": "transparent",
    "border": "none",
    "marginBottom": "4px",
    "cursor": "pointer",
    "fontSize": "14px",
    "fontWeight": "500",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "flex-start",
    "gap": "12px",
    "transition": "all 0.2s ease",
    "borderRadius": "8px",
    "margin": "0 16px 4px 16px" 
}

SELECTED_TAB_STYLE = {
    **TAB_STYLE,
    "color": "#1d4ed8",
    "backgroundColor": "#eff6ff", 
    "fontWeight": "500"
}

CARD_STYLE = {
    "backgroundColor": BG_SURFACE,
    "borderRadius": "12px",
    "padding": "1.5rem 2rem",
    "border": f"1px solid {BORDER_COLOR}",
    "boxShadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)"
}

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(
                src='/assets/pp_znak_konturowy_RGB.png', 
                style={'width': '32px', 'height': 'auto', 'marginRight': '12px'}
            ),
            html.Div([
                html.Div("Game Market", style={'fontWeight': '600', 'fontSize': '1.1rem', 'color': TEXT_PRIMARY}),
                html.Div("Analyzer", style={'fontWeight': '400', 'fontSize': '0.85rem', 'color': TEXT_SECONDARY})
            ], style={'lineHeight': '1.2'})
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '2.5rem', 'padding': '0 24px'}),
        
        dcc.Tabs(
            id='sidebar-tabs', 
            value='tab-summary', 
            vertical=True,
            parent_style={"width": "100%", "display": "flex", "flexDirection": "column"},
            style={'border': 'none', 'borderBottom': 'none'},
            colors={"border": "transparent", "primary": "transparent", "background": "transparent"},
            children=[
                dcc.Tab(label=html.Div([html.I(className="fa-solid fa-layer-group", style={"width": "20px"}), html.Span("Overview")]), value='tab-summary', style=TAB_STYLE, selected_style=SELECTED_TAB_STYLE),
                dcc.Tab(label=html.Div([html.I(className="fa-solid fa-compass", style={"width": "20px"}), html.Span("Explore")]), value='tab-explore', style=TAB_STYLE, selected_style=SELECTED_TAB_STYLE),
                dcc.Tab(label=html.Div([html.I(className="fa-solid fa-lightbulb", style={"width": "20px"}), html.Span("Insights")]), value='tab-insights', style=TAB_STYLE, selected_style=SELECTED_TAB_STYLE),
                dcc.Tab(label=html.Div([html.I(className="fa-solid fa-circle-info", style={"width": "20px"}), html.Span("About")]), value='tab-about', style=TAB_STYLE, selected_style=SELECTED_TAB_STYLE),
            ]
        )
    ], style=SIDEBAR_STYLE),

    html.Div(id='tab-content', style=CONTENT_STYLE)
], style=APP_STYLE)

@app.callback(
    Output('tab-content', 'children'),
    Input('sidebar-tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-summary':
        return html.Div([
            html.Div([
                html.H2('Overview', style={"fontSize": "1.8rem", "fontWeight": "600", "margin": "0", "color": TEXT_PRIMARY}),
                html.Div("A high-level view of the gaming market.", style={"color": TEXT_SECONDARY, "fontSize": "0.95rem", "marginTop": "4px"})
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
    elif tab == 'tab-about':
        return html.Div([
            html.Div([
                html.H2('About', style={"fontSize": "1.8rem", "fontWeight": "600", "margin": "0", "color": TEXT_PRIMARY}),
                html.Div("Learn more about the Game Market Analyzer.", style={"color": TEXT_SECONDARY, "fontSize": "0.95rem", "marginTop": "4px"})
            ], style={"marginBottom": "2rem"}),
            
            html.Div(style={**CARD_STYLE, "minHeight": "400px", "display": "flex", "alignItems": "center", "justifyContent": "center"}, children=[
                html.Div("Project information, credits, and documentation will be displayed here.", style={"color": TEXT_SECONDARY, "fontSize": "0.95rem"})
            ])
        ])
    else:
        title = 'Explore Data' if tab == 'tab-explore' else 'Market Insights'
        desc = 'Dive deeper into the dataset.' if tab == 'tab-explore' else 'Actionable takeaways from the data.'
        return html.Div([
            html.Div([
                html.H2(title, style={"fontSize": "1.8rem", "fontWeight": "600", "margin": "0", "color": TEXT_PRIMARY}),
                html.Div(desc, style={"color": TEXT_SECONDARY, "fontSize": "0.95rem", "marginTop": "4px"})
            ], style={"marginBottom": "2rem"}),
            
            html.Div(style={**CARD_STYLE, "minHeight": "400px", "display": "flex", "alignItems": "center", "justifyContent": "center"}, children=[
                html.Div("Module currently under construction", style={"color": TEXT_SECONDARY, "fontSize": "0.95rem"})
            ])
        ])

if __name__ == '__main__':
    app.run(debug=True)
