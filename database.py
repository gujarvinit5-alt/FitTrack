import sqlite3
import pandas as pd
from datetime import datetime
def create_database():
    '''Creates the SQLite database and all tables'''

    # Connect to database (creates fittrack.db file if it doesn't exist)
    conn = sqlite3.connect('fittrack.db')
    cursor = conn.cursor()

    # Table 1: User Profile (your personal info)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profile (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        weight REAL,
        height REAL,
        gender TEXT,
        activity_level TEXT,
        daily_calorie_target INTEGER
    )
    ''')

    # Table 2: Workout Log (stores every workout you do)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS workout_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        exercise_name TEXT,
        category TEXT,
        sets INTEGER,
        reps INTEGER,
        duration_mins INTEGER,
        intensity TEXT,
        calories_burned INTEGER,
        notes TEXT
    )
    ''')

    # Table 3: Diet Log (stores every meal you eat)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diet_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        meal_type TEXT,
        food_item TEXT,
        calories INTEGER,
        protein REAL,
        carbs REAL,
        fats REAL
    )
    ''')

    # Table 4: Exercise Library (pre-defined exercises)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercise_library (
        exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise_name TEXT UNIQUE,
        category TEXT,
        calories_per_min REAL,
        description TEXT
    )
    ''')

    # Table 5: Food Library (pre-defined foods + your custom additions)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_library (
        food_id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_name TEXT UNIQUE,
        serving_size TEXT,
        calories INTEGER,
        protein REAL,
        carbs REAL,
        fats REAL,
        is_custom INTEGER DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database created successfully!")

def calculate_bmr(age, weight, height, gender):
    '''Calculate Basal Metabolic Rate using Harris-Benedict equation'''
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

def calculate_daily_calories(bmr, activity_level):
    '''Calculate daily calorie target based on activity level'''
    activity_multipliers = {
        'Sedentary': 1.2,
        'Lightly Active': 1.375,
        'Moderately Active': 1.55,
        'Very Active': 1.725,
        'Extremely Active': 1.9
    }
    return int(bmr * activity_multipliers.get(activity_level, 1.2))

# Run this function to create the database
if __name__ == "__main__":
    create_database()