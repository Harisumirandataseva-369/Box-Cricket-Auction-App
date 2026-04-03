"""
Test script to verify Cricket Auction App setup
Run: python test_setup.py
"""

import sys
import os
from pathlib import Path

print("🏏 Cricket Auction App - Setup Verification Test")
print("=" * 60)

# Test 1: Check Python version
print("\n✓ Test 1: Python Version")
print(f"  Python {sys.version.split()[0]} - OK")

# Test 2: Check required files
print("\n✓ Test 2: Required Files")
required_files = [
    "app_final.py",
    "app_enhanced.py",
    "config.py",
    "utils.py",
    "requirements.txt",
    ".env",
    "README.md",
    "QUICK_START.md",
    "SQL_SETUP.sql"
]

missing = []
for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - MISSING")
        missing.append(file)

if missing:
    print(f"\n⚠️ Missing files: {', '.join(missing)}")

# Test 3: Check Python imports
print("\n✓ Test 3: Python Packages")
packages = {
    "streamlit": "Streamlit Web Framework",
    "supabase": "Supabase Database Client",
    "pandas": "Data Processing",
    "dotenv": "Environment Configuration"
}

missing_packages = []
for package, desc in packages.items():
    try:
        __import__(package)
        print(f"  ✓ {package:15} - {desc}")
    except ImportError:
        print(f"  ✗ {package:15} - MISSING")
        missing_packages.append(package)

if missing_packages:
    print(f"\n⚠️ Run: pip install -r requirements.txt")

# Test 4: Check environment variables
print("\n✓ Test 4: Environment Variables")
from dotenv import load_dotenv
load_dotenv()

env_vars = {
    "SUPABASE_URL": "Supabase Project URL",
    "SUPABASE_KEY": "Supabase API Key",
    "ADMIN_PASSWORD": "Admin Login Password"
}

for var, desc in env_vars.items():
    value = os.getenv(var)
    if value:
        masked = value[:10] + "..." if len(value) > 10 else value
        print(f"  ✓ {var:20} - {masked}")
    else:
        print(f"  ✗ {var:20} - NOT SET")

# Test 5: Test Supabase connection
print("\n✓ Test 5: Supabase Connection")
try:
    from supabase import create_client
    from config import SUPABASE_URL, SUPABASE_KEY
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print(f"  ✓ Connected to Supabase")
    
    # Try to fetch tables
    try:
        teams = supabase.table("teams").select("*").limit(1).execute()
        print(f"  ✓ Teams table exists")
    except:
        print(f"  ⚠️ Teams table not found (run SQL_SETUP.sql)")
    
    try:
        players = supabase.table("registration").select("*").limit(1).execute()
        print(f"  ✓ Registration table exists")
    except:
        print(f"  ⚠️ Registration table not found (import your CSV)")
    
    try:
        allocs = supabase.table("allocations").select("*").limit(1).execute()
        print(f"  ✓ Allocations table exists")
    except:
        print(f"  ⚠️ Allocations table not found (run SQL_SETUP.sql)")
        
except Exception as e:
    print(f"  ✗ Connection failed: {str(e)}")

# Test 6: Configuration check
print("\n✓ Test 6: Configuration")
try:
    from config import (
        APP_TITLE, COLOR_PRIMARY, ADMIN_PASSWORD,
        PLAYER_COLUMNS, TABLE_REGISTRATION, TABLE_TEAMS, TABLE_ALLOCATIONS
    )
    print(f"  ✓ App Title: {APP_TITLE}")
    print(f"  ✓ Admin Password set: {bool(ADMIN_PASSWORD)}")
    print(f"  ✓ Primary Color: {COLOR_PRIMARY}")
    print(f"  ✓ Database tables configured")
except Exception as e:
    print(f"  ✗ Config error: {str(e)}")

# Final summary
print("\n" + "=" * 60)
print("✅ Setup verification complete!")
print("\n📝 Next steps:")
print("  1. Run SQL_SETUP.sql in Supabase SQL Editor")
print("  2. Import your player registration CSV to 'registration' table")
print("  3. Start the app: streamlit run app_final.py")
print("\n" + "=" * 60)
