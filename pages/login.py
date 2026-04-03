import streamlit as st
from styles import inject_custom_css

def login_as_admin():
    st.session_state.user = "admin"
    st.session_state.user_role = "admin"
    st.query_params["user"] = "admin"
    st.query_params["user_role"] = "admin"
    st.success("Logged in as Admin!")
    st.rerun()

def login_as_captain(captain_name):
    supabase = st.session_state.supabase
    teams = supabase.table("teams").select("*").execute()
    captain_exists = any(
        t.get("captain_name") == captain_name
        for t in (teams.data or [])
    )
    if captain_exists:
        st.session_state.user = captain_name
        st.session_state.user_role = "captain"
        st.query_params["user"] = captain_name
        st.query_params["user_role"] = "captain"
        st.success(f"Logged in as Captain: {captain_name}!")
        st.rerun()
    else:
        st.error("Captain not found!")

def login_page():
   
    col_tgl1, col_tgl2 = st.columns([0.85, 0.15])
    with col_tgl2:
        is_light = st.toggle("🌞 Light / 🌙 Dark", value=(st.session_state.theme_mode == "Light"))
        new_theme = "Light" if is_light else "Dark"
        if new_theme != st.session_state.theme_mode:
            st.session_state.theme_mode = new_theme
            st.rerun()

    st.markdown("<div class='premium-title'>🏏 Hariprabodham Box Cricket Auction App</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>VVIP BOX CRICKET TOURNAMENT 2026</div>", unsafe_allow_html=True)
    
    st.markdown("---")

    col_space1, col1, col_space2, col2, col_space3 = st.columns([1, 4, 1, 4, 1])

    primary_color = "#c65f3f" if st.session_state.theme_mode == "Light" else "#00ffb3"

    with col1:
        st.markdown(f"<h3 style='text-align: center; color: {primary_color}; margin-bottom: 20px;'>👨‍💼 Admin Portal</h3>", unsafe_allow_html=True)
        admin_password = st.text_input("Admin Password", type="password", key="admin_pwd", placeholder="Enter Password...")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("LOGIN AS ADMIN", key="admin_login", width='stretch'):
            if admin_password == "admin123":
                login_as_admin()
            else:
                st.error("Invalid password!")

    with col2:
        st.markdown(f"<h3 style='text-align: center; color: {primary_color}; margin-bottom: 20px;'>⛹️ Captain Portal</h3>", unsafe_allow_html=True)
        captain_name = st.text_input("Your Registered Name", key="captain_name_input", placeholder="e.g. MS Dhoni")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("LOGIN AS CAPTAIN", key="captain_login", width='stretch'):
            if captain_name.strip():
                login_as_captain(captain_name)
            else:
                st.error("Please enter your name!")