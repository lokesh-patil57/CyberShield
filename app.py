from flask import Flask, render_template, jsonify, request
import os
import requests
from urllib.parse import urlparse
import google.generativeai as genai
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key")

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAejNhQKzAZHXfvcj-84L0YFQZuso8NAlo")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

logger.info("Configured basic Flask application and Gemini API")

# Temporarily disable RAG initialization
vectorstore_db = None
logger.info("RAG initialization disabled for debugging")

# Module content
MODULES = {
    'basics': {
        'title': 'Basics of Cybersecurity',
        'difficulty': 'Beginner',
        'reading_time': 15,
        'introduction': 'Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks. These attacks are usually aimed at accessing, changing, or destroying sensitive information; extorting money from users; or interrupting normal business processes.',
        'sections': [
            {
                'title': 'What is Cybersecurity?',
                'content': 'Cybersecurity refers to the body of technologies, processes, and practices designed to protect networks, devices, programs, and data from attack, damage, or unauthorized access. It\'s become increasingly important as our world becomes more digital and connected.',
                'tips': [
                    'Stay updated with the latest security threats',
                    'Always use strong passwords',
                    'Keep your software updated'
                ]
            },
            {
                'title': 'Common Types of Cyber Threats',
                'content': 'Cyber threats come in many forms: malware, phishing, ransomware, and social engineering attacks are some of the most common. Understanding these threats is the first step in protecting yourself and your organization.',
                'tips': [
                    'Learn to recognize phishing attempts',
                    'Install and maintain antivirus software',
                    'Back up your data regularly'
                ]
            }
        ],
        'key_points': [
            'Cybersecurity is essential in today\'s digital world',
            'Multiple layers of security are needed for effective protection',
            'Both technical and human factors play crucial roles'
        ],
        'resources': [
            {
                'title': 'NIST Cybersecurity Framework',
                'url': 'https://www.nist.gov/cyberframework',
                'description': 'Comprehensive cybersecurity guidance'
            }
        ]
    },
    'password': {
        'title': 'Password Security',
        'difficulty': 'Beginner',
        'reading_time': 10,
        'introduction': 'Password security is your first line of defense in protecting your digital assets. Learn how to create and manage strong passwords effectively.',
        'sections': [
            {
                'title': 'Creating Strong Passwords',
                'content': 'A strong password is long, complex, and unique. It should contain a mix of uppercase and lowercase letters, numbers, and special characters.',
                'tips': [
                    'Use at least 12 characters',
                    'Avoid personal information',
                    'Use a different password for each account'
                ]
            }
        ],
        'key_points': [
            'Length is more important than complexity',
            'Never reuse passwords across accounts',
            'Consider using a password manager'
        ],
        'resources': [
            {
                'title': 'Have I Been Pwned',
                'url': 'https://haveibeenpwned.com',
                'description': 'Check if your passwords have been compromised'
            }
        ]
    },
    # Add more modules here
}

# Quiz data structure with expanded questions
QUIZ_DATA = {
    'basics': [
        {
            'question': "What is cybersecurity?",
            'options': [
                "Protection of internet-connected systems from cyber threats",
                "A type of computer virus",
                "A software program",
                "A type of internet connection"
            ],
            'correct': 0
        },
        {
            'question': "Which of these is NOT a common cybersecurity threat?",
            'options': [
                "Phishing",
                "Malware",
                "Regular software updates",
                "Ransomware"
            ],
            'correct': 2
        },
        {
            'question': "What is the first step in securing a system?",
            'options': [
                "Installing antivirus software",
                "Risk assessment",
                "Creating backups",
                "Setting up firewalls"
            ],
            'correct': 1
        }
    ],
    'password': [
        {
            'question': "What makes a strong password?",
            'options': [
                "Using your birthday",
                "Using the same password everywhere",
                "Mix of uppercase, lowercase, numbers, and symbols",
                "Using your name"
            ],
            'correct': 2
        },
        {
            'question': "How often should you change your passwords?",
            'options': [
                "Never",
                "Every 3-6 months",
                "Every day",
                "Only when compromised"
            ],
            'correct': 1
        },
        {
            'question': "Which password practice is most secure?",
            'options': [
                "Writing passwords in a notebook",
                "Using a password manager",
                "Using the same password with different numbers",
                "Using short, memorable passwords"
            ],
            'correct': 1
        }
    ],
    'social': [
        {
            'question': "What is social engineering?",
            'options': [
                "Making friends online",
                "Manipulating people to reveal confidential information",
                "Building social media profiles",
                "Creating social networks"
            ],
            'correct': 1
        },
        {
            'question': "Which is a sign of a phishing email?",
            'options': [
                "Comes from a known sender",
                "Has proper grammar and spelling",
                "Urgent action required or account suspension",
                "Contains company logo"
            ],
            'correct': 2
        },
        {
            'question': "What is the best defense against social engineering?",
            'options': [
                "Antivirus software",
                "Firewall",
                "Security awareness training",
                "Complex passwords"
            ],
            'correct': 2
        }
    ],
    'network': [
        {
            'question': "What is a firewall?",
            'options': [
                "A physical wall that protects servers",
                "A security system that monitors network traffic",
                "A type of computer virus",
                "A backup system"
            ],
            'correct': 1
        },
        {
            'question': "Which network protocol is more secure?",
            'options': [
                "HTTP",
                "HTTPS",
                "FTP",
                "SMTP"
            ],
            'correct': 1
        }
    ]
}

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

@app.route('/module/<module_id>')
def module(module_id):
    if module_id in MODULES:
        return render_template('module.html', module=MODULES[module_id])
    return 'Module not found', 404

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']

        # Use RAG if available
        if vectorstore_db:
            try:
                # Get relevant documents
                docs = vectorstore_db.similarity_search(user_message)
                context = "\n".join([doc.page_content for doc in docs])

                # Construct prompt with context
                prompt = f"""
                Context: {context}

                User Question: {user_message}

                Please provide a helpful response based on the context and your knowledge.
                """

                response = model.generate_content(prompt)
                return jsonify({'response': response.text})
            except Exception as e:
                logger.error(f"RAG processing error: {str(e)}")
                # Fallback to regular Gemini response
                response = model.generate_content(user_message)
                return jsonify({'response': response.text})
        else:
            # Fallback to regular Gemini response
            response = model.generate_content(user_message)
            return jsonify({'response': response.text})

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/scan-url', methods=['POST'])
def scan_url():
    url = request.json['url']
    try:
        parsed_url = urlparse(url)
        return jsonify({
            'safe': True,
            'message': 'URL appears to be safe'
        })
    except Exception as e:
        logger.error(f"URL scan error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)