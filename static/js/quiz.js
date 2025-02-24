document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        basics: [
            {
                question: "What is cybersecurity?",
                options: [
                    "Protection of internet-connected systems from cyber threats",
                    "A type of computer virus",
                    "A software program",
                    "A type of internet connection"
                ],
                correct: 0
            },
            {
                question: "Which of these is NOT a common cybersecurity threat?",
                options: [
                    "Phishing",
                    "Malware",
                    "Regular software updates",
                    "Ransomware"
                ],
                correct: 2
            },
            {
                question: "What is the first step in securing a system?",
                options: [
                    "Installing antivirus software",
                    "Risk assessment",
                    "Creating backups",
                    "Setting up firewalls"
                ],
                correct: 1
            }
        ],
        password: [
            {
                question: "What makes a strong password?",
                options: [
                    "Using your birthday",
                    "Using the same password everywhere",
                    "Mix of uppercase, lowercase, numbers, and symbols",
                    "Using your name"
                ],
                correct: 2
            },
            {
                question: "How often should you change your passwords?",
                options: [
                    "Never",
                    "Every 3-6 months",
                    "Every day",
                    "Only when compromised"
                ],
                correct: 1
            },
            {
                question: "Which password practice is most secure?",
                options: [
                    "Writing passwords in a notebook",
                    "Using a password manager",
                    "Using the same password with different numbers",
                    "Using short, memorable passwords"
                ],
                correct: 1
            }
        ],
        social: [
            {
                question: "What is social engineering?",
                options: [
                    "Making friends online",
                    "Manipulating people to reveal confidential information",
                    "Building social media profiles",
                    "Creating social networks"
                ],
                correct: 1
            },
            {
                question: "Which is a sign of a phishing email?",
                options: [
                    "Comes from a known sender",
                    "Has proper grammar and spelling",
                    "Urgent action required or account suspension",
                    "Contains company logo"
                ],
                correct: 2
            },
            {
                question: "What is the best defense against social engineering?",
                options: [
                    "Antivirus software",
                    "Firewall",
                    "Security awareness training",
                    "Complex passwords"
                ],
                correct: 2
            }
        ],
        network: [
            {
                question: "What is a firewall?",
                options: [
                    "A physical wall that protects servers",
                    "A security system that monitors network traffic",
                    "A type of computer virus",
                    "A backup system"
                ],
                correct: 1
            },
            {
                question: "Which network protocol is more secure?",
                options: [
                    "HTTP",
                    "HTTPS",
                    "FTP",
                    "SMTP"
                ],
                correct: 1
            }
        ]
    };

    let currentQuiz = null;
    let currentQuestion = 0;
    let score = 0;
    let answers = [];

    const startQuiz = document.getElementById('startQuiz');
    const quizIntro = document.getElementById('quiz-intro');
    const quizQuestions = document.getElementById('quiz-questions');
    const quizResults = document.getElementById('quiz-results');
    const questionText = document.getElementById('question-text');
    const optionsContainer = document.getElementById('options-container');
    const submitAnswer = document.getElementById('submitAnswer');
    const retakeQuiz = document.getElementById('retakeQuiz');

    function showQuestion() {
        const question = quizData[currentQuiz][currentQuestion];
        questionText.textContent = `Question ${currentQuestion + 1}: ${question.question}`;

        optionsContainer.innerHTML = '';
        question.options.forEach((option, index) => {
            const button = document.createElement('button');
            button.className = 'option-btn btn btn-outline-primary mb-2';
            button.textContent = option;
            button.dataset.index = index;
            button.addEventListener('click', selectOption);
            optionsContainer.appendChild(button);
        });
    }

    function selectOption(e) {
        document.querySelectorAll('.option-btn').forEach(btn => {
            btn.classList.remove('selected');
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-outline-primary');
        });
        e.target.classList.add('selected');
        e.target.classList.remove('btn-outline-primary');
        e.target.classList.add('btn-primary');
    }

    function showResults() {
        const scoreContainer = document.getElementById('score-container');
        const answersReview = document.getElementById('answers-review');

        const percentage = (score / quizData[currentQuiz].length) * 100;
        scoreContainer.textContent = `Your score: ${score}/${quizData[currentQuiz].length} (${percentage}%)`;

        answersReview.innerHTML = '';
        answers.forEach((answer, index) => {
            const question = quizData[currentQuiz][index];
            const div = document.createElement('div');
            div.className = 'mb-3';
            const isCorrect = answer === question.correct;
            div.innerHTML = `
                <div class="card ${isCorrect ? 'border-success' : 'border-danger'}">
                    <div class="card-body">
                        <h5 class="card-title">Question ${index + 1}</h5>
                        <p>${question.question}</p>
                        <p class="text-${isCorrect ? 'success' : 'danger'}">
                            Your answer: ${question.options[answer]}
                        </p>
                        ${!isCorrect ? `
                        <p class="text-success">
                            Correct answer: ${question.options[question.correct]}
                        </p>
                        ` : ''}
                    </div>
                </div>
            `;
            answersReview.appendChild(div);
        });
    }

    startQuiz.addEventListener('click', function() {
        currentQuiz = document.getElementById('quizModule').value;
        currentQuestion = 0;
        score = 0;
        answers = [];

        quizIntro.style.display = 'none';
        quizQuestions.style.display = 'block';
        quizResults.style.display = 'none';

        showQuestion();
    });

    submitAnswer.addEventListener('click', function() {
        const selected = document.querySelector('.option-btn.selected');
        if (!selected) {
            alert('Please select an answer');
            return;
        }

        const answer = parseInt(selected.dataset.index);
        answers.push(answer);

        if (answer === quizData[currentQuiz][currentQuestion].correct) {
            score++;
        }

        currentQuestion++;

        if (currentQuestion < quizData[currentQuiz].length) {
            showQuestion();
        } else {
            quizQuestions.style.display = 'none';
            quizResults.style.display = 'block';
            showResults();
        }
    });

    retakeQuiz.addEventListener('click', function() {
        quizResults.style.display = 'none';
        quizIntro.style.display = 'block';
    });
});