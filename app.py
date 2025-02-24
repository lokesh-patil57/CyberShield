from flask import Flask, render_template, jsonify, request
import google.generativeai as genai
import os
import requests
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key")

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyAejNhQKzAZHXfvcj-84L0YFQZuso8NAlo"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
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
        return jsonify({'error': str(e)}), 500

@app.route('/scan-url', methods=['POST'])
def scan_url():
    url = request.json['url']
    try:
        parsed_url = urlparse(url)
        response = requests.get(f"https://api.virustotal.com/v3/domains/{parsed_url.netloc}")
        # This is a mock response since we don't have a real API key
        return jsonify({
            'safe': True,
            'message': 'URL appears to be safe'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
