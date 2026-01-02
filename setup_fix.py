import os
import pandas as pd

# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')
    print("✅ Created 'data' folder")

# Create exercise_library.csv
exercise_data = {
    'exercise_name': ['Push-ups', 'Bench Press', 'Dumbbell Press', 'Cable Flys', 'Incline Bench Press',
                      'Pull-ups', 'Lat Pulldown', 'Barbell Rows', 'Deadlifts', 'Seated Cable Rows', 'T-Bar Rows',
                      'Squats', 'Lunges', 'Leg Press', 'Leg Curls', 'Leg Extensions', 'Calf Raises', 'Romanian Deadlifts',
                      'Overhead Press', 'Lateral Raises', 'Front Raises', 'Rear Delt Flys', 'Shrugs',
                      'Bicep Curls', 'Tricep Extensions', 'Hammer Curls', 'Tricep Dips', 'Cable Curls',
                      'Planks', 'Crunches', 'Russian Twists', 'Leg Raises', 'Mountain Climbers', 'Bicycle Crunches',
                      'Treadmill', 'Cycling', 'Elliptical', 'Jump Rope', 'Burpees', 'Running', 'Walking', 
                      'Stair Climber', 'Rowing Machine', 'Boxing', 'Swimming'],
    'category': ['Chest', 'Chest', 'Chest', 'Chest', 'Chest',
                 'Back', 'Back', 'Back', 'Back', 'Back', 'Back',
                 'Legs', 'Legs', 'Legs', 'Legs', 'Legs', 'Legs', 'Legs',
                 'Shoulders', 'Shoulders', 'Shoulders', 'Shoulders', 'Shoulders',
                 'Arms', 'Arms', 'Arms', 'Arms', 'Arms',
                 'Core', 'Core', 'Core', 'Core', 'Core', 'Core',
                 'Cardio', 'Cardio', 'Cardio', 'Cardio', 'Cardio', 'Cardio', 'Cardio',
                 'Cardio', 'Cardio', 'Cardio', 'Cardio'],
    'calories_per_min': [7, 8, 7, 6, 8,
                         8, 7, 8, 9, 7, 8,
                         8, 7, 7, 5, 5, 4, 8,
                         7, 5, 5, 5, 5,
                         5, 5, 5, 7, 5,
                         6, 5, 6, 6, 9, 6,
                         10, 8, 9, 12, 11, 11, 4,
                         9, 10, 11, 10],
    'description': ['Bodyweight chest exercise', 'Barbell chest press', 'Dumbbell chest exercise', 
                    'Cable chest isolation', 'Upper chest exercise',
                    'Bodyweight back exercise', 'Machine back exercise', 'Rowing movement for back',
                    'Full body compound lift', 'Cable rowing exercise', 'Back thickness exercise',
                    'Barbell squat', 'Single leg exercise', 'Machine leg exercise',
                    'Hamstring isolation', 'Quad isolation', 'Calf muscle exercise', 'Hamstring exercise',
                    'Shoulder press', 'Side shoulder exercise', 'Front shoulder exercise',
                    'Rear shoulder exercise', 'Trap exercise',
                    'Bicep isolation', 'Tricep isolation', 'Alternative bicep exercise',
                    'Bodyweight tricep exercise', 'Cable bicep exercise',
                    'Core stability hold', 'Abdominal exercise', 'Oblique exercise',
                    'Lower ab exercise', 'Dynamic core exercise', 'Core rotation exercise',
                    'Running on treadmill', 'Stationary or outdoor cycling', 'Low-impact cardio machine',
                    'High-intensity cardio', 'Full body cardio exercise', 'Outdoor running', 'Low-intensity cardio',
                    'Stair climbing machine', 'Full body cardio', 'Combat cardio workout', 'Full body water exercise']
}

df_exercise = pd.DataFrame(exercise_data)
df_exercise.to_csv('data/exercise_library.csv', index=False)
print("✅ Created data/exercise_library.csv with 45 exercises")

# Create food_library.csv
food_data = {
    'food_name': ['Roti (Whole Wheat)', 'Rice (White Cooked)', 'Rice (Brown Cooked)', 'Dal (Mixed)', 'Rajma', 'Chole',
                  'Paneer', 'Tofu', 'Chicken Breast (Grilled)', 'Chicken Curry', 'Chicken Tandoori', 'Mutton Curry',
                  'Fish (Grilled)', 'Fish Curry', 'Egg (Boiled)', 'Omelette (2 eggs)', 'Egg Bhurji',
                  'Milk (Full Fat)', 'Milk (Toned)', 'Curd', 'Buttermilk',
                  'Banana', 'Apple', 'Orange', 'Mango', 'Papaya', 'Watermelon', 'Grapes',
                  'Almonds', 'Cashews', 'Walnuts', 'Peanuts',
                  'Bread (White)', 'Bread (Brown)', 'Paratha', 'Idli', 'Dosa (Plain)', 'Dosa (Masala)',
                  'Upma', 'Poha', 'Aloo Paratha', 'Paneer Paratha', 'Aloo Sabzi', 'Mixed Veg Sabzi', 'Palak Paneer',
                  'Samosa', 'Pakora', 'Biryani', 'Pav Bhaji', 'Vada Pav',
                  'Pasta (White Sauce)', 'Pasta (Red Sauce)', 'Pizza (1 slice)', 'Burger', 'Sandwich (Veg)',
                  'Momos (Veg)', 'Momos (Chicken)',
                  'Tea (with sugar)', 'Tea (without sugar)', 'Coffee (with sugar)', 'Coffee (without sugar)',
                  'Biscuits (Marie)', 'Biscuits (Digestive)', 'Chocolate', 'Ice Cream',
                  'Gulab Jamun', 'Jalebi', 'Lassi (Sweet)', 'Protein Shake', 'Oats', 'Cornflakes'],
    'serving_size': ['1 piece (30g)', '1 cup (200g)', '1 cup (200g)', '1 cup (240g)', '1 cup (240g)', '1 cup (240g)',
                     '100g', '100g', '100g', '1 serving (200g)', '100g', '1 serving (200g)',
                     '100g', '1 serving (200g)', '1 large', '1 serving', '1 serving',
                     '1 cup (240ml)', '1 cup (240ml)', '1 cup (240g)', '1 cup (240ml)',
                     '1 medium', '1 medium', '1 medium', '1 cup (165g)', '1 cup (145g)', '1 cup (150g)', '1 cup (150g)',
                     '10 nuts', '10 nuts', '5 halves', '1 tbsp (10g)',
                     '1 slice', '1 slice', '1 piece (100g)', '1 piece', '1 piece', '1 piece',
                     '1 cup (200g)', '1 cup (200g)', '1 piece', '1 piece', '1 cup (200g)', '1 cup (200g)', '1 cup (200g)',
                     '1 piece', '1 piece', '1 plate (300g)', '1 plate', '1 piece',
                     '1 plate (200g)', '1 plate (200g)', '1 slice (100g)', '1 piece', '1 piece',
                     '5 pieces', '5 pieces',
                     '1 cup', '1 cup', '1 cup', '1 cup',
                     '2 pieces', '2 pieces', '1 bar (40g)', '1 scoop (100g)',
                     '1 piece', '1 piece', '1 glass (250ml)', '1 serving', '1 cup cooked (240g)', '1 cup (30g)'],
    'calories': [70, 200, 215, 180, 225, 210,
                 265, 145, 165, 250, 150, 320,
                 140, 200, 70, 180, 200,
                 150, 120, 150, 40,
                 105, 95, 62, 99, 55, 46, 104,
                 70, 90, 65, 60,
                 80, 70, 280, 40, 120, 200,
                 200, 180, 300, 350, 150, 120, 280,
                 250, 80, 400, 400, 300,
                 350, 280, 250, 450, 250,
                 200, 250,
                 60, 5, 65, 5,
                 60, 80, 210, 200,
                 150, 150, 180, 150, 150, 110],
    'protein': [3, 4, 5, 12, 15, 12,
                18, 15, 31, 25, 25, 28,
                25, 22, 6, 13, 15,
                8, 8, 11, 2,
                1, 0, 1, 1, 1, 1, 1,
                3, 3, 2, 3,
                3, 3, 6, 2, 4, 6,
                5, 4, 7, 12, 3, 4, 15,
                4, 2, 15, 10, 6,
                10, 8, 10, 20, 8,
                6, 15,
                0, 0, 0, 0,
                1, 1, 3, 3,
                2, 1, 5, 25, 5, 2],
    'carbs': [15, 45, 45, 30, 40, 35,
              4, 4, 0, 8, 2, 5,
              0, 5, 0.5, 2, 5,
              12, 12, 17, 5,
              27, 25, 15, 25, 14, 11, 27,
              2, 5, 1, 2,
              15, 12, 35, 8, 20, 30,
              35, 30, 40, 38, 25, 18, 12,
              30, 8, 55, 50, 40,
              45, 50, 30, 45, 35,
              32, 28,
              14, 1, 15, 1,
              11, 12, 25, 24,
              25, 30, 30, 10, 27, 24],
    'fats': [1, 0.5, 2, 1, 1, 4,
             20, 8, 4, 12, 4, 20,
             4, 10, 5, 14, 12,
             8, 4, 4, 1,
             0, 0, 0, 0, 0, 0, 0,
             6, 7, 6, 5,
             1, 1, 12, 0.5, 2, 6,
             5, 5, 12, 15, 5, 4, 18,
             12, 5, 12, 15, 12,
             15, 6, 10, 20, 8,
             5, 8,
             1, 0, 1, 0,
             2, 3, 12, 10,
             6, 4, 5, 2, 3, 0]
}

df_food = pd.DataFrame(food_data)
df_food.to_csv('data/food_library.csv', index=False)
print("✅ Created data/food_library.csv with 70 Indian foods")

print("\n" + "="*60)
print("✅ Setup complete! Now run:")
print("="*60)
print("1. python database.py")
print("2. python load_data.py")
print("3. streamlit run app.py")