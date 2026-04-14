import streamlit as st
import pandas as pd
from config import COLORS

def _get_allocations(sb) -> dict:
    """Returns {team_name: [list of player dicts]} from DB."""
    result = {}
    try:
        allocs = sb.table("allocations").select("*").execute()
        for row in (allocs.data or []):
            tn = row["team_name"]
            result.setdefault(tn, []).append(row)
    except:
        pass
    return result

def _render_team_rosters(teams: list, allocations: dict, all_players: list):
    """all teams with their player counts and lists."""
    st.subheader("👥 Team Rosters")

    # Pre-build master list and dictionary for easy access
    player_dict = {p["CCID"]: p for p in all_players}
    master_list = []
    for tn, players in allocations.items():
        for p in players:
            ccid = p.get("player_ccid")
            full_info = player_dict.get(ccid, {})
            row = {
                "Team": tn,
                "Captain": p.get("captain_name"),
                "Player Name": p.get("player_name"),
                "Email": full_info.get("EMAIL") or p.get("player_email"),
                "Phone": full_info.get("MOBILE") or full_info.get("PHONE"),
                "Attendance": full_info.get("Attend Before"),
                "Amount": full_info.get("AMOUNT"),
                "Assigned At": p.get("allocated_at")
            }
            for k, v in full_info.items():
                if k not in ["NAME", "CCID", "EMAIL", "MOBILE", "PHONE", "Attend Before", "AMOUNT", "URL"]: 
                    row[k] = v
            master_list.append(row)

    def generate_excel(df_to_write, sheet_title="Sheet1"):
        import io
        out = io.BytesIO()
        with pd.ExcelWriter(out, engine='openpyxl') as writer:
            df_to_write.to_excel(writer, sheet_name=sheet_title, index=False)
            ws = writer.sheets[sheet_title]
            for cell in ws[1]:
                cell.font = cell.font.copy(bold=True)
            for col in ws.columns:
                col_letter = col[0].column_letter
                ws.column_dimensions[col_letter].width = min(max([len(str(cell.value)) for cell in col if cell.value] + [10]) + 2, 50)
        return out.getvalue()

    # ── Master Excel Export (All Teams) ──
    try:
        if allocations and master_list:
            import io
            out = io.BytesIO()
            with pd.ExcelWriter(out, engine='openpyxl') as writer:
                # All Allocations
                df_master = pd.DataFrame(master_list)
                df_master.to_excel(writer, sheet_name="All Allocations", index=False)
                ws_master = writer.sheets["All Allocations"]
                for cell in ws_master[1]:
                    cell.font = cell.font.copy(bold=True)
                for col in ws_master.columns:
                    col_letter = col[0].column_letter
                    ws_master.column_dimensions[col_letter].width = min(max([len(str(cell.value)) for cell in col if cell.value] + [10]) + 2, 50)
                
                # Tab for each team
                for t in teams:
                    tn = t["team_name"]
                    t_players = [m for m in master_list if m["Team"] == tn]
                    if t_players:
                        df_t = pd.DataFrame(t_players).drop(columns=["Team", "Captain"], errors="ignore")
                        sheet_title = tn[:31] # Max len for excel
                        df_t.to_excel(writer, sheet_name=sheet_title, index=False)
                        ws = writer.sheets[sheet_title]
                        for cell in ws[1]:
                            cell.font = cell.font.copy(bold=True)
                        for col in ws.columns:
                            col_letter = col[0].column_letter
                            ws.column_dimensions[col_letter].width = min(max([len(str(cell.value)) for cell in col if cell.value] + [10]) + 2, 50)
            
            b_data = out.getvalue()
            st.download_button(
                label="📥 Download ALL Teams Master Sheet",
                data=b_data,
                file_name="Tournament_Allocations_Master.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating Master Excel: {e}")

    # For laying out team expansions more nicely, let's use columns if there are many teams
    num_cols = 3
    team_cols = st.columns(num_cols)
    
    for i, team in enumerate(teams):
        col_idx = i % num_cols
        with team_cols[col_idx]:
            color   = COLORS[i % len(COLORS)]
            tn      = team["team_name"]
            players = allocations.get(tn, [])
            count   = len(players)
    
            with st.expander(f"{tn}  —  {count}/10", expanded=(count > 0)):
                st.markdown(
                    f"<span style='color:{color}; font-weight:700;'>Captain: {team['captain_name']}</span>",
                    unsafe_allow_html=True
                )
                
                if players:
                    # Extract this specific team's full data for Excel
                    t_master_players = [m for m in master_list if m["Team"] == tn]
                    if t_master_players:
                        df_team_full = pd.DataFrame(t_master_players)[["Player Name", "Phone"]]
                        df_team_full.rename(columns={"Phone": "Number"}, inplace=True)
                        b_team_data = generate_excel(df_team_full, tn[:31])
                        st.download_button(
                            label="📥 Export",
                            data=b_team_data,
                            file_name=f"{tn}_Roster.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"dl_team_{tn}",
                            use_container_width=True
                        )
    
                        # Show simplified view on the UI with large projector-friendly font
                        html_table = f"""
                        <style>
                            .projector-table-{i} {{
                                width: 100%;
                                border-collapse: collapse;
                                margin-top: 10px;
                            }}
                            .projector-table-{i} th, .projector-table-{i} td {{
                                border: 1px solid #444;
                                padding: 12px;
                                text-align: left;
                                font-size: 1.4em;
                            }}
                            .projector-table-{i} th {{
                                background-color: {color}22;
                                font-weight: bold;
                                color: {color};
                            }}
                            .projector-table-{i} td {{
                                font-weight: 500;
                            }}
                        </style>
                        <table class="projector-table-{i}">
                            <tr><th>Player</th><th>Mobile Number</th></tr>
                        """
                        for p in t_master_players:
                            html_table += f"<tr><td>{p.get('Player Name', '')}</td><td>{p.get('Phone', '')}</td></tr>"
                        html_table += "</table>"
                        st.markdown(html_table, unsafe_allow_html=True)
                else:
                    st.caption("No players yet.")

def teams_page():
    sb = st.session_state.supabase

    col_tgl1, col_tgl2 = st.columns([0.85, 0.15])
    with col_tgl2:
        is_light = st.toggle("🌞 Light / 🌙", value=(st.session_state.theme_mode == "Light"), key="tgl_teams")
        new_theme = "Light" if is_light else "Dark"
        if new_theme != st.session_state.theme_mode:
            st.session_state.theme_mode = new_theme
            st.rerun()

    col_title, col_actions = st.columns([0.80, 0.20])
    with col_title:
        st.markdown("<div class='premium-title' style='text-align: left; font-size: 2.2em;'>👥 Team Rosters</div>", unsafe_allow_html=True)
    with col_actions:
        st.write("")
        def nav_auction():
            st.session_state.nav_page = "Auction"
        st.button("↩ Back to Auction", type="primary", use_container_width=True, on_click=nav_auction)
    st.markdown("---")

    try:
        teams_resp   = sb.table("teams").select("*").execute()
        players_resp = sb.table("maintable").select("*").execute()

        if not teams_resp.data:
            st.info("No teams configured.")
            return
        if not players_resp.data:
            st.info("No players found.")
            return

        teams       = teams_resp.data
        all_players = players_resp.data
        allocations = _get_allocations(sb)

        _render_team_rosters(teams, allocations, all_players)

    except Exception as e:
        st.error(f"Error loading teams page: {e}")
