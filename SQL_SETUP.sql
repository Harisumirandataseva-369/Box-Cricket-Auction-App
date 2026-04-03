-- ==================== SUPABASE DATABASE SETUP ====================
-- Run these SQL commands in your Supabase SQL Editor
-- Go to: https://lammawgiqgmiovhibvfw.supabase.co → SQL Editor

-- 1. CREATE REGISTRATION TABLE
-- This table stores all the player registration data from your CSV/Excel
CREATE TABLE IF NOT EXISTS registration (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  CCID TEXT UNIQUE NOT NULL,
  STATUS TEXT,
  PI TEXT,
  AMOUNT TEXT,
  NAME TEXT NOT NULL,
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

-- 2. CREATE TEAMS TABLE
-- This table stores team information and captains
CREATE TABLE IF NOT EXISTS teams (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  team_name TEXT UNIQUE NOT NULL,
  captain_name TEXT UNIQUE NOT NULL,
  image_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  players_count INT DEFAULT 0
);

-- 3. CREATE ALLOCATIONS TABLE
-- This table stores player-to-team allocations
CREATE TABLE IF NOT EXISTS allocations (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  player_name TEXT NOT NULL,
  player_ccid TEXT NOT NULL,
  player_email TEXT,
  player_phone TEXT,
  team_name TEXT NOT NULL,
  captain_name TEXT NOT NULL,
  allocated_at TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (team_name) REFERENCES teams(team_name) ON DELETE CASCADE
);

-- 4. CREATE INDEXES FOR BETTER PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_allocations_team ON allocations(team_name);
CREATE INDEX IF NOT EXISTS idx_allocations_player_ccid ON allocations(player_ccid);
CREATE INDEX IF NOT EXISTS idx_teams_captain ON teams(captain_name);

-- 5. ENABLE ROW LEVEL SECURITY (RLS) - For Production
-- Note: For development, you can allow all. For production, implement proper policies.
ALTER TABLE registration ENABLE ROW LEVEL SECURITY;
ALTER TABLE teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE allocations ENABLE ROW LEVEL SECURITY;

-- 6. CREATE POLICIES (Public access for now - CHANGE in production!)
-- Registration table policies
CREATE POLICY "Enable read access for all" ON registration
  FOR SELECT USING (true);

CREATE POLICY "Enable insert access for all" ON registration
  FOR INSERT WITH CHECK (true);

-- Teams table policies
CREATE POLICY "Enable read access for all" ON teams
  FOR SELECT USING (true);

CREATE POLICY "Enable insert access for all" ON teams
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable delete access for all" ON teams
  FOR DELETE USING (true);

-- Allocations table policies
CREATE POLICY "Enable read access for all" ON allocations
  FOR SELECT USING (true);

CREATE POLICY "Enable insert access for all" ON allocations
  FOR INSERT WITH CHECK (true);

-- ==================== IMPORT REGISTRATION DATA ====================
-- Option 1: Direct CSV Import (Recommended)
-- 
-- 1. Go to: https://lammawgiqgmiovhibvfw.supabase.co
-- 2. Click "Tables" in left sidebar
-- 3. Click on "registration" table
-- 4. Click "Insert" → "Insert from CSV"
-- 5. Upload your Excel/CSV file with the following columns:
--    CCID, STATUS, PI, AMOUNT, NAME, MOBILE, EMAIL, Ref Name, DOB, Attend Before, Interest, Date, URL
--
-- Option 2: Manual Copy-Paste for testing
-- 
-- Insert sample data for testing:
-- INSERT INTO registration (CCID, STATUS, NAME, MOBILE, EMAIL, "Attend Before", Interest, Date)
-- VALUES 
--   ('CC001', 'Active', 'John Doe', '+91-9876543210', 'john@email.com', 'Yes', 'Cricket', '2024-01-01'),
--   ('CC002', 'Active', 'Jane Smith', '+91-9876543211', 'jane@email.com', 'Yes', 'Cricket', '2024-01-01'),
--   ('CC003', 'Active', 'Mike Johnson', '+91-9876543212', 'mike@email.com', 'Yes', 'Cricket', '2024-01-01');

-- ==================== USEFUL QUERIES ====================

-- View all tables
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Get team-wise player count
-- SELECT team_name, captain_name, COUNT(*) as player_count 
-- FROM allocations
-- GROUP BY team_name, captain_name
-- ORDER BY player_count DESC;

-- Get unallocated players
-- SELECT CCID, NAME, EMAIL FROM registration 
-- WHERE CCID NOT IN (SELECT player_ccid FROM allocations)
-- LIMIT 10;

-- Get allocation history for a team
-- SELECT player_name, player_email, allocated_at 
-- FROM allocations 
-- WHERE team_name = 'Team A'
-- ORDER BY allocated_at DESC;

-- ==================== NOTES ====================
-- 
-- 1. Make sure all table names match the column names used in app.py
-- 2. The CCID column should be UNIQUE as it's the player identifier
-- 3. team_name and captain_name in teams table should be UNIQUE
-- 4. For production, implement proper Row Level Security (RLS) policies
-- 5. Consider adding backup policies for security
-- 6. Never share secret keys in public repositories
--
-- ==================== TROUBLESHOOTING ====================
--
-- Q: "relation "registration" does not exist"
-- A: Make sure you ran the CREATE TABLE command. Check if the table appears in the Tables list.
--
-- Q: "duplicate key value violates unique constraint"
-- A: Try inserting with different CCID or team_name values
--
-- Q: Cannot see imported data?
-- A: Refresh the page, or check the data with: SELECT * FROM registration LIMIT 10;
--
-- Q: RLS policies blocking access?
-- A: For development, disable RLS or create PERMISSIVE policies as shown above
