from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from groq import Groq
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize Groq client with API key from .env
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    data = request.json
    system_prompt = """
    You are an expert travel planner with extensive knowledge of global destinations, cultures, and travel logistics. Your task is to create detailed, personalized travel itineraries based on user preferences. Please follow these guidelines:

    1. Provide a day-by-day breakdown of activities and accommodations.
    2. Suggest specific restaurants, attractions, and experiences that match the user's interests.
    3. Consider the user's budget when recommending accommodations and activities.
    4. Include estimated costs for major expenses (e.g., hotels, tours, transportation).
    5. Offer tips on local customs, weather, and what to pack.
    6. Suggest the best modes of transportation between locations.
    7. Include at least one "off the beaten path" or unique experience.
    8. Format the itinerary in a clear, easy-to-read structure using markdown.

    Aim to create an exciting, balanced itinerary that maximizes the user's experience within their constraints.
    """

    user_prompt = f"""
    Create a detailed travel itinerary for a trip to {data['destination']} for {data['duration']} days.

    The traveler's interests include {', '.join(data['interests'])} and their budget is {data['budget']}.
    They are traveling in {data['season']} and their preferred pace is {data['pace']}.
    Additional notes: {data['notes']}

    Please provide a comprehensive day-by-day itinerary based on this information.
    """

    try:
        completion = client.chat.completions.create(
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=0.65,
            stream=False,
            stop=None
        )
        itinerary = completion.choices[0].message.content.strip()
        return jsonify({"itinerary": itinerary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)