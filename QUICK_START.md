# 🚀 Quick Start Guide - Cricket Auction App

## 📋 Prerequisites
- Python 3.8+ installed
- Access to your Supabase account
- Your registration data (CSV or Excel file)

---

## 🔧 STEP-BY-STEP SETUP

### **STEP 1: Setup Supabase Database (5 minutes)**

1. Open your Supabase project:
   - URL: https://lammawgiqgmiovhibvfw.supabase.co
   - Go to **SQL Editor**

2. Copy-paste ALL the SQL from `SQL_SETUP.sql` file and run it
   - This creates the necessary tables: `registration`, `teams`, `allocations`

3. Import your registration data:
   - Go to **Tables** → **registration**
   - Click **Insert** → **Insert from CSV**
   - Select your CSV/Excel file with columns:
     ```
     CCID, STATUS, PI, AMOUNT, NAME, MOBILE, EMAIL, Ref Name, DOB, Attend Before, Interest, Date, URL
     ```

---

### **STEP 2: Install Python Dependencies (3 minutes)**

Open PowerShell in the AuctionApp folder:

```powershell
cd c:\Users\njain\Documents\AuctionApp
pip install -r requirements.txt
```

---

### **STEP 3: Configure Environment (1 minute)**

The `.env` file is already configured with your Supabase credentials:
```
SUPABASE_URL=https://lammawgiqgmiovhibvfw.supabase.co
SUPABASE_KEY=sb_secret_vX-d-QNJRec_Mg77e1hYYw_Cf-Qm8o0
ADMIN_PASSWORD=admin123
```

**For production, change ADMIN_PASSWORD to something secure!**

---

### **STEP 4: Run the Application (1 minute)**

```powershell
streamlit run app_enhanced.py
```

This will:
- Start a local server at `http://localhost:8501`
- Automatically open in your default browser

---

## 🎯 USAGE WORKFLOW

### **👨‍⚙️ ADMIN WORKFLOW**

1. **Login**
   - Select "Admin" radio button
   - Password: `admin123`
   - Click "Login as Admin"

2. **Add Teams** (Team Setup tab)
   - Team Name: e.g., "Team Sharks"
   - Captain Name: e.g., "Rajesh Kumar"
   - Click "Add Team"
   - Repeat for all teams

3. **View Players** (Player Management tab)
   - See all registered players
   - See already allocated players

4. **Monitor Auction** (Auction Control tab)
   - See live statistics
   - Monitor team-wise player allocation

---

### **🎡 AUCTION MASTER WORKFLOW**

1. **Access Auction Page**
   - Login as Admin (or create special "auction_master" role)
   - Click "Auction Control"

2. **Run the Auction**
   - All teams displayed at top with their captains
   - Current player to allocate is shown
   - Click **"SPIN WHEEL"** button
   - Random team is selected automatically
   - Player is allocated to that team

3. **View Live Team Updates**
   - Select team from dropdown
   - See all players allocated to that team
   - Updates in real-time

---

### **⛹️ CAPTAIN WORKFLOW**

1. **Login**
   - Select "Captain" radio button
   - Enter captain name (must match registered name)
   - Click "Login as Captain"

2. **View Team**
   - See team name and all allocated players
   - See email and phone numbers
   - Download team list as CSV

3. **Auto-Refresh**
   - Page automatically refreshes every 5 seconds
   - Always see live player allocations

---

## 🎨 APP FEATURES

### **Authentication**
- ✅ Admin login with password
- ✅ Captain login with verification
- ✅ Role-based access control

### **Admin Dashboard**
- 📋 Add/view/manage teams
- 👥 View player registrations
- 📊 See allocation statistics
- 📈 Team-wise player count charts

### **Auction Wheel**
- 🎡 Spin wheel for random team selection
- 🎯 One-click player allocation
- 📊 Live team player listings
- 🎉 Celebration animations

### **Captain Portal**
- 👥 View complete team roster
- 📧 See player contact details
- 📥 Download team list as CSV
- 🔄 Auto-refreshing live feed

---

## 📊 DATABASE STRUCTURE

### **registration** table
- `CCID`: Unique player ID
- `NAME`: Player name
- `EMAIL`: Email address
- `MOBILE`: Phone number
- `STATUS`: Registration status
- Other fields from your CSV

### **teams** table
- `team_name`: Name of the team
- `captain_name`: Captain's name (unique)
- `image_url`: Captain's image URL
- `created_at`: Team creation timestamp

### **allocations** table
- `player_name`: Name of allocated player
- `player_ccid`: Player's CCID (unique identifier)
- `team_name`: Allocated team
- `captain_name`: Team captain
- `allocated_at`: Allocation timestamp

---

## ⚙️ CONFIGURATION

### **Change Admin Password**
1. Open `app_enhanced.py`
2. Find line with: `if password == "admin123":`
3. Change `"admin123"` to your desired password
4. Save file

### **Change Wheel Spin Speed**
1. Open `app_enhanced.py`
2. Find the animation loop (search for `range(5)`)
3. Increase/decrease the range or sleep time

---

## 🐛 TROUBLESHOOTING

### **"Connection timeout" error**
```
✓ Check internet connection
✓ Verify Supabase URL is correct
✓ Check API key in .env file
```

### **"Table 'registration' does not exist"**
```
✓ Run the SQL_SETUP.sql queries in Supabase
✓ Wait a moment for table to be created
✓ Refresh the page
```

### **"No teams configured!"**
```
✓ Login as Admin
✓ Go to Team Setup → Add Team
✓ Add at least one team
```

### **"Captain not found"**
```
✓ Make sure captain name matches EXACTLY
✓ Admin must add the captain first
✓ Try with a different name (case-sensitive)
```

### **Players not showing up**
```
✓ Import CSV to 'registration' table in Supabase
✓ Make sure CSV has required columns
✓ Verify column names match: CCID, NAME, EMAIL, MOBILE
```

---

## 🔐 SECURITY NOTES ⚠️

**For Development (Current Setup - UNSAFE):**
- ✓ Simple password authentication
- ✓ Public API key used
- ✗ No row-level security

**For Production (REQUIRED):**
- [ ] Change admin password
- [ ] Use restricted API key (anon key instead of service role key)
- [ ] Implement Row Level Security (RLS) policies in Supabase
- [ ] Add OAuth/authentication (Google, GitHub, etc.)
- [ ] Use environment variables for all secrets
- [ ] Never commit `.env` file to git
- [ ] Add input validation and sanitization
- [ ] Enable CORS restrictions
- [ ] Use SSL/TLS certificates

---

## 📞 SUPPORT

If you face issues:

1. **Check logs**: Streamlit console shows detailed error messages
2. **Verify data**: Query tables directly in Supabase to check data
3. **Test connection**: Look for connection error messages
4. **Restart app**: `Ctrl+C` to stop, then `streamlit run app_enhanced.py`

---

## 📚 USEFUL RESOURCES

- **Streamlit Docs**: https://docs.streamlit.io
- **Supabase Docs**: https://supabase.com/docs
- **Python Docs**: https://docs.python.org/3/

---

## ✅ VERIFICATION CHECKLIST

Before going live with the auction:

- [ ] All teams are added with captains
- [ ] All players are imported to registration table
- [ ] Admin can login successfully
- [ ] Can add teams and see them immediately
- [ ] Spin wheel allocates players correctly
- [ ] Captains can login with their names
- [ ] Captains can see their team players
- [ ] New allocations appear immediately (live)
- [ ] No duplicate allocations

---

**Ready to auction!** 🏏 Good luck with your cricket auction! 🎉
