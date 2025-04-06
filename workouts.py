from flask import Flask, request, jsonify, render_template
import random
import json
import os
from pathlib import Path
import datetime


app = Flask(__name__)

# Minimal EXERCISES dictionary
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

    # ===== General Fitness (150-179) =====
    # Beginner (150-159)
    150: ("⏰ Standing Side Stretch", "timing"),
    151: ("⏳ Neck Stretches", "timing"),
    152: ("🕰️ Seated Forward Fold", "timing"),
    153: ("🧘🏻‍♀️ Cat-Cow Stretch", "reps"),
    154: ("⏰ Standing Quad Stretch", "timing"),
    155: ("⏳ Seated Spinal Twist", "timing"),
    156: ("💪 Shoulder Rolls", "reps"),
    157: ("🏋️ Ankle Rolls", "reps"),
    158: ("🕰️ Wrist Stretches", "timing"),
    159: ("⏰ Deep Breathing Exercises", "timing"),

    # Advanced (170-179)
    170: ("⏰ Handstand Hold (Wall)", "timing"),
    171: ("⏳ L-Sit Progressions", "timing"),
    172: ("🕰️ Bridge Hold", "timing"),
    173: ("⏰ V-Sit Progressions", "timing"),
    174: ("⏳ Towel Assisted Splits", "timing"),
    175: ("🤸‍♂️ Backbend Walkouts", "reps"),
    176: ("💀 Ninja Jump Rolls", "reps"),
    177: ("🏋️‍♂️ Parkour Basics (Wall Jumps)", "reps"),
    178: ("⏰ Capoeira Movements", "timing"),
    179: ("🕰️ Advanced Yoga Flow", "timing")
}
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
                "Moong dal chilla with mint chutney",
                "Idli with sambar and coconut chutney",
                "Ragi porridge with banana and almonds",
                "Poha with peanuts and vegetables",
                "Besan cheela with pudina chutney",
                "Dosa with sambar and tomato chutney",
                "Oats upma with vegetables"
            ],
            "Lunch": [
                "Brown rice with chicken curry and mixed vegetables",
                "Roti with dal and bhindi sabzi",
                "Quinoa khichdi with fish curry",
                "Soya chunks curry with jeera rice",
                "Jeera rice with rajma",
                "Missi roti with kadhi",
                "Vegetable pulao with raita"
            ],
            "Dinner": [
                "Grilled chicken with bajra roti and palak",
                "Fish curry with red rice",
                "Dal tadka with jowar roti",
                "Paneer bhurji with multigrain roti",
                "Soya keema with roti",
                "Dal makhani with jeera rice",
                "Vegetable stew with appam"
            ],
            "Snacks": [
                "Sprouts chaat",
                "Roasted chana with coconut",
                "Curd with flaxseeds and jaggery",
                "Makhana (fox nuts) with ghee",
                "Fruit with peanut butter",
                "Roasted makhana",
                "Paneer tikka"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Stuffed paratha with curd",
                "Egg omelette with multigrain toast",
                "Banana peanut butter smoothie",
                "Chana dal chilla",
                "Vegetable vermicelli upma",
                "Pongal with sambar",
                "Methi thepla with curd"
            ],
            "Lunch": [
                "Egg curry with millet roti",
                "Chicken sukka with jowar roti",
                "Palak paneer with bajra roti",
                "Soya biryani with raita",
                "Fish fry with quinoa",
                "Dal khichdi with ghee",
                "Keema paratha with curd"
            ],
            "Dinner": [
                "Grilled chicken with vegetables",
                "Palak paneer with roti",
                "Egg curry with rice",
                "Dal khichdi with ghee",
                "Soya chunks biryani",
                "Paneer tikka with roti",
                "Mushroom curry with rice"
            ],
            "Snacks": [
                "Dry fruit milkshake",
                "Sprouted moong salad",
                "Peanut ladoo",
                "Curd with chia seeds",
                "Roasted makhana",
                "Boiled egg whites",
                "Nuts and seeds mix"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Paneer paratha with curd",
                "Egg bhurji with multigrain toast",
                "Banana almond smoothie",
                "Vegetable oats upma",
                "Rava idli with sambar",
                "Stuffed besan chilla",
                "Poha with sprouts"
            ],
            "Lunch": [
                "Chicken curry with brown rice",
                "Dal tadka with bajra roti",
                "Soya biryani with raita",
                "Fish curry with quinoa",
                "Egg fried rice",
                "Paneer butter masala with roti",
                "Keema with jeera rice"
            ],
            "Dinner": [
                "Grilled fish with vegetables",
                "Dal makhani with roti",
                "Chicken stew with appam",
                "Vegetable khichdi with curd",
                "Egg bhurji with roti",
                "Soya chunks curry with rice",
                "Palak chicken with roti"
            ],
            "Snacks": [
                "Protein shake with dates",
                "Roasted chana with coconut",
                "Paneer cubes with mint chutney",
                "Fruit and nut yogurt",
                "Makhana chaat",
                "Sprouts salad",
                "Peanut butter with banana"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Vegetable stuffed paratha with curd",
                "Egg white omelette with toast",
                "Ragi malt with nuts",
                "Moong dal dosa with chutney",
                "Besan chilla with mint chutney",
                "Vegetable upma with peanuts",
                "Poha with sprouts and nuts"
            ],
            "Lunch": [
                "Brown rice with chicken curry",
                "Dal tadka with jowar roti",
                "Soya chunks biryani",
                "Fish curry with quinoa",
                "Paneer butter masala with roti",
                "Egg curry with rice",
                "Keema with jeera rice"
            ],
            "Dinner": [
                "Grilled chicken with vegetables",
                "Palak paneer with roti",
                "Dal khichdi with ghee",
                "Soya chunks curry with rice",
                "Fish fry with quinoa",
                "Vegetable pulao with raita",
                "Egg bhurji with roti"
            ],
            "Snacks": [
                "Dry fruit milkshake",
                "Sprouted moong salad",
                "Peanut ladoo",
                "Curd with chia seeds",
                "Roasted makhana",
                "Boiled egg whites",
                "Nuts and seeds mix"
            ]
        }
    },
    1: {  # Lose Fat (Complete 4 weeks)
        "Week 1": {
            "Breakfast": [
                "Vegetable dalia",
                "Moong dal chilla",
                "Fruit smoothie with flaxseeds",
                "Vegetable upma",
                "Besan cheela",
                "Dosa with coconut chutney",
                "Poha with vegetables"
            ],
            "Lunch": [
                "Brown rice with dal and lauki sabzi",
                "Jowar roti with palak dal",
                "Vegetable sambar with rice",
                "Grilled fish with salad",
                "Missi roti with kadhi",
                "Vegetable khichdi",
                "Dal with barley roti"
            ],
            "Dinner": [
                "Vegetable soup with multigrain roti",
                "Stir-fried vegetables with paneer",
                "Dal with barley roti",
                "Chicken clear soup with vegetables",
                "Vegetable stew with appam",
                "Grilled fish with salad",
                "Moong dal chilla with chutney"
            ],
            "Snacks": [
                "Cucumber slices with hummus",
                "Roasted chana",
                "Buttermilk with jeera",
                "Fruit chaat",
                "Sprouts salad",
                "Green tea with nuts",
                "Vegetable soup"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Ragi porridge with fruits",
                "Vegetable oats upma",
                "Moong dal chilla",
                "Fruit salad with flaxseeds",
                "Besan cheela with mint chutney",
                "Dosa with sambar",
                "Poha with vegetables"
            ],
            "Lunch": [
                "Quinoa khichdi with vegetables",
                "Jowar roti with lauki sabzi",
                "Vegetable sambar with brown rice",
                "Grilled chicken with salad",
                "Missi roti with kadhi",
                "Dal with bajra roti",
                "Vegetable pulao with raita"
            ],
            "Dinner": [
                "Vegetable soup with multigrain roti",
                "Stir-fried paneer with vegetables",
                "Dal with jowar roti",
                "Chicken clear soup with vegetables",
                "Vegetable stew with appam",
                "Grilled fish with salad",
                "Moong dal chilla with chutney"
            ],
            "Snacks": [
                "Cucumber carrot sticks",
                "Roasted makhana",
                "Buttermilk with jeera",
                "Fruit salad",
                "Sprouts chaat",
                "Green tea with nuts",
                "Vegetable soup"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Vegetable dalia",
                "Moong dal chilla",
                "Fruit smoothie with flaxseeds",
                "Vegetable upma",
                "Besan cheela",
                "Dosa with coconut chutney",
                "Poha with vegetables"
            ],
            "Lunch": [
                "Brown rice with dal and lauki sabzi",
                "Jowar roti with palak dal",
                "Vegetable sambar with rice",
                "Grilled fish with salad",
                "Missi roti with kadhi",
                "Vegetable khichdi",
                "Dal with barley roti"
            ],
            "Dinner": [
                "Vegetable soup with multigrain roti",
                "Stir-fried vegetables with paneer",
                "Dal with barley roti",
                "Chicken clear soup with vegetables",
                "Vegetable stew with appam",
                "Grilled fish with salad",
                "Moong dal chilla with chutney"
            ],
            "Snacks": [
                "Cucumber slices with hummus",
                "Roasted chana",
                "Buttermilk with jeera",
                "Fruit chaat",
                "Sprouts salad",
                "Green tea with nuts",
                "Vegetable soup"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Ragi porridge with fruits",
                "Vegetable oats upma",
                "Moong dal chilla",
                "Fruit salad with flaxseeds",
                "Besan cheela with mint chutney",
                "Dosa with sambar",
                "Poha with vegetables"
            ],
            "Lunch": [
                "Quinoa khichdi with vegetables",
                "Jowar roti with lauki sabzi",
                "Vegetable sambar with brown rice",
                "Grilled chicken with salad",
                "Missi roti with kadhi",
                "Dal with bajra roti",
                "Vegetable pulao with raita"
            ],
            "Dinner": [
                "Vegetable soup with multigrain roti",
                "Stir-fried paneer with vegetables",
                "Dal with jowar roti",
                "Chicken clear soup with vegetables",
                "Vegetable stew with appam",
                "Grilled fish with salad",
                "Moong dal chilla with chutney"
            ],
            "Snacks": [
                "Cucumber carrot sticks",
                "Roasted makhana",
                "Buttermilk with jeera",
                "Fruit salad",
                "Sprouts chaat",
                "Green tea with nuts",
                "Vegetable soup"
            ]
        }
    },
    2: {  # Improve Strength (Complete 4 weeks)
        "Week 1": {
            "Breakfast": [
                "Paneer paratha with curd",
                "Egg bhurji with multigrain toast",
                "Banana smoothie with almond butter",
                "Chana dal chilla",
                "Vegetable stuffed paratha",
                "Egg omelette with toast",
                "Poha with peanuts and vegetables"
            ],
            "Lunch": [
                "Brown rice with chicken curry",
                "Dal tadka with bajra roti",
                "Soya biryani with raita",
                "Fish curry with quinoa",
                "Egg fried rice",
                "Paneer butter masala with roti",
                "Keema with jeera rice"
            ],
            "Dinner": [
                "Grilled chicken with vegetables",
                "Palak paneer with roti",
                "Egg curry with rice",
                "Dal khichdi with ghee",
                "Soya chunks biryani",
                "Paneer tikka with roti",
                "Mushroom curry with rice"
            ],
            "Snacks": [
                "Sprouted moong salad",
                "Peanut ladoo",
                "Curd with chia seeds",
                "Roasted makhana",
                "Protein shake",
                "Boiled egg whites",
                "Nuts and seeds mix"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Vegetable stuffed paratha with curd",
                "Egg white omelette with toast",
                "Ragi malt with nuts",
                "Moong dal dosa with chutney",
                "Besan chilla with mint chutney",
                "Vegetable upma with peanuts",
                "Poha with sprouts and nuts"
            ],
            "Lunch": [
                "Brown rice with chicken curry",
                "Dal tadka with jowar roti",
                "Soya chunks biryani",
                "Fish curry with quinoa",
                "Paneer butter masala with roti",
                "Egg curry with rice",
                "Keema with jeera rice"
            ],
            "Dinner": [
                "Grilled chicken with vegetables",
                "Palak paneer with roti",
                "Dal khichdi with ghee",
                "Soya chunks curry with rice",
                "Fish fry with quinoa",
                "Vegetable pulao with raita",
                "Egg bhurji with roti"
            ],
            "Snacks": [
                "Dry fruit milkshake",
                "Sprouted moong salad",
                "Peanut ladoo",
                "Curd with chia seeds",
                "Roasted makhana",
                "Boiled egg whites",
                "Nuts and seeds mix"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Paneer paratha with curd",
                "Egg bhurji with multigrain toast",
                "Banana smoothie with almond butter",
                "Chana dal chilla",
                "Vegetable stuffed paratha",
                "Egg omelette with toast",
                "Poha with peanuts and vegetables"
            ],
            "Lunch": [
                "Brown rice with chicken curry",
                "Dal tadka with bajra roti",
                "Soya biryani with raita",
                "Fish curry with quinoa",
                "Egg fried rice",
                "Paneer butter masala with roti",
                "Keema with jeera rice"
            ],
            "Dinner": [
                "Grilled chicken with vegetables",
                "Palak paneer with roti",
                "Egg curry with rice",
                "Dal khichdi with ghee",
                "Soya chunks biryani",
                "Paneer tikka with roti",
                "Mushroom curry with rice"
            ],
            "Snacks": [
                "Sprouted moong salad",
                "Peanut ladoo",
                "Curd with chia seeds",
                "Roasted makhana",
                "Protein shake",
                "Boiled egg whites",
                "Nuts and seeds mix"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Vegetable stuffed paratha with curd",
                "Egg white omelette with toast",
                "Ragi malt with nuts",
                "Moong dal dosa with chutney",
                "Besan chilla with mint chutney",
                "Vegetable upma with peanuts",
                "Poha with sprouts and nuts"
            ],
            "Lunch": [
                "Brown rice with chicken curry",
                "Dal tadka with jowar roti",
                "Soya chunks biryani",
                "Fish curry with quinoa",
                "Paneer butter masala with roti",
                "Egg curry with rice",
                "Keema with jeera rice"
            ],
            "Dinner": [
                "Grilled chicken with vegetables",
                "Palak paneer with roti",
                "Dal khichdi with ghee",
                "Soya chunks curry with rice",
                "Fish fry with quinoa",
                "Vegetable pulao with raita",
                "Egg bhurji with roti"
            ],
            "Snacks": [
                "Dry fruit milkshake",
                "Sprouted moong salad",
                "Peanut ladoo",
                "Curd with chia seeds",
                "Roasted makhana",
                "Boiled egg whites",
                "Nuts and seeds mix"
            ]
        }
    },
    3: {  # Improve Stamina (Complete 4 weeks)
        "Week 1": {
            "Breakfast": [
                "Dalia with vegetables",
                "Pongal with coconut chutney",
                "Banana oats smoothie",
                "Vegetable uttapam",
                "Idli with sambar",
                "Poha with vegetables",
                "Dosa with chutney"
            ],
            "Lunch": [
                "Lemon rice with peanuts",
                "Vegetable khichdi",
                "Curd rice with pickle",
                "Sambar rice",
                "Jeera rice with dal",
                "Vegetable pulao",
                "Khichdi"
            ],
            "Dinner": [
                "Vegetable pulao with raita",
                "Dal with roti",
                "Vegetable soup with bread",
                "Poha with vegetables",
                "Vegetable soup with toast",
                "Dal with roti",
                "Vegetable stew"
            ],
            "Snacks": [
                "Fruit salad",
                "Roasted chana",
                "Buttermilk",
                "Dry fruits",
                "Coconut water",
                "Fruit chaat",
                "Roasted makhana"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Vegetable upma",
                "Pongal with sambar",
                "Banana smoothie with flaxseeds",
                "Rava idli with chutney",
                "Dalia with milk",
                "Poha with peanuts",
                "Dosa with sambar"
            ],
            "Lunch": [
                "Vegetable biryani with raita",
                "Dal khichdi",
                "Curd rice with vegetables",
                "Sambar rice with papad",
                "Jeera rice with vegetables",
                "Vegetable pulao with raita",
                "Khichdi with curd"
            ],
            "Dinner": [
                "Vegetable soup with bread",
                "Dal with roti",
                "Vegetable stew with appam",
                "Poha with vegetables",
                "Vegetable khichdi",
                "Dal with rice",
                "Vegetable pulao"
            ],
            "Snacks": [
                "Fruit yogurt",
                "Roasted makhana",
                "Buttermilk with jeera",
                "Dry fruits and nuts",
                "Coconut water",
                "Fruit salad",
                "Roasted chana"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Dalia with vegetables",
                "Pongal with coconut chutney",
                "Banana oats smoothie",
                "Vegetable uttapam",
                "Idli with sambar",
                "Poha with vegetables",
                "Dosa with chutney"
            ],
            "Lunch": [
                "Lemon rice with peanuts",
                "Vegetable khichdi",
                "Curd rice with pickle",
                "Sambar rice",
                "Jeera rice with dal",
                "Vegetable pulao",
                "Khichdi"
            ],
            "Dinner": [
                "Vegetable pulao with raita",
                "Dal with roti",
                "Vegetable soup with bread",
                "Poha with vegetables",
                "Vegetable soup with toast",
                "Dal with roti",
                "Vegetable stew"
            ],
            "Snacks": [
                "Fruit salad",
                "Roasted chana",
                "Buttermilk",
                "Dry fruits",
                "Coconut water",
                "Fruit chaat",
                "Roasted makhana"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Vegetable upma",
                "Pongal with sambar",
                "Banana smoothie with flaxseeds",
                "Rava idli with chutney",
                "Dalia with milk",
                "Poha with peanuts",
                "Dosa with sambar"
            ],
            "Lunch": [
                "Vegetable biryani with raita",
                "Dal khichdi",
                "Curd rice with vegetables",
                "Sambar rice with papad",
                "Jeera rice with vegetables",
                "Vegetable pulao with raita",
                "Khichdi with curd"
            ],
            "Dinner": [
                "Vegetable soup with bread",
                "Dal with roti",
                "Vegetable stew with appam",
                "Poha with vegetables",
                "Vegetable khichdi",
                "Dal with rice",
                "Vegetable pulao"
            ],
            "Snacks": [
                "Fruit yogurt",
                "Roasted makhana",
                "Buttermilk with jeera",
                "Dry fruits and nuts",
                "Coconut water",
                "Fruit salad",
                "Roasted chana"
            ]
        }
    },
    4: {  # Cardio (Complete 4 weeks)
        "Week 1": {
            "Breakfast": [
                "Fruit smoothie with seeds",
                "Vegetable upma",
                "Poha with peanuts",
                "Dosa with chutney",
                "Idli with sambar",
                "Poha with vegetables",
                "Dalia with milk"
            ],
            "Lunch": [
                "Jeera rice with dal",
                "Vegetable pulao",
                "Curd rice",
                "Khichdi",
                "Rice with dal and sabzi",
                "Roti with vegetable curry",
                "Khichdi with vegetables"
            ],
            "Dinner": [
                "Vegetable soup with toast",
                "Dal with roti",
                "Vegetable stew",
                "Grilled chicken with salad",
                "Vegetable soup with bread",
                "Dal with roti",
                "Vegetable pulao"
            ],
            "Snacks": [
                "Coconut water",
                "Fruit chaat",
                "Roasted makhana",
                "Buttermilk",
                "Fruits",
                "Nuts",
                "Roasted chana"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Banana smoothie with seeds",
                "Vegetable vermicelli upma",
                "Poha with sprouts",
                "Dosa with sambar",
                "Idli with chutney",
                "Poha with vegetables",
                "Dalia with fruits"
            ],
            "Lunch": [
                "Lemon rice with peanuts",
                "Vegetable khichdi",
                "Curd rice with vegetables",
                "Sambar rice",
                "Jeera rice with vegetables",
                "Vegetable pulao with raita",
                "Khichdi with curd"
            ],
            "Dinner": [
                "Vegetable soup with bread",
                "Dal with roti",
                "Vegetable stew with appam",
                "Grilled fish with salad",
                "Vegetable khichdi",
                "Dal with rice",
                "Vegetable pulao"
            ],
            "Snacks": [
                "Coconut water with pulp",
                "Fruit yogurt",
                "Roasted makhana",
                "Buttermilk with jeera",
                "Fruit salad",
                "Nuts and seeds",
                "Roasted chana"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Fruit smoothie with seeds",
                "Vegetable upma",
                "Poha with peanuts",
                "Dosa with chutney",
                "Idli with sambar",
                "Poha with vegetables",
                "Dalia with milk"
            ],
            "Lunch": [
                "Jeera rice with dal",
                "Vegetable pulao",
                "Curd rice",
                "Khichdi",
                "Rice with dal and sabzi",
                "Roti with vegetable curry",
                "Khichdi with vegetables"
            ],
            "Dinner": [
                "Vegetable soup with toast",
                "Dal with roti",
                "Vegetable stew",
                "Grilled chicken with salad",
                "Vegetable soup with bread",
                "Dal with roti",
                "Vegetable pulao"
            ],
            "Snacks": [
                "Coconut water",
                "Fruit chaat",
                "Roasted makhana",
                "Buttermilk",
                "Fruits",
                "Nuts",
                "Roasted chana"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Banana smoothie with seeds",
                "Vegetable vermicelli upma",
                "Poha with sprouts",
                "Dosa with sambar",
                "Idli with chutney",
                "Poha with vegetables",
                "Dalia with fruits"
            ],
            "Lunch": [
                "Lemon rice with peanuts",
                "Vegetable khichdi",
                "Curd rice with vegetables",
                "Sambar rice",
                "Jeera rice with vegetables",
                "Vegetable pulao with raita",
                "Khichdi with curd"
            ],
            "Dinner": [
                "Vegetable soup with bread",
                "Dal with roti",
                "Vegetable stew with appam",
                "Grilled fish with salad",
                "Vegetable khichdi",
                "Dal with rice",
                "Vegetable pulao"
            ],
            "Snacks": [
                "Coconut water with pulp",
                "Fruit yogurt",
                "Roasted makhana",
                "Buttermilk with jeera",
                "Fruit salad",
                "Nuts and seeds",
                "Roasted chana"
            ]
        }
    },
    5: {  # General Fitness (Complete 4 weeks)
        "Week 1": {
            "Breakfast": [
                "Idli with sambar",
                "Poha with vegetables",
                "Dalia with milk",
                "Paratha with curd",
                "Dosa with chutney",
                "Upma with vegetables",
                "Besan chilla"
            ],
            "Lunch": [
                "Rice with dal and sabzi",
                "Roti with vegetable curry",
                "Khichdi",
                "Curd rice",
                "Jeera rice with dal",
                "Vegetable pulao",
                "Sambar rice"
            ],
            "Dinner": [
                "Vegetable soup with bread",
                "Dal with roti",
                "Vegetable pulao",
                "Grilled fish with rice",
                "Vegetable khichdi",
                "Dal with rice",
                "Vegetable stew"
            ],
            "Snacks": [
                "Fruits",
                "Nuts",
                "Roasted chana",
                "Buttermilk",
                "Coconut water",
                "Fruit chaat",
                "Roasted makhana"
            ]
        },
        "Week 2": {
            "Breakfast": [
                "Idli with sambar",
                "Poha with vegetables",
                "Dalia with milk",
                "Paratha with curd",
                "Dosa with chutney",
                "Upma with vegetables",
                "Besan chilla"
            ],
            "Lunch": [
                "Rice with dal and sabzi",
                "Roti with vegetable curry",
                "Khichdi",
                "Curd rice",
                "Jeera rice with dal",
                "Vegetable pulao",
                "Sambar rice"
            ],
            "Dinner": [
                "Vegetable soup with bread",
                "Dal with roti",
                "Vegetable pulao",
                "Grilled fish with rice",
                "Vegetable khichdi",
                "Dal with rice",
                "Vegetable stew"
            ],
            "Snacks": [
                "Fruits",
                "Nuts",
                "Roasted chana",
                "Buttermilk",
                "Coconut water",
                "Fruit chaat",
                "Roasted makhana"
            ]
        },
        "Week 3": {
            "Breakfast": [
                "Idli with sambar",
                "Poha with vegetables",
                "Dalia with milk",
                "Paratha with curd",
                "Dosa with chutney",
                "Upma with vegetables",
                "Besan chilla"
            ],
            "Lunch": [
                "Rice with dal and sabzi",
                "Roti with vegetable curry",
                "Khichdi",
                "Curd rice",
                "Jeera rice with dal",
                "Vegetable pulao",
                "Sambar rice"
            ],
            "Dinner": [
                "Vegetable soup with bread",
                "Dal with roti",
                "Vegetable pulao",
                "Grilled fish with rice",
                "Vegetable khichdi",
                "Dal with rice",
                "Vegetable stew"
            ],
            "Snacks": [
                "Fruits",
                "Nuts",
                "Roasted chana",
                "Buttermilk",
                "Coconut water",
                "Fruit chaat",
                "Roasted makhana"
            ]
        },
        "Week 4": {
            "Breakfast": [
                "Idli with sambar",
                "Poha with vegetables",
                "Dalia with milk",
                "Paratha with curd",
                "Dosa with chutney",
                "Upma with vegetables",
                "Besan chilla"
            ],
            "Lunch": [
                "Rice with dal and sabzi",
                "Roti with vegetable curry",
                "Khichdi",
                "Curd rice",
                "Jeera rice with dal",
                "Vegetable pulao",
                "Sambar rice"
            ],
            "Dinner": [
                "Vegetable soup with bread",
                "Dal with roti",
                "Vegetable pulao",
                "Grilled fish with rice",
                "Vegetable khichdi",
                "Dal with rice",
                "Vegetable stew"
            ],
            "Snacks": [
                "Fruits",
                "Nuts",
                "Roasted chana",
                "Buttermilk",
                "Coconut water",
                "Fruit chaat",
                "Roasted makhana"
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
   
