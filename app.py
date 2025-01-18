from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import requests

app = Flask(__name__)
Bootstrap(app)

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
API_KEY = "AIzaSyB4_ngtPKrDSbWk_rsyvN8WZR_K3kzzpMQ"

def ask_gemini(question):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": question
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"{API_URL}?key={API_KEY}", json=payload, headers=headers
        )
        response_data = response.json()
        raw_reply = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No reply found.")
        
        # Định dạng lại câu trả lời
        formatted_reply = raw_reply.replace("\n", "<br>").replace("**", "<strong>").replace("*", "<em>")
        
        return formatted_reply
    except Exception as e:
        return f"Error: {e}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    if not question:
        return jsonify({"error": "No question provided."}), 400

    reply = ask_gemini(question)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
