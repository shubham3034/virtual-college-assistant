from flask import Flask, request, jsonify, render_template_string
from difflib import SequenceMatcher
import re

app = Flask(__name__)

# ==========================================
# COLLEGE INFORMATION DATABASE
# Customize this information for your college
# ==========================================

COLLEGE_NAME = "ABC College of Technology"

FAQS = [
    {
        "keywords": ["admission", "apply", "registration", "eligibility"],
        "answer": "Admissions are handled by the college admission office. Students generally need their academic certificates, identity proof and photographs. Contact the admission office for current dates and eligibility."
    },
    {
        "keywords": ["courses", "departments", "mca", "bca", "bba", "programs"],
        "answer": "Our sample college offers MCA, BCA, BBA and other undergraduate and postgraduate programs. Update this list according to your college."
    },
    {
        "keywords": ["fees", "fee structure", "payment", "scholarship"],
        "answer": "For information about tuition fees, payment deadlines and scholarships, please contact the college accounts department."
    },
    {
        "keywords": ["timetable", "time table", "class timing", "schedule", "lectures"],
        "answer": "Class timetables are generally provided by individual departments. Students can check the notice board or contact their department coordinator."
    },
    {
        "keywords": ["exam", "examination", "date sheet", "admit card", "result"],
        "answer": "Examination schedules, admit cards and results are announced by the examination department. Please check the official college notice board."
    },
    {
        "keywords": ["library", "books", "reading room", "book issue"],
        "answer": "Students can visit the college library using their valid student ID. Contact the librarian for book issue, return and renewal policies."
    },
    {
        "keywords": ["placement", "internship", "job", "career", "companies"],
        "answer": "The Training and Placement Cell provides career guidance, placement assistance, internship opportunities and interview preparation."
    },
    {
        "keywords": ["hostel", "canteen", "wifi", "sports", "transport", "facilities", "laboratory"],
        "answer": "Campus facilities may include laboratories, library, canteen, sports areas, Wi-Fi, transport and hostel facilities. Please confirm availability with your college."
    },
    {
        "keywords": ["contact", "phone", "email", "address", "location", "office"],
        "answer": "College: ABC College of Technology\nAddress: Your College Address, Your City\nPhone: +91-00000-00000\nEmail: info@example.com\nReplace these sample details with your actual college information."
    },
    {
        "keywords": ["holiday", "holidays", "working days", "office hours"],
        "answer": "Please refer to the academic calendar or contact the college office for official holidays and working hours."
    },
    {
        "keywords": ["principal", "director", "head"],
        "answer": "For information about the principal or college administration, please contact the college office."
    },
    {
        "keywords": ["thank you", "thanks"],
        "answer": "You're welcome! I'm always happy to help you. 😊"
    },
    {
        "keywords": ["hello", "hi", "hey", "good morning", "good afternoon"],
        "answer": "Hello! 👋 Welcome to CampusBuddy. How can I help you today?"
    }
]

def clean_text(text):
    return re.sub(r"[^a-z0-9 ]", " ", text.lower()).strip()

def get_answer(question):

    question = clean_text(question)

    best_answer = None
    best_score = 0

    for item in FAQS:

        for keyword in item["keywords"]:

            keyword = clean_text(keyword)

            score = SequenceMatcher(
                None, question, keyword
            ).ratio()

            q_words = set(question.split())
            k_words = set(keyword.split())

            if k_words:
                score = max(
                    score,
                    len(q_words & k_words) / len(k_words)
                )

            if keyword in question:
                score = max(score, 0.85)

            if score > best_score:
                best_score = score
                best_answer = item["answer"]

    if best_score >= 0.35:
        return best_answer

    return (
        "Sorry! I couldn't understand your question. "
        "Please ask about admissions, courses, fees, "
        "timetable, examinations, library, placements "
        "or college facilities."
    )


# ==========================================
# WEBSITE DESIGN
# ==========================================

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>CampusBuddy - Virtual College Assistant</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f2f4fb;
    color: #202844;
}

.container {
    display: flex;
    min-height: 100vh;
}

.sidebar {
    width: 260px;
    background: #171d35;
    color: white;
    padding: 30px 22px;
}

.logo {
    font-size: 25px;
    font-weight: bold;
    color: #a99cff;
}

.subtitle {
    font-size: 11px;
    color: #b9bfd1;
    letter-spacing: 2px;
}

.sidebar h2 {
    margin-top: 60px;
    font-size: 23px;
    line-height: 1.4;
}

.sidebar p {
    color: #bbc1d2;
    line-height: 1.7;
    font-size: 13px;
}

.main {
    flex: 1;
    padding: 35px;
    max-width: 1200px;
    margin: auto;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e2e5ee;
    padding-bottom: 20px;
}

.header h1 {
    font-size: 25px;
}

.online {
    color: #15996d;
    background: #e1f8ef;
    padding: 9px 15px;
    border-radius: 20px;
    font-size: 12px;
}

.welcome {
    margin: 30px 0;
}

.welcome h2 {
    font-size: 22px;
}

.welcome p {
    color: #7d859a;
}

.quick {
    margin-bottom: 25px;
}

.quick button {
    padding: 11px 15px;
    margin: 5px 4px;
    background: white;
    border: 1px solid #dddfee;
    border-radius: 9px;
    cursor: pointer;
    color: #444b65;
}

.quick button:hover {
    background: #eeeaff;
    border-color: #7968df;
}

.chatbox {
    background: white;
    border-radius: 16px;
    box-shadow: 0 5px 25px #00000008;
    overflow: hidden;
}

.chat-header {
    padding: 20px;
    border-bottom: 1px solid #eee;
    font-weight: bold;
}

.messages {
    height: 380px;
    overflow-y: auto;
    padding: 20px;
    background: #fcfcfe;
}

.message {
    padding: 13px 16px;
    margin: 12px 0;
    max-width: 80%;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.6;
    white-space: pre-wrap;
}

.bot {
    background: #efedff;
    color: #37305f;
}

.user {
    background: #6558d3;
    color: white;
    margin-left: auto;
}

.input-area {
    display: flex;
    padding: 15px;
    gap: 10px;
}

.input-area input {
    flex: 1;
    padding: 14px;
    border: 1px solid #ddd;
    border-radius: 9px;
    outline: none;
}

.input-area button {
    width: 50px;
    background: #6558d3;
    color: white;
    border: none;
    border-radius: 9px;
    font-size: 20px;
    cursor: pointer;
}

.input-area button:hover {
    background: #5144bd;
}

footer {
    text-align: center;
    margin-top: 25px;
    color: #999;
    font-size: 12px;
}

@media(max-width: 750px) {

    .container {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        padding: 20px;
    }

    .sidebar h2, .sidebar p {
        display: none;
    }

    .main {
        padding: 18px;
        width: 100%;
    }

    .header h1 {
        font-size: 19px;
    }

    .messages {
        height: 350px;
    }

    .message {
        max-width: 95%;
    }
}

</style>
</head>

<body>

<div class="container">

<aside class="sidebar">

    <div class="logo">CB CampusBuddy</div>

    <div class="subtitle">VIRTUAL COLLEGE ASSISTANT</div>

    <h2>Your College Helper</h2>

    <p>
        Get instant answers to your college-related
        questions with CampusBuddy.
    </p>

</aside>

<main class="main">

    <div class="header">

        <h1>Virtual College Assistant</h1>

        <div class="online">● Online</div>

    </div>

    <div class="welcome">

        <h2>Hello, Student! 👋</h2>

        <p>
        Welcome to CampusBuddy.
        What would you like to know today?
        </p>

    </div>

    <div class="quick">

        <button onclick="quickAsk('Admission process')">
        🎓 Admissions
        </button>

        <button onclick="quickAsk('Available courses')">
        📚 Courses
        </button>

        <button onclick="quickAsk('Fee structure')">
        💰 Fees
        </button>

        <button onclick="quickAsk('Class timetable')">
        🗓 Timetable
        </button>

        <button onclick="quickAsk('Examination details')">
        📝 Exams
        </button>

        <button onclick="quickAsk('College contact')">
        ☎ Contact
        </button>

    </div>

    <div class="chatbox">

        <div class="chat-header">
            🤖 CampusBuddy Assistant
            <button onclick="clearChat()"
            style="float:right;border:none;background:none;cursor:pointer;color:#6558d3">
            Clear Chat
            </button>
        </div>

        <div class="messages" id="messages">

            <div class="message bot">
            Hi! I'm CampusBuddy. Ask me anything about your college.
            </div>

        </div>

        <div class="input-area">

            <input
                type="text"
                id="question"
                placeholder="Type your question here..."
                onkeydown="if(event.key==='Enter') sendMessage()"
            >

            <button onclick="sendMessage()">➤</button>

        </div>

    </div>

    <footer>
        CampusBuddy | Virtual College Assistant | MCA Minor Project
    </footer>

</main>

</div>

<script>

async function sendMessage(text) {

    let input = document.getElementById("question");

    let question = text || input.value.trim();

    if (!question) return;

    addMessage(question, "user");

    input.value = "";

    try {

        let response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: question
            })

        });

        let data = await response.json();

        addMessage(data.reply, "bot");

    } catch(error) {

        addMessage(
            "Unable to connect to the assistant. Please try again.",
            "bot"
        );

    }

}

function quickAsk(question) {
    sendMessage(question);
}

function addMessage(text, sender) {

    let messages = document.getElementById("messages");

    let div = document.createElement("div");

    div.className = "message " + sender;

    div.textContent = text;

    messages.appendChild(div);

    messages.scrollTop = messages.scrollHeight;

}

function clearChat() {

    document.getElementById("messages").innerHTML = "";

    addMessage(
        "Chat cleared! How can I help you?",
        "bot"
    );

}

</script>

</body>
</html>
"""


# ==========================================
# FLASK ROUTES
# ==========================================

@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    question = data.get("message", "").strip()

    if not question:
        return jsonify({
            "reply": "Please enter a question."
        })

    answer = get_answer(question)

    return jsonify({
        "reply": answer
    })


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
