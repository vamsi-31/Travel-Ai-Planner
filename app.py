from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS
import os
from groq import Groq, RateLimitError, APIError # Import specific errors
from dotenv import load_dotenv
import json
import logging

# --- Configuration ---
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set.")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Flask App Setup ---
app = Flask(__name__, static_folder='static', static_url_path='') # Serve static files from root
CORS(app) # Allow requests from the frontend development server

# --- Groq Client ---
try:
    client = Groq(api_key=GROQ_API_KEY)
    logging.info("Groq client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize Groq client: {e}")
    # Depending on the desired behavior, you might want to exit or handle this differently
    client = None


# --- Utility Functions ---
def validate_input(data):
    """ Basic validation for incoming request data. """
    required_fields = ['destination', 'duration', 'budget', 'season', 'pace', 'interests']
    errors = []
    if not isinstance(data, dict):
         return ["Invalid request format: Expected JSON object."]

    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: '{field}'")

    if 'duration' in data:
        try:
            duration = int(data['duration'])
            if duration <= 0:
                errors.append("Duration must be a positive number.")
        except (ValueError, TypeError):
            errors.append("Duration must be a valid number.")

    if 'interests' in data and (not isinstance(data['interests'], list) or len(data['interests']) == 0):
        errors.append("At least one interest must be selected.")

    return errors

# --- Routes ---
@app.route('/')
def home():
    # Serve the main HTML file
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary_route():
    if not client:
         logging.error("Groq client not initialized. Cannot process request.")
         return jsonify({"error": "AI service is currently unavailable. Please try again later."}), 503 # Service Unavailable

    if not request.is_json:
        logging.warning("Request received without JSON data.")
        return jsonify({"error": "Invalid request: Content-Type must be application/json"}), 400

    data = request.json
    logging.info(f"Received itinerary request: {data}")

    # --- Input Validation ---
    validation_errors = validate_input(data)
    if validation_errors:
        logging.warning(f"Validation failed: {validation_errors}")
        # Return 400 Bad Request with specific errors
        return jsonify({"error": "Invalid input data.", "details": validation_errors}), 400

    # --- Prepare Prompts (Improved clarity) ---
    system_prompt = """
    You are TravelAI, an expert travel planner specializing in creating personalized, detailed, and engaging itineraries.
    Your goal is to craft a realistic and exciting travel plan based on user preferences.

    **Guidelines:**
    1.  **Structure:** Provide a clear day-by-day breakdown (e.g., "Day 1: Arrival and City Exploration").
    2.  **Details:** Suggest specific attractions, activities (with brief descriptions), and potential restaurants/cafes matching the user's interests and budget level. Mention opening hours or booking recommendations where relevant.
    3.  **Logistics:** Consider travel time between locations within the itinerary. Suggest appropriate modes of local transport (walking, public transit, taxi, ride-share).
    4.  **Budget:** Integrate budget considerations subtly. Suggest a mix of free activities and paid attractions. If the budget is specified as 'Luxury', suggest higher-end options; if 'Budget', focus on cost-effective choices. Use the budget description provided ('e.g., 2000 USD', 'Moderate', 'Luxury') as a guide.
    5.  **Pacing:** Adjust the density of activities based on the requested pace (Relaxed, Moderate, Fast-paced).
    6.  **Personalization:** Incorporate the user's specific interests and any additional notes they provided. Include at least one unique or "local gem" type of experience.
    7.  **Practical Tips:** Briefly mention relevant tips (e.g., best time to visit an attraction, local customs, currency, packing suggestions based on season).
    8.  **Formatting:** Use Markdown for clear formatting (headings, lists, bold text). Make it easy and pleasant to read.
    9.  **Tone:** Be enthusiastic, helpful, and knowledgeable.
    """

    # Enhanced user prompt with clearer placeholders and structure
    user_prompt = f"""
    Please create a personalized travel itinerary with the following details:

    *   **Destination:** {data['destination']}
    *   **Duration:** {data['duration']} days
    *   **Travel Period/Season:** {data['season']}
    *   **Budget Indication:** {data['budget']}
    *   **Travel Pace:** {data['pace']}
    *   **Primary Interests:** {', '.join(data['interests'])}
    *   **Additional Notes/Preferences:** {data.get('notes', 'None provided.')}

    Generate a day-by-day plan following the guidelines in the system prompt.
    """

    logging.info("Sending request to Groq API...")
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Using the recommended general-purpose model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,  # Balance creativity and predictability
            max_tokens=6000, # Increased token limit for potentially longer itineraries
            top_p=0.,       # Adjust top_p slightly
            stream=False,
            # stop=None # Optional: Define stop sequences if needed
        )
        itinerary = completion.choices[0].message.content.strip()

        if not itinerary:
             logging.warning("Groq API returned an empty itinerary.")
             return jsonify({"error": "Failed to generate itinerary content. The AI service returned an empty response."}), 500

        logging.info(f"Successfully generated itinerary for {data['destination']}.")
        return jsonify({"itinerary": itinerary})

    except RateLimitError as e:
        logging.error(f"Groq API Rate Limit Error: {e}")
        return jsonify({"error": "The service is currently experiencing high demand. Please try again later."}), 429 # Too Many Requests
    except APIError as e:
         logging.error(f"Groq API Error: Status Code: {e.status_code}, Message: {e.message}")
         return jsonify({"error": f"An error occurred while contacting the AI service (Status: {e.status_code}). Please try again."}), 502 # Bad Gateway
    except Exception as e:
        # Catch any other unexpected errors
        logging.exception(f"An unexpected error occurred: {e}") # Use logging.exception to include stack trace
        return jsonify({"error": "An unexpected internal server error occurred. Please try again later."}), 500

# --- Run the App ---
if __name__ == '__main__':
    # Use waitress or gunicorn for production instead of Flask's development server
    # Example: waitress-serve --host 0.0.0.0 --port 5000 app:app
    # For development:
    app.run(debug=True, port=5000) # debug=True is NOT for production