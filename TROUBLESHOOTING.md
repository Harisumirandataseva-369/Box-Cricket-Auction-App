# 🆘 Troubleshooting Guide

## Common Issues & Solutions

---

## 1. **"ModuleNotFoundError: No module named..."**

### Problem
```
ModuleNotFoundError: No module named 'streamlit'
```

### Solution
```powershell
cd c:\Users\njain\Documents\AuctionApp
pip install -r requirements.txt
```

### Alternative (if pip is not working)
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 2. **"Connection timeout" or "Cannot connect to Supabase"**

### Checklist
- [ ] Internet connection is working
- [ ] Supabase URL is correct in .env file
- [ ] Supabase project is active (check at supabase.com)
- [ ] Firewall not blocking connection

### Solution
1. Open `.env` file
2. Verify this line:
   ```
   SUPABASE_URL=https://lammawgiqgmiovhibvfw.supabase.co
   ```
3. Save and restart app

---

## 3. **"Table 'registration' does not exist"**

### Error Message
```
Error fetching players: relation "registration" does not exist
```

### Solution
1. Go to: https://lammawgiqgmiovhibvfw.supabase.co
2. Click **SQL Editor** (left sidebar)
3. Open `SQL_SETUP.sql` file from your project
4. Copy ALL content
5. Paste in SQL Editor
6. Click **Run**
7. Wait for success message

---

## 4. **"Admin login not working"**

### Issue
Admin password rejected

### Default Password
```
admin123
```

### To Change Password
1. Open `config.py`
2. Find: `ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")`
3. Change `"admin123"` to your new password
4. Save and restart app

---

## 5. **"Captain not found" - Cannot login as captain**

### Common Causes
1. Captain name doesn't exist in teams table
2. Name spelling is different
3. Case sensitivity (JavaScript is case-sensitive)

### Solution
1. Login as **Admin**
2. Go to **Teams** tab → **View Teams**
3. Copy the exact captain name
4. Logout and login as Captain with exact same name
5. Make sure no extra spaces

### Example
- ✅ Correct: `Rajesh Kumar`
- ❌ Wrong: `Rajesh Kumar ` (extra space)
- ❌ Wrong: `rajesh kumar` (lowercase)

---

## 6. **"No teams configured" - No teams showing up**

### Solution
1. Login as **Admin**
2. Go to **Teams** tab → **Add Team**
3. Enter team name: `Team A`
4. Enter captain name: `Captain Name`
5. Click **Add Team**
6. Go back to Auction page
7. Should show 1 team now

---

## 7. **Player CSV not importing to Supabase**

### Troubleshooting Steps
1. Check CSV file format:
   - Required columns: CCID, NAME, EMAIL, MOBILE
   - No merge cells in Excel
   - Save as .csv (not .xlsx)

2. In Supabase:
   - Go to **Tables** → **registration**
   - Try inserting a single row manually first
   - Then try CSV import

3. Column mapping:
   - CCID → CCID
   - NAME → NAME
   - EMAIL → EMAIL
   - MOBILE → MOBILE

---

## 8. **"Streamlit is taking too long to start"**

### Solution
```powershell
# Kill any existing streamlit processes
taskkill /F /IM python.exe

# Then restart
streamlit run app_final.py
```

---

## 9. **Players not showing up in the app**

### Checklist
- [ ] CSV file imported to Supabase registration table
- [ ] At least 1 player in database
- [ ] CCID column has unique values
- [ ] All required columns present: CCID, NAME, EMAIL, MOBILE

### To Verify
1. Go to Supabase: https://lammawgiqgmiovhibvfw.supabase.co
2. Click **Tables** → **registration**
3. Should see your player data

---

## 10. **"Insufficient privileges" error**

### Cause
RLS (Row Level Security) policies too strict

### Solution
1. Go to Supabase SQL Editor
2. Run this command:
   ```sql
   -- Disable RLS temporarily for development
   ALTER TABLE registration DISABLE ROW LEVEL SECURITY;
   ALTER TABLE teams DISABLE ROW LEVEL SECURITY;
   ALTER TABLE allocations DISABLE ROW LEVEL SECURITY;
   ```

---

## 11. **App runs slow or crashes**

### Try These
1. Restart the app:
   ```powershell
   # Press Ctrl+C in terminal
   # Then run again
   streamlit run app_final.py
   ```

2. Clear cache:
   ```powershell
   # Delete this folder
   %LOCALAPPDATA%\.streamlit\
   ```

3. Restart browser and refresh page

---

## 12. **"No unallocated players" - Even though players exist**

### Cause
All players may already be allocated

### To Check
1. Go to **Admin** → **Players** tab
2. Click **Unallocated** tab
3. If empty, all players are allocated

### To Reset
1. Go to Supabase
2. Go to **allocations** table
3. Delete all rows (to re-start auction)
4. Refresh app

---

## 13. **Page keeps refreshing / not loading**

### Solution
1. Hard refresh browser: **Ctrl+Shift+R**
2. Clear cookies for localhost:8501
3. Close and reopen browser
4. Check browser console (F12) for errors

---

## 14. **"CORS" or "Blocked by browser" error**

### Cause
Sometimes browser security blocks requests

### Solution
1. Try opening in Incognito/Private window
2. Try different browser (Chrome, Firefox, Edge)
3. Restart Streamlit app

---

## 15. **Environment variables not loading**

### Check .env file
1. Open `.env` file in project root
2. Make sure it looks like:
   ```
   SUPABASE_URL=https://lammawgiqgmiovhibvfw.supabase.co
   SUPABASE_KEY=sb_secret_vX-d-QNJRec_Mg77e1hYYw_Cf-Qm8o0
   ADMIN_PASSWORD=admin123
   ```

3. File must be at: `c:\Users\njain\Documents\AuctionApp\.env`
4. No extra spaces or quotes around values
5. Save and restart app

---

## 16. **Still Stuck?**

### Debug Mode - Get More Information

1. Open `app_final.py`
2. Find this line:
   ```python
   LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
   ```

3. Change to:
   ```python
   LOG_LEVEL = "DEBUG"
   ```

4. Save and run:
   ```powershell
   streamlit run app_final.py
   ```

5. Check terminal for detailed error messages

---

## 17. **Quick Verification Script**

Run this to check everything:

```powershell
python test_setup.py
```

This will check:
- ✓ Python version
- ✓ Required files
- ✓ Installed packages
- ✓ Supabase connection
- ✓ Database tables

---

## 📞 Before Asking for Help, Check:

1. ✓ Internet connection working
2. ✓ Python packages installed (`pip install -r requirements.txt`)
3. ✓ SQL_SETUP.sql executed in Supabase
4. ✓ Player CSV imported
5. ✓ At least 1 team added by admin
6. ✓ .env file configured correctly
7. ✓ Ran `python test_setup.py` and checked output

---

## 🎯 Common Workflows That Should Work:

### As Admin
1. Login with password: `admin123`
2. Add Team: Team A with Captain John
3. View teams - should show Team A
4. View players - should show imported players
5. Logout

### As Auction Master
1. See auction wheel page
2. Click "SPIN WHEEL"
3. Player allocated to random team
4. Click again - next player allocated
5. Repeat

### As Captain
1. Login with name: `John` (the captain)
2. See team page with players
3. Download CSV
4. Logout

---

**If issue persists after trying these steps, please provide:**
1. Error message (exact text)
2. What you were trying to do
3. Output from `python test_setup.py`

---

🏏 **Happy Auctioning!**
