# Cybersecurity Awareness Website

A comprehensive cybersecurity awareness platform featuring educational content, security tools, and an AI chatbot integration.

## Features

- Interactive homepage with cybersecurity threat updates
- Educational blogs and learning modules
- Security tools (Password Generator, URL Scanner)
- Knowledge assessment quizzes
- AI-powered chatbot using Gemini API
- Dark/Light theme toggle

## Prerequisites

Before running the project, ensure you have the following installed:

1. Python 3.11 or higher
   - Download from [Python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"

2. Git (optional, for cloning)
   - Download from [Git-scm.com](https://git-scm.com/downloads)

## Installation

### Windows Command Prompt Instructions

1. Create and navigate to a project directory:
```cmd
md cybersecurity-website
cd cybersecurity-website
```

2. Set up a Python virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

3. Install required packages:
```cmd
pip install flask flask-sqlalchemy google-generativeai requests email-validator gunicorn
```

4. Clone or download the project files to your directory

5. Set up environment variables (create a `.env` file or set via command prompt):
```cmd
set GEMINI_API_KEY=your_gemini_api_key
set SESSION_SECRET=your_session_secret
```

## Running the Application

1. Make sure you're in the project directory with the virtual environment activated

2. Start the Flask application:
```cmd
python main.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── chatbot.js
│       ├── main.js
│       ├── quiz.js
│       └── tools.js
├── templates/
│   ├── layout.html
│   ├── home.html
│   ├── blogs.html
│   ├── tools.html
│   └── quiz.html
├── app.py
├── main.py
└── README.md
```

## Features Overview

1. **Home Page**
   - Latest cybersecurity threats
   - Newsletter subscription
   - Theme toggle functionality

2. **Blogs & Modules**
   - Educational content
   - Learning resources
   - Cybersecurity best practices

3. **Security Tools**
   - Password Generator
   - URL Scanner
   - Interactive tool interfaces

4. **Quiz Section**
   - Module-based assessments
   - Score tracking
   - Answer review system

5. **AI Chatbot**
   - Powered by Google's Gemini API
   - Real-time cybersecurity assistance
   - Interactive chat interface

## Common Issues & Solutions

1. If you see "Port already in use" error:
   ```cmd
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

2. If packages fail to install:
   ```cmd
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. If the application doesn't start:
   - Check if all required packages are installed
   - Verify environment variables are set correctly
   - Ensure you're running Python 3.11 or higher

## Additional Notes

- The application runs in debug mode by default
- Always keep your Gemini API key secure
- The chat feature requires an active internet connection
