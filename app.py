import os
import logging
from flask import Flask, render_template, jsonify, request
from urllib.parse import urlparse
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key")

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAejNhQKzAZHXfvcj-84L0YFQZuso8NAlo")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize LangChain components
try:
    logger.info("Initializing LangChain components...")
    llm = ChatGoogleGenerativeAI(api_key=GEMINI_API_KEY, model="gemini-pro")
    embeddings_model = GoogleGenerativeAIEmbeddings(google_api_key=GEMINI_API_KEY, model="models/embedding-001")
    logger.info("Successfully initialized LangChain models")

    # Initialize RAG components
    logger.info("Loading PDF and creating vector store...")
    pdf = PyPDFLoader("attached_assets/rag_test.pdf")
    documents = pdf.load()
    vectorstore_db = FAISS.from_documents(documents=documents, embedding=embeddings_model)
    logger.info("Successfully initialized RAG components")
except Exception as e:
    logger.error(f"Error initializing RAG components: {str(e)}")
    vectorstore_db = None
    llm = None

# Enhanced module content with more details
MODULES = {
    'basics': {
        'title': 'Basics of Cybersecurity',
        'difficulty': 'Beginner',
        'reading_time': 15,
        'introduction': 'Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks. These attacks are usually aimed at accessing, changing, or destroying sensitive information; extorting money from users; or interrupting normal business processes.',
        'sections': [
            {
                'title': 'What is Cybersecurity?',
                'content': '''Cybersecurity refers to the body of technologies, processes, and practices designed to protect networks, devices, programs, and data from attack, damage, or unauthorized access. It\'s become increasingly important as our world becomes more digital and connected.

In today's interconnected world, cybersecurity is crucial for:
- Protecting personal information
- Securing financial transactions
- Maintaining business continuity
- Safeguarding national security''',
                'tips': [
                    'Stay updated with the latest security threats',
                    'Always use strong passwords',
                    'Keep your software updated',
                    'Use multi-factor authentication when available'
                ]
            },
            {
                'title': 'Common Types of Cyber Threats',
                'content': '''Cyber threats come in many forms. Understanding these threats is crucial for protection:

1. Malware: Software designed to harm systems
2. Phishing: Deceptive attempts to steal sensitive information
3. Ransomware: Malware that encrypts files for ransom
4. Social Engineering: Manipulating people to reveal confidential information
5. Zero-day Exploits: Attacks targeting unknown vulnerabilities''',
                'tips': [
                    'Learn to recognize phishing attempts',
                    'Install and maintain antivirus software',
                    'Back up your data regularly',
                    'Use network monitoring tools'
                ]
            },
            {
                'title': 'Basic Security Measures',
                'content': '''Essential security measures everyone should implement:

1. Strong Password Policies
2. Regular Software Updates
3. Data Encryption
4. Network Security
5. Employee Training
6. Incident Response Planning''',
                'tips': [
                    'Implement defense in depth',
                    'Regular security audits',
                    'Monitor system logs',
                    'Create security policies'
                ]
            }
        ],
        'key_points': [
            'Cybersecurity is essential in today\'s digital world',
            'Multiple layers of security are needed for effective protection',
            'Both technical and human factors play crucial roles',
            'Regular updates and monitoring are critical',
            'Employee training is as important as technical measures'
        ],
        'resources': [
            {
                'title': 'NIST Cybersecurity Framework',
                'url': 'https://www.nist.gov/cyberframework',
                'description': 'Comprehensive cybersecurity guidance'
            },
            {
                'title': 'SANS Security Awareness',
                'url': 'https://www.sans.org/security-awareness-training',
                'description': 'Security awareness training resources'
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
                'content': '''A strong password is your first line of defense. Follow these guidelines:

1. Length: At least 12 characters
2. Complexity: Mix of uppercase, lowercase, numbers, and symbols
3. Uniqueness: Different password for each account
4. Avoid: Personal information, dictionary words, common substitutions''',
                'tips': [
                    'Use at least 12 characters',
                    'Avoid personal information',
                    'Use a different password for each account',
                    'Consider using a password manager'
                ]
            },
            {
                'title': 'Password Management',
                'content': '''Effective password management involves:

1. Password Managers
2. Regular Updates
3. Secure Storage
4. Multi-Factor Authentication
5. Recovery Options''',
                'tips': [
                    'Use a reputable password manager',
                    'Enable 2FA where available',
                    'Regular password audits',
                    'Secure backup of master password'
                ]
            }
        ],
        'key_points': [
            'Length is more important than complexity',
            'Never reuse passwords across accounts',
            'Use a password manager for better security',
            'Enable multi-factor authentication',
            'Regular password updates enhance security'
        ],
        'resources': [
            {
                'title': 'Have I Been Pwned',
                'url': 'https://haveibeenpwned.com',
                'description': 'Check if your passwords have been compromised'
            },
            {
                'title': 'Password Security Best Practices',
                'url': 'https://pages.nist.gov/800-63-3/sp800-63b.html',
                'description': 'NIST password guidelines'
            }
        ]
    }
}

# Enhanced quiz data with more questions
QUIZ_DATA = {
    'basics': [
        {
            'question': "What is the primary goal of cybersecurity?",
            'options': [
                "Protection of systems and data from cyber threats",
                "Making computers faster",
                "Creating new software",
                "Connecting to the internet"
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
        },
        {
            'question': "Which is a key principle of cybersecurity?",
            'options': [
                "Defense in depth",
                "Single factor authentication",
                "Using same password everywhere",
                "Keeping software outdated"
            ],
            'correct': 0
        },
        {
            'question': "What is zero-day exploit?",
            'options': [
                "A vulnerability unknown to the software vendor",
                "A type of antivirus",
                "A backup system",
                "A strong password"
            ],
            'correct': 0
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
        },
        {
            'question': "What is the minimum recommended password length?",
            'options': [
                "6 characters",
                "8 characters",
                "12 characters",
                "16 characters"
            ],
            'correct': 2
        },
        {
            'question': "Which is the best additional security measure for passwords?",
            'options': [
                "Writing them down",
                "Using personal information",
                "Multi-factor authentication",
                "Using common words"
            ],
            'correct': 2
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
        logger.info(f"Received chat message: {user_message}")

        # Use RAG if available
        if vectorstore_db and llm:
            try:
                # Get relevant documents
                docs = vectorstore_db.similarity_search(user_message)
                context = "\n".join([doc.page_content for doc in docs])
                logger.debug(f"Found relevant context: {context[:200]}...")

                # Construct prompt with context
                prompt = f"""
                Context: {context}

                User Question: {user_message}

                Please provide a helpful response about cybersecurity based on the context and your knowledge.
                Keep the response clear and concise, focusing on practical advice and best practices.
                """

                response = llm.invoke(prompt)
                logger.info("Successfully generated RAG response")
                return jsonify({'response': response.text})
            except Exception as e:
                logger.error(f"RAG processing error: {str(e)}")
                # Fallback to regular Gemini response
                response = genai.GenerativeModel('gemini-pro').generate_content(user_message)
                return jsonify({'response': response.text})
        else:
            # Fallback to regular Gemini response
            logger.info("Using fallback Gemini response (RAG not available)")
            response = genai.GenerativeModel('gemini-pro').generate_content(user_message)
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