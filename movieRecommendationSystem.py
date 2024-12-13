import ollama
import chromadb
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

class moveAI:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./EmbeddingDB") 
        self.collection = self.client.get_or_create_collection(name="movie_embeddings")

    def convertPrompt(self, user_prompt):

        query_prompt = f"""
        Example output:
        'genre, genre' : a short movie description.

        Given the prompt: '{user_prompt}', extract the genre(s) and provide a brief description in the format: Genre(s), Description.
        """


        interpreted_query = ollama.generate(
            model="mistral-nemo",
            prompt=query_prompt
        )['response']
        return interpreted_query
    
    def embedQuery(self, interpreted_query):
        embedded_query = ollama.embeddings(
            prompt=interpreted_query,
            model="nomic-embed-text"
        )
        return embedded_query
    
    def queryDB(self, embedded_query):
        results = self.collection.query(
            query_embeddings=[embedded_query["embedding"]],
            n_results=1
        )
        return results["documents"][0]
    
    def explainQueryResponse(self, query_response, user_prompt):
        query_prompt = f"""
        You are an assistant helping users find movies. Your job is to explain their results clearly and concisely.

        User's search prompt: '{user_prompt}'
        Movie result: '{query_response}'

        Instructions:
        - Start by addressing the user directly (e.g., "Based on your search, we found this movie...").
        - Briefly explain the movie result with its title and a concise description. If necessary, rephrase or shorten the description to make it clearer.
        - If the result doesn’t closely match the user's search, acknowledge this and politely explain that the database has limited information.

        Examples:
        - User prompt: "action movie with cars and explosions"
        Movie result: "Fast & Furious: An adrenaline-packed action movie featuring high-speed car chases and thrilling stunts."
        Response: "Based on your search, we found 'Fast & Furious,' an action-packed movie with high-speed car chases and thrilling stunts. If this isn’t quite what you were looking for, please note that our database may not have every possible match."

        - User prompt: "romantic comedy about two strangers falling in love"
        Movie result: "When Harry Met Sally: A classic romantic comedy about friendship and unexpected love."
        Response: "We found 'When Harry Met Sally,' a classic romantic comedy about friendship and unexpected love. Let us know if you were hoping for something different!"

        - User prompt: "sci-fi thriller with space battles"
        Movie result: "Unknown Movie: No exact matches found."
        Response: "It seems we don’t have an exact match for your search. Our database is limited, but we’re constantly improving. Feel free to refine your query!"

        Now, craft a response for the user based on the provided search prompt and movie result.
        """

        response = ollama.generate(
            model="mistral-nemo",
            prompt=query_prompt
        )['response']
        return response

movieAI = moveAI()

@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize chat history if it doesn't exist
    if 'chatMessages' not in session:
        session['chatMessages'] = []

    chatMessages = session.get('chatMessages', [])  # Retrieve chat messages

    if request.method == "POST":
        if request.form.get('Submit') == 'Submit':
            user_prompt = request.form.get("user_prompt", "").strip()  # Safely retrieve input
            
            if not user_prompt:  # Check for empty input
                return render_template("index.html", chatMessages=chatMessages)

            # Add user's message to the chat history
            session['chatMessages'].append({"type": "user", "content": user_prompt})

            # Simplify the user prompt
            interpreted_query = movieAI.convertPrompt(user_prompt)

            # Embed the simplified query
            embedded_query = movieAI.embedQuery(interpreted_query)

            # Query the database for results
            query_response = movieAI.queryDB(embedded_query)

            response = movieAI.explainQueryResponse(query_response, user_prompt)

            # Add AI's response to the chat history
            session['chatMessages'].append({"type": "response", "content": response})

            # Update session to persist changes
            session.modified = True

        elif request.form.get('Clear Chat') == 'Clear Chat':
            session.pop('chatMessages', None)
            chatMessages = []  # Reset chatMessages after clearing
            session.modified = True

    return render_template("index.html", chatMessages=chatMessages)



if __name__ == "__main__":
    app.run(debug=True)
