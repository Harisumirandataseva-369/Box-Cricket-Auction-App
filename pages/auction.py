import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from datetime import datetime
import random
from config import COLORS

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def _supabase():
    return st.session_state.supabase


def _get_initials(name: str) -> str:
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper()


def _avatar_html(name: str, color: str, size: int = 80) -> str:
    initials = _get_initials(name)
    return f"""
    <div style="
        width:{size}px; height:{size}px; border-radius:50%;
        background:{color}; display:flex; align-items:center;
        justify-content:center; font-size:{size//3}px;
        font-weight:bold; color:white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin: 0 auto 8px auto;">
        {initials}
    </div>"""


def _get_allocations() -> dict:
    """Returns {team_name: [list of player dicts]} from DB."""
    sb = _supabase()
    result = {}
    try:
        allocs = sb.table("allocations").select("*").execute()
        for row in (allocs.data or []):
            tn = row["team_name"]
            result.setdefault(tn, []).append(row)
    except:
        pass
    return result


def _get_allocated_ccids(allocations: dict) -> set:
    ccids = set()
    for players in allocations.values():
        for p in players:
            ccids.add(p["player_ccid"])
    return ccids


def _get_current_team_turn(teams: list, allocations: dict) -> dict:
    """
    Round-robin: the team with the fewest players goes next.
    Ties broken by original team order (index).
    """
    counts = {t["team_name"]: len(allocations.get(t["team_name"], [])) for t in teams}
    min_count = min(counts.values())
    for team in teams:
        if counts[team["team_name"]] == min_count:
            return team
    return teams[0]


# ─────────────────────────────────────────────
#  WHEEL HTML
# ─────────────────────────────────────────────
# Wheel component extracted to /wheel_component folder


# ─────────────────────────────────────────────
#  SUB-SECTIONS
# ─────────────────────────────────────────────

def _render_player_spotlight(player: dict, team_turn: dict, color: str):
    """Left panel: current player card."""

    image_url = player.get("URL")
    if image_url and str(image_url).strip():
        avatar_html = f'''<div style="width:150px; height:150px; border-radius:50%; margin: 0 auto 15px auto; overflow:hidden; border: 4px solid {color}; box-shadow: 0 4px 12px rgba(0,0,0,0.3); background:#fff; display:flex; align-items:center; justify-content:center;">
<img src="{image_url}" style="width:100%; height:100%; object-fit:cover;">
</div>'''
    else:
        avatar_html = _avatar_html(player["NAME"], color, size=150)

    txt_color = "#2c3e50" if st.session_state.theme_mode == "Light" else "white"

    st.markdown(f"""<div class="premium-card" style="padding: 40px 20px; text-align:center; border: 2px solid {color}; box-shadow: 0 10px 40px {color}66; margin-bottom: 20px; transition: transform 0.3s; background-color: transparent;">
{avatar_html}
<h2 style="color:{txt_color}; margin:10px 0 0 0; font-size:26px;">{player['NAME']}</h2>
</div>""", unsafe_allow_html=True)


def _render_team_rosters(teams: list, allocations: dict):
    """Right panel: all teams with their player counts and lists."""
    st.subheader("👥 Team Rosters")

    for i, team in enumerate(teams):
        color   = COLORS[i % len(COLORS)]
        tn      = team["team_name"]
        players = allocations.get(tn, [])
        count   = len(players)

        with st.expander(f"{tn}  —  {count} player(s)", expanded=(count > 0)):
            st.markdown(
                f"<span style='color:{color}; font-weight:700;'>Captain: {team['captain_name']}</span>",
                unsafe_allow_html=True
            )
            if players:
                df = pd.DataFrame(players)[["player_name", "player_email", "allocated_at"]]
                df.columns = ["Player", "Email", "Allocated At"]
                df["Allocated At"] = pd.to_datetime(df["Allocated At"]).dt.strftime("%H:%M:%S")
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.caption("No players yet.")


# ─────────────────────────────────────────────
#  MAIN PAGE
# ─────────────────────────────────────────────

def auction_page():
    sb = _supabase()

    # ── Top bar ──────────────────────────────
    col_tgl1, col_tgl2 = st.columns([0.85, 0.15])
    with col_tgl2:
        is_light = st.toggle("🌞 Light / 🌙 Dark", value=(st.session_state.theme_mode == "Light"), key="tgl_auc")
        new_theme = "Light" if is_light else "Dark"
        if new_theme != st.session_state.theme_mode:
            st.session_state.theme_mode = new_theme
            st.rerun()

    col_title, col_logout = st.columns([0.85, 0.15])
    with col_title:
        st.markdown("<div class='premium-title' style='text-align: left; font-size: 2.2em;'>🏏 Live Auction Arena</div>", unsafe_allow_html=True)
    with col_logout:
        st.write("")
        if st.button("🚪 Logout", key="auction_logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.user_role = None
            st.query_params.clear()
            st.rerun()

    st.markdown("---")

    try:
        teams_resp   = sb.table("teams").select("*").execute()
        players_resp = sb.table("maintable").select("*").execute()

        if not teams_resp.data:
            st.error("⚠️ No teams configured. Ask admin to add teams first.")
            return
        if not players_resp.data:
            st.error("⚠️ No players found in maintable.")
            return

        teams       = teams_resp.data
        all_players = players_resp.data

        # ── Live data ────────────────────────
        allocations     = _get_allocations()
        allocated_ccids = _get_allocated_ccids(allocations)
        captain_names   = {t.get("captain_name") for t in teams if t.get("captain_name")}
        
        unallocated     = [
            p for p in all_players 
            if p["CCID"] not in allocated_ccids and p["NAME"] not in captain_names
        ]

        # ── Progress bar ─────────────────────
        total     = len([p for p in all_players if p["NAME"] not in captain_names])
        allocated = total - len(unallocated)
        st.markdown(
            f"**Auction Progress:** {allocated} / {total} players allocated"
        )
        st.progress(allocated / total if total else 0)
        st.markdown("")

        if not unallocated:
            st.success("🎉 All players have been allocated! Auction complete.")
            _render_team_rosters(teams, allocations)
            return

        # ── Eligible Teams ────────────────
        eligible_teams = [t for t in teams if len(allocations.get(t["team_name"], [])) < 10]
        if not eligible_teams:
            st.success("🎉 All teams have reached their maximum of 11 players! Auction complete.")
            _render_team_rosters(teams, allocations)
            return

        # ── Whose turn ───────────────────────
        current_team  = _get_current_team_turn(eligible_teams, allocations)
        team_index    = next((i for i, t in enumerate(teams) if t["team_name"] == current_team["team_name"]), 0)
        team_color    = COLORS[team_index % len(COLORS)]

        # Next player is first unallocated
        current_player = unallocated[0]

        # ── Pre-calculate Wheel Winner ────────
        if "wheel_winner" not in st.session_state:
            st.session_state.wheel_winner = {}
        curr_ccid = current_player["CCID"]
        if curr_ccid not in st.session_state.wheel_winner:
            st.session_state.wheel_winner[curr_ccid] = random.choice(eligible_teams)["team_name"]
            
        winning_team_name = st.session_state.wheel_winner[curr_ccid]



        # ── Main 3-column layout ──────────────
        col_left, col_mid, col_right = st.columns([0.25, 0.45, 0.30])

        with col_left:
            _render_player_spotlight(current_player, current_team, team_color)

        with col_mid:
            st.subheader("🎡 Spin the Wheel")
            team_names   = [t["team_name"] for t in eligible_teams]
            wheel_colors = [COLORS[next((i for i, t in enumerate(teams) if t["team_name"] == name), 0) % len(COLORS)] for name in team_names]
            winner_idx   = next(i for i, name in enumerate(team_names) if name == winning_team_name)
            
            from pathlib import Path
            component_path = str(Path(__file__).parent.parent / "wheel_component")
            wheel_comp = components.declare_component("wheel_component", path=component_path)
            
            returned_team = wheel_comp(team_names=team_names, wheel_colors=wheel_colors, winner_index=winner_idx, key="wheel_" + curr_ccid)
            
            if returned_team:
                st.success(f"🎉 **{current_player['NAME']}** is going to **{returned_team}**!")
                if st.button("✅ Assign & Next Player", use_container_width=True):
                    selected_team = next(t for t in teams if t["team_name"] == returned_team)
                    try:
                        sb.table("allocations").insert({
                            "player_name":  current_player["NAME"],
                            "player_ccid":  current_player["CCID"],
                            "player_email": current_player.get("EMAIL", ""),
                            "team_name":    selected_team["team_name"],
                            "captain_name": selected_team["captain_name"],
                            "allocated_at": datetime.now().isoformat()
                        }).execute()
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving allocation: {e}")

        with col_right:
            _render_team_rosters(teams, allocations)

    except Exception as e:
        st.error(f"Error loading auction page: {e}")
        st.exception(e)