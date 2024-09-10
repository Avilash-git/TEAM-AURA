import os
from google.cloud import generativeai

def get_diet_and_workout_plan(bmi, current_fitness_level, desired_fitness_level, dissablity):
    # Set API key and project ID directly as environment variables
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Z:\SIH\project\login ss\ip files\gen ai json file.json"
    os.environ["GOOGLE_CLOUD_PROJECT"] = "Generative-Language-Client"

    # Create a client
    client = generativeai.Client()

    # Choose a model (replace with the desired model name)
    model_name = "gemini-1.5-pro"

    # Construct the prompt
    prompt = f"Create a personalized diet and workout plan for a person with a BMI of {bmi}, current fitness level of {current_fitness_level}, and desired fitness level of {desired_fitness_level},dissablity facing are {dissablity}."

    # Generate a response
    response = client.generate_text(model_name=model_name, prompt=prompt)

    return response.text

# Get user input
bmi = float(input("Enter your BMI: "))
current_fitness_level = input("Enter your current fitness level (e.g., beginner, intermediate, advanced): ")
desired_fitness_level = input("Enter your desired fitness level (e.g., beginner, intermediate, advanced): ")
dissablity = input("Enter your dissablities (e.g., have diabeties , faatty liver , genetic probs): ")

# Generate and display the plan
plan = get_diet_and_workout_plan(bmi, current_fitness_level, desired_fitness_level,dissablity)
print(plan)