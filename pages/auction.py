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


def _get_current_team_turn(teams: list, allocations: dict, player_dict: dict, auction_type: str) -> dict:
    """
    Round-robin: the team with the fewest players in the target category goes next.
    Ties broken by original team order (index).
    """
    counts = {}
    for t in teams:
        tn = t["team_name"]
        t_allocs = allocations.get(tn, [])
        cat_count = 0
        for p in t_allocs:
            ccid_str = str(p.get("player_ccid", ""))
            if ccid_str in player_dict:
                p_cat = str(player_dict[ccid_str].get("Player Category", "")).lower()
                if auction_type == "Marquee Players" and "marquee" in p_cat:
                    cat_count += 1
                elif auction_type == "Pavilion Players" and "pavilion" in p_cat:
                    cat_count += 1
        counts[tn] = cat_count
        
    min_count = min(counts.values()) if counts else 0
    for team in teams:
        if counts[team["team_name"]] == min_count:
            return team
    return teams[0]


# ─────────────────────────────────────────────
#  WHEEL HTML
# ─────────────────────────────────────────────
# Wheel component extracted to /wheel_component folder


# ─────────────────────────────────────────────
#  DIALOG HELPER & CELEBRATION
# ─────────────────────────────────────────────

def _render_celebration():
    outcomes = [
        ("IT'S A SIX! 🚀", "🏏💥", "#e74c3c"), 
        ("SMASHED FOR FOUR!", "💨4️⃣", "#3498db"),
        ("HOWZAT! OUT!", "☝️😲", "#e67e22"),
        ("CLEAN BOWLED!", "🎯💥", "#2ecc71"),
        ("WHAT A CATCH!", "🤲🥎", "#9b59b6"),
        ("NOT OUT!", "🙅‍♂️😎", "#f1c40f")
    ]
    title, emoji, color = random.choice(outcomes)
    
    css = f"""
    <style>
    @keyframes epicBounceDrop {{
        0% {{ transform: translate(-50%, -150vh) scale(0.5) rotate(-15deg); opacity: 0; }}
        20% {{ transform: translate(-50%, -50%) scale(1.1) rotate(5deg); opacity: 1; }}
        30% {{ transform: translate(-50%, -50%) scale(1) rotate(0deg); opacity: 1; }}
        75% {{ transform: translate(-50%, -50%) scale(1) rotate(0deg); opacity: 1; }}
        100% {{ transform: translate(-50%, 150vh) scale(0.8) rotate(15deg); opacity: 0; }}
    }}
    .single-funny-celeb {{
        position: fixed;
        top: 50%;
        left: 50%;
        background: #ffffff;
        border: 8px solid {color};
        border-radius: 40px;
        padding: 50px 80px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.6);
        z-index: 9999999;
        text-align: center;
        pointer-events: none;
        animation: epicBounceDrop 2.8s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    .single-funny-celeb h1 {{ font-size: 70px; margin: 0; color: {color}; text-transform: uppercase; font-family: 'Impact', sans-serif; text-shadow: 2px 2px 0px rgba(0,0,0,0.2); line-height: 1.1; }}
    .single-funny-celeb p {{ font-size: 160px; margin: 20px 0 0 0; line-height: 1; animation: wobble 1s infinite alternate; }}
    @keyframes wobble {{
        0% {{ transform: scale(1); }}
        100% {{ transform: scale(1.1); }}
    }}
    </style>
    """
    html = f"""
    <div class="single-funny-celeb">
        <h1>{title}</h1>
        <p>{emoji}</p>
    </div>
    """
    st.markdown(css + html, unsafe_allow_html=True)

def __show_dialog_content(selected_player, current_team, team_color, sb, turn_key):
    p_img = selected_player.get("URL")
    
    # Larger, comparable to captain image
    if p_img and str(p_img).strip():
        img_html = f'<img src="{p_img}" style="width:320px; height:320px; border-radius:15px; border: 4px solid {team_color}; object-fit:contain; background:#fff; margin-bottom:15px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); display:block; margin: 0 auto;">'
    else:
        img_html = _avatar_html(selected_player["NAME"], team_color, size=320)
    
    anim_css = """
    <style>
    @keyframes popIn { 0% { transform: scale(0.6); opacity: 0; } 70% { transform: scale(1.05); } 100% { transform: scale(1); opacity: 1; } }
    @keyframes swing { 0% { transform: rotate(-30deg); } 50% { transform: rotate(50deg); } 100% { transform: rotate(-30deg); } }
    @keyframes fly { 0% { transform: translate(10px, 0); } 50% { transform: translate(-30px, -50px); } 100% { transform: translate(10px, 0); } }
    .anim-container { text-align: center; font-size: 60px; margin-bottom: -20px; }
    .bat { display: inline-block; animation: swing 1.2s infinite ease-in-out; transform-origin: bottom center; }
    .ball { display: inline-block; animation: fly 1.2s infinite ease-in-out; }
    </style>
    """
    
    st.markdown(anim_css + f"""
    <div style='animation: popIn 0.6s ease-out; text-align:center;'>
        <div class="anim-container">
            <span class="bat">🏏</span><span class="ball">🔴</span>
        </div>
        <br>
        {img_html}
        <h2 style='margin-bottom:0; font-size:32px;'>{selected_player['NAME']}</h2>
        <p style='margin:10px 0 25px 0; font-size: 22px;'>Assigned to <b style='color:{team_color}; font-size:26px;'>{current_team['team_name']}</b></p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Reject & Re-spin", use_container_width=True, key="btn_reject_dialog"):
            if turn_key in st.session_state.get("wheel_winner", {}):
                del st.session_state.wheel_winner[turn_key]
            st.session_state.spin_attempts = st.session_state.get("spin_attempts", 0) + 1
            st.rerun()

    with col2:
        if st.button("✅ Confirm & Next Team", use_container_width=True, key="btn_confirm_dialog", type="primary"):
            try:
                sb.table("allocations").insert({
                    "player_name":  selected_player["NAME"],
                    "player_ccid":  selected_player["CCID"],
                    "team_name":    current_team["team_name"],
                    "captain_name": current_team["captain_name"],
                    "allocated_at": datetime.now().isoformat()
                }).execute()
                # Clean up session state and force wheel UI reset
                if turn_key in st.session_state.get("wheel_winner", {}):
                    del st.session_state.wheel_winner[turn_key]
                st.session_state.spin_attempts = st.session_state.get("spin_attempts", 0) + 1
                
                st.session_state.show_celebration = True
                st.rerun()
            except Exception as e:
                st.error(f"Error saving allocation: {e}")

if hasattr(st, "dialog"):
    show_winner_dialog = st.dialog("🎉 Player Selected!")(__show_dialog_content)
elif hasattr(st, "experimental_dialog"):
    show_winner_dialog = st.experimental_dialog("🎉 Player Selected!")(__show_dialog_content)
else:
    def show_winner_dialog(*args, **kwargs):
        with st.container():
            st.markdown("---")
            st.markdown("### 🎉 Player Selected!")
            __show_dialog_content(*args, **kwargs)
            st.markdown("---")

# ─────────────────────────────────────────────
#  SUB-SECTIONS
# ─────────────────────────────────────────────

def _render_team_spotlight(team: dict, color: str):
    """Left panel: current team and captain card."""

    image_url = team.get("image_url")
    if image_url and str(image_url).strip():
        # Using a wider, more visible rounded rectangle instead of a circle
        avatar_html = f'''<div style="width:100%; height:320px; border-radius:12px; margin: 0 auto 15px auto; overflow:hidden; border: 4px solid {color}; box-shadow: 0 6px 18px rgba(0,0,0,0.3); background:#fff; display:flex; align-items:center; justify-content:center;">
<img src="{image_url}" style="width:100%; height:100%; object-fit:contain; object-position: center;">
</div>'''
    else:
        # Fallback to initials but keeping the same wider rectangular shape
        initials = _get_initials(team["team_name"])
        avatar_html = f"""<div style="width:100%; height:320px; border-radius:12px; border: 4px solid {color}; background:{color}44; display:flex; align-items:center; justify-content:center; font-size:80px; font-weight:bold; color:{color}; margin: 0 auto 15px auto; box-shadow: 0 6px 18px rgba(0,0,0,0.2);">{initials}</div>"""

    txt_color = "#2c3e50" if st.session_state.theme_mode == "Light" else "white"

    st.markdown(f"""<div class="premium-card" style="padding: 30px 20px; text-align:center; border: 2px solid {color}; box-shadow: 0 10px 40px {color}66; margin-bottom: 20px; transition: transform 0.3s; background-color: transparent; border-radius: 12px;">
{avatar_html}
<h2 style="color:{txt_color}; margin:15px 0 0 0; font-size:32px;">{team['team_name']}</h2>
<h4 style="color:{color}; margin:8px 0 0 0; font-size:22px;">Captain: {team['captain_name']}</h4>
</div>""", unsafe_allow_html=True)




# ─────────────────────────────────────────────
#  MAIN PAGE
# ─────────────────────────────────────────────

def auction_page():
    sb = _supabase()

    if st.session_state.pop("show_celebration", False):
        _render_celebration()

    # ── Top bar ──────────────────────────────
    col_tgl1, col_tgl2 = st.columns([0.85, 0.15])
    with col_tgl2:
        is_light = st.toggle("🌞 Light / 🌙", value=(st.session_state.theme_mode == "Light"), key="tgl_auc")
        new_theme = "Light" if is_light else "Dark"
        if new_theme != st.session_state.theme_mode:
            st.session_state.theme_mode = new_theme
            st.rerun()

    col_title, col_actions = st.columns([0.55, 0.45])
    with col_title:
        st.markdown("<div class='premium-title' style='text-align: left; font-size: 2.2em;'>🏏 Live Auction Arena</div>", unsafe_allow_html=True)
    with col_actions:
        st.write("")
        b1, b2, b3 = st.columns(3)
        with b1:
            def nav_teams():
                st.session_state.nav_page = "Teams"
            st.button("👥 Teams Page", type="primary", use_container_width=True, on_click=nav_teams)
        with b2:
            if st.button("🚪 Logout", key="auction_logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.user_role = None
                st.query_params.clear()
                st.rerun()
        with b3:
            if st.button("🔄 Reset", type="secondary", use_container_width=True):
                st.session_state.show_reset_confirm = True

    st.markdown("---")

    if st.session_state.get("show_reset_confirm", False):
        st.warning("Are you sure you want to delete all allocations and reset the auction?")
        colY, colN = st.columns(2)
        if colY.button("Yes, Reset", type="primary"):
            try:
                # To guarantee a bulk delete works, we select all IDs and delete them.
                allocs = sb.table("allocations").select("player_ccid").execute()
                if allocs.data:
                    ccids = [r["player_ccid"] for r in allocs.data]
                    sb.table("allocations").delete().in_("player_ccid", ccids).execute()
                st.session_state.show_reset_confirm = False
                if "wheel_winner" in st.session_state:
                    del st.session_state["wheel_winner"]
                st.success("Auction Reset! Refreshing...")
                st.rerun()
            except Exception as e:
                st.error(f"Error resetting: {e}")
        if colN.button("Cancel"):
            st.session_state.show_reset_confirm = False
            st.rerun()


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
        player_dict = {p["CCID"]: p for p in all_players}

        # ── Auction Type Selector ────────────────
        st.markdown("<h3 style='color: #a0aab2;'>🎯 Select Auction Mode</h3>", unsafe_allow_html=True)
        auction_type = st.radio(
            "Auction Type", 
            ["Marquee Players", "Pavilion Players"], 
            horizontal=True,
            label_visibility="collapsed"
        )
        
        target_display_name = "Marquee" if auction_type == "Marquee Players" else "Pavilion Player"
        max_category = 2 if auction_type == "Marquee Players" else 5
        
        def is_target_category(p_cat):
            c_str = str(p_cat).strip().lower()
            if auction_type == "Marquee Players":
                return "marquee" in c_str
            else:
                return "pavilion" in c_str

        # ── Live data ────────────────────────
        allocations     = _get_allocations()
        allocated_ccids = _get_allocated_ccids(allocations)
        captain_names   = {t.get("captain_name") for t in teams if t.get("captain_name")}
        
        unallocated_all = [
            p for p in all_players 
            if p["CCID"] not in allocated_ccids and p["NAME"] not in captain_names
        ]
        
        unallocated_target = [
            p for p in unallocated_all
            if is_target_category(p.get("Player Category", ""))
        ]

        # ── Progress bar ─────────────────────
        total_target_in_db = len([p for p in all_players if is_target_category(p.get("Player Category", ""))])
        allocated_target = total_target_in_db - len(unallocated_target)
        
        st.markdown(
            f"**{auction_type} Progress:** {allocated_target} / {total_target_in_db} players allocated"
        )
        st.progress(allocated_target / total_target_in_db if total_target_in_db else 0)
        st.markdown("")

        if not unallocated_target:
            st.success(f"🎉 All {target_display_name} players have been allocated!")
            return
            
        def get_category_count(team_allocations):
            count = 0
            for p in team_allocations:
                ccid_str = str(p.get("player_ccid", ""))
                if ccid_str in player_dict and is_target_category(player_dict[ccid_str].get("Player Category", "")):
                    count += 1
            return count

        # ── Eligible Teams ────────────────
        eligible_teams = [t for t in teams if get_category_count(allocations.get(t["team_name"], [])) < max_category]
        
        if not eligible_teams:
            st.success(f"🎉 All teams have reached their maximum of {max_category} {target_display_name} players!")
            return


        # ── Whose turn ───────────────────────
        current_team  = _get_current_team_turn(eligible_teams, allocations, player_dict, auction_type)
        team_index    = next((i for i, t in enumerate(teams) if t["team_name"] == current_team["team_name"]), 0)
        team_color    = COLORS[team_index % len(COLORS)]

        # ── Pre-calculate Wheel Winner ────────
        if "wheel_winner" not in st.session_state:
            st.session_state.wheel_winner = {}
        
        cat_count = get_category_count(allocations.get(current_team['team_name'], []))
        turn_key = f"{auction_type}_{current_team['team_name']}_{cat_count}"
        
        if turn_key not in st.session_state.wheel_winner:
            st.session_state.wheel_winner[turn_key] = random.choice(unallocated_target)["NAME"]
            
        winning_player_name = st.session_state.wheel_winner[turn_key]

        # ── Main 2-column layout ──────────────
        col_left, col_mid = st.columns([0.35, 0.65])

        with col_left:
            _render_team_spotlight(current_team, team_color)

        with col_mid:
            st.subheader("🎡 Spin the Wheel")
            player_names = [p["NAME"] for p in unallocated_target]
            wheel_colors = [COLORS[i % len(COLORS)] for i in range(len(player_names))]
            winner_idx   = next((i for i, name in enumerate(player_names) if name == winning_player_name), 0)
            
            from pathlib import Path
            component_path = str(Path(__file__).parent.parent / "wheel_component")
            wheel_comp = components.declare_component("wheel_component", path=component_path)
            
            wheel_key = f"wheel_{turn_key}_{st.session_state.get('spin_attempts', 0)}"
            returned_player = wheel_comp(team_names=player_names, wheel_colors=wheel_colors, winner_index=winner_idx, key=wheel_key)
            
            if returned_player:
                selected_player = next((p for p in unallocated_target if p["NAME"] == returned_player), None)
                if selected_player:
                    show_winner_dialog(selected_player, current_team, team_color, sb, turn_key)

    except Exception as e:
        st.error(f"Error loading auction page: {e}")
        st.exception(e)