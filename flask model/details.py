from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai
import math
import os
import random


# Initialize the Flask app
app = Flask(__name__)

# Set up the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'fitness_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a User model to store fitness data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    waist = db.Column(db.Float, nullable=False)
    neck = db.Column(db.Float, nullable=False)
    hip = db.Column(db.Float, nullable=True)
    fitness_level = db.Column(db.String(50), nullable=False)
    fitness_goal = db.Column(db.String(50), nullable=False)
    injury_setbacks = db.Column(db.String(50), nullable=False)
    fat_percentage = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    sleep_routine = db.Column(db.String(50), nullable=False)
    medi_condition = db.Column(db.Text, nullable=True)

# Function to calculate body fat percentage using the U.S. Navy Method
def calculate_body_fat_percentage(gender, height, waist, neck, hip=None):
    if gender == 'male':
        return 86.010 * math.log10(waist - neck) - 70.041 * math.log10(height) + 36.76
    return 163.205 * math.log10(waist + hip - neck) - 97.684 * math.log10(height) - 78.387

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_in_meters = height / 100  # Convert height from cm to meters
    return weight / (height_in_meters ** 2)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/personalfit')
def personalfit():
    return render_template('personalfit.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')



@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        # Get form data
        id = random.randint(1, 1000)
        gender = request.form.get('gender')
        age = int(request.form.get('age'))
        height = float(request.form.get('height'))
        weight = float(request.form.get('weight'))
        waist = float(request.form.get('waist'))
        neck = float(request.form.get('neck'))
        hip = float(request.form.get('hip')) if gender == 'female' else None
        fitness_level = request.form.get('fitness_level')
        fitness_goal = request.form.get('fitness_goal')
        sleep_routine = request.form.get('sleep_routine')
        medi_condition = request.form.get('medi_condition')
        injury_setbacks = request.form.get('injury_setbacks')

        # Calculate body fat percentage and BMI
        fat_percentage = calculate_body_fat_percentage(gender, height, waist, neck, hip)
        bmi = calculate_bmi(weight, height)

        # Create a new User entry
        new_user = User(
            id=id,
            gender=gender,
            age=age,
            height=height,
            weight=weight,
            waist=waist,
            neck=neck,
            hip=hip,
            fitness_level=fitness_level,
            fitness_goal=fitness_goal,
            injury_setbacks=injury_setbacks,
            fat_percentage=fat_percentage,
            bmi=bmi,
            sleep_routine=sleep_routine,
            medi_condition=medi_condition
        )

        # Save user data to the database
        db.session.add(new_user)
        db.session.commit()

        # Get diet and workout plan
        diet_plan = get_diet_and_workout_plan(gender, age, height, weight, waist, neck, hip, fitness_level, fitness_goal, injury_setbacks, fat_percentage, bmi, sleep_routine, medi_condition)

        # Return the result page with the fitness classification and plans
        return render_template('result.html', classification=fitness_level, diet_plan=diet_plan, workout_plan=diet_plan)

def get_diet_and_workout_plan(gender, age, height, weight, waist, neck, hip, fitness_level, fitness_goal, injury_setbacks, fat_percentage, bmi, sleep_routine, medi_condition):
    # Choose a model (replace with the desired model name)
    genai.configure(api_key="AIzaSyCq5XjUyIku8TIhp_3NcsmB8GJf0JaMtdE")
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Construct the prompt for structured output
    prompt = (f"""
Create a personalized, well-structured fitness and diet plan based on the following user information. The plan should include a detailed weekly workout schedule, daily workout routine, and a comprehensive nutrition plan tailored to their specific needs. The output should be scientifically sound and aligned with their fitness goals, taking into account all provided parameters. Please structure the plan in the following way:

User Information:

Gender: {gender}
Age: {age}
Height: {height} cm/inches
Weight: {weight} kg/lbs
Waist measurement: {waist} cm/inches
Neck measurement: {neck} cm/inches
Hip measurement: {hip} cm/inches (if applicable)
Fitness level: {fitness_level}
Fitness goals: {fitness_goal}
Injury setbacks: {injury_setbacks}
Body fat percentage: {fat_percentage}%
BMI: {bmi}
Sleep routine: {sleep_routine}
Medical conditions: {medi_condition}


Output Requirements:

1. Weekly Workout Split:

Design a 7-day workout schedule, clearly defining which muscle groups or fitness components (e.g., strength, endurance, flexibility) are worked on each day.
Include rest days and recovery sessions (e.g., stretching, yoga, or low-intensity cardio) optimized for recovery based on injury setbacks or fatigue.
The workout split should be aligned with their fitness level and goal (e.g., muscle building, fat loss, endurance training).
Specify exact training modes (e.g., push-pull split, full-body workouts, upper/lower body days, etc.).

2. Daily Workout Routine:

For each workout day, provide a detailed breakdown of exercises (e.g., squats, bench press, deadlifts), including:
- Number of sets and reps.
- Rest time between sets.
- Weight recommendations based on fitness level and goal.
- Modifications for injury setbacks (e.g., knee injury: replace squats with leg press).
- Include warm-up and cool-down routines specific to the user’s needs.

3. Nutrition Plan:

- Provide a daily caloric intake suggestion based on their age, weight, height, activity level, and fitness goal.
- Create a macro breakdown (percentage of protein, carbohydrates, and fats) tailored to their goal (e.g., high-protein for muscle gain, lower carbs for fat loss).
- Suggest 3-6 meals per day, with specific portion sizes and examples for each meal, considering dietary preferences (e.g., if vegan, list plant-based proteins).
- Include pre- and post-workout meal ideas for optimizing performance and recovery.
- Provide hydration guidelines based on body weight and activity level.

4. Weekly Nutrition Schedule:

- Organize the nutrition plan by day, outlining when to increase or decrease carbs (carb cycling) to align with workout intensity (e.g., higher carbs on leg day, lower carbs on rest days).
- Include guidance on meal timing to optimize energy, recovery, and muscle synthesis (e.g., post-workout meal within 45 minutes of training).
- Suggest snack options for mid-morning, mid-afternoon, or evening cravings.

5. Sleep Optimization Tips:

- Suggest a tailored sleep improvement strategy to improve overall recovery and performance, based on their current routine.
- Include recommendations for enhancing sleep quality (e.g., avoiding screens before bed, practicing relaxation techniques).

6. Additional Health Tips:

- Provide specific advice on hydration, stress management, and recovery techniques (e.g., foam rolling, ice baths) relevant to their lifestyle.
- Address any medical conditions (e.g., adjustments for heart disease or diabetes) in both workout and nutrition plans.
- Include tips for improving mental focus, motivation, and habit-building strategies to maintain long-term fitness progress.
"""
    )



    # Generate the response
    response = model.generate_content(prompt)

    # Split the response into diet and workout plans (if possible)
    output = response.text.split("\n")  # Assuming each line represents a different part

    # Formatting output
    structured_output = "\n".join(line.strip() for line in output if line.strip())

    return structured_output



if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
