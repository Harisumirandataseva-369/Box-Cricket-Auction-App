import streamlit as st
from pages.login import login_page
from pages.admin import admin_page
from pages.auction import auction_page
from pages.captain import captain_page
from config import init_supabase

st.set_page_config(page_title="Cricket Auction App", layout="wide")

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"

import styles

if "supabase" not in st.session_state:
    st.session_state.supabase = init_supabase()

# Session state defaults
for key, default in {
    "user": None,
    "user_role": None,
    "teams": {},
    "players_allocated": {},
    "current_wheel_spin": None,
    "all_players": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Sync session state with query params securely to persist over reload
saved_user = st.query_params.get("user")
saved_role = st.query_params.get("user_role")

if saved_user and getattr(st.session_state, "user", None) is None:
    st.session_state.user = saved_user
    st.session_state.user_role = saved_role

def main():
    if st.session_state.user is None:
        styles.inject_custom_css(st.session_state.theme_mode, show_sidebar=False)
        login_page()
    elif st.session_state.user_role == "admin":
        styles.inject_custom_css(st.session_state.theme_mode, show_sidebar=True)
        page = st.sidebar.radio("Navigate", ["Dashboard", "Auction"])
        if page == "Dashboard":
            admin_page()
        else:
            auction_page()
    elif st.session_state.user_role == "captain":
        styles.inject_custom_css(st.session_state.theme_mode, show_sidebar=False)
        captain_page()

if __name__ == "__main__":
    main()