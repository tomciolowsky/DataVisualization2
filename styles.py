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