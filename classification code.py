from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import math
import os

app = Flask(__name__)

# Set up the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'fitness_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a User model to store fitness data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    waist = db.Column(db.Float, nullable=False)
    neck = db.Column(db.Float, nullable=False)
    hip = db.Column(db.Float, nullable=True)
    fitness_goal = db.Column(db.String(50), nullable=False)
    workout_routine = db.Column(db.Integer, nullable=False)
    fat_percentage = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    fitness_classification = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.id}: {self.gender}, {self.age}, {self.fitness_classification}>"

# Function to calculate body fat percentage using the U.S. Navy Method
def calculate_body_fat_percentage(gender, height, waist, neck, hip=None):
    if gender == 'male':
        return 86.010 * math.log10(waist - neck) - 70.041 * math.log10(height) + 36.76
    return 163.205 * math.log10(waist + hip - neck) - 97.684 * math.log10(height) - 78.387

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_in_meters = height / 100  # Convert height from cm to meters
    return weight / (height_in_meters ** 2)

# Function to classify fitness level
def classify_fitness(fat_percentage, workout_routine, bmi, age, fitness_goal):
    thresholds = {
        4: (10, 15, "Very Fit", "Fit", "Average"),
        3: (12, 18, "Fit", "Average", "Below Average"),
        2: (15, 100, "Average", "Below Average", "Unfit"),
        1: (20, 100, "Below Average", "Unfit", "Unfit")
    }
    low, high, level_1, level_2, level_3 = thresholds.get(workout_routine)

    # Adjust thresholds based on age
    age_adjustment = 0
    if age > 50:
        age_adjustment = 5
    elif age > 30:
        age_adjustment = 2

    low += age_adjustment
    high += age_adjustment

    # Adjust fitness classification based on BMI
    if bmi < 18.5:
        return "Underweight"
    elif bmi > 30:
        return "Obese"

    if fat_percentage < low:
        fitness_classification = level_1
    elif fat_percentage < high:
        fitness_classification = level_2
    else:
        fitness_classification = level_3

    # Personalize classification based on fitness goals
    goal_adjustment = {
        "weight_loss": "Focus on reducing body fat and overall weight.",
        "muscle_gain": "Prioritize strength training for muscle development.",
        "endurance_improvement": "Include more cardiovascular exercises.",
        "general_fitness": "Maintain a balanced approach."
    }
    
    return fitness_classification + " - " + goal_adjustment[fitness_goal]

# Route to display the workout form
@app.route('/')
def index():
    return render_template('workout_form.html')

# Route to handle form submission and fitness classification
@app.route('/submit_form.php', methods=['POST'])
def submit_form():
    # Extract form data from POST request
    gender = request.form['gender'].lower()
    age = int(request.form['age'])
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    waist = float(request.form['waist'])
    neck = float(request.form['neck'])
    hip = float(request.form['hip']) if gender == 'female' else None
    fitness_goal = request.form['fitness_goals']
    workout_routine = int(request.form['fitness_level'])  # Assume workout routine is tied to fitness level

    # Calculate body fat percentage and BMI
    fat_percentage = calculate_body_fat_percentage(gender, height, waist, neck, hip)
    bmi = calculate_bmi(weight, height)

    # Classify fitness level
    fitness_classification = classify_fitness(fat_percentage, workout_routine, bmi, age, fitness_goal)

    # Create a new User entry
    new_user = User(
        gender=gender,
        age=age,
        height=height,
        weight=weight,
        waist=waist,
        neck=neck,
        hip=hip,
        fitness_goal=fitness_goal,
        workout_routine=workout_routine,
        fat_percentage=fat_percentage,
        bmi=bmi,
        fitness_classification=fitness_classification
    )

    # Save user data to the database
    db.session.add(new_user)
    db.session.commit()

    # Return a RESULT page with the fitness classification
    return f"""
    <h1>Your Fitness Classification</h1>
    <p>Body Fat Percentage: {fat_percentage:.2f}%</p>
    <p>BMI: {bmi:.2f}</p>
    <p>Fitness Level: {fitness_classification}</p>
    """

if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
