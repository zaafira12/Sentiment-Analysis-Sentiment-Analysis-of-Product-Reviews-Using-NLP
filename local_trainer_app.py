# local_app.py

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# --- IMPORTANT ---
# Paste the public URL you got from your Google Colab notebook here.
# Make sure it ends with /analyze
COLAB_API_URL = "https://unschooled-collaterally-arianna.ngrok-free.dev/analyze"


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            feedback_text = request.form['feedback']
            if not feedback_text.strip():
                result = {"error": "Feedback text cannot be empty."}
            else:
                payload = {'feedback_text': feedback_text}
                # Send the request to your Colab backend
                response = requests.post(COLAB_API_URL, json=payload, timeout=20)
                response.raise_for_status() # Raise an exception for bad status codes
                result = response.json()
        except requests.exceptions.RequestException as e:
            result = {"error": f"Could not connect to the Colab API. Is the server running and the URL correct? Details: {e}"}
        except Exception as e:
            result = {"error": f"An unexpected error occurred: {e}"}

    return render_template('index.html', result=result)

if __name__ == '__main__':
    # Runs the local web server on http://1227.0.0.1:5000
    print("🚀 Starting local Flask server at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)