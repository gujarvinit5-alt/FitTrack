import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="FitTrack Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
        border-left: 5px solid #ffb6b6;
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
    .section-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #353535 100%);
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
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    .item-card:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
    }
    .category-badge {
        display: inline-block;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);
    }
    .goal-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px 30px;
        border-radius: 25px;
        display: inline-block;
        font-weight: bold;
        font-size: 18px;
        margin: 15px 0;
        color: white !important;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'user_registered' not in st.session_state:
        st.session_state.user_registered = False
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'user_age' not in st.session_state:
        st.session_state.user_age = 0
    if 'user_weight' not in st.session_state:
        st.session_state.user_weight = 0
    if 'user_height' not in st.session_state:
        st.session_state.user_height = 0
    if 'fitness_goal' not in st.session_state:
        st.session_state.fitness_goal = ""
    if 'workouts' not in st.session_state:
        st.session_state.workouts = []
    if 'meals' not in st.session_state:
        st.session_state.meals = []

init_session_state()

# Workout and Food Data
WORKOUT_LIBRARY = {
    "Strength Training": {
        "Chest": ["Bench Press", "Push-ups", "Dumbbell Flyes", "Cable Crossover"],
        "Back": ["Pull-ups", "Deadlift", "Bent Over Rows", "Lat Pulldown"],
        "Legs": ["Squats", "Leg Press", "Lunges", "Leg Curls", "Calf Raises"],
        "Shoulders": ["Overhead Press", "Lateral Raises", "Front Raises", "Shrugs"],
        "Arms": ["Bicep Curls", "Tricep Dips", "Hammer Curls", "Skull Crushers"],
        "Core": ["Planks", "Russian Twists", "Leg Raises", "Mountain Climbers"]
    },
    "Cardio": {
        "Running": ["Treadmill Run", "Outdoor Run", "Sprint Intervals", "Hill Running"],
        "Cycling": ["Stationary Bike", "Outdoor Cycling", "Spin Class"],
        "Other": ["Jump Rope", "Rowing", "Elliptical", "Swimming", "Stairs"]
    },
    "Flexibility": {
        "Yoga": ["Hatha Yoga", "Vinyasa Flow", "Power Yoga", "Yin Yoga"],
        "Stretching": ["Full Body Stretch", "Lower Body Stretch", "Upper Body Stretch"],
        "Mobility": ["Hip Mobility", "Shoulder Mobility", "Ankle Mobility"]
    }
}

FOOD_DATABASE = {
    "Proteins": {
        "Chicken Breast (100g)": 165,
        "Salmon (100g)": 208,
        "Eggs (2 large)": 140,
        "Greek Yogurt (100g)": 59,
        "Tofu (100g)": 76,
        "Protein Shake": 120,
        "Tuna (100g)": 132,
        "Turkey (100g)": 135
    },
    "Carbs": {
        "Rice (100g)": 130,
        "Oats (100g)": 389,
        "Whole Wheat Bread (2 slices)": 160,
        "Sweet Potato (100g)": 86,
        "Quinoa (100g)": 120,
        "Pasta (100g)": 131,
        "Banana (1 medium)": 105
    },
    "Vegetables": {
        "Broccoli (100g)": 34,
        "Spinach (100g)": 23,
        "Carrots (100g)": 41,
        "Bell Peppers (100g)": 31,
        "Tomatoes (100g)": 18,
        "Cucumber (100g)": 16
    },
    "Fats": {
        "Avocado (100g)": 160,
        "Almonds (30g)": 170,
        "Peanut Butter (2 tbsp)": 190,
        "Olive Oil (1 tbsp)": 119,
        "Cheese (30g)": 113
    },
    "Snacks": {
        "Apple (1 medium)": 95,
        "Protein Bar": 200,
        "Trail Mix (30g)": 150,
        "Dark Chocolate (30g)": 170
    }
}

# Sidebar with Reset Button
with st.sidebar:
    st.markdown("# 💪 FitTrack Pro")
    st.markdown("### Ultimate Edition")
    
    st.markdown("---")
    
    # User Controls Section
    st.markdown("### 👤 User Controls")
    
    if st.button("🔄 New User / Reset", help="Clear all data and start fresh"):
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("✅ Data cleared! Please register as new user.")
        st.rerun()
    
    st.markdown("---")
    
    # Show user info if registered
    if st.session_state.user_registered:
        st.markdown(f"### 👋 Hello, {st.session_state.user_name}!")
        st.markdown(f"**Goal:** {st.session_state.fitness_goal}")
        st.markdown(f"**Age:** {st.session_state.user_age} years")
        st.markdown(f"**Weight:** {st.session_state.user_weight} kg")
        st.markdown(f"**Height:** {st.session_state.user_height} cm")
    
    st.markdown("---")
    st.markdown("### 💡 Your only limit is you!")

# Main Title
st.markdown("<h1 style='text-align: center;'>💪 Welcome back, Vinit Gujar!</h1>", unsafe_allow_html=True)

# Motivational Quote
motivation_quotes = [
    "The only bad workout is the one that didn't happen! 💪",
    "Your body can stand almost anything. It's your mind you have to convince! 🧠",
    "Don't wish for it, work for it! 🔥",
    "Sweat is fat crying! 💦",
    "The pain you feel today will be the strength you feel tomorrow! ⚡"
]
st.markdown(f"<div class='motivation-quote'>🔥 {motivation_quotes[datetime.now().day % len(motivation_quotes)]}</div>", unsafe_allow_html=True)

# Navigation
menu = st.sidebar.radio("Navigation", 
                       ["🏠 Dashboard", "📋 Workout Plan", "🍽️ Meal Plan", 
                        "💪 Log Workout", "🥗 Log Diet", "📊 Progress", 
                        "📦 Export", "⚙️ Settings"])

# Registration Page (only if not registered)
if not st.session_state.user_registered:
    st.markdown("## 👤 User Registration")
    st.markdown("### Please register to start your fitness journey!")
    
    with st.form("registration_form"):
        name = st.text_input("Full Name", placeholder="Enter your name")
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintenance", "General Fitness"])
        
        submit = st.form_submit_button("🚀 Start My Journey!")
        
        if submit and name:
            st.session_state.user_registered = True
            st.session_state.user_name = name
            st.session_state.user_age = age
            st.session_state.user_weight = weight
            st.session_state.user_height = height
            st.session_state.fitness_goal = goal
            st.success(f"✅ Welcome aboard, {name}! Let's achieve your {goal} goal!")
            st.balloons()
            st.rerun()
        elif submit:
            st.error("❌ Please enter your name!")

# Dashboard
elif menu == "🏠 Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    
    total_workouts = len(st.session_state.workouts)
    total_calories = sum([meal['calories'] for meal in st.session_state.meals])
    
    with col1:
        st.metric("💪 Total Workouts", total_workouts)
    with col2:
        st.metric("🔥 Calories Consumed", f"{total_calories} kcal")
    with col3:
        st.metric("🎯 Current Weight", f"{st.session_state.user_weight} kg")
    with col4:
        st.metric("📈 Goal", st.session_state.fitness_goal)

# Workout Plan
elif menu == "📋 Workout Plan":
    st.markdown("## 💪 Your Personalized Workout Plan")
    
    if st.session_state.fitness_goal == "Weight Loss":
        st.markdown("### 🔥 Fat Burning Program")
        st.markdown("**Focus:** High-intensity cardio + moderate strength training")
    elif st.session_state.fitness_goal == "Muscle Gain":
        st.markdown("### 🏋️ Muscle Building Program")
        st.markdown("**Focus:** Heavy compound lifts + progressive overload")
    else:
        st.markdown("### 🎯 General Fitness Program")
        st.markdown("**Focus:** Balanced mix of cardio and strength")

# Log Workout
elif menu == "💪 Log Workout":
    st.markdown("## 💪 Log Your Workout")
    
    workout_type = st.selectbox("Workout Type", list(WORKOUT_LIBRARY.keys()))
    category = st.selectbox("Category", list(WORKOUT_LIBRARY[workout_type].keys()))
    exercise = st.selectbox("Exercise", WORKOUT_LIBRARY[workout_type][category])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sets = st.number_input("Sets", min_value=1, max_value=10, value=3)
    with col2:
        reps = st.number_input("Reps", min_value=1, max_value=50, value=10)
    with col3:
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, value=0.0, step=2.5)
    
    if st.button("✅ Log Workout"):
        workout_data = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'type': workout_type,
            'category': category,
            'exercise': exercise,
            'sets': sets,
            'reps': reps,
            'weight': weight
        }
        st.session_state.workouts.append(workout_data)
        st.success(f"✅ Logged: {exercise} - {sets}x{reps} @ {weight}kg")
        st.balloons()

# Log Diet
elif menu == "🥗 Log Diet":
    st.markdown("## 🥗 Log Your Meal")
    
    food_category = st.selectbox("Food Category", list(FOOD_DATABASE.keys()))
    food_item = st.selectbox("Food Item", list(FOOD_DATABASE[food_category].keys()))
    quantity = st.number_input("Quantity (servings)", min_value=0.5, max_value=10.0, value=1.0, step=0.5)
    
    calories = int(FOOD_DATABASE[food_category][food_item] * quantity)
    
    st.info(f"📊 Estimated Calories: **{calories} kcal**")
    
    if st.button("✅ Log Meal"):
        meal_data = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'category': food_category,
            'food': food_item,
            'quantity': quantity,
            'calories': calories
        }
        st.session_state.meals.append(meal_data)
        st.success(f"✅ Logged: {food_item} - {calories} kcal")

# Progress
elif menu == "📊 Progress":
    st.markdown("## 📊 Your Progress")
    
    if st.session_state.workouts:
        df_workouts = pd.DataFrame(st.session_state.workouts)
        st.markdown("### 💪 Workout History")
        st.dataframe(df_workouts, use_container_width=True)
    
    if st.session_state.meals:
        df_meals = pd.DataFrame(st.session_state.meals)
        st.markdown("### 🥗 Meal History")
        st.dataframe(df_meals, use_container_width=True)

# Export
elif menu == "📦 Export":
    st.markdown("## 📦 Export Your Data")
    
    if st.button("📥 Download Workout Data"):
        if st.session_state.workouts:
            df = pd.DataFrame(st.session_state.workouts)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "workouts.csv", "text/csv")
        else:
            st.warning("No workout data to export!")
    
    if st.button("📥 Download Meal Data"):
        if st.session_state.meals:
            df = pd.DataFrame(st.session_state.meals)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "meals.csv", "text/csv")
        else:
            st.warning("No meal data to export!")

# Settings
elif menu == "⚙️ Settings":
    st.markdown("## ⚙️ Settings")
    
    with st.form("update_profile"):
        st.markdown("### Update Your Profile")
        new_weight = st.number_input("Weight (kg)", value=float(st.session_state.user_weight))
        new_goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintenance", "General Fitness"],
                               index=["Weight Loss", "Muscle Gain", "Maintenance", "General Fitness"].index(st.session_state.fitness_goal))
        
        if st.form_submit_button("💾 Update Profile"):
            st.session_state.user_weight = new_weight
            st.session_state.fitness_goal = new_goal
            st.success("✅ Profile updated successfully!")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>💪 FitTrack Pro v4.0 - Ultimate Edition | Made with ❤️ for fitness enthusiasts</p>", unsafe_allow_html=True)
