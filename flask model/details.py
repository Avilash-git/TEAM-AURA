from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import math
import os

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
    #workout_routine = db.Column(db.String(50), nullable=False)
    fitness_goal = db.Column(db.String(50), nullable=False)
    injury_setbacks = db.Column(db.String(50), nullable=False)
    fat_percentage = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    #fitness_classification = db.Column(db.String(50), nullable=False)
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


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    # Get form data
    id = 101
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
    print(gender)

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
        #workout_routine=workout_routine,  # Adjust if needed
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

    # Return a result page with the fitness classification
    return #

if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
