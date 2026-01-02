import sqlite3
import pandas as pd

print("🔄 Updating exercise library...")

# Connect to database
conn = sqlite3.connect('fittrack.db')

# Read the new expanded exercise library
df = pd.read_csv('exercise_library_expanded.csv')

# Replace the old exercise library with new one
df.to_sql('exercise_library', conn, if_exists='replace', index=False)

conn.close()

print("✅ Exercise library updated successfully!")
print(f"📊 Total exercises: {len(df)}")
print("\nExercises by category:")
for category in df['category'].unique():
    count = len(df[df['category'] == category])
    print(f"  {category}: {count} exercises")