from flask import Flask, request, jsonify, render_template
import random
import json
import os

app = Flask(__name__)

# Minimal EXERCISES dictionary
EXERCISES = {
    0: ("Push-ups", "reps" ), 1: ("Wide Push-ups", "reps"), 2: ("Diamond Push-ups", "reps"), 3: ("Archer Push-ups", "reps"),
    4: ("Glute Bridges", "timing"), 5: ("Single-Leg Glute Bridges", "timing"), 6: ("Squats", "reps"), 7: ("Pistol Squat Prep", "reps"),
    8: ("Tricep Dips", "reps"), 9: ("Wall Push-ups", "reps"), 10: ("Lunges", "reps"), 11: ("Reverse Lunges", "reps"),
    12: ("Side Lunges", "reps"), 13: ("Close-Grip Push-ups", "reps"), 14: ("Bulgarian Split Squat", "reps"), 15: ("Hand-Release Push-ups", "reps"),
    16: ("Single-Leg Squat", "reps"), 17: ("Tricep Extensions", "reps"), 18: ("Calf Raises", "reps"), 19: ("Knee-to-Elbow Push-ups", "reps"),
    20: ("Incline Push-ups", "reps"), 21: ("Decline Push-ups", "reps"), 22: ("Squat Pulses", "reps"), 23: ("Lunge Pulses", "reps"),
    24: ("Wall Tricep Push-ups", "reps"), 25: ("Single-Leg Calf Raise", "reps"), 26: ("Step-Ups", "reps"), 27: ("Chair Dips", "reps"),
    28: ("Squat Hold to Jump", "reps"), 29: ("Reverse Plank Leg Lift", "timing"), 30: ("Side Squat", "reps"), 31: ("Forward Lunge", "reps"),
    32: ("Push-up to Plank", "reps"), 33: ("Glute Bridge March", "reps"), 34: ("Wall Squat Thrust", "reps"), 35: ("Tricep Kickbacks", "reps"),
    36: ("Single-Arm Push-up Prep", "reps"), 37: ("Lunge to Knee Drive", "reps"), 38: ("Calf Raise Hold", "timing"), 39: ("Squat to Lunge", "reps"),
    40: ("Burpees", "reps"), 41: ("Mountain Climbers", "reps"), 42: ("Squat Jumps", "reps"), 43: ("High Knees", "reps"),
    44: ("Jumping Jacks", "reps"), 45: ("Skier Jumps", "reps"), 46: ("Power Jacks", "reps"), 47: ("Tuck Jumps", "reps"),
    48: ("Plank Jacks", "reps"), 49: ("Star Jumps", "reps"), 50: ("Jump Lunges", "reps"), 51: ("Lateral Hops", "reps"),
    52: ("Fast Feet", "reps"), 53: ("Butt Kicks", "reps"), 54: ("Cross Jacks", "reps"), 55: ("Skater Jumps", "reps"),
    56: ("Knee Tuck Jumps", "reps"), 57: ("Heisman Jumps", "reps"), 58: ("Power Skips", "reps"), 59: ("Frog Jumps", "reps"),
    60: ("Boxer Shuffle", "reps"), 61: ("Side-to-Side Hops", "reps"), 62: ("Pulse Jumps", "reps"), 63: ("Jump Squat Twist", "reps"),
    64: ("Switch Lunges", "reps"), 65: ("High Knee Twists", "reps"), 66: ("Burpee Tuck Jumps", "reps"), 67: ("Lateral Skips", "reps"),
    68: ("Sprint Bursts", "reps"), 69: ("Jump Rope (Imaginary)", "reps"), 70: ("Side Kick Jumps", "reps"), 71: ("Plank to Jump", "reps"),
    72: ("Mountain Climber Twists", "reps"), 73: ("Squat Thrusts", "reps"), 74: ("Lunge Jumps", "reps"), 75: ("Knee Drive Hops", "reps"),
    76: ("Pop Squats", "reps"), 77: ("Side Lunge Jumps", "reps"), 78: ("Speed Skaters", "reps"), 79: ("Explosive Push-ups", "reps"),
    80: ("Plank", "timing"), 81: ("Wall Sit", "timing"), 82: ("Plank Rotations", "timing"), 83: ("Isometric Squat", "timing"),
    84: ("Side Plank", "timing"), 85: ("Superman Hold", "timing"), 86: ("Reverse Plank", "timing"), 87: ("Lunge Hold", "timing"),
    88: ("Squat Hold", "timing"), 89: ("Single-Leg Wall Sit", "timing"), 90: ("Plank Up-Downs", "timing"), 91: ("Side Lunge Hold", "timing"),
    92: ("Calf Raise Hold", "timing"), 93: ("Tricep Dip Hold", "timing"), 94: ("Chair Pose", "timing"), 95: ("Single-Leg Balance", "timing"),
    96: ("Wall Plank", "timing"), 97: ("Knee-to-Chest Plank", "timing"), 98: ("Hover Lunge", "timing"), 99: ("Plank Shoulder Taps", "timing"),
    100: ("Static Push-up Hold", "timing"), 101: ("Bridge Hold", "timing"), 102: ("Side Plank Twist", "timing"), 103: ("Squat Pulse Hold", "timing"),
    104: ("Lunge Pulse Hold", "timing"), 105: ("Wall Sit Twist", "timing"), 106: ("Plank Leg Lift", "timing"), 107: ("Superman Pulse", "timing"),
    108: ("Single-Leg Glute Bridge", "timing"), 109: ("Tricep Push-up Hold", "timing"), 110: ("Isometric Calf Raise", "timing"), 111: ("Plank to Pike", "timing"),
    112: ("Side Plank Reach", "timing"), 113: ("Wall Sit Pulse", "timing"), 114: ("Hover Squat", "timing"), 115: ("Reverse Plank Lift", "timing"),
    116: ("Static Lunge Twist", "timing"), 117: ("Plank Knee Tuck", "timing"), 118: ("Chair Pose Twist", "timing"), 119: ("Single-Arm Plank", "timing"),
    120: ("High Knees", "reps"), 121: ("Mountain Climbers", "reps"), 122: ("Shuttle Runs", "reps"), 123: ("Step Hops", "reps"),
    124: ("Sprint-in-Place", "reps"), 125: ("Lateral Shuffles", "reps"), 126: ("Burpees", "reps"), 127: ("Jumping Jacks", "reps"),
    128: ("Skater Jumps", "reps"), 129: ("Fast Feet", "reps"), 130: ("Butt Kicks", "reps"), 131: ("Cross Jacks", "reps"),
    132: ("Tuck Jumps", "reps"), 133: ("Star Jumps", "reps"), 134: ("Power Skips", "reps"), 135: ("Frog Jumps", "reps"),
    136: ("Boxer Shuffle", "reps"), 137: ("Side-to-Side Hops", "reps"), 138: ("Knee Tuck Jumps", "reps"), 139: ("Heisman Jumps", "reps"),
    140: ("High Knee Twists", "reps"), 141: ("Sprint Bursts", "reps"), 142: ("Lateral Skips", "reps"), 143: ("Jump Rope (Imaginary)", "reps"),
    144: ("Side Kick Jumps", "reps"), 145: ("Plank to Jump", "reps"), 146: ("Mountain Climber Twists", "reps"), 147: ("Squat Thrusts", "reps"),
    148: ("Lunge Jumps", "reps"), 149: ("Knee Drive Hops", "reps"), 150: ("Pop Squats", "reps"), 151: ("Side Lunge Jumps", "reps"),
    152: ("Speed Skaters", "reps"), 153: ("Pulse Jumps", "reps"), 154: ("Switch Lunges", "reps"), 155: ("High Knee Sprints", "reps"),
    156: ("Plank Jack Burpees", "reps"), 157: ("Step-Up Jumps", "reps"), 158: ("Lateral Hop Twists", "reps"), 159: ("Explosive Knee Lifts", "reps"),
    160: ("Jumping Jacks", "reps"), 161: ("Burpees", "reps"), 162: ("Mountain Climbers", "reps"), 163: ("High Knee Sprints", "reps"),
    164: ("Squat Jumps", "reps"), 165: ("Skater Jumps", "reps"), 166: ("Sprint-in-Place", "reps"), 167: ("Lateral Skips", "reps"),
    168: ("Fast Feet", "reps"), 169: ("Butt Kicks", "reps"), 170: ("Cross Jacks", "reps"), 171: ("Tuck Jumps", "reps"),
    172: ("Star Jumps", "reps"), 173: ("Heisman Jumps", "reps"), 174: ("Power Skips", "reps"), 175: ("Frog Jumps", "reps"),
    176: ("Boxer Shuffle", "reps"), 177: ("Side-to-Side Hops", "reps"), 178: ("Knee Tuck Jumps", "reps"), 179: ("Pulse Jumps", "reps"),
    180: ("High Knees", "reps"), 181: ("Skier Jumps", "reps"), 182: ("Power Jacks", "reps"), 183: ("Plank Jacks", "reps"),
    184: ("Jump Lunges", "reps"), 185: ("Lateral Hops", "reps"), 186: ("Switch Lunges", "reps"), 187: ("High Knee Twists", "reps"),
    188: ("Sprint Bursts", "reps"), 189: ("Side Kick Jumps", "reps"), 190: ("Plank to Jump", "reps"), 191: ("Mountain Climber Twists", "reps"),
    192: ("Squat Thrusts", "reps"), 193: ("Knee Drive Hops", "reps"), 194: ("Pop Squats", "reps"), 195: ("Side Lunge Jumps", "reps"),
    196: ("Speed Skaters", "reps"), 197: ("Explosive Push-ups", "reps"), 198: ("Jump Rope (Imaginary)", "reps"), 199: ("Lateral Hop Twists", "reps"),
    200: ("Shadow Boxing Punches", "reps"), 201: ("Side-Step Jacks", "reps"), 202: ("Knee-to-Elbow Twists", "reps"), 203: ("Cardio Marching", "reps"),
    204: ("Double Unders (Imaginary)", "reps"), 205: ("Alternating Knee Lifts", "reps"), 206: ("Side Step Burpees", "reps"), 207: ("Jumping Knee Tucks", "reps"),
    208: ("Cross-Body Kicks", "reps"), 209: ("Quick Step-Ups", "reps"), 210: ("Twist Jumps", "reps"), 211: ("Low-Impact Burpees", "reps"),
    212: ("Side Shuffle Hops", "reps"), 213: ("Front Kick Jumps", "reps"), 214: ("Heel Tap Jumps", "reps"), 215: ("Cardio Knee Drives", "reps"),
    216: ("Plank Jack Twists", "reps"), 217: ("Lateral Step Jumps", "reps"), 218: ("Reverse Lunge Jumps", "reps"), 219: ("Standing Side Crunches", "reps"),
    220: ("High Knee March", "reps"), 221: ("Boxer Jab Cross", "reps"), 222: ("Side Hop Burpees", "reps"), 223: ("Pulse Squat Jumps", "reps"),
    224: ("Knee Lift Twists", "reps"), 225: ("Quick Lateral Steps", "reps"), 226: ("Burpee to Side Kick", "reps"), 227: ("Cross Jack Twists", "reps"),
    228: ("Sprint Pulse", "reps"), 229: ("Low Skater Hops", "reps"), 230: ("Front-to-Back Hops", "reps"), 231: ("Cardio Side Lunges", "reps"),
    232: ("Jumping Heel Clicks", "reps"), 233: ("Plank Hop Outs", "reps"), 234: ("Twist Skaters", "reps"), 235: ("Side Kick Burpees", "reps"),
    236: ("Fast Marching Twists", "reps"), 237: ("Lunge Jump Twists", "reps"), 238: ("Quick Boxer Steps", "reps"), 239: ("Low-Impact Skaters", "reps"),
    240: ("Side Step Kicks", "reps"), 241: ("Knee Drive Skips", "reps"), 242: ("Cross-Body Hops", "reps"), 243: ("Pulse High Knees", "reps"),
    244: ("Jumping Side Steps", "reps"), 245: ("Cardio Arm Swings", "reps"), 246: ("Burpee Knee Tucks", "reps"), 247: ("Lateral Pulse Jumps", "reps"),
    248: ("Quick Heel Taps", "reps"), 249: ("Twist Power Jacks", "reps"), 250: ("Side-to-Side Skips", "reps"), 251: ("Low Jump Squats", "reps"),
    252: ("Cross Kick Jumps", "reps"), 253: ("Fast Knee Lifts", "reps"), 254: ("Plank Side Hops", "reps"), 255: ("Cardio Twist Steps", "reps"),
    256: ("Jumping Cross Punches", "reps"), 257: ("Side Lunge Hops", "reps"), 258: ("Quick Skater Twists", "reps"), 259: ("Burpee March", "reps"),
    260: ("Bear Crawls", "reps"), 261: ("Crab Walks", "reps"), 262: ("Spider Lunges", "reps"), 263: ("Plank to Side Plank", "reps"),
    264: ("Side Plank Dips", "reps"), 265: ("Plank to Toe Touch", "reps"), 266: ("Superman Pulls", "reps"), 267: ("Bird Dogs", "reps"),
    268: ("Dead Bug", "reps"), 269: ("Hollow Body Hold", "timing"), 270: ("Arch Body Hold", "timing"), 271: ("V-Ups", "reps"),
    272: ("Bicycle Crunches", "reps"), 273: ("Flutter Kicks", "reps"), 274: ("Leg Raises", "reps"), 275: ("Russian Twists", "reps"),
    276: ("Mountain Climber Crossovers", "reps"), 277: ("Burpee Broad Jumps", "reps"), 278: ("Side Plank with Reach Through", "reps"),
    279: ("Plank with Arm Lift", "reps"), 280: ("Plank with Leg Lift", "reps"), 281: ("Plank with Opposite Arm and Leg Lift", "reps"),
    282: ("Side Plank with Rotation", "reps"), 283: ("Side Plank with Knee Tuck", "reps"), 284: ("Side Plank with Leg Lift", "reps"),
    285: ("Side Plank with Hip Dips", "reps"), 286: ("Side Plank with Toe Tap", "reps"), 287: ("Side Plank with Arm Reach", "reps"),
    288: ("Side Plank with Knee Drive", "reps"), 289: ("Side Plank with Leg Circles", "reps"), 290: ("Side Plank with Side Crunch", "reps"),
    291: ("Side Plank with Side Kick", "reps"), 292: ("Side Plank with Side Step", "reps"), 293: ("Side Plank with Side Twist", "reps"),
    294: ("Side Plank with Side Reach", "reps"), 295: ("Side Plank with Side Tap", "reps"), 296: ("Side Plank with Side Lift", "reps"),
    297: ("Side Plank with Side Pulse", "reps"), 298: ("Side Plank with Side Hold", "timing"), 299: ("Side Plank with Side March", "reps"),
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

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Ideal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def generate_workout(age, exp, activity, sleep, water, week=None):
    base_reps = BASE_REPS[exp]
    sets = [3, 4, 5][exp]

    # Adjust for age
    if age >= 50:
        base_reps = int(base_reps * 0.8)

    # Adjust for sleep
    if sleep < 7:  # Less than recommended sleep
        base_reps = int(base_reps * 0.9)  # Reduce reps by 10%

    # Adjust for water intake
    if water < 2:  # Less than recommended water intake
        base_reps = int(base_reps * 0.9)  # Reduce reps by 10%

    # Warmup: 2 exercises
    warmup_ex = random.sample([ex for ex in range(len(EXERCISES))], min(2, len(EXERCISES)))
    warmup = [(ex, 2, base_reps) for ex in warmup_ex]

    # Main: 4 exercises
    main_ex = random.sample([ex for ex in range(len(EXERCISES))], min(4, len(EXERCISES)))
    main = [(ex, sets, base_reps) for ex in main_ex]

    return warmup, main

def generate_month_plan(age, exp, activity, sleep, water):
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    plan = {}

    for week in range(1, 5):
        week_plan = {}
        for day_index in range(7):
            day_name = day_names[day_index]
            warmup, main = generate_workout(age, exp, activity, sleep, water, week)
            week_plan[day_name] = {
                "Warmup": [f"2x{val}r {EXERCISES[ex][0]}" for ex, _, val in warmup],
                "Main": [f"{sets}x{val}r {EXERCISES[ex][0]}" for ex, sets, val in main],
                "Cooldown": ["30s Hamstring Stretch", "30s Quad Stretch"]
            }
        plan[f"Week {week}"] = week_plan

    return plan

def save_response_to_json(data, filename='responses.json'):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)

    with open(filename, 'r') as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []

    existing_data.append(data)

    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-workout', methods=['POST'])
def generate_workout_route():
    data = request.json
    age = int(data['age'])
    height = int(data['height'])
    weight = int(data['weight'])
    exp = int(data['experience_level'])
    goal = int(data['fitness_goal'])
    activity = data['activity_level']
    sleep = int(data['sleep'])
    water = int(data['water'])

    # Calculate BMI
    bmi = calculate_bmi(weight, height)
    bmi_category = get_bmi_category(bmi)

    # Generate workout plan
    workout_plan = generate_month_plan(age, exp, activity, sleep, water)

    # Prepare response data
    response_data = {
        "bmi": bmi,
        "bmi_category": bmi_category,
        "workout_plan": workout_plan
    }

    # Save response to JSON file
    save_response_to_json(response_data)

    return jsonify(response_data)

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
   
