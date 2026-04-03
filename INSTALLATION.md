# 🏏 Cricket Auction App - Complete Installation Guide

## ✅ What's Included

Your complete Streamlit web application is ready with the following components:

### 📦 Core Application Files
- **app_final.py** ⭐ **← START HERE** (Recommended - Production ready)
- app_enhanced.py (Feature-rich version)
- app.py (Basic version)

### 🔧 Supporting Files
- config.py (Configuration management)
- utils.py (Utility functions & database helpers)
- requirements.txt (Python dependencies)
- .env (Pre-configured environment variables)

### 📚 Documentation
- README.md (Full documentation)
- QUICK_START.md (Step-by-step guide)
- SQL_SETUP.sql (Database schema)
- test_setup.py (Verification script)

---

## 🚀 Installation Steps

### STEP 1: Install Python Packages

Open PowerShell and run:

```powershell
cd c:\Users\njain\Documents\AuctionApp
pip install -r requirements.txt
```

**Wait for installation to complete (1-2 minutes)**

---

### STEP 2: Setup Supabase Database

1. Go to: **https://lammawgiqgmiovhibvfw.supabase.co**
2. Click **SQL Editor** (left sidebar)
3. Open file: `SQL_SETUP.sql`
4. Copy ALL content and paste in Supabase SQL Editor
5. Click **Run** button
6. Wait for success message

---

### STEP 3: Import Your Registration Data

1. In Supabase, go to **Tables** (left sidebar)
2. Click **registration** table
3. Click **Insert** → **Insert from CSV**
4. Select your player CSV file
5. Map columns if needed:
   ```
   CCID → CCID
   NAME → NAME
   EMAIL → EMAIL
   MOBILE → MOBILE
   STATUS → STATUS
   ```
6. Click **Import**

---

### STEP 4: Test Setup (Optional)

```powershell
python test_setup.py
```

This verifies all components are configured correctly.

---

### STEP 5: Start the Application

```powershell
streamlit run app_final.py
```

**The app will automatically open in your browser at `http://localhost:8501`**

---

## 🎯 How to Use

### **For Admin:**
1. Login with password: `admin123`
2. Go to **Teams** tab → Add teams and their captains
3. Go to **Players** tab → Verify your registration data is imported
4. Go to **Auction** tab → Start allocating players

### **For Auction Master:**
1. Stay on main **Auction Wheel** page
2. Click **SPIN WHEEL** to randomly allocate players
3. Watch live team updates

### **For Captains:**
1. Login with their name (must match registered captain name)
2. View their team players
3. See live updates as players are allocated

---

## 📋 Features Overview

### 👨‍⚙️ **Admin Dashboard**
- ✅ Add/view/delete teams dynamically
- ✅ View all registered players
- ✅ Monitor auction progress
- ✅ View team-wise statistics
- ✅ Generate reports

### 🎡 **Auction Wheel**
- ✅ Random team selection (spinning wheel)
- ✅ One-click player allocation
- ✅ Live team roster updates
- ✅ Real-time player tracking
- ✅ Celebration animations

### ⛹️ **Captain Portal**
- ✅ View complete team roster
- ✅ See player details (name, email, phone)
- ✅ Download team list as CSV
- ✅ Auto-refreshing live feed (5-sec updates)

---

## 🔐 Security & Customization

### Change Admin Password:
1. Open `config.py`
2. Find: `ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")`
3. Change the default value
4. Save file

### Disable Auto-Refresh (Optional):
1. Open `app_final.py`
2. Find lines with `st.rerun()` in captain_page()
3. Remove or comment out the auto-refresh section

---

## 📱 File Locations

```
c:\Users\njain\Documents\AuctionApp\
├── app_final.py           ← Run this
├── app_enhanced.py
├── app.py
├── config.py
├── utils.py
├── .env
├── requirements.txt
├── SQL_SETUP.sql          ← Run in Supabase
├── README.md
├── QUICK_START.md
└── test_setup.py
```

---

## 🔗 Supabase Credentials

Your app is pre-configured with:
- **Project URL**: https://lammawgiqgmiovhibvfw.supabase.co
- **API Key**: (stored in .env file)
- **Tables**: registration, teams, allocations

---

## 📊 Database Structure

### registration (Player Data)
```
CCID | NAME | EMAIL | MOBILE | STATUS | AMOUNT | DOB | Date | URL | ...
```

### teams (Team Setup)
```
team_name | captain_name | image_url | created_at
```

### allocations (Results)
```
player_name | player_ccid | player_email | team_name | captain_name | allocated_at
```

---

## ✅ Verification Checklist

Before running the auction:

- [ ] All packages installed (pip install -r requirements.txt)
- [ ] SQL_SETUP.sql executed in Supabase
- [ ] Player CSV imported to registration table
- [ ] At least one team added
- [ ] Admin password tested
- [ ] Captain login verified
- [ ] Spin wheel test allocation works

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
```powershell
pip install -r requirements.txt
```

### "Connection timeout" for Supabase
- Check internet connection
- Verify .env file has correct URL and key
- Check Supabase status at: https://status.supabase.com

### "Table 'registration' does not exist"
- Run SQL_SETUP.sql in Supabase SQL Editor
- Wait a few seconds and refresh

### "Admin login not working"
- Default password: `admin123`
- Check config.py for changes

### "Captain not found"
- Captain name must match exactly (case-sensitive)
- Admin must add captain first in Teams section

---

## 📞 Support Resources

- **Streamlit**: https://docs.streamlit.io
- **Supabase**: https://supabase.com/docs
- **Python**: https://docs.python.org/3/
- **Pandas**: https://pandas.pydata.org/docs/

---

## 🎉 Ready to Start?

```powershell
cd c:\Users\njain\Documents\AuctionApp
streamlit run app_final.py
```

**Your cricket auction app is now live! 🏏**

---

## 💡 Tips & Tricks

1. **Multiple Teams**: Add as many teams as needed - system is completely dynamic
2. **Live Updates**: All pages auto-refresh to show real-time allocations
3. **Export Data**: Captains can download their team list as CSV
4. **Analytics**: Admin dashboard shows visual charts and statistics
5. **Mobile Friendly**: Works on phones/tablets for portable auction management

---

## 📝 Notes

- Password for admin is currently set to: `admin123` (CHANGE in production!)
- App uses Supabase real-time capabilities
- Supports unlimited teams and players
- All data is persistent in your Supabase database

---

**Made with ❤️ for your cricket auction!**

Need modifications? Just let me know! 🚀
