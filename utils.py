import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import logging
from config import *

# Setup logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

# ==================== SUPABASE CONNECTION ====================

@st.cache_resource
def get_supabase_client() -> Client:
    """Initialize and cache Supabase client"""
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logger.error(f"Failed to connect to Supabase: {str(e)}")
        st.error(f"❌ Database Connection Error: {str(e)}")
        return None

# ==================== AUTHENTICATION HELPERS ====================

def verify_admin_password(password: str) -> bool:
    """Verify admin password"""
    return password == ADMIN_PASSWORD

def is_valid_captain(captain_name: str, supabase: Client) -> bool:
    """Check if captain exists in teams table"""
    try:
        response = supabase.table(TABLE_TEAMS).select("captain_name").eq("captain_name", captain_name).execute()
        return len(response.data) > 0
    except Exception as e:
        logger.error(f"Error verifying captain: {str(e)}")
        return False

# ==================== TEAM OPERATIONS ====================

def get_all_teams(supabase: Client) -> list:
    """Fetch all teams"""
    try:
        response = supabase.table(TABLE_TEAMS).select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        logger.error(f"Error fetching teams: {str(e)}")
        st.error(f"Error fetching teams: {str(e)}")
        return []

def add_new_team(team_name: str, captain_name: str, supabase: Client) -> bool:
    """Add new team"""
    try:
        if not team_name or not captain_name:
            st.error("Team and captain names are required!")
            return False
        
        if len(team_name) > MAX_TEAM_NAME_LENGTH or len(captain_name) > MAX_CAPTAIN_NAME_LENGTH:
            st.error("Name too long!")
            return False
        
        team_data = {
            "team_name": team_name.strip(),
            "captain_name": captain_name.strip(),
            "image_url": "",
            "created_at": datetime.now().isoformat()
        }
        
        supabase.table(TABLE_TEAMS).insert(team_data).execute()
        logger.info(f"Team added: {team_name} with captain {captain_name}")
        return True
    except Exception as e:
        logger.error(f"Error adding team: {str(e)}")
        st.error(f"Error adding team: {str(e)}")
        return False

def delete_team(team_name: str, supabase: Client) -> bool:
    """Delete a team"""
    try:
        supabase.table(TABLE_TEAMS).delete().eq("team_name", team_name).execute()
        logger.info(f"Team deleted: {team_name}")
        return True
    except Exception as e:
        logger.error(f"Error deleting team: {str(e)}")
        st.error(f"Error deleting team: {str(e)}")
        return False

# ==================== PLAYER OPERATIONS ====================

def get_all_players(supabase: Client) -> list:
    """Fetch all registered players"""
    try:
        response = supabase.table(TABLE_REGISTRATION).select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        logger.error(f"Error fetching players: {str(e)}")
        st.error(f"Error fetching players: {str(e)}")
        return []

def get_unallocated_players(supabase: Client) -> list:
    """Get list of players not yet allocated to any team"""
    try:
        all_players = get_all_players(supabase)
        allocations = get_all_allocations(supabase)
        allocated_ccids = {a.get("player_ccid") for a in allocations if allocations}
        
        unallocated = [p for p in all_players if p.get("CCID") not in allocated_ccids]
        logger.info(f"Found {len(unallocated)} unallocated players")
        return unallocated
    except Exception as e:
        logger.error(f"Error getting unallocated players: {str(e)}")
        return []

def players_to_dataframe(players: list) -> pd.DataFrame:
    """Convert player list to DataFrame"""
    if not players:
        return pd.DataFrame()
    
    df = pd.DataFrame([{
        "Name": p.get("NAME", "N/A"),
        "Email": p.get("EMAIL", "N/A"),
        "Phone": p.get("MOBILE", "N/A"),
        "Status": p.get("STATUS", "N/A"),
        "Attendance": p.get("Attend Before", "N/A"),
        "Interest": p.get("Interest", "N/A"),
    } for p in players])
    
    return df

# ==================== ALLOCATION OPERATIONS ====================

def get_all_allocations(supabase: Client) -> list:
    """Fetch all player allocations"""
    try:
        response = supabase.table(TABLE_ALLOCATIONS).select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        logger.error(f"Error fetching allocations: {str(e)}")
        return []

def get_team_players(team_name: str, supabase: Client) -> list:
    """Get all players allocated to a specific team"""
    try:
        response = supabase.table(TABLE_ALLOCATIONS).select("*").eq("team_name", team_name).execute()
        return response.data if response.data else []
    except Exception as e:
        logger.error(f"Error fetching team players: {str(e)}")
        return []

def allocate_player(player: dict, team: dict, supabase: Client) -> bool:
    """Allocate a player to a team"""
    try:
        allocation = {
            "player_name": player.get("NAME", "N/A"),
            "player_ccid": player.get("CCID", ""),
            "player_email": player.get("EMAIL", ""),
            "player_phone": player.get("MOBILE", ""),
            "team_name": team["team_name"],
            "captain_name": team["captain_name"],
            "allocated_at": datetime.now().isoformat()
        }
        
        supabase.table(TABLE_ALLOCATIONS).insert(allocation).execute()
        logger.info(f"Player {player.get('NAME')} allocated to {team['team_name']}")
        return True
    except Exception as e:
        logger.error(f"Error allocating player: {str(e)}")
        st.error(f"Error allocating player: {str(e)}")
        return False

def get_team_stats(supabase: Client) -> dict:
    """Get team statistics"""
    try:
        allocations = get_all_allocations(supabase)
        teams = get_all_teams(supabase)
        
        stats = {}
        for team in teams:
            team_name = team["team_name"]
            count = len([a for a in allocations if a.get("team_name") == team_name])
            stats[team_name] = count
        
        return stats
    except Exception as e:
        logger.error(f"Error getting team stats: {str(e)}")
        return {}

def allocations_to_dataframe(allocations: list) -> pd.DataFrame:
    """Convert allocations list to DataFrame"""
    if not allocations:
        return pd.DataFrame()
    
    df = pd.DataFrame([{
        "Player": a.get("player_name", "N/A"),
        "Email": a.get("player_email", "N/A"),
        "Phone": a.get("player_phone", "N/A"),
        "Team": a.get("team_name", "N/A"),
        "Captain": a.get("captain_name", "N/A"),
        "Allocated": a.get("allocated_at", "N/A")
    } for a in allocations])
    
    return df

# ==================== UI HELPERS ====================

def render_stat_card(label: str, value: str, color: str = "#667eea"):
    """Render a styled metric card"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color} 0%, rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:7], 16)},0.8) 100%);
                border-radius: 10px;
                padding: 20px;
                color: white;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <p style="margin: 0; font-size: 14px; opacity: 0.8;">{label}</p>
        <h2 style="margin: 10px 0 0 0;">{value}</h2>
    </div>
    """, unsafe_allow_html=True)

def render_info_box(text: str, color: str = "#667eea"):
    """Render an info box with custom color"""
    st.markdown(f"""
    <div style="background: {color}20;
                border-left: 4px solid {color};
                padding: 15px;
                border-radius: 5px;">
        {text}
    </div>
    """, unsafe_allow_html=True)

# ==================== DATA EXPORT ====================

def export_to_csv(data: list, filename: str) -> str:
    """Convert data to CSV"""
    if not data:
        return ""
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

def export_team_roster(team_name: str, supabase: Client) -> str:
    """Export team roster as CSV"""
    try:
        players = get_team_players(team_name, supabase)
        return export_to_csv(players, f"{team_name}_roster.csv")
    except Exception as e:
        logger.error(f"Error exporting roster: {str(e)}")
        return ""

# ==================== VALIDATION ====================

def validate_team_input(team_name: str, captain_name: str) -> tuple[bool, str]:
    """Validate team input"""
    if not team_name or not team_name.strip():
        return False, "Team name is required!"
    
    if not captain_name or not captain_name.strip():
        return False, "Captain name is required!"
    
    if len(team_name) > MAX_TEAM_NAME_LENGTH:
        return False, f"Team name too long (max {MAX_TEAM_NAME_LENGTH} characters)"
    
    if len(captain_name) > MAX_CAPTAIN_NAME_LENGTH:
        return False, f"Captain name too long (max {MAX_CAPTAIN_NAME_LENGTH} characters)"
    
    return True, ""

# ==================== STATISTICS ====================

def get_auction_stats(supabase: Client) -> dict:
    """Get overall auction statistics"""
    try:
        teams = get_all_teams(supabase)
        players = get_all_players(supabase)
        allocations = get_all_allocations(supabase)
        unallocated = get_unallocated_players(supabase)
        
        return {
            "total_teams": len(teams),
            "total_players": len(players),
            "total_allocated": len(allocations),
            "total_unallocated": len(unallocated),
            "percentage_complete": (len(allocations) / len(players) * 100) if players else 0
        }
    except Exception as e:
        logger.error(f"Error calculating stats: {str(e)}")
        return {}
