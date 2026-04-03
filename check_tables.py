from supabase import create_client

SUPABASE_URL = "https://lammawgiqgmiovhibvfw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxhbW1hd2dpcWdtaW92aGlidmZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ1Mzc3MzgsImV4cCI6MjA5MDExMzczOH0.KFjo3xKw77ylmHrLoyeqeWG3CMTeeqf8AfPQcz3oQIE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Get all tables
try:
    result = supabase.table("information_schema.tables").select("table_name").eq("table_schema", "public").execute()
    
    print("Available tables in Supabase:")
    print("-" * 40)
    if result.data:
        for row in result.data:
            print(f"  • {row['table_name']}")
    else:
        print("No tables found")
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative method...")
    
    # Alternative: Try to list some common table names
    tables_to_check = ["registration", "teams", "allocations", "maintable", "players"]
    print("\nChecking common table names:")
    for table_name in tables_to_check:
        try:
            result = supabase.table(table_name).select("*", count="exact").execute()
            print(f"  ✓ {table_name} - {result.count if result.count else 0} records")
        except:
            pass
