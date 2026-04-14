import streamlit as st
import pandas as pd
import time

def logout():
    st.session_state.user = None
    st.session_state.user_role = None
    st.query_params.clear()
    st.rerun()

def captain_page():
    supabase = st.session_state.supabase
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.markdown(f"<div class='premium-title' style='text-align: left; font-size: 2em;'>⛹️ Captain {st.session_state.user}</div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #00ffb3; font-weight: 600; font-size: 1.1em;'>Your Team Dashboard</p>", unsafe_allow_html=True)
    with col2:
        st.write("") # spacer
        if st.button("🚪 Logout", key="captain_logout", use_container_width=True):
            logout()
    st.markdown("---")

    try:
        team_info = supabase.table("teams").select("*").eq(
            "captain_name", st.session_state.user
        ).execute()

        if not team_info.data:
            st.error("Team information not found!")
            return

        team = team_info.data[0]
        st.markdown(f"<h3 style='color: #00b3ff; margin-bottom: 20px;'>🏟️ Team: {team['team_name']}</h3>", unsafe_allow_html=True)

        allocations = supabase.table("allocations").select("*").eq(
            "team_name", team["team_name"]
        ).execute()

        if allocations.data:
            df = pd.DataFrame(allocations.data)
            
            ccids = [a["player_ccid"] for a in allocations.data if "player_ccid" in a]
            players_resp = supabase.table("maintable").select("CCID, MOBILE").in_("CCID", ccids).execute()
            player_dict = {p["CCID"]: (p.get("MOBILE") ) for p in (players_resp.data or [])}

            if "player_ccid" in df.columns:
                df["Mobile Number"] = df["player_ccid"].map(player_dict)
            else:
                df["Mobile Number"] = ""
                
            df.rename(columns={"player_name": "Player Name"}, inplace=True)
            
            st.markdown(f"""
            <div style='background: rgba(0, 255, 179, 0.1); border: 1px solid rgba(0, 255, 179, 0.3); border-radius: 10px; padding: 15px; margin-bottom: 20px;'>
                <span style='color: #e0e1dd; font-size: 1.2em;'>Total Players Allocated: </span>
                <span style='color: #00ffb3; font-weight: bold; font-size: 1.5em;'>{len(df)} ⚡</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Show simplified view on the UI with large projector-friendly font, similar to teams page or just dataframe? The user said "only show player name and mobile number"
            st.dataframe(df[["Player Name", "Mobile Number"]], use_container_width=True, hide_index=True)
        else:
            st.info("No players allocated to your team yet!")

        st.markdown("<p style='text-align: center; color: #a0aab2; margin-top: 20px;'>📊 <i>Live data - Refreshes every 5 seconds</i></p>", unsafe_allow_html=True)
        time.sleep(5)
        st.rerun()

    except Exception as e:
        st.error(f"Error loading team data: {e}")