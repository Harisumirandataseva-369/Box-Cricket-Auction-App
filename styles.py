import streamlit as st

def inject_custom_css(theme_mode="Dark", show_sidebar=False):
    sidebar_visibility = "block" if show_sidebar else "none"
    BASE_CSS = """
        <style>
        /* Import premium font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

        html, body, [class*="css"]  {
        
            font-family: 'Outfit', sans-serif !important;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {background: transparent !important;}
        .stAppDeployButton {display: none !important;}
        
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        /* ✅ Control sidebar visibility based on role */
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {{
            display: {sidebar_visibility} !important;
        }}
        
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
        </style>
    """
    
    if theme_mode == "Light":
        THEME_CSS = """
        <style>
        .stApp, .block-container, header {
            background-color: #f8f6f0 !important;
            background-image: none !important;
        }

        [data-testid="stSidebar"] {
            background: #ffffff !important;
            border-right: 1px solid rgba(198, 95, 63, 0.2);
        }
        /* Force text colors to dark */
        .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp span, .stApp div, .stApp label {
            color: #2c3e50 !important;
        }

        /* Re-override button component text explicitly */
        .stButton > button * {
            color: #ffffff !important;
        }
        
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(198, 95, 63, 0.2);
            border-radius: 15px;
            padding: 20px !important;
            box-shadow: 0 8px 32px 0 rgba(198, 95, 63, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(198, 95, 63, 0.15);
            border: 1px solid rgba(198, 95, 63, 0.4);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            background-color: transparent !important;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background-color: transparent !important;
            border-radius: 4px 4px 0px 0px;
            font-weight: 600;
            color: #8894a0 !important;
            border-bottom: 2px solid transparent !important;
            transition: all 0.3s ease-in-out;
            padding-bottom: 5px;
        }
        .stTabs [aria-selected="true"] {
            color: #c65f3f !important;
            border-bottom: 2px solid #c65f3f !important;
            text-shadow: none !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #c65f3f 0%, #db8867 100%) !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 0.5rem 2rem !important;
            box-shadow: 0 4px 15px rgba(198, 95, 63, 0.3) !important;
            text-transform: uppercase;
        }
        .stButton > button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 8px 25px rgba(198, 95, 63, 0.5) !important;
        }
        
        .stButton > button:contains("Logout") {
            background: rgba(255, 69, 58, 0.1) !important;
            color: #ff453a !important;
            border: 1px solid rgba(255, 69, 58, 0.4) !important;
            box-shadow: none !important;
        }

        [data-baseweb="input"] > div,
        [data-baseweb="select"] > div,
        [data-baseweb="number-input"] > div {
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease;
        }
        [data-baseweb="input"] > div:focus-within,
        [data-baseweb="select"] > div:focus-within,
        [data-baseweb="number-input"] > div:focus-within {
            border-color: #c65f3f !important;
            box-shadow: 0 0 0 2px rgba(198, 95, 63, 0.2) !important;
        }
        input, select, textarea {
            color: #1e293b !important;
            background: transparent !important;
        }

        [data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.8) !important;
            border: 1px solid rgba(198, 95, 63, 0.2) !important;
            border-radius: 12px;
            overflow: hidden;
        }

        .premium-card {
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(198, 95, 63, 0.15);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(198, 95, 63, 0.08);
            margin-bottom: 20px;
        }
        
        .premium-title {
            background: -webkit-linear-gradient(45deg, #c65f3f, #a03c20);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5em;
            font-weight: 800;
            margin-bottom: 0.2em;
            text-align: center;
            text-transform: uppercase;
        }
        .subtitle {
            color: #2c3e50 !important;
            text-align: center;
            font-size: 1.1em;
            margin-bottom: 2em;
            letter-spacing: 1px;
        }

        hr {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, transparent, rgba(198, 95, 63, 0.3), transparent);
            margin: 30px 0;
        }
        </style>
        """
    else:
        # DARK MODE (the existing code)
        THEME_CSS = """
        <style>
        /* Modern Glassmorphism Root Container */
        .stApp, .block-container, header {
             background-color: transparent !important;
             background-image: none !important;
        }
        [data-testid="stSidebar"] {
            background: rgba(13, 27, 42, 0.9) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(0, 255, 179, 0.2);
        }

        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(0, 255, 179, 0.2);
            border: 1px solid rgba(0, 255, 179, 0.4);
        }

        /* Beautiful Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            background-color: transparent !important;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent !important;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            font-weight: 600;
            color: #a0aab2;
            transition: all 0.3s ease-in-out;
        }
        .stTabs [aria-selected="true"] {
            color: #00ffb3 !important;
            border-bottom: 2px solid #00ffb3 !important;
            text-shadow: 0 0 15px rgba(0, 255, 179, 0.6);
        }

        /* Button Styling - Glow Effect */
        .stButton > button {
            background: linear-gradient(135deg, #00ffb3 0%, #00b3ff 100%) !important;
            color: #0d1b2a !important;
            font-weight: 800 !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 0.5rem 2rem !important;
            transition: all 0.4s ease !important;
            box-shadow: 0 4px 15px rgba(0, 255, 179, 0.3) !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stButton > button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 8px 25px rgba(0, 255, 179, 0.6) !important;
        }
        
        /* Secondary "Logout" Button style hacking using specific keys or text */
        .stButton > button:contains("Logout") {
            background: rgba(255, 69, 58, 0.1) !important;
            color: #ff453a !important;
            border: 1px solid rgba(255, 69, 58, 0.4) !important;
            box-shadow: none !important;
        }
        .stButton > button:contains("Logout"):hover {
            background: rgba(255, 69, 58, 0.2) !important;
            box-shadow: 0 4px 15px rgba(255, 69, 58, 0.4) !important;
        }

        /* Inputs and Select Boxes Glow/Colors - Dark Theme */
        [data-baseweb="input"] > div,
        [data-baseweb="select"] > div,
        [data-baseweb="number-input"] > div {
            background: rgba(27, 38, 59, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            transition: all 0.3s ease;
        }
        [data-baseweb="input"] > div:focus-within,
        [data-baseweb="select"] > div:focus-within,
        [data-baseweb="number-input"] > div:focus-within {
            border-color: #00ffb3 !important;
            box-shadow: 0 0 0 2px rgba(0, 255, 179, 0.2) !important;
        }
        input, select, textarea {
            color: white !important;
            background: transparent !important;
        }

        /* Dataframes Styling */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.02);
        }

        /* Beautiful Containers */
        .premium-card {
            background: rgba(27, 38, 59, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            margin-bottom: 20px;
        }
        
        .premium-title {
            background: -webkit-linear-gradient(45deg, #00ffb3, #00b3ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5em;
            font-weight: 800;
            margin-bottom: 0.2em;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .subtitle {
            text-align: center;
            color: #a0aab2;
            font-size: 1.1em;
            margin-bottom: 2em;
            letter-spacing: 1px;
        }

        /* Neon Text utility */
        .neon-text {
            color: #00ffb3;
            text-shadow: 0 0 10px rgba(0, 255, 179, 0.5);
            font-weight: 800;
        }
        
        /* Gradient Divider */
        hr {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, transparent, rgba(0, 255, 179, 0.5), transparent);
            margin: 30px 0;
        }
        </style>
        """

    st.markdown(BASE_CSS + THEME_CSS, unsafe_allow_html=True)

def card_container(html_content):
    """Helper to wrap HTML content in a premium card"""
    st.markdown(f'<div class="premium-card">{{html_content}}</div>', unsafe_allow_html=True)
