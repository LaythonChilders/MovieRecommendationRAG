Movie AI Recommendation App - README

Overview
This project is a Movie Recommendation web app built using Flask, Ollama, and ChromaDB. The app allows users to enter a movie-related prompt, which is processed to retrieve and explain a movie recommendation. The system uses Ollama models for natural language processing and movie-related embeddings stored in a ChromaDB collection.

Prerequisites
Before running the app, ensure you have the following installed:
	•	Python 3.8+ (Download from python.org)
	•	pip (Python package manager; should be installed with Python)
	•	Ollama (for model access) - ollama.com
You will also need to download the necessary models for Ollama to function correctly. This can be done through the Ollama CLI after installation.

Step-by-Step Setup

1. Install Python
    If you don't already have Python installed, download it from the official website and follow the installation instructions based on your operating system.

2. Install Required Libraries
    Ensure you have pip installed. Open your terminal or command prompt and run the following commands to install the necessary dependencies:

    	pip install flask
    	pip install chromadb
    	pip install ollama

    OR:

    	pip3 install flask
    	pip3 install chromadb
    	pip3 install ollama

    OR:

    	python3 -m pip install flask
    	python3 -m pip install chromadb
    	python3 -m pip install ollama

    IF CHROMADB GIVES AN ERROR MENTIONING FAILED TO BUILD WHEEL:
    On Mac try running this in terminal and then installing chromadb:
    
	export HNSWLIB_NO_NATIVE=1

    On Windows try the first answer here:
    
	https://stackoverflow.com/questions/73969269/error-could-not-build-wheels-for-hnswlib-which-is-required-to-install-pyprojec


3. Download Ollama Models
    Once Ollama is installed, you need to download the models required by the app. In your terminal or command prompt, run the following commands to download the models:

    ollama pull mistral-nemo
    ollama pull nomic-embed-text

These commands pull the necessary models for generating and embedding text for movie recommendations.

4. Running the Application
    In your terminal, navigate to the project directory and run the following command to start the Flask server:

    python3 movieRecommendationSystem.py

    OR

    python movieRecommendationSystem.py

    This will start the Flask development server. By default, it will be accessible at http://127.0.0.1:5000/ in your web browser.
    
5. Using the Application
	•	When you visit the app in your browser, you will see a prompt input field. Enter a movie-related request like “I want a movie with love and romance,” and click the Submit button.
	•	The app will process the input, query the ChromaDB, and return a movie recommendation along with an explanation.
	•	You can clear the chat history by clicking the Clear Chat button.


    WHEN YOU CLICK SUBMIT/ENTER YOU WILL SEE THAT THE TAB IS LOADING AS NOTED BY A PINWHEEL ON THE TAB ITSELF IN YOUR BROWSER
    BE PATIENT AND WAIT. THIS WAS DEVELOPED ON AN M3 MAX MAC AND RUNS QUICKLY BUT OTHER MACHINES MAY TAKE A COUPLE MINUTES PER REQUEST
    IF YOU WOULD LIKE I WOULD BE WILLING TO DEMO IN ZOOM/TEAMS CALL
    PLEASE CONTACT ME IF YOU HAVE ANY ISSUES

