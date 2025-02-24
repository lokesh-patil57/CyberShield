from flask import Flask, render_template, jsonify, request
import os
import requests
from urllib.parse import urlparse
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key")

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAejNhQKzAZHXfvcj-84L0YFQZuso8NAlo")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    print("Accessing home route")  # Debug print
    return render_template('home.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        response = model.generate_content(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        print(f"Chat error: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/scan-url', methods=['POST'])
def scan_url():
    url = request.json['url']
    try:
        parsed_url = urlparse(url)
        # This is a mock response since we don't have a real API key
        return jsonify({
            'safe': True,
            'message': 'URL appears to be safe'
        })
    except Exception as e:
        print(f"URL scan error: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask application...")  # Debug print
    app.run(host='0.0.0.0', port=5000, debug=True)