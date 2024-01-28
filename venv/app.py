from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
openai.api_key = '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'

@app.route('/', methods=['POST','GET'])

def index():
    if request.method == 'POST':
        return get_recommendations()
    return render_template('index.html')

def get_recommendations():
    if request.method == 'POST':
        # Retrieve form data
        gender = request.form.get('gender', '')
        age = request.form.get('age', '')
        height = request.form.get('height', '')
        weight = request.form.get('weight', '')
        activity_level = request.form.get('activity_level', '')
        diet_type = request.form.get('diet_type', '')
        goal = request.form.get('goal', '')

        # Check if required fields are missing
        if not all([gender, age, height, weight, activity_level, diet_type, goal]): 
            return render_template('index.html', error='Missing required fields')

        # Generate prompts for ChatGPT
        chat_prompt = f"I am a {gender} aged {age}, who is {height} cm tall and {weight} kg with a {activity_level} activity level and with a {diet_type} diet and my goal is {goal}."

        # Get 3-day gym routine from ChatGPT
        gym_routine_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": chat_prompt + "\nGenerate a 3-day gym routine:"}
        ],
        
)

        if 'choices' in gym_routine_response:
        # Check if there is at least one choice
            if gym_routine_response['choices']:
        # Access the text content
                gym_routine = gym_routine_response['choices'][0]['message']['content'].strip()
            else:
                gym_routine = "No response from the model."
        else:
            gym_routine = "Invalid response format from the model."
        # Get 5-day meal recipes from ChatGPT
        meal_recipes_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": chat_prompt + "\nCalculate my BMR and generate a 5-day meal recipes based on this and my goal:"}
        ],
        
)
        if 'choices' in meal_recipes_response:
        # Check if there is at least one choice
            if meal_recipes_response['choices']:
        # Access the text content
                meal_recipes = meal_recipes_response['choices'][0]['message']['content'].strip()
            else:
                meal_recipes = "No response from the model."
        else:
            meal_recipes = "Invalid response format from the model."

        # Return recommendations
        return render_template('index.html', gym_routine=gym_routine ,meal_recipes=meal_recipes)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

