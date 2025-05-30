from quart import Quart, request, jsonify, send_from_directory, abort
from quart_cors import cors as CORS # Import cors and alias it
import os
from groq import Groq, RateLimitError, APIError # Import specific errors
from dotenv import load_dotenv
import json
import logging
import asyncio # Added for asyncio.to_thread

# --- Configuration ---
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set.")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Quart App Setup ---
app = Quart(__name__, static_folder='static', static_url_path='') # Serve static files from root
app = CORS(app, allow_origin="*") # Allow requests from the frontend development server, more explicit CORS for Quart

# --- Groq Client ---
try:
    client = Groq(api_key=GROQ_API_KEY)
    logging.info("Groq client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize Groq client: {e}")
    # Depending on the desired behavior, you might want to exit or handle this differently
    client = None


# --- Prompt Creation Functions ---
def create_system_prompt() -> str:
    """Generates the system prompt for the Groq API."""
    return """
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

def create_user_prompt(data: dict) -> str:
    """Generates the user prompt for the Groq API based on validated user data."""
    # It's assumed 'data' is validated by validate_input before this function is called
    return f"""
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

# --- Utility Functions ---
def validate_input(data: dict) -> list[str]: # Added type hints
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
async def home(): # Changed to async def
    # Serve the main HTML file
    return await send_from_directory(app.static_folder, 'index.html') # Added await

@app.route('/generate_itinerary', methods=['POST'])
async def generate_itinerary_route(): # Changed to async def
    if not client:
         logging.error("Groq client not initialized. Cannot process request.")
         return jsonify({"error": "AI service is currently unavailable. Please try again later."}), 503 # Service Unavailable

    if not request.is_json: # Remains the same in Quart
        logging.warning("Request received without JSON data.")
        return jsonify({"error": "Invalid request: Content-Type must be application/json"}), 400

    data = await request.get_json() # Changed to await request.get_json()
    logging.info(f"Received itinerary request: {data}")

    # --- Input Validation ---
    validation_errors = validate_input(data)
    if validation_errors:
        logging.warning(f"Validation failed: {validation_errors}")
        # Return 400 Bad Request with specific errors
        return jsonify({"error": "Invalid input data.", "details": validation_errors}), 400

    # --- Prepare Prompts using new functions ---
    system_prompt = create_system_prompt()
    user_prompt = create_user_prompt(data)

    logging.info("Sending request to Groq API...")
    try:
        # Use asyncio.to_thread for the synchronous Groq client call
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=6000,
            top_p=0.9,
            stream=False,
        )
        itinerary = completion.choices[0].message.content.strip()

        if not itinerary:
             logging.warning("Groq API returned an empty itinerary.")
             # Using the new error handler, though this is not an exception
             return jsonify({"error": "Failed to generate itinerary content. The AI service returned an empty response."}), 500


        logging.info(f"Successfully generated itinerary for {data['destination']}.")
        return jsonify({"itinerary": itinerary})

    except RateLimitError as e:
        return handle_api_error(e, "The service is currently experiencing high demand. Please try again later.", 429)
    except APIError as e:
        # Customize message for APIError to include status code if desired, or keep it general
        user_msg = f"An error occurred while contacting the AI service. Please try again."
        if hasattr(e, 'status_code'): # Check if status_code attribute exists
            user_msg = f"An error occurred while contacting the AI service (Status: {e.status_code}). Please try again."
        return handle_api_error(e, user_msg, getattr(e, 'status_code', 502)) # Use actual status code or default to 502
    except Exception as e:
        return handle_api_error(e, "An unexpected internal server error occurred. Please try again later.", 500, log_level="exception")

# --- Error Handling Helper ---
def handle_api_error(exception: Exception, user_message: str, status_code: int, log_level: str = "error"):
    """
    Logs an error and returns a JSON response for API errors.
    """
    log_func = getattr(logging, log_level, logging.error) # Default to logging.error
    
    # More detailed logging for debugging
    if isinstance(exception, APIError):
        log_func(f"API Error: {user_message} - Status: {getattr(exception, 'status_code', 'N/A')}, Details: {exception}")
    else:
        log_func(f"Error: {user_message} - Details: {exception}")

    # Include exception details in the response if appropriate (e.g., not for generic 500 in production)
    # For this exercise, we'll include string representation of the exception for more clarity during development/testing.
    # In a production environment, you might want to limit the details exposed to the client for security reasons.
    error_details = str(exception)
    
    return jsonify({"error": user_message, "details": error_details}), status_code


# --- Run the App ---
if __name__ == '__main__':
    # Instructions for running with Hypercorn
    print("To run the app, use: hypercorn -b 0.0.0.0:5000 app:app")
    # For programmatic execution (optional, usually CLI is preferred for Hypercorn):
    # from hypercorn.config import Config
    # from hypercorn.asyncio import serve
    # import asyncio
    # config = Config()
    # config.bind = ["0.0.0.0:5000"]
    # asyncio.run(serve(app, config))
# Added a newline at the end of the file