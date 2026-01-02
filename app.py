import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import hashlib

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
    .login-container {
        max-width: 500px;
        margin: 50px auto;
        padding: 40px;
        background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border: 2px solid #00c6ff;
    }
    .welcome-header {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
    .logout-btn {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        padding: 12px 24px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        border: none;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'users_db' not in st.session_state:
        st.session_state.users_db = {}  # Format: {username: {password, name, age, weight, height, goal, workouts, meals}}
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None

init_session_state()

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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

# LOGIN/REGISTRATION PAGE
if not st.session_state.logged_in:
    st.markdown("<h1 class='welcome-header'>💪 FitTrack Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: #cccccc;'>Your Ultimate Fitness Companion</p>", unsafe_allow_html=True)
    
    # Tabs for Login and Sign Up
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    # LOGIN TAB
    with tab1:
        st.markdown("### 👋 Welcome Back!")
        
        with st.form("login_form"):
            login_username = st.text_input("Username", placeholder="Enter your username")
            login_password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            login_btn = st.form_submit_button("🚀 Login")
            
            if login_btn:
                if login_username in st.session_state.users_db:
                    if st.session_state.users_db[login_username]['password'] == hash_password(login_password):
                        st.session_state.logged_in = True
                        st.session_state.current_user = login_username
                        st.success(f"✅ Welcome back, {st.session_state.users_db[login_username]['name']}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password!")
                else:
                    st.error("❌ Username not found! Please sign up first.")
    
    # SIGN UP TAB
    with tab2:
        st.markdown("### 🎯 Join FitTrack Pro!")
        
        with st.form("signup_form"):
            signup_username = st.text_input("Choose Username", placeholder="Create a unique username")
            signup_password = st.text_input("Choose Password", type="password", placeholder="Create a strong password")
            signup_password_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            
            st.markdown("---")
            st.markdown("#### 👤 Your Details")
            
            signup_name = st.text_input("Full Name", placeholder="Enter your full name")
            col1, col2 = st.columns(2)
            with col1:
                signup_age = st.number_input("Age", min_value=10, max_value=100, value=25)
                signup_weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
            with col2:
                signup_height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
                signup_goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintenance", "General Fitness"])
            
            signup_btn = st.form_submit_button("🎉 Create Account")
            
            if signup_btn:
                # Validation
                if not signup_username or not signup_password or not signup_name:
                    st.error("❌ Please fill all fields!")
                elif signup_password != signup_password_confirm:
                    st.error("❌ Passwords don't match!")
                elif signup_username in st.session_state.users_db:
                    st.error("❌ Username already exists! Please choose another.")
                elif len(signup_password) < 4:
                    st.error("❌ Password must be at least 4 characters!")
                else:
                    # Create new user
                    st.session_state.users_db[signup_username] = {
                        'password': hash_password(signup_password),
                        'name': signup_name,
                        'age': signup_age,
                        'weight': signup_weight,
                        'height': signup_height,
                        'goal': signup_goal,
                        'workouts': [],
                        'meals': []
                    }
                    st.success(f"✅ Account created successfully! Please login with your credentials.")
                    st.balloons()

# MAIN APP (Only accessible after login)
else:
    # Get current user data
    user_data = st.session_state.users_db[st.session_state.current_user]
    
    # Sidebar
    with st.sidebar:
        st.markdown("# 💪 FitTrack Pro")
        st.markdown("### Ultimate Edition")
        
        st.markdown("---")
        
        # User Info
        st.markdown(f"### 👋 Hello, {user_data['name']}!")
        st.markdown(f"**@{st.session_state.current_user}**")
        st.markdown(f"**Goal:** {user_data['goal']}")
        st.markdown(f"**Age:** {user_data['age']} years")
        st.markdown(f"**Weight:** {user_data['weight']} kg")
        st.markdown(f"**Height:** {user_data['height']} cm")
        
        st.markdown("---")
        
        # Logout Button
        if st.button("🚪 Logout", help="Logout and return to login screen"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.success("✅ Logged out successfully!")
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 Your only limit is you!")
    
    # Main Title
    st.markdown(f"<h1 style='text-align: center;'>💪 Welcome back, {user_data['name']}!</h1>", unsafe_allow_html=True)
    
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
    
    # Dashboard
    if menu == "🏠 Dashboard":
        col1, col2, col3, col4 = st.columns(4)
        
        total_workouts = len(user_data['workouts'])
        total_calories = sum([meal['calories'] for meal in user_data['meals']])
        
        with col1:
            st.metric("💪 Total Workouts", total_workouts)
        with col2:
            st.metric("🔥 Calories Consumed", f"{total_calories} kcal")
        with col3:
            st.metric("🎯 Current Weight", f"{user_data['weight']} kg")
        with col4:
            st.metric("📈 Goal", user_data['goal'])
        
        # Recent Activity
        st.markdown("---")
        st.markdown("## 📋 Recent Activity")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💪 Recent Workouts")
            if user_data['workouts']:
                for workout in user_data['workouts'][-5:]:
                    st.markdown(f"**{workout['exercise']}** - {workout['sets']}x{workout['reps']} @ {workout['weight']}kg")
                    st.caption(workout['date'])
            else:
                st.info("No workouts logged yet. Start your journey!")
        
        with col2:
            st.markdown("### 🥗 Recent Meals")
            if user_data['meals']:
                for meal in user_data['meals'][-5:]:
                    st.markdown(f"**{meal['food']}** - {meal['calories']} kcal")
                    st.caption(meal['date'])
            else:
                st.info("No meals logged yet. Start tracking!")
    
    # Workout Plan
    elif menu == "📋 Workout Plan":
        st.markdown("## 💪 Your Personalized Workout Plan")
        
        if user_data['goal'] == "Weight Loss":
            st.markdown("### 🔥 Fat Burning Program")
            st.markdown("**Focus:** High-intensity cardio + moderate strength training")
            st.markdown("""
            **Weekly Plan:**
            - **Monday:** Full Body Strength + 20min Cardio
            - **Tuesday:** HIIT Cardio (30min)
            - **Wednesday:** Upper Body Strength
            - **Thursday:** Active Recovery (Yoga/Stretching)
            - **Friday:** Lower Body Strength + 20min Cardio
            - **Saturday:** Long Cardio Session (45min)
            - **Sunday:** Rest
            """)
        elif user_data['goal'] == "Muscle Gain":
            st.markdown("### 🏋️ Muscle Building Program")
            st.markdown("**Focus:** Heavy compound lifts + progressive overload")
            st.markdown("""
            **Weekly Plan:**
            - **Monday:** Chest & Triceps
            - **Tuesday:** Back & Biceps
            - **Wednesday:** Legs
            - **Thursday:** Rest
            - **Friday:** Shoulders & Arms
            - **Saturday:** Full Body Power
            - **Sunday:** Active Recovery
            """)
        else:
            st.markdown("### 🎯 General Fitness Program")
            st.markdown("**Focus:** Balanced mix of cardio and strength")
            st.markdown("""
            **Weekly Plan:**
            - **Monday:** Full Body Strength
            - **Tuesday:** Cardio (30min)
            - **Wednesday:** Upper Body
            - **Thursday:** Yoga/Flexibility
            - **Friday:** Lower Body
            - **Saturday:** Mixed Cardio & Core
            - **Sunday:** Rest
            """)
    
    # Meal Plan
    elif menu == "🍽️ Meal Plan":
        st.markdown("## 🍽️ Your Personalized Meal Plan")
        
        # Calculate BMR and daily calories
        bmr = 10 * user_data['weight'] + 6.25 * user_data['height'] - 5 * user_data['age'] + 5
        
        if user_data['goal'] == "Weight Loss":
            daily_calories = int(bmr * 1.5 * 0.8)  # 20% deficit
        elif user_data['goal'] == "Muscle Gain":
            daily_calories = int(bmr * 1.7 * 1.15)  # 15% surplus
        else:
            daily_calories = int(bmr * 1.5)
        
        st.markdown(f"### 🎯 Your Daily Target: **{daily_calories} calories**")
        
        st.markdown("""
        **Macronutrient Split:**
        - **Protein:** 30% (Muscle building & repair)
        - **Carbs:** 40% (Energy for workouts)
        - **Fats:** 30% (Hormone regulation)
        """)
        
        protein_g = int(daily_calories * 0.3 / 4)
        carbs_g = int(daily_calories * 0.4 / 4)
        fats_g = int(daily_calories * 0.3 / 9)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🥩 Protein", f"{protein_g}g")
        with col2:
            st.metric("🍚 Carbs", f"{carbs_g}g")
        with col3:
            st.metric("🥑 Fats", f"{fats_g}g")
    
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
            user_data['workouts'].append(workout_data)
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
            user_data['meals'].append(meal_data)
            st.success(f"✅ Logged: {food_item} - {calories} kcal")
    
    # Progress
    elif menu == "📊 Progress":
        st.markdown("## 📊 Your Progress")
        
        tab1, tab2 = st.tabs(["💪 Workouts", "🥗 Nutrition"])
        
        with tab1:
            if user_data['workouts']:
                df_workouts = pd.DataFrame(user_data['workouts'])
                st.markdown(f"### Total Workouts: {len(df_workouts)}")
                st.dataframe(df_workouts, use_container_width=True)
                
                # Workout type distribution
                if len(df_workouts) > 0:
                    fig = px.pie(df_workouts, names='type', title='Workout Type Distribution')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No workout data yet. Start logging your workouts!")
        
        with tab2:
            if user_data['meals']:
                df_meals = pd.DataFrame(user_data['meals'])
                st.markdown(f"### Total Meals Logged: {len(df_meals)}")
                st.markdown(f"### Total Calories: {df_meals['calories'].sum()} kcal")
                st.dataframe(df_meals, use_container_width=True)
                
                # Calorie trend
                if len(df_meals) > 0:
                    fig = px.bar(df_meals, x='date', y='calories', title='Daily Calorie Intake')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No meal data yet. Start tracking your nutrition!")
    
    # Export
    elif menu == "📦 Export":
        st.markdown("## 📦 Export Your Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💪 Workout Data")
            if user_data['workouts']:
                df = pd.DataFrame(user_data['workouts'])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Workouts",
                    data=csv,
                    file_name=f"{st.session_state.current_user}_workouts.csv",
                    mime="text/csv"
                )
                st.success(f"✅ {len(df)} workouts ready to export!")
            else:
                st.warning("No workout data to export!")
        
        with col2:
            st.markdown("### 🥗 Meal Data")
            if user_data['meals']:
                df = pd.DataFrame(user_data['meals'])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Meals",
                    data=csv,
                    file_name=f"{st.session_state.current_user}_meals.csv",
                    mime="text/csv"
                )
                st.success(f"✅ {len(df)} meals ready to export!")
            else:
                st.warning("No meal data to export!")
    
    # Settings
    elif menu == "⚙️ Settings":
        st.markdown("## ⚙️ Settings")
        
        with st.form("update_profile"):
            st.markdown("### Update Your Profile")
            
            new_name = st.text_input("Name", value=user_data['name'])
            
            col1, col2 = st.columns(2)
            with col1:
                new_age = st.number_input("Age", value=user_data['age'])
                new_weight = st.number_input("Weight (kg)", value=float(user_data['weight']))
            with col2:
                new_height = st.number_input("Height (cm)", value=user_data['height'])
                new_goal = st.selectbox("Fitness Goal", 
                                       ["Weight Loss", "Muscle Gain", "Maintenance", "General Fitness"],
                                       index=["Weight Loss", "Muscle Gain", "Maintenance", "General Fitness"].index(user_data['goal']))
            
            if st.form_submit_button("💾 Update Profile"):
                user_data['name'] = new_name
                user_data['age'] = new_age
                user_data['weight'] = new_weight
                user_data['height'] = new_height
                user_data['goal'] = new_goal
                st.success("✅ Profile updated successfully!")
                st.rerun()
        
        st.markdown("---")
        
        # Danger Zone
        st.markdown("### ⚠️ Danger Zone")
        if st.button("🗑️ Delete All My Data", type="secondary"):
            user_data['workouts'] = []
            user_data['meals'] = []
            st.warning("⚠️ All your workout and meal data has been deleted!")
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>💪 FitTrack Pro v5.0 - Instagram-Style Edition | Made with ❤️ by Vinit</p>", unsafe_allow_html=True)
