# 🏏 Cricket Auction App - Streamlit Web Application

A complete web application for managing box cricket player auctions with dynamic team creation, random player allocation via spinning wheel, and live player tracking.

## Features

✅ **Admin Dashboard**
- Add captains and create teams dynamically
- Upload captain images/avatars
- Manage player registrations

✅ **Auction Wheel**
- Random player allocation to teams
- Live spinning wheel animation
- Real-time player assignment display

✅ **Captain View**
- View their allocated team players
- Live data feed with auto-refresh
- Monitor team composition

✅ **Authentication**
- Admin login with secure password
- Captain login with verification
- Role-based access control

## Setup Instructions

### 1. **Install Python Dependencies**

```bash
cd c:\Users\njain\Documents\AuctionApp
pip install -r requirements.txt
```

### 2. **Setup Supabase Database**

At https://lammawgiqgmiovhibvfw.supabase.co, run the following SQL commands in the SQL Editor:

```sql
-- Create registration table (if not exists)
CREATE TABLE IF NOT EXISTS registration (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  CCID TEXT UNIQUE,
  STATUS TEXT,
  PI TEXT,
  AMOUNT TEXT,
  NAME TEXT,
  MOBILE TEXT,
  EMAIL TEXT,
  "Ref Name" TEXT,
  DOB TEXT,
  "Attend Before" TEXT,
  Interest TEXT,
  Date TEXT,
  URL TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create teams table
CREATE TABLE IF NOT EXISTS teams (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  team_name TEXT UNIQUE NOT NULL,
  captain_name TEXT UNIQUE NOT NULL,
  image_url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create allocations table
CREATE TABLE IF NOT EXISTS allocations (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  player_name TEXT NOT NULL,
  player_ccid TEXT NOT NULL,
  player_email TEXT,
  team_name TEXT NOT NULL,
  captain_name TEXT NOT NULL,
  allocated_at TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (team_name) REFERENCES teams(team_name)
);

-- Enable RLS (Row Level Security) if needed
ALTER TABLE registration ENABLE ROW LEVEL SECURITY;
ALTER TABLE teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE allocations ENABLE ROW LEVEL SECURITY;

-- Create public policies (for now - restrict in production)
CREATE POLICY "Enable read access for all users" ON registration FOR SELECT USING (true);
CREATE POLICY "Enable read access for all users" ON teams FOR SELECT USING (true);
CREATE POLICY "Enable read access for all users" ON allocations FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON teams FOR INSERT USING (true);
CREATE POLICY "Enable insert for all users" ON allocations FOR INSERT USING (true);
```

### 3. **Import Registration Data to Supabase**

1. Go to Supabase Dashboard → Tables → registration
2. Click "Insert" → "Insert from CSV"
3. Upload your registration Excel/CSV file

### 4. **Run the Application**

```bash
streamlit run app.py
```

The app will start at http://localhost:8501

## Usage Workflow

### For Admin:
1. **Login**: Enter password: `admin123`
2. **Add Teams**: Go to "Add Team Captain" tab
   - Enter team name (e.g., "Team A", "Team B")
   - Enter captain name
   - Click "Add Team & Captain"
3. **View Status**: Check "View Teams" to see all teams
4. **Manage Players**: View all registered players

### For Auction Master:
1. Navigate to **Auction Wheel** page
2. See all teams with captains at the top
3. Current player to be allocated is shown
4. Click **"SPIN THE WHEEL"** button
5. Random team is selected and player is allocated
6. Live player list updates for each team

### For Captains:
1. **Login**: Enter captain name (must match registered captain)
2. **View Team**: See all players allocated to their team
3. **Live Feed**: Page auto-refreshes every 5 seconds

## Architecture

```
AuctionApp/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
└── README.md            # This file
```

## Database Schema

### registration table
- CCID (unique identifier)
- NAME, EMAIL, MOBILE
- STATUS, PI, AMOUNT
- DOB, Attend Before, Interest
- Date, URL

### teams table
- team_name (unique)
- captain_name (unique)
- image_url
- created_at

### allocations table
- player_name, player_ccid, player_email
- team_name, captain_name
- allocated_at

## Credentials

- **Supabase URL**: https://lammawgiqgmiovhibvfw.supabase.co
- **Supabase Key**: sb_secret_vX-d-QNJRec_Mg77e1hYYw_Cf-Qm8o0
- **Admin Password**: admin123 (change this in production!)

## Security Notes ⚠️

For production, you should:
1. Change admin password to something secure
2. Use environment variables for all credentials (already set in .env)
3. Enable proper Row Level Security (RLS) policies in Supabase
4. Use anon key instead of service role key for client-side operations
5. Implement proper authentication (Supabase Auth, OAuth, etc.)
6. Add input validation and sanitization

## Troubleshooting

**"No teams configured!"**
- Make sure you've added at least one team as admin first

**"Players not showing up"**
- Import your registration CSV to Supabase registration table

**"Connection timeout"**
- Check your internet connection
- Verify Supabase credentials in .env file

## Future Enhancements

- 🎨 Beautiful scrolling wheel animation
- 📸 Captain image upload and display
- 📊 Auction statistics and reports
- 🔐 Advanced authentication system
- ⚙️ Team budget management
- 💾 Auction history and export

---

**Questions?** Check Supabase docs: https://supabase.com/docs
