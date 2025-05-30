# TravelAI - Intelligent Travel Planner

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Quart](https://img.shields.io/badge/Quart-0.19+-purple.svg)](https://quart.palletsprojects.com/)
[![Groq API](https://img.shields.io/badge/AI-Groq%20LLaMA%203.3%2070B-green.svg)](https://groq.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=flat&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=flat&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=flat&logo=javascript&logoColor=%23F7DF1E)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Project Status: Active](https://img.shields.io/badge/status-active%20development-brightgreen)](https://github.com/vamsi-31/Travel-Ai-Planner)

TravelAI is a modern web application designed to simplify your travel planning. By leveraging the power of large language models via the Groq API, it generates personalized and detailed travel itineraries based on your unique preferences. The application features an asynchronous backend built with Quart for high performance and a sleek, responsive frontend for an intuitive user experience.

## ✨ Features

*   **Personalized Itineraries:** Generates custom travel plans based on destination, duration, budget, season, preferred pace, and specific interests.
*   **AI-Powered:** Utilizes the Groq LPU with the LLaMA 3.3 70B model for fast and intelligent itinerary creation.
*   **Asynchronous Backend:** Built with Quart (an ASGI framework similar to Flask but asynchronous) to handle API calls and user requests efficiently without blocking.
*   **Sleek, Minimalistic UI:** Modern, responsive design with a light blue color scheme, gradients, and blur effects for an enhanced user experience.
*   **Interactive Itinerary Display:**
    *   **Collapsible Sections:** Each day in the generated itinerary is presented in a collapsible section for improved readability and navigation.
    *   **Copy to Clipboard:** Easily copy the generated itinerary (in Markdown format) with a single click.
*   **User-Friendly Form:** Interactive form with clear input fields and validation.
*   **Markdown Rendering:** Itineraries are beautifully rendered from Markdown using Marked.js.

## 🛠️ Tech Stack

*   **Backend:**
    *   Python 3.8+
    *   Quart (ASGI web framework)
    *   Groq Python SDK (for interacting with the Groq API)
*   **Frontend:**
    *   HTML5
    *   CSS3
    *   Vanilla JavaScript
    *   Marked.js (for rendering Markdown to HTML)
*   **AI Model:**
    *   Groq LPU running LLaMA 3.3 70B (or other models available via Groq API)
*   **Local Deployment/Serving:**
    *   Hypercorn (ASGI server)

## 🚀 Setup and Installation

Follow these steps to get TravelAI running on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/vamsi-31/Travel-Ai-Planner.git
    cd Travel-Ai-Planner
    ```

2.  **Create and Activate a Virtual Environment** (Recommended):
    *   On macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    *   Create a file named `.env` in the root directory of the project.
    *   Add your Groq API key to this file:
        ```env
        GROQ_API_KEY='your_actual_groq_api_key_here'
        ```
    *   You can obtain a Groq API key by signing up at [GroqCloud](https://console.groq.com/keys).

5.  **Ensure `.env` is in `.gitignore`:**
    The `.env` file should not be committed to version control. The provided `.gitignore` file should already include it.

## 🏃 Running the Application

1.  **Start the Hypercorn ASGI Server:**
    Open your terminal in the project root directory (where `app.py` is located) and run:
    ```bash
    hypercorn -b 0.0.0.0:5000 app:app
    ```
    *   `-b 0.0.0.0:5000` binds the server to all available network interfaces on port 5000.
    *   `app:app` tells Hypercorn to load the Quart application instance named `app` from the `app.py` file.

2.  **Access the Application:**
    Open your web browser and navigate to:
    [http://localhost:5000](http://localhost:5000)

    Fill out the travel preferences form, and TravelAI will generate your personalized itinerary!

## ⚡ Asynchronous Backend Explained

TravelAI's backend is built using Quart, an asynchronous Python web framework. This means:
*   It uses `async` and `await` keywords to handle operations that might take time (like making API calls to Groq) without freezing the entire server.
*   When a request to generate an itinerary comes in, the call to the Groq API is performed asynchronously. While waiting for Groq's response, the server can handle other incoming requests, making the application more responsive and scalable, especially under load.
*   Hypercorn, being an ASGI server, is designed to work with asynchronous applications like those built with Quart.

## 📸 Screenshots

<!-- Add a screenshot of the UI here -->
*Awaiting screenshot of the sleek, updated UI in action!*

Example:
![TravelAI UI Screenshot Placeholder](https://via.placeholder.com/800x500.png?text=TravelAI+UI+Screenshot)


## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or encounter any issues, please feel free to:
1.  Open an issue on the GitHub repository.
2.  Fork the repository, create a feature branch, make your changes, and submit a pull request.

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

## 🙏 Acknowledgements

*   [Quart](https://quart.palletsprojects.com/) for the asynchronous web framework.
*   [Groq](https://groq.com/) for providing the high-speed LPU and API for language model inference.
*   [Marked.js](https://marked.js.org/) for easy Markdown-to-HTML conversion.
*   [Poppins Font](https://fonts.google.com/specimen/Poppins) by Google Fonts.
*   [Shields.io](https://shields.io/) for the cool badges.

---
*Plan your next adventure with TravelAI!*
