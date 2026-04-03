import os
from dotenv import load_dotenv
from supabase import create_client, Client
# Load environment variables
load_dotenv()

# ==================== SUPABASE CONFIGURATION ====================
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://lammawgiqgmiovhibvfw.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxhbW1hd2dpcWdtaW92aGlidmZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ1Mzc3MzgsImV4cCI6MjA5MDExMzczOH0.KFjo3xKw77ylmHrLoyeqeWG3CMTeeqf8AfPQcz3oQIE")

# ==================== ADMIN CONFIGURATION ====================
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # CHANGE in production!

# ==================== APP CONFIGURATION ====================
APP_TITLE = "🏏 Cricket Auction App"
APP_DESCRIPTION = "Box Cricket Tournament Player Allocation System"

# Page refresh intervals (in seconds)
CAPTAIN_REFRESH_INTERVAL = 5
AUCTION_REFRESH_INTERVAL = 3

# Wheel animation settings
WHEEL_SPIN_DURATION = 3  # seconds
WHEEL_ANIMATION_FRAMES = 5

# ==================== DATABASE TABLE NAMES ====================
TABLE_REGISTRATION = "maintable"
TABLE_TEAMS = "teams"
TABLE_ALLOCATIONS = "allocations"

# ==================== PLAYER COLUMNS ====================
# Map to your CSV column names
PLAYER_COLUMNS = {
    "id": "CCID",
    "name": "NAME",
    "email": "EMAIL",
    "phone": "MOBILE",
    "status": "STATUS",
    "amount": "AMOUNT",
    "attendance": "Attend Before",
    "interest": "Interest",
    "dob": "DOB",
}

# ==================== UI CONFIGURATION ====================
SIDEBAR_STATE = "expanded"
LAYOUT = "wide"

# Color scheme
COLOR_PRIMARY = "#667eea"
COLOR_SECONDARY = "#764ba2"
COLOR_SUCCESS = "#16a34a"
COLOR_ERROR = "#dc2626"
COLOR_WARNING = "#ea580c"

# ==================== LOGGING ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# ==================== FEATURE FLAGS ====================
ENABLE_CAPTAIN_IMAGE_UPLOAD = True
ENABLE_PLAYER_IMAGE_DISPLAY = True
ENABLE_TEAM_BUDGET = False  # Future feature
ENABLE_AUCTION_HISTORY = True
ENABLE_EXPORT_REPORTS = True

# ==================== VALIDATION ====================
MIN_TEAM_NAME_LENGTH = 1
MAX_TEAM_NAME_LENGTH = 100
MIN_CAPTAIN_NAME_LENGTH = 2
MAX_CAPTAIN_NAME_LENGTH = 100

# ==================== PERFORMANCE ====================
DB_QUERY_TIMEOUT = 30  # seconds
CACHE_EXPIRY = 300  # seconds (5 minutes)

# ==================== SECURITY ====================
# For production, set these to stricter values
ALLOWED_UPLOAD_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB


def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


COLORS = [
    "#FF6384","#36A2EB","#FFCE56","#4BC0C0",
    "#9966FF","#FF9F40","#E7E9ED","#71B37C",
    "#F7464A","#46BFBD","#FDB45C","#949FB1",
]