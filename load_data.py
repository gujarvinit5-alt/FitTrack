import sqlite3
import pandas as pd

def load_exercise_library():
    '''Load exercises from CSV into database'''
    conn = sqlite3.connect('fittrack.db')

    # Read CSV
    df = pd.read_csv('data/exercise_library.csv')

    # Insert into database (replace if already exists)
    df.to_sql('exercise_library', conn, if_exists='replace', index=False)

    conn.close()
    print("✅ Exercise library loaded!")

def load_food_library():
    '''Load foods from CSV into database'''
    conn = sqlite3.connect('fittrack.db')

    # Read CSV
    df = pd.read_csv('data/food_library.csv')
    df['is_custom'] = 0  # Mark as pre-defined (not custom)

    # Insert into database (replace if already exists)
    df.to_sql('food_library', conn, if_exists='replace', index=False)

    conn.close()
    print("✅ Food library loaded!")

# Run this to load all data
if __name__ == "__main__":
    load_exercise_library()
    load_food_library()
    print("✅ All data loaded successfully!")