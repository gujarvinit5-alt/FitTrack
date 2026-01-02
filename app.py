import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go
import random

# Page Configuration
st.set_page_config(
    page_title="FitTrack - Your Fitness Journey",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'selected_food_category' not in st.session_state:
    st.session_state.selected_food_category = None

# ENHANCED Matte Black Theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b3d 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d0d 0%, #1a1a2e 100%);
    }

    p, span, div, label {
        color: #ffffff !important;
    }

    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }

    .motivation-quote {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: white;
        margin: 20px 0;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }

    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        border: none;
        box-shadow: 0 8px 16px rgba(0, 198, 255, 0.3);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(0, 198, 255, 0.5);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        border-left: 5px solid #00c6ff;
    }

    [data-testid="stMetricValue"] {
        font-size: 36px;
        font-weight: bold;
        color: #00c6ff !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 16px;
        color: #cccccc !important;
        font-weight: 600;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: #2a2a2a;
        color: white;
        border: 2px solid #444;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
    }

    .goal-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px 30px;
        border-radius: 25px;
        display: inline-block;
        font-weight: bold;
        font-size: 18px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }

    .section-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 5px solid #00c6ff;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }

    .item-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #353535 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 5px solid #ff6b6b;
        transition: all 0.3s ease;
    }

    .item-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
    }

    .category-badge {
        display: inline-block;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        margin: 5px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
</style>
""", unsafe_allow_html=True)

MOTIVATION_QUOTES = [
    "💪 The only bad workout is the one you didn't do!",
    "🔥 Your body can stand almost anything. It's your mind you have to convince!",
    "⚡ Don't wish for it, work for it!",
    "🎯 Success starts with self-discipline!",
    "💯 The pain you feel today will be the strength you feel tomorrow!",
    "🏆 Make yourself proud!",
    "🌟 Push yourself because no one else is going to do it for you!",
    "💎 Your only limit is you!",
    "🚀 Progress, not perfection!",
    "✨ Believe in yourself and you will be unstoppable!"
]

# Database Functions
def get_db_connection():
    conn = sqlite3.connect("fittrack.db")
    return conn

def check_user_profile():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile WHERE user_id = 1")
    user = cursor.fetchone()
    conn.close()
    return user

def save_user_profile(name, age, weight, height, gender, activity_level, calorie_target, fitness_goal):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE user_profile ADD COLUMN fitness_goal TEXT")
        conn.commit()
    except:
        pass

    cursor.execute("""
        INSERT OR REPLACE INTO user_profile 
        (user_id, name, age, weight, height, gender, activity_level, daily_calorie_target, fitness_goal)
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, age, weight, height, gender, activity_level, calorie_target, fitness_goal))
    conn.commit()
    conn.close()

def calculate_bmr(age, weight, height, gender):
    if gender.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

def calculate_daily_calories(bmr, activity_level, fitness_goal):
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extremely Active": 1.9
    }

    maintenance = int(bmr * activity_multipliers.get(activity_level, 1.2))

    if fitness_goal == "Lose Weight":
        return maintenance - 500
    elif fitness_goal == "Gain Weight (Muscle)":
        return maintenance + 300
    elif fitness_goal == "Get Shredded (Cuts)":
        return maintenance - 700
    else:
        return maintenance

def get_workout_recommendations(fitness_goal):
    workouts = {
        "Lose Weight": {
            "focus": "🔥 Cardio & Fat Burning",
            "exercises": [
                {"name": "Outdoor Running", "sets": "N/A", "reps": "30-40 min", "category": "Cardio", "benefit": "Burns max calories"},
                {"name": "Jump Rope", "sets": "4", "reps": "5 min", "category": "Cardio", "benefit": "High intensity fat burn"},
                {"name": "Burpees", "sets": "4", "reps": "15-20", "category": "Cardio", "benefit": "Full body cardio"},
                {"name": "Cycling", "sets": "N/A", "reps": "30 min", "category": "Cardio", "benefit": "Low impact cardio"},
                {"name": "Mountain Climbers", "sets": "3", "reps": "30", "category": "Core", "benefit": "Core + cardio combo"},
            ],
            "tips": "Do cardio 5-6 days per week. Drink 3-4L water daily. Maintain calorie deficit. Morning cardio works best."
        },
        "Gain Weight (Muscle)": {
            "focus": "💪 Strength & Hypertrophy",
            "exercises": [
                {"name": "Flat Bench Press", "sets": "4", "reps": "8-10", "category": "Chest", "benefit": "Build chest mass"},
                {"name": "Barbell Squats", "sets": "4", "reps": "8-10", "category": "Legs", "benefit": "Build leg mass"},
                {"name": "Deadlifts", "sets": "4", "reps": "6-8", "category": "Back", "benefit": "Overall strength"},
                {"name": "Overhead Press", "sets": "4", "reps": "8-10", "category": "Shoulders", "benefit": "Shoulder mass"},
            ],
            "tips": "Lift heavy 4-5 days per week. Progressive overload is key. Eat 150-200g protein daily. Sleep 8+ hours."
        },
        "Get Shredded (Cuts)": {
            "focus": "⚡ Cardio + Strength Combo",
            "exercises": [
                {"name": "Sprints", "sets": "8", "reps": "30 sec", "category": "Cardio", "benefit": "Fat burning"},
                {"name": "Push-ups", "sets": "4", "reps": "15-20", "category": "Chest", "benefit": "Maintain muscle"},
                {"name": "Pull-ups", "sets": "4", "reps": "8-12", "category": "Back", "benefit": "Upper body definition"},
                {"name": "Planks", "sets": "3", "reps": "60 sec", "category": "Core", "benefit": "Core definition"},
            ],
            "tips": "Train 6 days per week. Mix HIIT with strength. Low carb, high protein. Drink 4L+ water daily."
        },
        "Maintain Weight": {
            "focus": "⚖️ Balanced Training",
            "exercises": [
                {"name": "Barbell Squats", "sets": "3", "reps": "12", "category": "Legs", "benefit": "Leg strength"},
                {"name": "Flat Bench Press", "sets": "3", "reps": "10", "category": "Chest", "benefit": "Upper body"},
                {"name": "Outdoor Running", "sets": "N/A", "reps": "20 min", "category": "Cardio", "benefit": "Cardio health"},
            ],
            "tips": "Train 3-4 days per week. Balance cardio with strength. Eat maintenance calories. Stay consistent."
        }
    }
    return workouts.get(fitness_goal, workouts["Maintain Weight"])

def get_meal_recommendations(fitness_goal, calorie_target):
    meals = {
        "Lose Weight": {
            "focus": "🥗 Low Calorie, High Protein",
            "breakfast": [
                {"food": "Oats", "qty": "1 cup", "cal": 150, "protein": 5, "carbs": 27, "fats": 3},
                {"food": "Egg (Boiled)", "qty": "2 eggs", "cal": 140, "protein": 12, "carbs": 1, "fats": 10},
            ],
            "lunch": [
                {"food": "Chicken Breast (Grilled)", "qty": "150g", "cal": 250, "protein": 45, "carbs": 0, "fats": 5},
                {"food": "Rice (Brown)", "qty": "1/2 cup", "cal": 110, "protein": 3, "carbs": 23, "fats": 1},
            ],
            "dinner": [
                {"food": "Fish (Grilled)", "qty": "100g", "cal": 140, "protein": 25, "carbs": 0, "fats": 5},
                {"food": "Roti (Whole Wheat)", "qty": "2 pieces", "cal": 140, "protein": 5, "carbs": 25, "fats": 3},
            ],
            "snacks": [
                {"food": "Almonds", "qty": "10 nuts", "cal": 70, "protein": 3, "carbs": 3, "fats": 6},
            ],
            "tips": "Eat more protein and less carbs. Avoid sugar and fried foods. Drink water before meals."
        },
        "Gain Weight (Muscle)": {
            "focus": "💪 High Protein, High Calorie",
            "breakfast": [
                {"food": "Omelette (3 eggs)", "qty": "1 serving", "cal": 270, "protein": 18, "carbs": 2, "fats": 20},
                {"food": "Bread (Brown)", "qty": "3 slices", "cal": 210, "protein": 9, "carbs": 36, "fats": 3},
            ],
            "lunch": [
                {"food": "Chicken Curry", "qty": "1 serving", "cal": 250, "protein": 30, "carbs": 10, "fats": 10},
                {"food": "Rice (White)", "qty": "1.5 cups", "cal": 300, "protein": 6, "carbs": 66, "fats": 1},
            ],
            "dinner": [
                {"food": "Mutton Curry", "qty": "1 serving", "cal": 320, "protein": 25, "carbs": 8, "fats": 20},
                {"food": "Rice", "qty": "1 cup", "cal": 200, "protein": 4, "carbs": 44, "fats": 1},
            ],
            "snacks": [
                {"food": "Protein Shake", "qty": "1 serving", "cal": 150, "protein": 25, "carbs": 5, "fats": 3},
            ],
            "tips": "Eat every 3 hours. Consume 150-200g protein daily. Sleep is crucial for growth."
        },
        "Get Shredded (Cuts)": {
            "focus": "⚡ Very Low Calorie, Ultra High Protein",
            "breakfast": [
                {"food": "Egg Whites", "qty": "4 whites", "cal": 70, "protein": 14, "carbs": 1, "fats": 0},
                {"food": "Oats", "qty": "1/2 cup", "cal": 75, "protein": 3, "carbs": 14, "fats": 2},
            ],
            "lunch": [
                {"food": "Chicken Breast", "qty": "200g", "cal": 330, "protein": 60, "carbs": 0, "fats": 7},
                {"food": "Salad", "qty": "1 large bowl", "cal": 50, "protein": 2, "carbs": 10, "fats": 0},
            ],
            "dinner": [
                {"food": "Fish (Grilled)", "qty": "150g", "cal": 210, "protein": 38, "carbs": 0, "fats": 7},
                {"food": "Mixed Veg", "qty": "1 cup", "cal": 120, "protein": 3, "carbs": 15, "fats": 5},
            ],
            "snacks": [
                {"food": "Protein Shake", "qty": "1 serving", "cal": 150, "protein": 25, "carbs": 5, "fats": 3},
            ],
            "tips": "Minimal carbs after 4 PM. 200g+ protein daily. Drink 4-5L water. ZERO cheat meals."
        },
        "Maintain Weight": {
            "focus": "⚖️ Balanced Nutrition",
            "breakfast": [
                {"food": "Idli", "qty": "3 pieces", "cal": 120, "protein": 3, "carbs": 24, "fats": 1},
                {"food": "Egg", "qty": "2 boiled", "cal": 140, "protein": 12, "carbs": 1, "fats": 10},
            ],
            "lunch": [
                {"food": "Dal", "qty": "1 cup", "cal": 180, "protein": 12, "carbs": 30, "fats": 1},
                {"food": "Rice", "qty": "1 cup", "cal": 200, "protein": 4, "carbs": 44, "fats": 1},
            ],
            "dinner": [
                {"food": "Chicken Curry", "qty": "1 serving", "cal": 250, "protein": 30, "carbs": 10, "fats": 10},
                {"food": "Roti", "qty": "2 pieces", "cal": 140, "protein": 5, "carbs": 25, "fats": 3},
            ],
            "snacks": [
                {"food": "Almonds", "qty": "10 nuts", "cal": 70, "protein": 3, "carbs": 3, "fats": 6},
            ],
            "tips": "40% carbs, 30% protein, 30% fats. Balanced meals. Stay consistent."
        }
    }
    return meals.get(fitness_goal, meals["Maintain Weight"])

def get_workout_streak():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT DISTINCT date FROM workout_log ORDER BY date DESC", conn)
    conn.close()

    if df.empty:
        return 0

    streak = 0
    current_date = date.today()

    for i in range(len(df)):
        workout_date = datetime.strptime(df.iloc[i]["date"], "%Y-%m-%d").date()
        expected_date = current_date - timedelta(days=i)

        if workout_date == expected_date:
            streak += 1
        else:
            break

    return streak

def get_weekly_calories_burned():
    conn = get_db_connection()
    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    df = pd.read_sql_query(f"""
        SELECT SUM(calories_burned) as total 
        FROM workout_log 
        WHERE date >= '{week_start.strftime("%Y-%m-%d")}'
    """, conn)
    conn.close()
    return int(df['total'][0]) if df['total'][0] else 0

# Sidebar Navigation
st.sidebar.title("💪 FitTrack Pro")
st.sidebar.markdown("---")
st.sidebar.info(random.choice(MOTIVATION_QUOTES))
st.sidebar.markdown("---")

user_profile = check_user_profile()

if user_profile is None:
    page = "Setup Profile"
else:
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Dashboard", "💡 Workout Plan", "🍽️ Meal Plan", "🏋️ Log Workout", "🥗 Log Diet", 
         "📊 Progress", "📥 Export", "⚙️ Settings"]
    )

# REGISTRATION PAGE with CLICKABLE GOAL CARDS
if user_profile is None or page == "⚙️ Settings":
    st.markdown("<h1 style='text-align: center; font-size: 48px;'>🏋️ Welcome to FitTrack Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: #00c6ff;'>Your Ultimate Fitness Companion</p>", unsafe_allow_html=True)

    quote = random.choice(MOTIVATION_QUOTES)
    st.markdown(f"<div class='motivation-quote'>{quote}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Initialize goal in session state
    if 'selected_goal' not in st.session_state:
        st.session_state.selected_goal = "Lose Weight"

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("📝 Full Name", value=user_profile[1] if user_profile else "", placeholder="Enter your name")
        age = st.number_input("🎂 Age", min_value=15, max_value=100, value=int(user_profile[2]) if user_profile else 25)
        weight = st.number_input("⚖️ Current Weight (kg)", min_value=30.0, max_value=200.0, 
                                value=float(user_profile[3]) if user_profile else 70.0, step=0.5)

    with col2:
        height = st.number_input("📏 Height (cm)", min_value=100.0, max_value=250.0, 
                                value=float(user_profile[4]) if user_profile else 170.0, step=0.5)
        gender = st.selectbox("⚧️ Gender", ["Male", "Female"], 
                             index=0 if (user_profile and user_profile[5]=="Male") else 0)
        activity_level = st.selectbox(
            "🏃 Activity Level",
            ["Sedentary (Little/no exercise)", 
             "Lightly Active (1-3 days/week)", 
             "Moderately Active (3-5 days/week)", 
             "Very Active (6-7 days/week)", 
             "Extremely Active (Athlete)"],
            index=2
        )

    activity_map = {
        "Sedentary (Little/no exercise)": "Sedentary",
        "Lightly Active (1-3 days/week)": "Lightly Active",
        "Moderately Active (3-5 days/week)": "Moderately Active",
        "Very Active (6-7 days/week)": "Very Active",
        "Extremely Active (Athlete)": "Extremely Active"
    }
    activity_clean = activity_map[activity_level]

    st.markdown("---")
    st.markdown("### 🎯 Your Fitness Goal")
    st.markdown("<p style='text-align: center;'>Click on a goal below:</p>", unsafe_allow_html=True)

    # CLICKABLE GOAL BUTTONS - FIXED SYNTAX
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔥 Lose Weight", use_container_width=True, key="goal_lose"):
            st.session_state.selected_goal = "Lose Weight"

    with col2:
        if st.button("💪 Gain Muscle", use_container_width=True, key="goal_gain"):
            st.session_state.selected_goal = "Gain Weight (Muscle)"

    with col3:
        if st.button("⚡ Get Shredded", use_container_width=True, key="goal_shred"):
            st.session_state.selected_goal = "Get Shredded (Cuts)"

    with col4:
        if st.button("⚖️ Maintain", use_container_width=True, key="goal_maintain"):
            st.session_state.selected_goal = "Maintain Weight"

    # Show selected goal
    st.success(f"✅ Selected Goal: **{st.session_state.selected_goal}**")

    goal_descriptions = {
        "Lose Weight": "🔥 Focus: Cardio + 500 cal deficit | Lose 0.5-1 kg/week",
        "Gain Weight (Muscle)": "💪 Focus: Strength + 300 cal surplus | Gain 0.5 kg/week",
        "Get Shredded (Cuts)": "⚡ Focus: HIIT + 700 cal deficit | Maximum definition",
        "Maintain Weight": "⚖️ Focus: Balanced training + maintenance calories"
    }
    st.info(goal_descriptions[st.session_state.selected_goal])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Start Your Journey", use_container_width=True):
        if name:
            bmr = calculate_bmr(age, weight, height, gender)
            calorie_target = calculate_daily_calories(bmr, activity_clean, st.session_state.selected_goal)
            save_user_profile(name, age, weight, height, gender, activity_clean, calorie_target, st.session_state.selected_goal)
            st.success(f"✅ Welcome {name}! Daily target: {calorie_target} calories")
            st.balloons()
            st.rerun()
        else:
            st.error("⚠️ Please enter your name")

# DASHBOARD
elif page == "🏠 Dashboard":
    try:
        fitness_goal = user_profile[8] if len(user_profile) > 8 else "Maintain Weight"
    except:
        fitness_goal = "Maintain Weight"

    st.markdown(f"<h1 style='text-align: center;'>🏠 Welcome back, {user_profile[1]}!</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='goal-badge' style='text-align: center; display: block;'>🎯 Goal: {fitness_goal}</div>", unsafe_allow_html=True)

    daily_quote = random.choice(MOTIVATION_QUOTES)
    st.markdown(f"<div class='motivation-quote'>{daily_quote}</div>", unsafe_allow_html=True)

    st.markdown(f"<p style='text-align: center; font-size: 18px;'>📅 {date.today().strftime('%A, %B %d, %Y')}</p>", unsafe_allow_html=True)

    st.markdown("---")

    today_str = date.today().strftime("%Y-%m-%d")
    conn = get_db_connection()

    today_workout = pd.read_sql_query(f"SELECT COUNT(*) as count FROM workout_log WHERE date = '{today_str}'", conn)
    today_calories = pd.read_sql_query(f"SELECT SUM(calories) as total FROM diet_log WHERE date = '{today_str}'", conn)

    conn.close()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        workout_done = "✅ Done" if today_workout["count"][0] > 0 else "❌ Pending"
        st.metric("🏋️ Today's Workout", workout_done)

    with col2:
        calories_consumed = int(today_calories["total"][0]) if today_calories["total"][0] else 0
        calorie_target = user_profile[7]
        remaining = calorie_target - calories_consumed
        st.metric("🍽️ Calories", f"{calories_consumed}/{calorie_target}", 
                 f"{remaining} remaining" if remaining > 0 else f"{abs(remaining)} over")

    with col3:
        streak = get_workout_streak()
        st.metric("🔥 Workout Streak", f"{streak} days")

    with col4:
        weekly_cal = get_weekly_calories_burned()
        st.metric("⚡ Weekly Burn", f"{weekly_cal} cal")

# WORKOUT PLAN
elif page == "💡 Workout Plan":
    try:
        fitness_goal = user_profile[8] if len(user_profile) > 8 else "Maintain Weight"
    except:
        fitness_goal = "Maintain Weight"

    st.markdown(f"<h1 style='text-align: center;'>💡 Your Personalized Workout Plan</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='goal-badge' style='text-align: center; display: block;'>🎯 Goal: {fitness_goal}</div>", unsafe_allow_html=True)

    plan = get_workout_recommendations(fitness_goal)

    st.markdown(f"<div class='section-card'><h2>{plan['focus']}</h2></div>", unsafe_allow_html=True)
    st.info(f"💡 **Expert Tips:** {plan['tips']}")

    st.markdown("### 📋 Recommended Exercises")

    for i, exercise in enumerate(plan['exercises'], 1):
        st.markdown(f"""
        <div class='item-card'>
            <h3>{i}. {exercise['name']} <span class='category-badge'>{exercise['category']}</span></h3>
            <p><strong>📊 Sets:</strong> {exercise['sets']} | <strong>🔢 Reps:</strong> {exercise['reps']}</p>
            <p style='color: #00c6ff;'><strong>✨ Benefit:</strong> {exercise['benefit']}</p>
        </div>
        """, unsafe_allow_html=True)

# MEAL PLAN
elif page == "🍽️ Meal Plan":
    try:
        fitness_goal = user_profile[8] if len(user_profile) > 8 else "Maintain Weight"
    except:
        fitness_goal = "Maintain Weight"

    calorie_target = user_profile[7]

    st.markdown(f"<h1 style='text-align: center;'>🍽️ Your Personalized Meal Plan</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='goal-badge' style='text-align: center; display: block;'>🎯 {fitness_goal} | Target: {calorie_target} cal</div>", unsafe_allow_html=True)

    plan = get_meal_recommendations(fitness_goal, calorie_target)

    st.markdown(f"<div class='section-card'><h2>{plan['focus']}</h2></div>", unsafe_allow_html=True)
    st.info(f"💡 **Tips:** {plan['tips']}")

    st.markdown("### 🌅 Breakfast")
    for item in plan['breakfast']:
        st.markdown(f"- **{item['food']}** ({item['qty']}) - {item['cal']} cal | P: {item['protein']}g | C: {item['carbs']}g | F: {item['fats']}g")

    st.markdown("### ☀️ Lunch")
    for item in plan['lunch']:
        st.markdown(f"- **{item['food']}** ({item['qty']}) - {item['cal']} cal | P: {item['protein']}g | C: {item['carbs']}g | F: {item['fats']}g")

    st.markdown("### 🌙 Dinner")
    for item in plan['dinner']:
        st.markdown(f"- **{item['food']}** ({item['qty']}) - {item['cal']} cal | P: {item['protein']}g | C: {item['carbs']}g | F: {item['fats']}g")

# LOG WORKOUT - WITH REACTIVE DROPDOWN OUTSIDE FORM
elif page == "🏋️ Log Workout":
    st.markdown("<h1 style='text-align: center;'>🏋️ Log Your Workout</h1>", unsafe_allow_html=True)

    conn = get_db_connection()
    exercises_df = pd.read_sql_query("SELECT * FROM exercise_library", conn)
    conn.close()

    if exercises_df.empty:
        st.error("❌ No exercises found. Please update exercise library.")
    else:
        categories = sorted(exercises_df["category"].unique())

        # OUTSIDE FORM - This allows reactive updates!
        st.markdown("### 💪 Step 1: Select Exercise Category")
        selected_category = st.selectbox("Choose Category", categories, key="workout_category")

        # Filter exercises
        category_exercises = exercises_df[exercises_df["category"] == selected_category]
        exercise_list = sorted(category_exercises["exercise_name"].tolist())

        st.caption(f"📊 {len(exercise_list)} exercises available in **{selected_category}**")

        st.markdown("### 🎯 Step 2: Select Exercise")
        selected_exercise = st.selectbox("Choose Exercise", exercise_list, key="workout_exercise")

        # NOW USE FORM for submission only
        with st.form("workout_form"):
            workout_date = st.date_input("📅 Workout Date", value=date.today())

            exercise_info = exercises_df[exercises_df["exercise_name"] == selected_exercise].iloc[0]

            st.markdown("### 📊 Step 3: Enter Details")

            col1, col2, col3 = st.columns(3)

            with col1:
                sets = st.number_input("📊 Sets", min_value=1, max_value=20, value=3)
            with col2:
                reps = st.number_input("🔢 Reps", min_value=1, max_value=100, value=10)
            with col3:
                duration = st.number_input("⏱️ Duration (min)", min_value=1, max_value=180, value=15)

            intensity = st.select_slider("💥 Intensity", 
                                        options=["Light", "Moderate", "Heavy"], 
                                        value="Moderate")

            base_calories = exercise_info["calories_per_min"] * duration
            intensity_multiplier = {"Light": 0.8, "Moderate": 1.0, "Heavy": 1.2}
            calories_burned = int(base_calories * intensity_multiplier[intensity])

            st.success(f"🔥 Estimated Calories: {calories_burned} cal")

            notes = st.text_area("📝 Notes", placeholder="How did you feel?")

            submitted = st.form_submit_button("💾 Save Workout", use_container_width=True)

            if submitted:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO workout_log 
                    (date, exercise_name, category, sets, reps, duration_mins, intensity, calories_burned, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (workout_date.strftime("%Y-%m-%d"), selected_exercise, selected_category, 
                      sets, reps, duration, intensity, calories_burned, notes))
                conn.commit()
                conn.close()

                st.success("✅ Workout logged! 💪")
                st.balloons()

# LOG DIET - WITH REACTIVE DROPDOWN OUTSIDE FORM
elif page == "🥗 Log Diet":
    st.markdown("<h1 style='text-align: center;'>🥗 Log Your Meal</h1>", unsafe_allow_html=True)

    try:
        fitness_goal = user_profile[8] if len(user_profile) > 8 else "Maintain Weight"
    except:
        fitness_goal = "Maintain Weight"

    with st.expander("📋 View Recommended Meal Plan"):
        calorie_target = user_profile[7]
        plan = get_meal_recommendations(fitness_goal, calorie_target)
        st.info(f"**{plan['focus']}** - {plan['tips']}")

    st.markdown("---")

    conn = get_db_connection()
    foods_df = pd.read_sql_query("SELECT * FROM food_library ORDER BY food_name", conn)

    food_categories = {
        "🍞 Grains & Breads": ["Roti", "Rice", "Bread", "Paratha", "Idli", "Dosa"],
        "🥘 Curries & Dals": ["Dal", "Rajma", "Chole", "Chicken Curry", "Fish Curry"],
        "🥩 Proteins": ["Paneer", "Chicken", "Fish", "Egg", "Omelette"],
        "🥗 Vegetables": ["Aloo", "Mixed Veg", "Salad"],
        "🍎 Fruits": ["Banana", "Apple", "Mango"],
        "🥜 Nuts": ["Almonds", "Cashews", "Peanuts"],
        "🥤 Beverages": ["Milk", "Curd", "Tea"],
        "➕ Manual Entry": []
    }

    # OUTSIDE FORM for reactive dropdown
    st.markdown("### 🎨 Step 1: Select Category")
    selected_food_category = st.selectbox("Choose Category", list(food_categories.keys()), key="food_category")

    # NOW USE FORM
    with st.form("diet_form"):
        diet_date = st.date_input("📅 Date", value=date.today())
        meal_type = st.selectbox("🍴 Meal Type", ["🌅 Breakfast", "☀️ Lunch", "🌙 Dinner", "🍪 Snacks"])
        meal_type_clean = meal_type.split()[1]

        if selected_food_category == "➕ Manual Entry":
            st.markdown("### ✍️ Enter Custom Food")
            food_item = st.text_input("🏷️ Food Name", placeholder="e.g., Homemade Pasta")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                calories = st.number_input("🔥 Calories", min_value=0, value=100)
            with col2:
                protein = st.number_input("🥩 Protein (g)", min_value=0.0, value=0.0)
            with col3:
                carbs = st.number_input("🍞 Carbs (g)", min_value=0.0, value=0.0)
            with col4:
                fats = st.number_input("🧈 Fats (g)", min_value=0.0, value=0.0)

            add_to_library = st.checkbox("💾 Save to library", value=True)
        else:
            keywords = food_categories[selected_food_category]
            filtered_foods = []

            for keyword in keywords:
                matching = foods_df[foods_df["food_name"].str.contains(keyword, case=False, na=False)]["food_name"].tolist()
                filtered_foods.extend(matching)

            filtered_foods = sorted(list(set(filtered_foods)))

            if filtered_foods:
                st.caption(f"📊 {len(filtered_foods)} foods in **{selected_food_category}**")

                st.markdown("### 🥘 Step 2: Select Food")
                selected_food = st.selectbox("Choose Food", filtered_foods, key="food_item")

                food_info = foods_df[foods_df["food_name"] == selected_food].iloc[0]
                food_item = selected_food

                st.markdown("### 📊 Nutrition Info")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🔥 Calories", int(food_info["calories"]))
                with col2:
                    st.metric("🥩 Protein", f"{food_info['protein']}g")
                with col3:
                    st.metric("🍞 Carbs", f"{food_info['carbs']}g")
                with col4:
                    st.metric("🧈 Fats", f"{food_info['fats']}g")

                calories = int(food_info["calories"])
                protein = float(food_info["protein"])
                carbs = float(food_info["carbs"])
                fats = float(food_info["fats"])
                add_to_library = False
            else:
                st.warning(f"⚠️ No foods in '{selected_food_category}'")
                food_item = ""
                calories = protein = carbs = fats = 0
                add_to_library = False

        submitted = st.form_submit_button("✅ Add to Diet Log", use_container_width=True)

        if submitted and food_item:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO diet_log 
                (date, meal_type, food_item, calories, protein, carbs, fats)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (diet_date.strftime("%Y-%m-%d"), meal_type_clean, food_item, calories, protein, carbs, fats))
            conn.commit()

            if selected_food_category == "➕ Manual Entry" and add_to_library:
                cursor.execute("""
                    INSERT OR IGNORE INTO food_library 
                    (food_name, serving_size, calories, protein, carbs, fats, is_custom)
                    VALUES (?, ?, ?, ?, ?, ?, 1)
                """, (food_item, "Custom", calories, protein, carbs, fats))
                conn.commit()
                st.success(f"✅ Logged and saved '{food_item}' to library! 🎉")
            else:
                st.success("✅ Meal logged successfully! 🥗")

            st.balloons()

    conn.close()

# PROGRESS
elif page == "📊 Progress":
    st.markdown("<h1 style='text-align: center;'>📊 Your Progress</h1>", unsafe_allow_html=True)

    date_range = st.selectbox("📅 Period", ["Last 7 Days", "Last 30 Days"])
    days = 7 if date_range == "Last 7 Days" else 30
    start_date = date.today() - timedelta(days=days)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = date.today().strftime("%Y-%m-%d")

    conn = get_db_connection()

    workouts_df = pd.read_sql_query(f"""
        SELECT date, COUNT(*) as workout_count
        FROM workout_log 
        WHERE date BETWEEN '{start_str}' AND '{end_str}'
        GROUP BY date
    """, conn)

    diet_df = pd.read_sql_query(f"""
        SELECT date, SUM(calories) as total_calories 
        FROM diet_log 
        WHERE date BETWEEN '{start_str}' AND '{end_str}'
        GROUP BY date
    """, conn)

    conn.close()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💪 Total Workouts", len(workouts_df) if not workouts_df.empty else 0)
    with col2:
        avg = int(diet_df["total_calories"].mean()) if not diet_df.empty else 0
        st.metric("🍽️ Avg Calories", avg)
    with col3:
        st.metric("🔥 Streak", f"{get_workout_streak()} days")

    if not workouts_df.empty:
        fig = px.bar(workouts_df, x="date", y="workout_count", title="Workout Frequency")
        st.plotly_chart(fig, use_container_width=True)

# EXPORT
elif page == "📥 Export":
    st.markdown("<h1 style='text-align: center;'>📥 Export Reports</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        export_start = st.date_input("📅 From", value=date.today() - timedelta(days=30))
    with col2:
        export_end = st.date_input("📅 To", value=date.today())

    start_str = export_start.strftime("%Y-%m-%d")
    end_str = export_end.strftime("%Y-%m-%d")

    conn = get_db_connection()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 Export Workouts", use_container_width=True):
            df = pd.read_sql_query(f"""
                SELECT * FROM workout_log 
                WHERE date BETWEEN '{start_str}' AND '{end_str}'
            """, conn)
            if not df.empty:
                csv = df.to_csv(index=False)
                st.download_button("⬇️ Download", csv, f"workouts_{start_str}.csv", "text/csv")
            else:
                st.warning("⚠️ No data found")

    with col2:
        if st.button("🍽️ Export Diet", use_container_width=True):
            df = pd.read_sql_query(f"""
                SELECT * FROM diet_log 
                WHERE date BETWEEN '{start_str}' AND '{end_str}'
            """, conn)
            if not df.empty:
                csv = df.to_csv(index=False)
                st.download_button("⬇️ Download", csv, f"diet_{start_str}.csv", "text/csv")
            else:
                st.warning("⚠️ No data found")

    conn.close()

st.sidebar.markdown("---")
st.sidebar.markdown("**💪 FitTrack Pro v4.0**")
st.sidebar.markdown("*Ultimate Edition*")