import streamlit as st
import pandas as pd
from datetime import datetime
from styles import inject_custom_css

def logout():
    st.session_state.user = None
    st.session_state.user_role = None
    st.query_params.clear()
    st.rerun()

def admin_page():
    col_tgl1, col_tgl2 = st.columns([0.85, 0.15])
    with col_tgl2:
        is_light = st.toggle("🌞 Light / 🌙 Dark", value=(st.session_state.theme_mode == "Light"), key="tgl_admin")
        new_theme = "Light" if is_light else "Dark"
        if new_theme != st.session_state.theme_mode:
            st.session_state.theme_mode = new_theme
            st.rerun()

    primary_color = "#c65f3f" if st.session_state.theme_mode == "Light" else "#00ffb3"

    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.markdown("<div class='premium-title' style='text-align: left; font-size: 2em;'>👨‍⚙️ Admin Dashboard</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {primary_color}; font-weight: 600; font-size: 1.1em;'>Team & Player Management Center</p>", unsafe_allow_html=True)
    with col2:
        st.write("") # spacer to align button
        if st.button("🚪 Logout", key="admin_logout", width='stretch'):
            logout()
    
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Add Team Captain", "View Teams", "Manage Players"])

    with tab1:
        _add_team_tab()

    with tab2:
        _view_teams_tab()

    with tab3:
        _manage_players_tab()

def _add_team_tab():
    supabase = st.session_state.supabase
    primary_color = "#c65f3f" if st.session_state.theme_mode == "Light" else "#00ffb3"

    st.markdown(f"<h3 style='color: {primary_color}; margin-top: 10px;'>➕ Register New Team</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0aab2; margin-bottom: 20px;'>Fill in the details below to add a new team and its captain to the tournament.</p>", unsafe_allow_html=True)
    
    try:
        players_resp = supabase.table("maintable").select("NAME, URL").execute()
        teams_resp = supabase.table("teams").select("captain_name").execute()
        
        player_urls = {p["NAME"]: p.get("URL", "") for p in (players_resp.data or []) if p.get("NAME")}
        existing_captains = {t["captain_name"] for t in (teams_resp.data or []) if t.get("captain_name")}
        player_names = sorted(list({p["NAME"] for p in (players_resp.data or []) if p.get("NAME") and p["NAME"] not in existing_captains}))
    except Exception as e:
        player_names = []
        player_urls = {}

    col1, col2, col3 = st.columns(3)
    with col1:
        team_name = st.text_input("Team Name", placeholder="e.g., Team A")
    with col2:
        if player_names:
            captain_name = st.selectbox("Captain Name", options=player_names, index=None, placeholder="Select a captain...")
        else:
            captain_name = st.text_input("Captain Name", placeholder="e.g., John Doe")
    with col3:
        if captain_name and player_urls.get(captain_name):
            st.image(player_urls[captain_name], width=150, caption=f"{captain_name}'s Avatar")
        elif captain_name:
            st.info("👤 No image provided for this player")
        else:
            st.info("👤 Image will auto-load when a captain is selected")

    if st.button("Add Team & Captain", key="add_team_btn"):
        if team_name and captain_name:
            try:
                img_url = player_urls.get(captain_name) if captain_name in player_urls and player_urls[captain_name] else "https://via.placeholder.com/150"
                
                supabase.table("teams").insert({
                    "team_name": team_name,
                    "captain_name": captain_name,
                    "image_url": img_url,
                    "created_at": datetime.now().isoformat()
                }).execute()
                st.success(f"✅ Team '{team_name}' with captain '{captain_name}' added!")
                st.balloons()
            except Exception as e:
                st.error(f"Error adding team: {e}")
        else:
            st.warning("Please fill in all fields!")

def _view_teams_tab():
    supabase = st.session_state.supabase
    alt_color = "#a03c20" if st.session_state.theme_mode == "Light" else "#00b3ff"

    st.markdown(f"<h3 style='color: {alt_color}; margin-top: 10px;'>📋 Registered Teams</h3>", unsafe_allow_html=True)
    try:
        teams = supabase.table("teams").select("*").execute()
        if teams.data:
            # Header
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1: st.markdown("**Team Name**")
            with col2: st.markdown("**Captain Name**")
            with col3: st.markdown("**Created At**")
            with col4: st.markdown("**Action**")
            st.markdown("---")
            
            for team in teams.data:
                c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
                with c1: st.write(team.get("team_name", ""))
                with c2: st.write(team.get("captain_name", ""))
                
                created_str = team.get("created_at", "")
                if created_str:
                    try:
                        created_str = datetime.fromisoformat(created_str.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                with c3: st.write(created_str)
                
                with c4:
                    if st.button("🗑️ Delete", key=f"del_team_{team.get('team_name', '')}", use_container_width=True):
                        try:
                            supabase.table("teams").delete().eq("team_name", team.get("team_name")).execute()
                            st.success(f"Team '{team.get('team_name')}' deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to delete team: {e}")
        else:
            st.info("No teams added yet!")
    except Exception as e:
        st.error(f"Error fetching teams: {e}")

def _manage_players_tab():
    supabase = st.session_state.supabase
    txt_color = "#2c3e50" if st.session_state.theme_mode == "Light" else "#a0aab2"

    st.markdown(f"<h3 style='color: {txt_color}; margin-top: 10px;'>🏃 Manage Players Database</h3>", unsafe_allow_html=True)
    try:
        players = supabase.table("maintable").select("*").execute()
        if players.data:
            df = pd.DataFrame(players.data)
            st.metric("Total Registered Players", len(df))
            st.dataframe(df[["NAME", "EMAIL", "MOBILE", "Attend Before"]], use_container_width=True)
        else:
            st.info("No players registered yet!")
    except Exception as e:
        st.error(f"Error fetching players: {e}")