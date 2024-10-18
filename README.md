
# TravelAI - Your Intelligent Travel Planner

TravelAI is a web application that leverages AI to generate personalized travel itineraries based on user preferences. It uses Flask for the backend, vanilla JavaScript for the frontend, and integrates with the Groq API for AI-powered itinerary generation.

## Features

- User-friendly interface for inputting travel preferences
- AI-generated personalized travel itineraries
- Responsive design for various screen sizes
- Markdown rendering of generated itineraries

## Prerequisites

Before you begin, ensure you have met the following requirements:
```
- Python 3.7+
- pip (Python package manager)
- Node.js and npm (for potential future frontend development)
- A Groq API key
```
## Installation

1. Clone the repository:
   ```
   git clone https://github.com/vamsi-31/Travel-Ai-Planner.git
   cd travelai
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required Python packages:
   ```
   pip install flask flask-cors groq python-dotenv
   ```

4. Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Configuration

1. Update the `app.py` file to use the environment variable:

   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()

   client = Groq(api_key=os.getenv('GROQ_API_KEY'))
   ```

2. Ensure that `.env` is added to your `.gitignore` file to keep your API key secret.

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://127.0.0.1:5000`

3. Fill out the travel preferences form and click "Generate Itinerary" to receive your personalized travel plan.

## Project Structure

```
travelai/
│
├── app.py              # Flask application
├── static/
│   └── index.html      # Frontend HTML file
├── .env                # Environment variables (not in version control)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Contributing

Contributions to TravelAI are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Groq](https://groq.com/)
- [Marked.js](https://marked.js.org/)

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.

