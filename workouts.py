from flask import Flask, request, jsonify, render_template
import random
import json
import os
from pathlib import Path
import datetime


app = Flask(__name__)

EXERCISES = {
    # ===== Gain Muscle (0-29) =====
    # Beginner (0-9)
    0: ("💪 Wall Push-ups", "reps"),
    1: ("🏋️ Knee Push-ups (Hands on Bed)", "reps"),
    2: ("💪🏼 Incline Push-ups (Kitchen Counter)", "reps"),
    3: ("🏋️ Squats (Holding Chair for Balance)", "reps"),
    4: ("💪 Glute Bridges (Pillow Between Knees)", "reps"),
    5: ("🏋️‍♂️ Step-ups (Bottom Stair)", "reps"),
    6: ("🎯 Towel Rows (Door Anchor)", "reps"),
    7: ("⏰ Deadbugs", "timing"),
    8: ("🕰️ Plank (Knees Down)", "timing"),
    9: ("💪🏼 Assisted Lunges (Wall Support)", "reps"),

    # Intermediate (10-19)
    10: ("🏋️ Standard Push-ups", "reps"),
    11: ("💪 Wide Push-ups", "reps"),
    12: ("🏆 Diamond Push-ups", "reps"),
    13: ("💪🏼 Pistol Squats (Assisted by Chair)", "reps"),
    14: ("🏋️ Bulgarian Split Squats (Back Foot on Chair)", "reps"),
    15: ("💪 Single-leg Glute Bridges", "reps"),
    16: ("🎯 Table Rows (Under Sturdy Table)", "reps"),
    17: ("⏳ Side Plank (From Knees)", "timing"),
    18: ("🕰️ Bear Crawls", "timing"),
    19: ("🏋️‍♂️ Jump Squats (Onto Pillow)", "reps"),

    # Advanced (20-29)
    20: ("💪 Archer Push-ups (Sliding Towels)", "reps"),
    21: ("🏋️ One-arm Push-up Progressions", "reps"),
    22: ("💪🏼 Nordic Curls (Towel Under Knees)", "reps"),
    23: ("🏆 Handstand Push-ups (Wall-assisted)", "reps"),
    24: ("💪 Dragon Flag Progressions", "reps"),
    25: ("⏰ Planche Lean (Towel Slides)", "timing"),
    26: ("🕰️ Human Flag Progressions (Tree Branch)", "timing"),
    27: ("🎯 One-arm Towel Rows", "reps"),
    28: ("🏋️ Towel Front Lever Rows", "reps"),
    29: ("💪🏼 Towel Muscle-up Progressions", "reps"),

    # ===== Lose Fat (30-59) =====
    # Beginner (30-39)
    30: ("⏰ Marching in Place", "timing"),
    31: ("🏃 Seated Knee Lifts", "reps"),
    32: ("💪 Standing Side Bends", "reps"),
    33: ("⏳ Wall Sit", "timing"),
    34: ("🕰️ Step Touch (Side Steps)", "timing"),
    35: ("⏰ Arm Circles (Water Bottles)", "timing"),
    36: ("🏃 Chair Step-ups", "reps"),
    37: ("💪🏼 Standing Leg Raises (Wall Support)", "reps"),
    38: ("🏋️ Seated Russian Twists (Hold Shoes)", "reps"),
    39: ("🏃 Slow Mountain Climbers", "reps"),

    # Intermediate (40-49)
    40: ("⏰ Jumping Jacks", "timing"),
    41: ("🏃 Standing Knee-to-Elbow", "reps"),
    42: ("💪 Standing Bicycle Crunches", "reps"),
    43: ("⏳ Squat Hold", "timing"),
    44: ("🕰️ Butt Kicks", "timing"),
    45: ("⏰ High Knees", "timing"),
    46: ("🏃 Step-back Lunges", "reps"),
    47: ("💪🏼 Standing Side Leg Raises", "reps"),
    48: ("🏋️ Standing Russian Twists", "reps"),
    49: ("🏃 Mountain Climbers", "reps"),

    # Advanced (50-59)
    50: ("⏰ Burpees (No Push-up)", "timing"),
    51: ("🏃 Jump Lunges", "reps"),
    52: ("💪 Standing Bicycle Crunches with Twist", "reps"),
    53: ("⏳ Single-leg Wall Sit", "timing"),
    54: ("🕰️ Fast High Knees", "timing"),
    55: ("⏰ Plank Jacks", "timing"),
    56: ("🏃 Box Jumps (Onto Step)", "reps"),
    57: ("💪🏼 Hanging Leg Raises (Door Frame)", "reps"),
    58: ("🏋️ Standing Weighted Twists", "reps"),
    59: ("🏃 Fast Mountain Climbers", "reps"),

    # ===== Improve Strength (60-89) =====
    # Beginner (60-69)
    60: ("💪 Towel-Resisted Push-ups", "reps"),
    61: ("🏋️ Chair Pistol Squats", "reps"),
    62: ("⏰ Farmer's Walk (Water Jugs)", "timing"),
    63: ("💪🏼 Towel Deadlifts", "reps"),
    64: ("🎯 Table Rows", "reps"),
    65: ("⏳ Wall Handstand Hold", "timing"),
    66: ("🏋️ Towel Pallof Press", "reps"),
    67: ("💪 Box Squats (To Chair)", "reps"),
    68: ("🏋️‍♂️ Bird Dogs", "reps"),
    69: ("💪🏼 Clamshells (Towel Under Knee)", "reps"),

    # Intermediate (70-79)
    70: ("💪 Resistance Band Push-ups", "reps"),
    71: ("🏋️ Single-leg Squats", "reps"),
    72: ("⏰ Farmer's Walk (Heavy Objects)", "timing"),
    73: ("💪🏼 Single-leg Deadlifts", "reps"),
    74: ("🎯 Inverted Rows (Under Table)", "reps"),
    75: ("⏳ Wall Handstand Push-ups", "timing"),
    76: ("🏋️ Resistance Band Pallof Press", "reps"),
    77: ("💪 Bulgarian Split Squats", "reps"),
    78: ("🏋️‍♂️ Supermans", "reps"),
    79: ("💪🏼 Side-lying Leg Raises", "reps"),

    # Advanced (80-89)
    80: ("💪 Weighted Push-ups (Backpack)", "reps"),
    81: ("🏋️ Pistol Squats", "reps"),
    82: ("⏰ Single-arm Farmer's Walk", "timing"),
    83: ("💪🏼 Single-leg Romanian Deadlifts", "reps"),
    84: ("🎯 One-arm Inverted Rows", "reps"),
    85: ("⏳ Freestanding Handstand Hold", "timing"),
    86: ("🏋️ Weighted Pallof Press", "reps"),
    87: ("💪 Shrimp Squats", "reps"),
    88: ("🏋️‍♂️ Hanging Leg Raises", "reps"),
    89: ("💪🏼 Weighted Side Plank", "timing"),

    # ===== Improve Stamina (90-119) =====
    # Beginner (90-99)
    90: ("⏰ Brisk Walking (Indoor/Outdoor)", "timing"),
    91: ("⏳ Shadow Boxing (Slow Pace)", "timing"),
    92: ("🕰️ Step Touch (Low Intensity)", "timing"),
    93: ("🏃 Seated Knee Lifts (Slow)", "reps"),
    94: ("⏰ Wall Push-up Holds", "timing"),
    95: ("💪 Standing Side Bends (Slow)", "reps"),
    96: ("🏃 Chair Step-ups (Slow Pace)", "reps"),
    97: ("⏳ Arm Circles (No Weight)", "timing"),
    98: ("🕰️ Seated Marches", "timing"),
    99: ("⏰ Breathing Exercises", "timing"),

    # Intermediate (100-109)
    100: ("⏰ Power Walking", "timing"),
    101: ("⏳ Shadow Boxing (Moderate Pace)", "timing"),
    102: ("🕰️ Step Touch (Moderate Intensity)", "timing"),
    103: ("🏃 Standing Knee Lifts (Fast)", "reps"),
    104: ("⏰ Push-up to Plank Holds", "timing"),
    105: ("💪 Standing Side Bends (Fast)", "reps"),
    106: ("🏃 Alternating Step-ups", "reps"),
    107: ("⏳ Arm Circles (With Weight)", "timing"),
    108: ("🕰️ Standing Marches", "timing"),
    109: ("⏰ Box Breathing Exercises", "timing"),

    # Advanced (110-119)
    110: ("⏰ Stair Climbing", "timing"),
    111: ("⏳ Shadow Boxing (High Intensity)", "timing"),
    112: ("🕰️ High Knee Step Touch", "timing"),
    113: ("🏃 Jumping Knee Lifts", "reps"),
    114: ("⏰ Plank to Push-up Holds", "timing"),
    115: ("💪 Weighted Side Bends", "reps"),
    116: ("🏃 Plyometric Step-ups", "reps"),
    117: ("⏳ Weighted Arm Circles", "timing"),
    118: ("🕰️ High Knee Marches", "timing"),
    119: ("⏰ Wim Hof Breathing", "timing"),

    # ===== Cardio (120-149) =====
    # Beginner (120-129)
    120: ("⏰ Marching in Place", "timing"),
    121: ("⏳ Seated Dancing", "timing"),
    122: ("🕰️ Arm Swings", "timing"),
    123: ("⏰ Leg Swings (Holding Wall)", "timing"),
    124: ("⏳ Neck Rolls", "timing"),
    125: ("🕰️ Ankle Circles", "timing"),
    126: ("🏃 Seated Jumping Jacks", "reps"),
    127: ("💪 Standing Knee Hugs", "reps"),
    128: ("🏋️ Heel Touches", "reps"),
    129: ("⏰ Breath Focus Walks", "timing"),

    # Intermediate (130-139)
    130: ("⏰ Jogging in Place", "timing"),
    131: ("⏳ Standing Dancing", "timing"),
    132: ("🕰️ Arm Circles", "timing"),
    133: ("⏰ Leg Raises", "timing"),
    134: ("⏳ Shoulder Rolls", "timing"),
    135: ("🕰️ Hip Circles", "timing"),
    136: ("🏃 Standing Jumping Jacks", "reps"),
    137: ("💪 Standing Quad Stretches", "reps"),
    138: ("🏋️ Toe Touches", "reps"),
    139: ("⏰ Power Walking", "timing"),

    # Advanced (140-149)
    140: ("⏰ High Knee Running in Place", "timing"),
    141: ("⏳ Dance Cardio", "timing"),
    142: ("🕰️ Arm Punches", "timing"),
    143: ("⏰ Dynamic Leg Swings", "timing"),
    144: ("⏳ Dynamic Neck Stretches", "timing"),
    145: ("🕰️ Dynamic Hip Openers", "timing"),
    146: ("🏃 Plyometric Jumping Jacks", "reps"),
    147: ("💪 Dynamic Stretching Routine", "reps"),
    148: ("🏋️ Jump Rope (Imaginary)", "timing"),
    149: ("⏰ Interval Running", "timing"),

    ===== General Fitness (150-179) =====

# Beginner (150-159)  
# Upper Body
150: ("🧍 Wall Push-ups", "reps"),  
151: ("🙌 Lateral Arm Raises", "reps"),  
152: ("🧍 Front Arm Raises", "reps"),  
153: ("🙋 Overhead Reaches", "reps"),
# Core  
154: ("🪨 Front Plank", "timing"),  
155: ("🧍 Standing Knee Raises", "reps"),  
# Lower Body
156: ("🏃 Jumping Jacks", "reps"),  
157: ("🧍 Bodyweight Squats", "reps"),  
158: ("🧍 Standing Leg Raises", "reps"),  
159: ("🦵 Forward Lunges", "reps"),  

# Intermediate (160-169)  
# Upper Body
160: ("💪 Chair/Couch Dips", "reps"),  
161: ("💪 Wide-Grip Push-ups", "reps"),  
162: ("🧍 Wall Mountain Climbers", "reps"),  
163: ("🧍 Standing Reverse Fly", "reps"),
# Core  
164: ("🧎 Shoulder Taps in Plank", "reps"),  
165: ("🪨 Straight-Arm Side Plank", "timing"),  
166: ("🧍 Standing Bicycle Crunch", "reps"),
# Lower Body  
167: ("🏃 High Knees", "reps"),  
168: ("🧍 Lateral Lunges", "reps"),  
169: ("🧍 Standing Glute Kickbacks", "reps"),  

# Advanced (170-179)  
# Upper Body
170: ("💪 Pike Push-ups", "reps"),  
171: ("💪 Decline Push-ups", "reps"),  
172: ("🪨 Up-Down Plank", "reps"),  
173: ("🧍 Wall Handstand Hold", "timing"),
# Core  
174: ("🧎 Superman Pose", "timing"),  
175: ("🪨 Extended Arm Plank", "timing"),  
176: ("🧍 Standing Leg Raises with Hold", "reps"),
# Lower Body  
177: ("🧍 Single-Leg Squats", "reps"),  
178: ("🦵 Jump Squats", "reps"),  
179: ("🏃 Split Jump Lunges", "reps")

HIIT_EXERCISES = {
    180: ("Burpees (No Push-up)", "timing"),  # Beginner
    181: ("Modified Jump Squats", "timing"),
    182: ("Slow Mountain Climbers", "timing"),
    183: ("Step-Back Lunges", "timing"),
    184: ("Standing Alternating Toe Touches", "timing"),
    185: ("Wall Push-up to Knee Drive", "timing"),
    186: ("Seated Leg Raises", "timing"),
    187: ("Standing Side Hops", "timing"),
    188: ("Arm Circles (Fast Pace)", "timing"),
    189: ("Shadow Boxing (Basic)", "timing"),
    
    # Intermediate (190-199)
    190: ("Full Burpees", "timing"),
    191: ("Jump Squats", "timing"),
    192: ("Mountain Climbers", "timing"),
    193: ("Skater Hops", "timing"),
    194: ("Plank Jacks", "timing"),
    195: ("High Knees", "timing"),
    196: ("Butt Kicks", "timing"),
    197: ("Standing Bicycle Crunches", "timing"),
    198: ("Towel Slams", "timing"),  # Use rolled towel
    199: ("Shadow Boxing (Combos)", "timing"),
    
    # Advanced (200-209)
    200: ("Plyo Push-ups", "timing"),
    201: ("Tuck Jumps", "timing"),
    202: ("Spiderman Push-up Climbers", "timing"),
    203: ("180° Jump Squats", "timing"),
    204: ("Dive Bomber Push-ups", "timing"),
    205: ("Single-Leg Burpees", "timing"),
    206: ("Frog Jumps", "timing"),
    207: ("Star Jumps", "timing"),
    208: ("Towel Battle Rope Waves", "timing"),  # Use towel as rope
    209: ("Combo Punches with Squats", "timing")
}


# Diet plans with Indian foods
DIET_PLANS = {
    0: {  # Gain Muscle (Complete 4 weeks)
        "Week 1": {
            "Breakfast": [
                "2 Masala Dosa with Coconut Chutney (Protein: 12g, Carbs: 60g, Fats: 15g, Energy: 380kcal)",
                "3 Idlis with Sambar (Protein: 15g, Carbs: 50g, Fats: 5g, Energy: 300kcal)",
                "Pongal with Ghee + 2 Egg Whites (Protein: 20g, Carbs: 45g, Fats: 10g, Energy: 350kcal)",
                "Ragi Dosa with Peanut Chutney (Protein: 18g, Carbs: 55g, Fats: 12g, Energy: 400kcal)"
            ],
            "Lunch": [
                "2 Chapati + Chicken Curry (150g) + Curd (Protein: 40g, Carbs: 60g, Fats: 20g, Energy: 550kcal)",
                "Brown Rice + Fish Curry (200g) + Rasam (Protein: 45g, Carbs: 70g, Fats: 15g, Energy: 600kcal)",
                "Quinoa Khichdi with Soya Chunks (Protein: 35g, Carbs: 65g, Fats: 12g, Energy: 500kcal)",
                "Millet Rice + Egg Curry (3 eggs) + Vegetable Salad (Protein: 38g, Carbs: 55g, Fats: 25g, Energy: 580kcal)"
            ],
            "Dinner": [
                "2 Roti + Paneer Bhurji (100g) + Dal (Protein: 35g, Carbs: 50g, Fats: 18g, Energy: 500kcal)",
                "Dosa with Chicken Keema (100g) (Protein: 40g, Carbs: 45g, Fats: 15g, Energy: 480kcal)",
                "Jeera Rice + Prawns Curry (150g) + Curd (Protein: 42g, Carbs: 60g, Fats: 12g, Energy: 520kcal)",
                "Ragi Mudde + Chicken Stew (Protein: 38g, Carbs: 55g, Fats: 20g, Energy: 550kcal)"
            ],
            "Snacks": [
                "Sprouts Chaat (100g) (Protein: 15g, Carbs: 30g, Fats: 5g, Energy: 220kcal)",
                "Peanut Sundal (50g) (Protein: 12g, Carbs: 15g, Fats: 10g, Energy: 200kcal)",
                "Boiled Egg (2) + Banana (Protein: 12g, Carbs: 25g, Fats: 10g, Energy: 250kcal)",
                "Curd with Flaxseeds (200g) (Protein: 10g, Carbs: 15g, Fats: 8g, Energy: 180kcal)"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Egg Dosa (3 eggs) with Chutney (Protein: 25g, Carbs: 40g, Fats: 18g, Energy: 420kcal)",
                "Rava Upma with Vegetables + 2 Egg Whites (Protein: 20g, Carbs: 50g, Fats: 12g, Energy: 380kcal)",
                "Pesarattu (Green Gram Dosa) with Ginger Chutney (Protein: 22g, Carbs: 55g, Fats: 10g, Energy: 400kcal)",
                "Oats Idli with Sambar (Protein: 18g, Carbs: 60g, Fats: 8g, Energy: 350kcal)"
            ],
            "Lunch": [
                "2 Chapati + Mutton Curry (100g) + Curd (Protein: 42g, Carbs: 60g, Fats: 25g, Energy: 600kcal)",
                "Brown Rice + Chicken Chettinad (150g) + Vegetable Salad (Protein: 45g, Carbs: 65g, Fats: 18g, Energy: 580kcal)",
                "Quinoa Pulao with Fish Fry (Protein: 40g, Carbs: 55g, Fats: 15g, Energy: 520kcal)",
                "Millet Roti + Egg Bhurji (3 eggs) + Dal (Protein: 38g, Carbs: 50g, Fats: 22g, Energy: 550kcal)"
            ],
            "Dinner": [
                "2 Roti + Chicken Keema (100g) + Vegetable Salad (Protein: 40g, Carbs: 45g, Fats: 20g, Energy: 500kcal)",
                "Dosa with Egg Curry (3 eggs) (Protein: 38g, Carbs: 40g, Fats: 18g, Energy: 480kcal)",
                "Jeera Rice + Prawns Masala (150g) + Curd (Protein: 45g, Carbs: 55g, Fats: 15g, Energy: 520kcal)",
                "Ragi Mudde + Mutton Curry (Protein: 42g, Carbs: 50g, Fats: 25g, Energy: 600kcal)"
            ],
            "Snacks": [
                "Paneer Tikka (100g) (Protein: 20g, Carbs: 10g, Fats: 15g, Energy: 250kcal)",
                "Roasted Chana (50g) (Protein: 15g, Carbs: 30g, Fats: 5g, Energy: 220kcal)",
                "Banana Milkshake with Peanut Butter (Protein: 15g, Carbs: 40g, Fats: 12g, Energy: 320kcal)",
                "Curd with Chia Seeds (200g) (Protein: 12g, Carbs: 15g, Fats: 10g, Energy: 200kcal)"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Paneer Uttapam (2) with Coconut Chutney (Protein: 28g, Carbs: 55g, Fats: 18g, Energy: 480kcal)",
                "4 Egg Whites + 1 Whole Egg Bhurji with Multigrain Toast (Protein: 32g, Carbs: 35g, Fats: 22g, Energy: 450kcal)",
                "Moong Dal Cheela with Mint Chutney (Protein: 25g, Carbs: 40g, Fats: 12g, Energy: 380kcal)",
                "Ragi Idli with Chicken Keema (100g) (Protein: 35g, Carbs: 50g, Fats: 15g, Energy: 500kcal)"
            ],
            "Lunch": [
                "3 Roti + Beef Curry (150g) + Vegetable Salad (Protein: 50g, Carbs: 65g, Fats: 28g, Energy: 700kcal)",
                "Red Rice + Crab Curry (200g) + Rasam (Protein: 48g, Carbs: 60g, Fats: 18g, Energy: 620kcal)",
                "Bajra Khichdi with Soya Chunks (Protein: 38g, Carbs: 55g, Fats: 15g, Energy: 520kcal)",
                "Quinoa Rice + Egg Masala (4 eggs) + Avocado Salad (Protein: 42g, Carbs: 50g, Fats: 30g, Energy: 650kcal)"
            ],
            "Dinner": [
                "2 Roti + Chicken Liver Fry (150g) + Dal (Protein: 45g, Carbs: 45g, Fats: 25g, Energy: 580kcal)",
                "Adai with Jaggery and Butter (Protein: 30g, Carbs: 70g, Fats: 20g, Energy: 600kcal)",
                "Jeera Rice + Fish Molee (200g) + Curd (Protein: 48g, Carbs: 55g, Fats: 18g, Energy: 580kcal)",
                "Ragi Roti + Mutton Sukka (Protein: 45g, Carbs: 50g, Fats: 28g, Energy: 650kcal)"
            ],
            "Snacks": [
                "Soya Chunk Chaat (150g) (Protein: 25g, Carbs: 20g, Fats: 8g, Energy: 280kcal)",
                "Dates + Almonds (5 each) (Protein: 10g, Carbs: 50g, Fats: 15g, Energy: 350kcal)",
                "Boiled Sweet Potato + Peanut Butter (Protein: 8g, Carbs: 45g, Fats: 12g, Energy: 320kcal)",
                "Greek Yogurt with Walnuts (200g) (Protein: 20g, Carbs: 15g, Fats: 18g, Energy: 300kcal)"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Methi Paratha (3) with Curd + 2 Egg Whites (Protein: 35g, Carbs: 75g, Fats: 20g, Energy: 600kcal)",
                "Chicken Keema Dosa (Protein: 40g, Carbs: 50g, Fats: 25g, Energy: 580kcal)",
                "Besan Chilla with Paneer Stuffing (Protein: 30g, Carbs: 35g, Fats: 22g, Energy: 450kcal)",
                "Oats Pongal with Ghee + 3 Egg Whites (Protein: 32g, Carbs: 60g, Fats: 18g, Energy: 520kcal)"
            ],
            "Lunch": [
                "3 Roti + Duck Curry (150g) + Vegetable Salad (Protein: 55g, Carbs: 70g, Fats: 30g, Energy: 750kcal)",
                "Black Rice + Prawn Biryani (Protein: 50g, Carbs: 65g, Fats: 25g, Energy: 680kcal)",
                "Millet Khichdi with Chicken Pieces (Protein: 45g, Carbs: 60g, Fats: 20g, Energy: 600kcal)",
                "Quinoa Dosa with Mutton Keema (Protein: 48g, Carbs: 55g, Fats: 28g, Energy: 650kcal)"
            ],
            "Dinner": [
                "2 Roti + Egg Curry (4 eggs) + Palak (Protein: 42g, Carbs: 40g, Fats: 30g, Energy: 600kcal)",
                "Neer Dosa with Chicken Ghee Roast (Protein: 45g, Carbs: 50g, Fats: 35g, Energy: 680kcal)",
                "Jeera Rice + Fish Curry (250g) + Avocado (Protein: 55g, Carbs: 60g, Fats: 25g, Energy: 700kcal)",
                "Ragi Roti + Mutton Liver Masala (Protein: 50g, Carbs: 45g, Fats: 30g, Energy: 650kcal)"
            ],
            "Snacks": [
                "Peanut Chikki (50g) + Milk (Protein: 18g, Carbs: 40g, Fats: 20g, Energy: 400kcal)",
                "Roasted Grams + Jaggery (Protein: 15g, Carbs: 50g, Fats: 10g, Energy: 350kcal)",
                "Banana + Almond Butter Smoothie (Protein: 12g, Carbs: 60g, Fats: 18g, Energy: 450kcal)",
                "Paneer Wrap with Multigrain Roti (Protein: 25g, Carbs: 40g, Fats: 22g, Energy: 480kcal)"
            ]
        }
    },
    1: {  # Lose Fat (Complete 4 weeks)
        "Week 1": {
            "Breakfast": [
                "Moong Dal Chilla (2) with Mint Chutney (Protein: 15g, Carbs: 30g, Fats: 5g, Energy: 220kcal)",
                "Vegetable Oats Upma (Protein: 12g, Carbs: 40g, Fats: 5g, Energy: 250kcal)",
                "Ragi Porridge with Almonds (Protein: 10g, Carbs: 35g, Fats: 8g, Energy: 240kcal)",
                "Poha with Vegetables (Protein: 8g, Carbs: 45g, Fats: 5g, Energy: 250kcal)"
            ],
            "Lunch": [
                "Brown Rice + Sambar (1 cup) + Vegetable Salad (Protein: 15g, Carbs: 50g, Fats: 5g, Energy: 300kcal)",
                "2 Roti + Dal + Lauki Sabzi (Protein: 18g, Carbs: 40g, Fats: 5g, Energy: 280kcal)",
                "Quinoa Khichdi with Vegetables (Protein: 20g, Carbs: 45g, Fats: 8g, Energy: 320kcal)",
                "Millet Rice + Fish Curry (100g) + Rasam (Protein: 25g, Carbs: 40g, Fats: 10g, Energy: 350kcal)"
            ],
            "Dinner": [
                "Vegetable Soup + 1 Roti (Protein: 10g, Carbs: 25g, Fats: 3g, Energy: 180kcal)",
                "Dosa with Tomato Chutney (Protein: 12g, Carbs: 35g, Fats: 5g, Energy: 220kcal)",
                "Vegetable Khichdi with Curd (Protein: 15g, Carbs: 40g, Fats: 5g, Energy: 280kcal)",
                "Grilled Chicken (100g) with Salad (Protein: 30g, Carbs: 10g, Fats: 8g, Energy: 250kcal)"
            ],
            "Snacks": [
                "Cucumber Slices with Hummus (Protein: 5g, Carbs: 15g, Fats: 5g, Energy: 120kcal)",
                "Roasted Makhana (30g) (Protein: 5g, Carbs: 20g, Fats: 2g, Energy: 120kcal)",
                "Buttermilk with Jeera (Protein: 3g, Carbs: 10g, Fats: 2g, Energy: 80kcal)",
                "Fruit Chaat (100g) (Protein: 2g, Carbs: 25g, Fats: 0g, Energy: 120kcal)"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Ragi Idli (3) with Tomato Chutney (Protein: 12g, Carbs: 45g, Fats: 3g, Energy: 250kcal)",
                "Vegetable Daliya (Protein: 15g, Carbs: 50g, Fats: 5g, Energy: 300kcal)",
                "Oats Porridge with Flaxseeds (Protein: 10g, Carbs: 40g, Fats: 8g, Energy: 280kcal)",
                "Besan Chilla with Mint Chutney (Protein: 18g, Carbs: 30g, Fats: 5g, Energy: 250kcal)"
            ],
            "Lunch": [
                "Quinoa Rice + Dal + Cucumber Salad (Protein: 20g, Carbs: 55g, Fats: 8g, Energy: 350kcal)",
                "2 Roti + Lauki Chana Dal + Curd (Protein: 22g, Carbs: 45g, Fats: 8g, Energy: 320kcal)",
                "Millet Khichdi with Vegetables (Protein: 18g, Carbs: 50g, Fats: 8g, Energy: 350kcal)",
                "Brown Rice + Fish Curry (150g) + Beetroot Salad (Protein: 30g, Carbs: 45g, Fats: 12g, Energy: 400kcal)"
            ],
            "Dinner": [
                "Vegetable Clear Soup + 1 Roti (Protein: 12g, Carbs: 30g, Fats: 5g, Energy: 220kcal)",
                "Adai (2) with Coconut Chutney (Protein: 15g, Carbs: 40g, Fats: 8g, Energy: 300kcal)",
                "Moong Dal Khichdi with Curd (Protein: 20g, Carbs: 45g, Fats: 5g, Energy: 320kcal)",
                "Grilled Fish (150g) with Stir-fried Vegetables (Protein: 35g, Carbs: 15g, Fats: 10g, Energy: 300kcal)"
            ],
            "Snacks": [
                "Carrot Sticks with Hummus (Protein: 6g, Carbs: 20g, Fats: 5g, Energy: 150kcal)",
                "Roasted Chana (40g) (Protein: 12g, Carbs: 25g, Fats: 4g, Energy: 200kcal)",
                "Green Tea + 5 Almonds (Protein: 5g, Carbs: 5g, Fats: 8g, Energy: 120kcal)",
                "Watermelon (200g) (Protein: 2g, Carbs: 30g, Fats: 0g, Energy: 130kcal)"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Oats Idli (4) with Sambar (Protein: 15g, Carbs: 50g, Fats: 5g, Energy: 300kcal)",
                "Vegetable Rava Upma with Flaxseeds (Protein: 12g, Carbs: 45g, Fats: 8g, Energy: 300kcal)",
                "Pesarattu (2) with Ginger Chutney (Protein: 18g, Carbs: 40g, Fats: 8g, Energy: 320kcal)",
                "Ragi Porridge with Walnuts (Protein: 12g, Carbs: 35g, Fats: 10g, Energy: 280kcal)"
            ],
            "Lunch": [
                "Brown Rice + Dal + Cabbage Sabzi (Protein: 18g, Carbs: 55g, Fats: 8g, Energy: 350kcal)",
                "2 Jowar Roti + Bottle Gourd Dal + Curd (Protein: 20g, Carbs: 40g, Fats: 8g, Energy: 320kcal)",
                "Quinoa Pulao with Vegetables (Protein: 15g, Carbs: 50g, Fats: 8g, Energy: 350kcal)",
                "Millet Rice + Chicken Clear Soup (Protein: 25g, Carbs: 40g, Fats: 10g, Energy: 380kcal)"
            ],
            "Dinner": [
                "Vegetable Soup + 1 Multigrain Roti (Protein: 12g, Carbs: 35g, Fats: 5g, Energy: 230kcal)",
                "Dosa with Mint Chutney (Protein: 10g, Carbs: 40g, Fats: 5g, Energy: 250kcal)",
                "Vegetable Khichdi with Curd (Protein: 18g, Carbs: 45g, Fats: 5g, Energy: 300kcal)",
                "Grilled Chicken (120g) with Stir-fried Vegetables (Protein: 30g, Carbs: 20g, Fats: 8g, Energy: 280kcal)"
            ],
            "Snacks": [
                "Cucumber + Tomato Salad (Protein: 3g, Carbs: 15g, Fats: 2g, Energy: 90kcal)",
                "Roasted Makhana (40g) (Protein: 6g, Carbs: 25g, Fats: 3g, Energy: 160kcal)",
                "Buttermilk with Cumin (Protein: 4g, Carbs: 12g, Fats: 3g, Energy: 90kcal)",
                "Papaya (200g) (Protein: 2g, Carbs: 35g, Fats: 0g, Energy: 150kcal)"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Moong Dal Chilla (2) with Coriander Chutney (Protein: 18g, Carbs: 30g, Fats: 5g, Energy: 250kcal)",
                "Vegetable Oats Upma with Flaxseeds (Protein: 15g, Carbs: 45g, Fats: 8g, Energy: 320kcal)",
                "Ragi Dosa with Tomato Chutney (Protein: 12g, Carbs: 40g, Fats: 5g, Energy: 250kcal)",
                "Poha with Sprouts (Protein: 15g, Carbs: 50g, Fats: 5g, Energy: 300kcal)"
            ],
            "Lunch": [
                "Quinoa Rice + Dal + Cucumber Raita (Protein: 22g, Carbs: 50g, Fats: 8g, Energy: 350kcal)",
                "2 Bajra Roti + Lauki Dal + Salad (Protein: 20g, Carbs: 40g, Fats: 8g, Energy: 320kcal)",
                "Millet Khichdi with Vegetables (Protein: 18g, Carbs: 45g, Fats: 8g, Energy: 350kcal)",
                "Brown Rice + Fish Curry (150g) + Beetroot Salad (Protein: 30g, Carbs: 40g, Fats: 12g, Energy: 400kcal)"
            ],
            "Dinner": [
                "Vegetable Clear Soup + 1 Roti (Protein: 12g, Carbs: 30g, Fats: 5g, Energy: 220kcal)",
                "Adai (2) with Coconut Chutney (Protein: 15g, Carbs: 40g, Fats: 8g, Energy: 300kcal)",
                "Moong Dal Khichdi with Curd (Protein: 20g, Carbs: 45g, Fats: 5g, Energy: 320kcal)",
                "Grilled Fish (150g) with Stir-fried Vegetables (Protein: 35g, Carbs: 15g, Fats: 10g, Energy: 300kcal)"
            ],
            "Snacks": [
                "Carrot Sticks with Hummus (Protein: 6g, Carbs: 20g, Fats: 5g, Energy: 150kcal)",
                "Roasted Chana (40g) (Protein: 12g, Carbs: 25g, Fats: 4g, Energy: 200kcal)",
                "Green Tea + 5 Almonds (Protein: 5g, Carbs: 5g, Fats: 8g, Energy: 120kcal)",
                "Watermelon (200g) (Protein: 2g, Carbs: 30g, Fats: 0g, Energy: 130kcal)"
            ]
        }
    },
    2: {  # Improve Strength (Complete 4 weeks)
        "Week 1": {
            "Breakfast": [
                "Paneer Paratha (2) with Curd (Protein: 25g, Carbs: 60g, Fats: 15g, Energy: 450kcal)",
                "Egg Bhurji (3 eggs) with Multigrain Toast (Protein: 30g, Carbs: 40g, Fats: 20g, Energy: 480kcal)",
                "Banana Almond Smoothie with Chia Seeds (Protein: 20g, Carbs: 50g, Fats: 15g, Energy: 400kcal)",
                "Chana Dal Chilla with Mint Chutney (Protein: 22g, Carbs: 45g, Fats: 10g, Energy: 350kcal)"
            ],
            "Lunch": [
                "Brown Rice + Chicken Curry (150g) + Vegetable Salad (Protein: 45g, Carbs: 60g, Fats: 20g, Energy: 600kcal)",
                "2 Roti + Dal Tadka + Palak Sabzi (Protein: 30g, Carbs: 50g, Fats: 15g, Energy: 450kcal)",
                "Soya Biryani with Raita (Protein: 35g, Carbs: 55g, Fats: 12g, Energy: 500kcal)",
                "Fish Curry (200g) with Quinoa (Protein: 50g, Carbs: 45g, Fats: 15g, Energy: 550kcal)"
            ],
            "Dinner": [
                "Grilled Chicken (150g) with Vegetables (Protein: 45g, Carbs: 20g, Fats: 15g, Energy: 400kcal)",
                "Palak Paneer (100g) with 2 Roti (Protein: 30g, Carbs: 40g, Fats: 20g, Energy: 450kcal)",
                "Egg Curry (3 eggs) with Rice (Protein: 35g, Carbs: 50g, Fats: 18g, Energy: 500kcal)",
                "Dal Khichdi with Ghee (Protein: 25g, Carbs: 60g, Fats: 15g, Energy: 480kcal)"
            ],
            "Snacks": [
                "Sprouted Moong Salad (100g) (Protein: 15g, Carbs: 30g, Fats: 5g, Energy: 220kcal)",
                "Peanut Ladoo (2 small) (Protein: 12g, Carbs: 20g, Fats: 15g, Energy: 250kcal)",
                "Curd with Chia Seeds (200g) (Protein: 12g, Carbs: 15g, Fats: 10g, Energy: 200kcal)",
                "Roasted Makhana (50g) (Protein: 8g, Carbs: 35g, Fats: 5g, Energy: 220kcal)"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Egg Dosa (3 eggs) with Chutney (Protein: 25g, Carbs: 40g, Fats: 18g, Energy: 420kcal)",
                "Rava Upma with Vegetables + 2 Egg Whites (Protein: 20g, Carbs: 50g, Fats: 12g, Energy: 380kcal)",
                "Pesarattu (Green Gram Dosa) with Ginger Chutney (Protein: 22g, Carbs: 55g, Fats: 10g, Energy: 400kcal)",
                "Oats Idli with Sambar (Protein: 18g, Carbs: 60g, Fats: 8g, Energy: 350kcal)"
            ],
            "Lunch": [
                "2 Chapati + Mutton Curry (100g) + Curd (Protein: 42g, Carbs: 60g, Fats: 25g, Energy: 600kcal)",
                "Brown Rice + Chicken Chettinad (150g) + Vegetable Salad (Protein: 45g, Carbs: 65g, Fats: 18g, Energy: 580kcal)",
                "Quinoa Pulao with Fish Fry (Protein: 40g, Carbs: 55g, Fats: 15g, Energy: 520kcal)",
                "Millet Roti + Egg Bhurji (3 eggs) + Dal (Protein: 38g, Carbs: 50g, Fats: 22g, Energy: 550kcal)"
            ],
            "Dinner": [
                "2 Roti + Chicken Keema (100g) + Vegetable Salad (Protein: 40g, Carbs: 45g, Fats: 20g, Energy: 500kcal)",
                "Dosa with Egg Curry (3 eggs) (Protein: 38g, Carbs: 40g, Fats: 18g, Energy: 480kcal)",
                "Jeera Rice + Prawns Masala (150g) + Curd (Protein: 45g, Carbs: 55g, Fats: 15g, Energy: 520kcal)",
                "Ragi Mudde + Mutton Curry (Protein: 42g, Carbs: 50g, Fats: 25g, Energy: 600kcal)"
            ],
            "Snacks": [
                "Paneer Tikka (100g) (Protein: 20g, Carbs: 10g, Fats: 15g, Energy: 250kcal)",
                "Roasted Chana (50g) (Protein: 15g, Carbs: 30g, Fats: 5g, Energy: 220kcal)",
                "Banana Milkshake with Peanut Butter (Protein: 15g, Carbs: 40g, Fats: 12g, Energy: 320kcal)",
                "Curd with Chia Seeds (200g) (Protein: 12g, Carbs: 15g, Fats: 10g, Energy: 200kcal)"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Paneer Uttapam (2) with Coconut Chutney (Protein: 28g, Carbs: 55g, Fats: 18g, Energy: 480kcal)",
                "4 Egg Whites + 1 Whole Egg Bhurji with Multigrain Toast (Protein: 32g, Carbs: 35g, Fats: 22g, Energy: 450kcal)",
                "Moong Dal Cheela with Mint Chutney (Protein: 25g, Carbs: 40g, Fats: 12g, Energy: 380kcal)",
                "Ragi Idli with Chicken Keema (100g) (Protein: 35g, Carbs: 50g, Fats: 15g, Energy: 500kcal)"
            ],
            "Lunch": [
                "3 Roti + Beef Curry (150g) + Vegetable Salad (Protein: 50g, Carbs: 65g, Fats: 28g, Energy: 700kcal)",
                "Red Rice + Crab Curry (200g) + Rasam (Protein: 48g, Carbs: 60g, Fats: 18g, Energy: 620kcal)",
                "Bajra Khichdi with Soya Chunks (Protein: 38g, Carbs: 55g, Fats: 15g, Energy: 520kcal)",
                "Quinoa Rice + Egg Masala (4 eggs) + Avocado Salad (Protein: 42g, Carbs: 50g, Fats: 30g, Energy: 650kcal)"
            ],
            "Dinner": [
                "2 Roti + Chicken Liver Fry (150g) + Dal (Protein: 45g, Carbs: 45g, Fats: 25g, Energy: 580kcal)",
                "Adai with Jaggery and Butter (Protein: 30g, Carbs: 70g, Fats: 20g, Energy: 600kcal)",
                "Jeera Rice + Fish Molee (200g) + Curd (Protein: 48g, Carbs: 55g, Fats: 18g, Energy: 580kcal)",
                "Ragi Roti + Mutton Sukka (Protein: 45g, Carbs: 50g, Fats: 28g, Energy: 650kcal)"
            ],
            "Snacks": [
                "Soya Chunk Chaat (150g) (Protein: 25g, Carbs: 20g, Fats: 8g, Energy: 280kcal)",
                "Dates + Almonds (5 each) (Protein: 10g, Carbs: 50g, Fats: 15g, Energy: 350kcal)",
                "Boiled Sweet Potato + Peanut Butter (Protein: 8g, Carbs: 45g, Fats: 12g, Energy: 320kcal)",
                "Greek Yogurt with Walnuts (200g) (Protein: 20g, Carbs: 15g, Fats: 18g, Energy: 300kcal)"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Methi Paratha (3) with Curd + 2 Egg Whites (Protein: 35g, Carbs: 75g, Fats: 20g, Energy: 600kcal)",
                "Chicken Keema Dosa (Protein: 40g, Carbs: 50g, Fats: 25g, Energy: 580kcal)",
                "Besan Chilla with Paneer Stuffing (Protein: 30g, Carbs: 35g, Fats: 22g, Energy: 450kcal)",
                "Oats Pongal with Ghee + 3 Egg Whites (Protein: 32g, Carbs: 60g, Fats: 18g, Energy: 520kcal)"
            ],
            "Lunch": [
                "3 Roti + Duck Curry (150g) + Vegetable Salad (Protein: 55g, Carbs: 70g, Fats: 30g, Energy: 750kcal)",
                "Black Rice + Prawn Biryani (Protein: 50g, Carbs: 65g, Fats: 25g, Energy: 680kcal)",
                "Millet Khichdi with Chicken Pieces (Protein: 45g, Carbs: 60g, Fats: 20g, Energy: 600kcal)",
                "Quinoa Dosa with Mutton Keema (Protein: 48g, Carbs: 55g, Fats: 28g, Energy: 650kcal)"
            ],
            "Dinner": [
                "2 Roti + Egg Curry (4 eggs) + Palak (Protein: 42g, Carbs: 40g, Fats: 30g, Energy: 600kcal)",
                "Neer Dosa with Chicken Ghee Roast (Protein: 45g, Carbs: 50g, Fats: 35g, Energy: 680kcal)",
                "Jeera Rice + Fish Curry (250g) + Avocado (Protein: 55g, Carbs: 60g, Fats: 25g, Energy: 700kcal)",
                "Ragi Roti + Mutton Liver Masala (Protein: 50g, Carbs: 45g, Fats: 30g, Energy: 650kcal)"
            ],
            "Snacks": [
                "Peanut Chikki (50g) + Milk (Protein: 18g, Carbs: 40g, Fats: 20g, Energy: 400kcal)",
                "Roasted Grams + Jaggery (Protein: 15g, Carbs: 50g, Fats: 10g, Energy: 350kcal)",
                "Banana + Almond Butter Smoothie (Protein: 12g, Carbs: 60g, Fats: 18g, Energy: 450kcal)",
                "Paneer Wrap with Multigrain Roti (Protein: 25g, Carbs: 40g, Fats: 22g, Energy: 480kcal)"
            ]
        }
    },
    3: {  # Improve Stamina (Complete 4 weeks)
        "Week 1": {
            "Breakfast": [
                "Dalia with Vegetables (Protein: 15g, Carbs: 60g, Fats: 5g, Energy: 350kcal)",
                "Pongal with Coconut Chutney (Protein: 12g, Carbs: 65g, Fats: 10g, Energy: 380kcal)",
                "Banana Oats Smoothie (Protein: 10g, Carbs: 70g, Fats: 5g, Energy: 350kcal)",
                "Vegetable Uttapam with Sambar (Protein: 15g, Carbs: 55g, Fats: 8g, Energy: 320kcal)"
            ],
            "Lunch": [
                "Lemon Rice with Peanuts (Protein: 15g, Carbs: 80g, Fats: 10g, Energy: 450kcal)",
                "Vegetable Khichdi with Curd (Protein: 18g, Carbs: 70g, Fats: 8g, Energy: 420kcal)",
                "Curd Rice with Pickle (Protein: 12g, Carbs: 75g, Fats: 10g, Energy: 400kcal)",
                "Sambar Rice with Papad (Protein: 15g, Carbs: 65g, Fats: 8g, Energy: 380kcal)"
            ],
            "Dinner": [
                "Vegetable Pulao with Raita (Protein: 15g, Carbs: 60g, Fats: 8g, Energy: 350kcal)",
                "Dal with 2 Roti (Protein: 20g, Carbs: 50g, Fats: 5g, Energy: 320kcal)",
                "Vegetable Soup with Bread (Protein: 12g, Carbs: 45g, Fats: 5g, Energy: 280kcal)",
                "Poha with Vegetables (Protein: 10g, Carbs: 55g, Fats: 5g, Energy: 300kcal)"
            ],
            "Snacks": [
                "Fruit Salad (200g) (Protein: 2g, Carbs: 40g, Fats: 1g, Energy: 180kcal)",
                "Roasted Chana (50g) (Protein: 15g, Carbs: 30g, Fats: 5g, Energy: 220kcal)",
                "Buttermilk (300ml) (Protein: 5g, Carbs: 10g, Fats: 2g, Energy: 80kcal)",
                "Dry Fruits (30g) (Protein: 5g, Carbs: 20g, Fats: 12g, Energy: 200kcal)"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Vegetable Upma with Peanuts (Protein: 15g, Carbs: 65g, Fats: 10g, Energy: 400kcal)",
                "Pongal with Sambar (Protein: 18g, Carbs: 70g, Fats: 12g, Energy: 450kcal)",
                "Banana Smoothie with Flaxseeds (Protein: 12g, Carbs: 75g, Fats: 8g, Energy: 420kcal)",
                "Rava Idli with Chutney (Protein: 15g, Carbs: 60g, Fats: 8g, Energy: 380kcal)"
            ],
            "Lunch": [
                "Tomato Rice with Curd (Protein: 15g, Carbs: 85g, Fats: 10g, Energy: 480kcal)",
                "Vegetable Biryani with Raita (Protein: 18g, Carbs: 75g, Fats: 12g, Energy: 450kcal)",
                "Curd Rice with Vegetables (Protein: 15g, Carbs: 80g, Fats: 10g, Energy: 450kcal)",
                "Sambar Rice with Ghee (Protein: 18g, Carbs: 70g, Fats: 15g, Energy: 480kcal)"
            ],
            "Dinner": [
                "Vegetable Khichdi with Papad (Protein: 18g, Carbs: 65g, Fats: 8g, Energy: 400kcal)",
                "Dal with 2 Roti (Protein: 22g, Carbs: 55g, Fats: 8g, Energy: 380kcal)",
                "Vegetable Stew with Appam (Protein: 15g, Carbs: 70g, Fats: 10g, Energy: 420kcal)",
                "Poha with Peanuts (Protein: 12g, Carbs: 60g, Fats: 10g, Energy: 380kcal)"
            ],
            "Snacks": [
                "Fruit Yogurt (200g) (Protein: 8g, Carbs: 45g, Fats: 5g, Energy: 250kcal)",
                "Roasted Makhana (40g) (Protein: 8g, Carbs: 35g, Fats: 5g, Energy: 220kcal)",
                "Buttermilk with Jeera (Protein: 5g, Carbs: 15g, Fats: 3g, Energy: 100kcal)",
                "Dry Fruits and Nuts (40g) (Protein: 8g, Carbs: 25g, Fats: 15g, Energy: 250kcal)"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Dalia with Milk and Nuts (Protein: 18g, Carbs: 70g, Fats: 12g, Energy: 450kcal)",
                "Pongal with Ghee and Cashews (Protein: 15g, Carbs: 75g, Fats: 15g, Energy: 480kcal)",
                "Banana Date Smoothie (Protein: 10g, Carbs: 80g, Fats: 8g, Energy: 420kcal)",
                "Vegetable Dosa with Chutney (Protein: 15g, Carbs: 65g, Fats: 10g, Energy: 400kcal)"
            ],
            "Lunch": [
                "Lemon Rice with Peanuts and Cashews (Protein: 18g, Carbs: 85g, Fats: 15g, Energy: 520kcal)",
                "Vegetable Pulao with Raita (Protein: 18g, Carbs: 80g, Fats: 12g, Energy: 480kcal)",
                "Curd Rice with Fried Gram (Protein: 18g, Carbs: 85g, Fats: 12g, Energy: 480kcal)",
                "Sambar Rice with Ghee and Papad (Protein: 20g, Carbs: 75g, Fats: 18g, Energy: 520kcal)"
            ],
            "Dinner": [
                "Vegetable Khichdi with Curd (Protein: 20g, Carbs: 70g, Fats: 10g, Energy: 450kcal)",
                "Dal with 2 Roti (Protein: 25g, Carbs: 60g, Fats: 10g, Energy: 420kcal)",
                "Vegetable Stew with Idiyappam (Protein: 15g, Carbs: 75g, Fats: 12g, Energy: 450kcal)",
                "Poha with Vegetables and Nuts (Protein: 15g, Carbs: 65g, Fats: 12g, Energy: 420kcal)"
            ],
            "Snacks": [
                "Fruit Salad with Honey (200g) (Protein: 3g, Carbs: 50g, Fats: 2g, Energy: 230kcal)",
                "Roasted Chana with Coconut (50g) (Protein: 15g, Carbs: 35g, Fats: 8g, Energy: 280kcal)",
                "Buttermilk with Mint (Protein: 6g, Carbs: 20g, Fats: 5g, Energy: 150kcal)",
                "Dry Fruits and Seeds (50g) (Protein: 10g, Carbs: 30g, Fats: 20g, Energy: 320kcal)"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Dalia with Vegetables and Ghee (Protein: 20g, Carbs: 75g, Fats: 15g, Energy: 500kcal)",
                "Pongal with Cashews and Raisins (Protein: 18g, Carbs: 80g, Fats: 18g, Energy: 520kcal)",
                "Banana Nut Smoothie with Honey (Protein: 12g, Carbs: 85g, Fats: 12g, Energy: 480kcal)",
                "Rava Dosa with Chutney and Sambar (Protein: 18g, Carbs: 70g, Fats: 15g, Energy: 480kcal)"
            ],
            "Lunch": [
                "Lemon Rice with Fried Gram (Protein: 20g, Carbs: 90g, Fats: 18g, Energy: 580kcal)",
                "Vegetable Biryani with Raita (Protein: 20g, Carbs: 85g, Fats: 15g, Energy: 550kcal)",
                "Curd Rice with Pickle and Papad (Protein: 18g, Carbs: 90g, Fats: 15g, Energy: 550kcal)",
                "Sambar Rice with Ghee and Vegetables (Protein: 22g, Carbs: 80g, Fats: 20g, Energy: 580kcal)"
            ],
            "Dinner": [
                "Vegetable Khichdi with Curd and Papad (Protein: 22g, Carbs: 75g, Fats: 15g, Energy: 520kcal)",
                "Dal with 2 Roti and Ghee (Protein: 25g, Carbs: 65g, Fats: 15g, Energy: 480kcal)",
                "Vegetable Stew with Appam and Coconut Milk (Protein: 18g, Carbs: 80g, Fats: 18g, Energy: 520kcal)",
                "Poha with Nuts and Seeds (Protein: 18g, Carbs: 70g, Fats: 15g, Energy: 480kcal)"
            ],
            "Snacks": [
                "Fruit Yogurt with Honey (200g) (Protein: 10g, Carbs: 55g, Fats: 8g, Energy: 320kcal)",
                "Roasted Makhana with Ghee (50g) (Protein: 10g, Carbs: 40g, Fats: 10g, Energy: 300kcal)",
                "Buttermilk with Jeera and Mint (Protein: 8g, Carbs: 25g, Fats: 8g, Energy: 200kcal)",
                "Dry Fruits and Nuts Mix (60g) (Protein: 12g, Carbs: 35g, Fats: 25g, Energy: 380kcal)"
            ]
        }
    },
    4: {  # Cardio (Complete 4 weeks)
        "Week 1": {
            "Breakfast": [
                "Fruit Smoothie with Seeds (Protein: 10g, Carbs: 50g, Fats: 8g, Energy: 300kcal)",
                "Vegetable Upma (Protein: 12g, Carbs: 55g, Fats: 5g, Energy: 320kcal)",
                "Poha with Peanuts (Protein: 10g, Carbs: 60g, Fats: 8g, Energy: 350kcal)",
                "Dosa with Chutney (Protein: 12g, Carbs: 45g, Fats: 10g, Energy: 320kcal)"
            ],
            "Lunch": [
                "Jeera Rice with Dal (Protein: 15g, Carbs: 70g, Fats: 8g, Energy: 400kcal)",
                "Vegetable Pulao (Protein: 12g, Carbs: 65g, Fats: 5g, Energy: 350kcal)",
                "Curd Rice (Protein: 10g, Carbs: 75g, Fats: 10g, Energy: 400kcal)",
                "Khichdi with Vegetables (Protein: 15g, Carbs: 60g, Fats: 8g, Energy: 380kcal)"
            ],
            "Dinner": [
                "Vegetable Soup with Toast (Protein: 10g, Carbs: 40g, Fats: 5g, Energy: 250kcal)",
                "Dal with 1 Roti (Protein: 15g, Carbs: 35g, Fats: 5g, Energy: 250kcal)",
                "Vegetable Stew (Protein: 8g, Carbs: 45g, Fats: 5g, Energy: 250kcal)",
                "Grilled Chicken (100g) with Salad (Protein: 30g, Carbs: 10g, Fats: 8g, Energy: 250kcal)"
            ],
            "Snacks": [
                "Coconut Water (300ml) (Protein: 2g, Carbs: 15g, Fats: 0g, Energy: 70kcal)",
                "Fruit Chaat (150g) (Protein: 2g, Carbs: 35g, Fats: 1g, Energy: 160kcal)",
                "Roasted Makhana (30g) (Protein: 5g, Carbs: 20g, Fats: 2g, Energy: 120kcal)",
                "Buttermilk (300ml) (Protein: 5g, Carbs: 10g, Fats: 2g, Energy: 80kcal)"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Banana Smoothie with Seeds (Protein: 12g, Carbs: 55g, Fats: 8g, Energy: 320kcal)",
                "Vegetable Vermicelli Upma (Protein: 15g, Carbs: 60g, Fats: 5g, Energy: 350kcal)",
                "Poha with Sprouts (Protein: 15g, Carbs: 55g, Fats: 5g, Energy: 320kcal)",
                "Dosa with Sambar (Protein: 15g, Carbs: 50g, Fats: 8g, Energy: 320kcal)"
            ],
            "Lunch": [
                "Lemon Rice with Peanuts (Protein: 15g, Carbs: 75g, Fats: 10g, Energy: 450kcal)",
                "Vegetable Khichdi (Protein: 18g, Carbs: 65g, Fats: 8g, Energy: 400kcal)",
                "Curd Rice with Vegetables (Protein: 12g, Carbs: 70g, Fats: 10g, Energy: 400kcal)",
                "Sambar Rice (Protein: 15g, Carbs: 65g, Fats: 8g, Energy: 380kcal)"
            ],
            "Dinner": [
                "Vegetable Soup with Bread (Protein: 12g, Carbs: 45g, Fats: 5g, Energy: 280kcal)",
                "Dal with Roti (Protein: 18g, Carbs: 40g, Fats: 5g, Energy: 280kcal)",
                "Vegetable Stew with Appam (Protein: 12g, Carbs: 60g, Fats: 8g, Energy: 350kcal)",
                "Poha with Vegetables (Protein: 12g, Carbs: 50g, Fats: 5g, Energy: 300kcal)"
            ],
            "Snacks": [
                "Coconut Water with Pulp (300ml) (Protein: 3g, Carbs: 20g, Fats: 2g, Energy: 100kcal)",
                "Fruit Yogurt (200g) (Protein: 8g, Carbs: 40g, Fats: 5g, Energy: 230kcal)",
                "Roasted Makhana (40g) (Protein: 8g, Carbs: 30g, Fats: 5g, Energy: 200kcal)",
                "Buttermilk with Jeera (Protein: 5g, Carbs: 15g, Fats: 3g, Energy: 100kcal)"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Fruit Smoothie with Chia Seeds (Protein: 12g, Carbs: 60g, Fats: 10g, Energy: 380kcal)",
                "Vegetable Oats Upma (Protein: 15g, Carbs: 65g, Fats: 5g, Energy: 350kcal)",
                "Poha with Peanuts and Coconut (Protein: 12g, Carbs: 60g, Fats: 10g, Energy: 380kcal)",
                "Dosa with Tomato Chutney (Protein: 12g, Carbs: 50g, Fats: 8g, Energy: 320kcal)"
            ],
            "Lunch": [
                "Jeera Rice with Dal and Salad (Protein: 18g, Carbs: 70g, Fats: 8g, Energy: 420kcal)",
                "Vegetable Pulao with Raita (Protein: 15g, Carbs: 65g, Fats: 8g, Energy: 380kcal)",
                "Curd Rice with Fried Gram (Protein: 15g, Carbs: 75g, Fats: 10g, Energy: 420kcal)",
                "Khichdi with Vegetables and Curd (Protein: 18g, Carbs: 65g, Fats: 8g, Energy: 400kcal)"
            ],
            "Dinner": [
                "Vegetable Soup with Multigrain Toast (Protein: 12g, Carbs: 50g, Fats: 5g, Energy: 300kcal)",
                "Dal with 1 Roti (Protein: 15g, Carbs: 40g, Fats: 5g, Energy: 280kcal)",
                "Vegetable Stew with Rice (Protein: 12g, Carbs: 60g, Fats: 8g, Energy: 350kcal)",
                "Grilled Fish (100g) with Salad (Protein: 25g, Carbs: 15g, Fats: 8g, Energy: 250kcal)"
            ],
            "Snacks": [
                "Coconut Water with Banana (Protein: 3g, Carbs: 40g, Fats: 2g, Energy: 180kcal)",
                "Fruit Chaat with Chia Seeds (150g) (Protein: 5g, Carbs: 45g, Fats: 5g, Energy: 230kcal)",
                "Roasted Makhana with Ghee (40g) (Protein: 8g, Carbs: 35g, Fats: 8g, Energy: 250kcal)",
                "Buttermilk with Mint (Protein: 5g, Carbs: 20g, Fats: 5g, Energy: 150kcal)"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Banana Date Smoothie with Almonds (Protein: 15g, Carbs: 70g, Fats: 12g, Energy: 450kcal)",
                "Vegetable Rava Upma with Peanuts (Protein: 18g, Carbs: 70g, Fats: 10g, Energy: 450kcal)",
                "Poha with Sprouts and Coconut (Protein: 18g, Carbs: 65g, Fats: 10g, Energy: 420kcal)",
                "Dosa with Sambar and Chutney (Protein: 18g, Carbs: 60g, Fats: 10g, Energy: 400kcal)"
            ],
            "Lunch": [
                "Lemon Rice with Cashews (Protein: 18g, Carbs: 80g, Fats: 15g, Energy: 520kcal)",
                "Vegetable Biryani with Raita (Protein: 18g, Carbs: 75g, Fats: 12g, Energy: 480kcal)",
                "Curd Rice with Vegetables and Fried Gram (Protein: 18g, Carbs: 80g, Fats: 12g, Energy: 480kcal)",
                "Sambar Rice with Ghee and Papad (Protein: 20g, Carbs: 75g, Fats: 15g, Energy: 500kcal)"
            ],
            "Dinner": [
                "Vegetable Soup with Multigrain Bread (Protein: 15g, Carbs: 55g, Fats: 8g, Energy: 350kcal)",
                "Dal with 1 Roti (Protein: 18g, Carbs: 45g, Fats: 8g, Energy: 320kcal)",
                "Vegetable Stew with Appam (Protein: 15g, Carbs: 70g, Fats: 10g, Energy: 420kcal)",
                "Grilled Chicken (120g) with Stir-fried Vegetables (Protein: 30g, Carbs: 20g, Fats: 8g, Energy: 280kcal)"
            ],
            "Snacks": [
                "Coconut Water with Pulp and Chia (300ml) (Protein: 5g, Carbs: 30g, Fats: 5g, Energy: 180kcal)",
                "Fruit Yogurt with Flaxseeds (200g) (Protein: 10g, Carbs: 50g, Fats: 8g, Energy: 300kcal)",
                "Roasted Makhana with Ghee and Pepper (50g) (Protein: 10g, Carbs: 40g, Fats: 10g, Energy: 300kcal)",
                "Buttermilk with Jeera and Mint (Protein: 6g, Carbs: 25g, Fats: 5g, Energy: 160kcal)"
            ]
        }
    },
    5: {  # General Fitness (Complete 4 weeks)
        "Week 1": {
            "Breakfast": [
                "Idli (3) with Sambar (Protein: 15g, Carbs: 50g, Fats: 5g, Energy: 300kcal)",
                "Poha with Vegetables (Protein: 8g, Carbs: 55g, Fats: 5g, Energy: 300kcal)",
                "Dalia with Milk (Protein: 12g, Carbs: 60g, Fats: 8g, Energy: 350kcal)",
                "Paratha (2) with Curd (Protein: 15g, Carbs: 65g, Fats: 10g, Energy: 400kcal)"
            ],
            "Lunch": [
                "Rice with Dal and Sabzi (Protein: 18g, Carbs: 70g, Fats: 8g, Energy: 420kcal)",
                "Roti (2) with Vegetable Curry (Protein: 15g, Carbs: 50g, Fats: 10g, Energy: 350kcal)",
                "Khichdi with Curd (Protein: 20g, Carbs: 60g, Fats: 8g, Energy: 400kcal)",
                "Curd Rice with Pickle (Protein: 12g, Carbs: 75g, Fats: 10g, Energy: 400kcal)"
            ],
            "Dinner": [
                "Vegetable Soup with Bread (Protein: 10g, Carbs: 40g, Fats: 5g, Energy: 250kcal)",
                "Dal with 2 Roti (Protein: 20g, Carbs: 50g, Fats: 5g, Energy: 320kcal)",
                "Vegetable Pulao with Raita (Protein: 15g, Carbs: 60g, Fats: 8g, Energy: 350kcal)",
                "Grilled Fish (100g) with Rice (Protein: 30g, Carbs: 50g, Fats: 10g, Energy: 400kcal)"
            ],
            "Snacks": [
                "Fruits (200g) (Protein: 2g, Carbs: 40g, Fats: 1g, Energy: 180kcal)",
                "Nuts (30g) (Protein: 8g, Carbs: 10g, Fats: 15g, Energy: 200kcal)",
                "Roasted Chana (50g) (Protein: 15g, Carbs: 30g, Fats: 5g, Energy: 220kcal)",
                "Buttermilk (300ml) (Protein: 5g, Carbs: 10g, Fats: 2g, Energy: 80kcal)"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Idli (3) with Chutney (Protein: 12g, Carbs: 55g, Fats: 5g, Energy: 300kcal)",
                "Dosa with Sambar (Protein: 15g, Carbs: 50g, Fats: 8g, Energy: 320kcal)",
                "Upma with Vegetables (Protein: 12g, Carbs: 60g, Fats: 8g, Energy: 350kcal)",
                "Pongal with Ghee (Protein: 15g, Carbs: 65g, Fats: 10g, Energy: 400kcal)"
            ],
            "Lunch": [
                "Rice with Sambar and Vegetables (Protein: 18g, Carbs: 75g, Fats: 8g, Energy: 450kcal)",
                "Roti (2) with Dal and Sabzi (Protein: 20g, Carbs: 55g, Fats: 10g, Energy: 380kcal)",
                "Khichdi with Papad (Protein: 18g, Carbs: 65g, Fats: 10g, Energy: 420kcal)",
                "Curd Rice with Pickle and Fried Gram (Protein: 18g, Carbs: 80g, Fats: 12g, Energy: 450kcal)"
            ],
            "Dinner": [
                "Vegetable Soup with Toast (Protein: 12g, Carbs: 45g, Fats: 5g, Energy: 280kcal)",
                "Dal with 2 Roti (Protein: 22g, Carbs: 55g, Fats: 8g, Energy: 380kcal)",
                "Vegetable Pulao with Raita (Protein: 18g, Carbs: 65g, Fats: 10g, Energy: 420kcal)",
                "Grilled Chicken (120g) with Rice (Protein: 35g, Carbs: 55g, Fats: 12g, Energy: 450kcal)"
            ],
            "Snacks": [
                "Fruit Salad (200g) (Protein: 3g, Carbs: 45g, Fats: 2g, Energy: 200kcal)",
                "Nuts and Seeds (40g) (Protein: 10g, Carbs: 15g, Fats: 20g, Energy: 280kcal)",
                "Roasted Makhana (50g) (Protein: 10g, Carbs: 35g, Fats: 5g, Energy: 230kcal)",
                "Buttermilk with Jeera (Protein: 6g, Carbs: 15g, Fats: 5g, Energy: 130kcal)"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Idli (4) with Sambar (Protein: 18g, Carbs: 60g, Fats: 5g, Energy: 350kcal)",
                "Dosa with Chutney and Sambar (Protein: 18g, Carbs: 55g, Fats: 10g, Energy: 380kcal)",
                "Upma with Peanuts and Vegetables (Protein: 15g, Carbs: 65g, Fats: 10g, Energy: 400kcal)",
                "Pongal with Cashews and Ghee (Protein: 18g, Carbs: 70g, Fats: 15g, Energy: 480kcal)"
            ],
            "Lunch": [
                "Rice with Rasam and Vegetables (Protein: 18g, Carbs: 80g, Fats: 8g, Energy: 450kcal)",
                "Roti (2) with Paneer Sabzi (Protein: 25g, Carbs: 50g, Fats: 15g, Energy: 420kcal)",
                "Khichdi with Curd and Papad (Protein: 22g, Carbs: 70g, Fats: 12g, Energy: 480kcal)",
                "Curd Rice with Fried Gram and Pickle (Protein: 22g, Carbs: 85g, Fats: 15g, Energy: 520kcal)"
            ],
            "Dinner": [
                "Vegetable Soup with Multigrain Bread (Protein: 15g, Carbs: 50g, Fats: 8g, Energy: 320kcal)",
                "Dal with 2 Roti (Protein: 25g, Carbs: 60g, Fats: 10g, Energy: 420kcal)",
                "Vegetable Pulao with Raita (Protein: 20g, Carbs: 70g, Fats: 12g, Energy: 480kcal)",
                "Grilled Fish (150g) with Rice and Salad (Protein: 40g, Carbs: 60g, Fats: 15g, Energy: 520kcal)"
            ],
            "Snacks": [
                "Fruit Salad with Honey (200g) (Protein: 3g, Carbs: 50g, Fats: 2g, Energy: 230kcal)",
                "Nuts and Dry Fruits (50g) (Protein: 12g, Carbs: 25g, Fats: 25g, Energy: 350kcal)",
                "Roasted Chana with Coconut (60g) (Protein: 18g, Carbs: 40g, Fats: 10g, Energy: 320kcal)",
                "Buttermilk with Mint and Jeera (Protein: 8g, Carbs: 20g, Fats: 8g, Energy: 180kcal)"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Idli (4) with Sambar and Chutney (Protein: 20g, Carbs: 65g, Fats: 8g, Energy: 400kcal)",
                "Dosa with Potato Masala (Protein: 18g, Carbs: 60g, Fats: 12g, Energy: 420kcal)",
                "Upma with Vegetables and Nuts (Protein: 18g, Carbs: 70g, Fats: 15g, Energy: 480kcal)",
                "Pongal with Ghee, Cashews and Raisins (Protein: 20g, Carbs: 75g, Fats: 18g, Energy: 520kcal)"
            ],
            "Lunch": [
                "Rice with Sambar, Rasam and Vegetables (Protein: 22g, Carbs: 85g, Fats: 10g, Energy: 520kcal)",
                "Roti (2) with Dal Makhani and Salad (Protein: 28g, Carbs: 60g, Fats: 18g, Energy: 480kcal)",
                "Khichdi with Curd, Papad and Pickle (Protein: 25g, Carbs: 75g, Fats: 15g, Energy: 520kcal)",
                "Curd Rice with Fried Gram, Pickle and Papad (Protein: 25g, Carbs: 90g, Fats: 18g, Energy: 580kcal)"
            ],
            "Dinner": [
                "Vegetable Soup with Garlic Bread (Protein: 18g, Carbs: 60g, Fats: 12g, Energy: 420kcal)",
                "Dal with 2 Roti and Ghee (Protein: 28g, Carbs: 65g, Fats: 15g, Energy: 480kcal)",
                "Vegetable Pulao with Raita and Papad (Protein: 22g, Carbs: 75g, Fats: 15g, Energy: 520kcal)",
                "Grilled Chicken (150g) with Rice and Stir-fried Vegetables (Protein: 45g, Carbs: 65g, Fats: 18g, Energy: 580kcal)"
            ],
            "Snacks": [
                "Fruit Salad with Yogurt and Honey (200g) (Protein: 8g, Carbs: 60g, Fats: 5g, Energy: 320kcal)",
                "Nuts, Seeds and Dry Fruits (60g) (Protein: 15g, Carbs: 35g, Fats: 30g, Energy: 420kcal)",
                "Roasted Chana with Coconut and Spices (70g) (Protein: 20g, Carbs: 45g, Fats: 12g, Energy: 380kcal)",
                "Buttermilk with Jeera, Mint and Ginger (Protein: 10g, Carbs: 25g, Fats: 10g, Energy: 220kcal)"
            ]
        }
    }
}
# Base reps and timings by experience level
BASE_REPS = {0: 10, 1: 20, 2: 30}  # Beginner, Intermediate, Advanced
BASE_TIMINGS = {0: 20, 1: 40, 2: 60}  # Beginner, Intermediate, Advanced
WEEK_INCREMENTS = [0, 2, 4, 6]
MONTHLY_INCREMENT = 6

def calculate_bmi(weight, height):
    # BMI formula: weight (kg) / height (m)^2
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

HIIT_GOAL_MAPPING = {
    "beginner": {
        "sedentary": list(range(180, 185)),
        "active": list(range(185, 190)),
        "highly_active": list(range(190, 195))
    },
    "intermediate": {
        "sedentary": list(range(190, 195)),
        "active": list(range(195, 200)),
        "highly_active": list(range(200, 205))
    },
    "advanced": {
        "sedentary": list(range(200, 205)),
        "active": list(range(205, 210)),
        "highly_active": list(range(210, 215))
    }
}

def generate_hiit_workout(exp_level, week=None, intensity_multiplier=1.0, activity=None):
    """Generate a HIIT workout based on experience level and activity level"""
    exp_key = ["beginner", "intermediate", "advanced"][exp_level]
    exercise_ids = HIIT_GOAL_MAPPING[exp_key][activity]  # Use activity level to get exercises
    
    # Select 2-3 exercises for a complete HIIT circuit for beginners
    if exp_level == 0:  # Beginner
        selected_ids = random.sample(exercise_ids, min(len(exercise_ids), random.randint(2, 3)))
    else:  # Intermediate and Advanced
        selected_ids = random.sample(exercise_ids, min(len(exercise_ids), random.randint(4, 6)))

    exercises = [HIIT_EXERCISES[ex_id] for ex_id in selected_ids]
    
    # Determine work/rest intervals based on experience
    work_rest = {
        0: (20 * intensity_multiplier, 40),  # Beginner: 20s work, 40s rest
        1: (30 * intensity_multiplier, 30),  # Intermediate: 30s work, 30s rest
        2: (40 * intensity_multiplier, 20)   # Advanced: 40s work, 20s rest
    }
    work, rest = work_rest[exp_level]
    
    # Apply weekly progression
    if week:
        work += WEEK_INCREMENTS[min(week-1, 3)]
        rest = max(10, rest - WEEK_INCREMENTS[min(week-1, 3)]//2)
    
    return [{
        "exercise": ex[0],
        "work_sec": work,
        "rest_sec": rest,
        "sets": 3 if exp_level < 2 else 4
    } for ex in exercises]

@app.route('/generate-hiit-plan', methods=['POST'])
def generate_hiit_plan():
    try:
        data = request.json
        exp = int(data['experience_level'])
        
        # Generate 4-week progressive HIIT plan
        plan = {}
        for week in range(1, 5):
            plan[f"Week {week}"] = {
                "Monday": generate_hiit_workout(exp, week),
                "Wednesday": generate_hiit_workout(exp, week),
                "Friday": generate_hiit_workout(exp, week),
                "Notes": f"Rest days: Tuesday/Thursday. Weekend: Active recovery (walking/yoga)"
            }
        
        return jsonify({
            "hiit_plan": plan,
            "instructions": {
                "beginner": "Complete 3 rounds with 2min rest between circuits",
                "intermediate": "Complete 4 rounds with 1min rest between circuits",
                "advanced": "Complete 5 rounds with 30s rest between circuits"
            }[["beginner", "intermediate", "advanced"][exp]]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_exercises_by_goal_and_experience(goal, exp):
    # Define the mapping of goals to experience levels
    goal_experience_mapping = {
        0: {  # Gain Muscle
            "beginner": [0, 1, 3, 4, 6, 7, 9],  # Only beginner-friendly exercises
            "intermediate": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            "advanced": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        },
        1: {  # Lose Fat
            "beginner": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
            "intermediate": [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
            "advanced": [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
        },
        2: {  # Improve Strength
            "beginner": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
            "intermediate": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
            "advanced": [80, 81, 82, 83, 84, 85, 86, 87, 88, 89]
        },
        3: {  # Improve Stamina
            "beginner": [90, 91, 92, 93, 94, 95, 96, 97, 98, 99],
            "intermediate": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            "advanced": [110, 111, 112, 113, 114, 115, 116, 117, 118, 119]
        },
        4: {  # Cardio
            "beginner": [120, 121, 122, 123, 124, 125, 126, 127, 128, 129],
            "intermediate": [130, 131, 132, 133, 134, 135, 136, 137, 138, 139],
            "advanced": [140, 141, 142, 143, 144, 145, 146, 147, 148, 149]
        },
        5: {  # General Fitness
            "beginner": [150, 151, 152, 153, 154, 155, 156, 157, 158, 159],
            "intermediate": [160, 161, 162, 163, 164, 165, 166, 167, 168, 169],
            "advanced": [170, 171, 172, 173, 174, 175, 176, 177, 178, 179]
        }
    }

    # Get the list of exercise indices based on the user's goal and experience level
    exercise_indices = goal_experience_mapping.get(goal, {}).get(
        ["beginner", "intermediate", "advanced"][exp], []
    )

    # Return the corresponding exercises
    return [EXERCISES[i] for i in exercise_indices]

def generate_workout(age, exp, activity, goal, week=None):
    # Get exercises based on goal and experience
    selected_exercises = get_exercises_by_goal_and_experience(goal, exp)

    if not selected_exercises:
        print(f"No exercises found for goal: {goal} and experience level: {exp}")
        return [], [], []  # Return empty lists if no exercises are found

    # Randomly select exercises for warmup, main, and HIIT


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Ideal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"
    
def generate_workout(age, exp, activity, goal, week=None):
    # Get exercises based on goal and experience
    selected_exercises = get_exercises_by_goal_and_experience(goal, exp)

    if not selected_exercises:
        print(f"No exercises found for goal: {goal} and experience level: {exp}")
        return [], [], []  # Return empty lists if no exercises are found

    # Adjust the intensity of the workout based on the user's activity level
    if activity == "sedentary":
        intensity_multiplier = 0.5
    elif activity == "active":
        intensity_multiplier = 1.0
    elif activity == "highly_active":
        intensity_multiplier = 1.5

    # Randomly select exercises for warmup, main, and HIIT
    warmup_ex = random.sample(selected_exercises, min(2, len(selected_exercises)))
    main_ex = random.sample(selected_exercises, min(4, len(selected_exercises)))

    # Select HIIT exercises based on experience level and activity level
    hiit_ex = generate_hiit_workout(exp, week, intensity_multiplier, activity)

    # Format the workouts
    warmup = [(ex[0], 2, 10) for ex in warmup_ex]  # 2 sets of 10 reps
    main = [(ex[0], 3, 10) for ex in main_ex]  # 3 sets of 10 reps

    return warmup, main, hiit_ex  # Return HIIT exercises directly # Return HIIT exercises directly

def generate_month_plan(age, exp, activity, goal, rest_days):
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    plan = {}

    for week in range(1, 5):
        week_plan = {}
        for day_index in range(7):
            day_name = day_names[day_index]
            if day_name in rest_days:
                week_plan[day_name] = "Rest Day"
            else:
                warmup, main, hiit = generate_workout(age, exp, activity, goal)

                # Format HIIT workouts with work/rest intervals
                formatted_hiit = []
                for exercise in hiit:
                    formatted_hiit.append(f"{exercise['sets']}x ({exercise['work_sec']}s {exercise['exercise']}, {exercise['rest_sec']}s Rest)")

                week_plan[day_name] = {
                    "Warmup": [f"2x{val}r {ex}" for ex, _, val in warmup],
                    "Main": [f"{sets}x{val}r {ex}" for ex, sets, val in main],
                    "HIIT": formatted_hiit,
                    "Cooldown": ["30s Hamstring Stretch", "30s Quad Stretch"]
                }
        plan[f"Week {week}"] = week_plan

    return plan

def save_response_to_json(data, filename='responses.json'):
    try:
        # Get absolute path to avoid any directory confusion
        file_path = Path(filename).absolute()
        print(f"Attempting to save to: {file_path}")
        
        # Initialize with empty list if file doesn't exist
        if not file_path.exists():
            print("File doesn't exist, creating new one")
            with open(file_path, 'w') as f:
                json.dump([], f)
        
        # Read existing data
        with open(file_path, 'r') as f:
            try:
                existing_data = json.load(f)
                print(f"Successfully read {len(existing_data)} existing entries")
            except json.JSONDecodeError:
                print("File was empty/corrupt, starting fresh")
                existing_data = []
        
        # Append new data
        existing_data.append(data)
        
        # Write back to file
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=4)
            print(f"Successfully saved new data (total entries: {len(existing_data)})")
            
        return True
        
    except Exception as e:
        print(f"ERROR saving to JSON: {str(e)}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-workout', methods=['POST'])
def generate_workout_route():
    try:
        data = request.json
        age = int(data['age'])
        height = int(data['height'])
        weight = int(data['weight'])
        exp = int(data['experience_level'])
        goal = int(data['fitness_goal'])
        activity = data['activity_level']
        rest_days = data['rest_days']  # Get the rest days from the request

           # Backend validation for exactly 2 rest days
        if len(rest_days) != 2:
            return jsonify({"error": "Exactly 2 rest days must be selected"}), 400

        # Rest of your existing validation and logic...
        if not all([age, height, weight, exp is not None, goal is not None, activity]):
            return jsonify({"error": "All fields are required"}), 400

        # Calculate BMI
        bmi = calculate_bmi(weight, height)
        bmi_category = get_bmi_category(bmi)

        # Generate workout plan
        workout_plan = generate_month_plan(age, exp, activity, goal, rest_days)  # Pass rest_days to the function

        # Prepare response data
        response_data = {
            "user_details": {
                "age": age,
                "height": height,
                "weight": weight,
                "experience_level": exp,
                "fitness_goal": goal,
                "activity_level": activity,
                "bmi": bmi,
                "bmi_category": bmi_category
            },
            "workout_plan": workout_plan,
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Save response to JSON file
        save_success = save_response_to_json(response_data)
        if not save_success:
            print("Warning: Failed to save to JSON file")

        return jsonify(response_data)

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        return jsonify({"error": str(e)}), 400

@app.route('/generate-diet-plan', methods=['POST'])
def generate_diet_plan():
    data = request.json
    exp = int(data['experience_level'])
    goal = int(data['fitness_goal'])

    # Generate diet plan based on the user's goal
    diet_plan = DIET_PLANS.get(goal, {})

    # Prepare the response with diet plans for all weeks
    return jsonify({"diet_plan": diet_plan})  

if __name__ == '__main__':
    app.run(debug=True)
   
