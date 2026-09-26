EduGenie: Google Gemini Powered Learning Assistant

Project Description
EduGenie is a lightweight AI-powered educational assistant that simplifies learning through generative AI. Designed for students of all academic levels, EduGenie enables users to:
Ask questions and receive smart, concise answers
Understand complex concepts through simplified explanations
Generate quizzes from topics or text
Receive personalized learning recommendations
Summarize large educational passages
Built with FastAPI for the backend and a simple HTML+CSS frontend, EduGenie leverages lightweight and cloud-based AI models for local efficiency and cloud power. It works well on devices like the Mac M1, making it accessible to a broad range of learners and developers.
Scenarios
Scenario 1: A student wants to know about oceans and rivers uses EduGenie to ask “Which is the largest ocean?”
Scenario 2: A student wants to know the level of her understanding of “The Pythagoras Theorem” and clicks “Generate Quiz.”
Scenario 3: A learner exploring SQL requests a learning path which is a structured plan with beginner to advanced topics, timelines, and suggestions.

ARCHITECTURAL DIAGRAM

Pre-requisites
Python 3.10+
Official Documentation: Google AI for Developers
Installation Guide: Tom's Hardware
Popular Tutorial: Python Programming Tutorial - Full Course for Beginners
Installation Steps:
Download the latest Python 3.10+ installer for your operating system from the official website.
Run the installer and ensure you check the box that says "Add Python to PATH".
Follow the installation prompts to complete the setup.
Verify the installation by opening a terminal or command prompt and typing python --version.

FastAPI Framework –
Official Documentation: FastAPI
User Guide: FastAPI
Popular Tutorial: FastAPI Crash Course
HTML & CSS – Basic templating used in /templates and /static
Google Gemini API Key
Official Documentation: Google AI for Developers
Setup Guide: GeeksforGeeks
Popular Tutorial: How to Use Google Gemini API Key
Setup Steps:
Visit the Google AI Studio and sign in with your Google account.
Create a new project and enable the Gemini API.
Generate an API key and securely store it.
Uvicorn (ASGI Server)
Official Documentation: PyPI
Installation Steps:
Install Uvicorn using pip: pip install uvicorn
Jinja2 (HTML Templating Engine)
Official Documentation: Jinja2 Documentation
Installation Steps:
Install Jinja2 using pip: pip install jinja2

Project Workflow
MILESTONE 1: Model Selection and Architecture
Activity 1.1: Select AI Models
Gemini 1.5 Pro (via API):
Used for: Q&A, summarization, quiz generation, learning paths
Benefits: Advanced reasoning, structured outputs, and cloud inference
LaMini-Flan-T5-783M (local):
Used for: Concept explanation
Benefits: Instruction-tuned, lightweight, CPU-compatible
Folder Architecture:
EduGenie/
main.py                  # FastAPI app
explanation_module.py    # Concept explanation logic
qna.py                   # Question answering
quiz_module.py           # Quiz generation
summary_module.py        # Summarization
learning_path.py         # Learning recommendations
templates/index.html     # HTML frontend
static/style.css         # Styling
requirements.txt         # Python dependencies

FIG. Showing the Folder Architecture
MILESTONE 2: Core Functionalities Development
Activity 2.1. : Module Implementation
Explanation Module
EduGenie utilizes the LaMini-Flan-T5 model, a lightweight yet powerful generative AI, to deliver educational content in a simplified and highly readable manner. This model is specifically fine-tuned to provide concise, context-aware responses that break down complex topics into easily understandable language. By focusing on clarity and brevity, EduGenie ensures that learners with minimal background knowledge or technical experience can grasp essential concepts without feeling overwhelmed. This makes it particularly valuable for beginners, school students, or self-learners seeking straightforward explanations. The integration of LaMini-Flan-T5 empowers EduGenie to act as a reliable and accessible study companion for foundational learning across subjects.

Fig. Explanation module logic
QnA Module
EduGenie is powered by Gemini 1.5 Pro, enabling it to handle a wide range of general knowledge and academic question-answering tasks with precision. Its advanced understanding and contextual capabilities make it an effective tool for learners seeking accurate, AI-driven assistance across diverse educational topics and subjects.

Fig. Q/A Module
Quiz Module
EduGenie generates three multiple-choice questions (MCQs) from a given passage, each containing four carefully crafted options. It utilizes the Gemini model to comprehend the context and meaning of the passage, ensuring that the questions are relevant and the distractors are plausible. The final output is structured in JSON format for easy integration.

Fig. Quiz Module Logic
It sends a structured prompt to the model, expecting a valid JSON response with each question containing four options and a correct answer. To ensure proper parsing, it cleans any Markdown code blocks using the clean_json_blockfunction. The cleaned response is then parsed into a Python list. If an error occurs during generation or parsing, it returns a detailed error message for debugging.
Summary Module
This feature leverages Gemini’s generative capabilities to summarize long paragraphs into concise, easy-to-understand versions, making it ideal for quick revision. It ensures the core information is retained while eliminating redundancy, helping learners absorb key points efficiently without losing clarity or context.

Fig. Summary Module

Learning Path Module
The get_learning_recommendations function uses Google Gemini to generate a personalized, structured learning path for any given topic. By crafting a detailed prompt, it instructs the AI to suggest beginner to advanced concepts, organized by difficulty, and supported with useful resources such as videos, articles, or books. It ensures adaptability to the learner’s level. The function safely handles API responses and errors, providing either the generated text or a helpful error message if the response is invalid or incomplete.

Fig. Learning Path Module

Activity 2.2 : Backend API with FastAPI
Defined RESTful endpoints for each module:
/qa
/explain
/quiz
/summarize
/learn/recommendations
Connected each endpoint to a respective module logic

Fig. Endpoints of API

Fig. Endpoints of API
MILESTONE 3: Frontend Development
Activity 3.1: Build Web Interface
HTML Form (index.html):
Task dropdown (Explain, QnA, Quiz, Summary, Recommend Path)
Text area for user input
Submit button
CSS Styling (style.css):
Responsive design
Styled buttons, input areas, and result container

Fig. Showing Frontend Intergration
Activity 3.2: Live Integration
Form submission sends POST request to FastAPI backend
Result appears below input box in real-time

MILESTONE 4: Deployment
Activity 4.1: Run Locally
Run locally with uvicorn main:app --reload
Navigate to: http://127.0.0.1:8000

Fig. Showing the Application can be accessed
Activity 4.2: Functional Testing
Ask a question
Get an explanation
Generate a quiz
Summarize content
Get a personalized learning plan

Fig. EDUGENIE

Fig. EDUGENIE

Exploring EduGenie:

Asking questions:

Explanation of any topic:

Summarising long paragraphs:

Generating quizzes:

It generates three questions with 4 options each. It corrects the answer if chosen wrong.

Guiding with learning recommendations from beginners level to advanced level

It provides along with details of resources from where to learn and stepwise guidance through-out.

Conclusion:
EduGenie has been developed as a robust and accessible AI-powered educational assistant that seamlessly integrates cloud-based intelligence with an intuitive, low-footprint web interface. Designed to support self-learners, educational institutions, and content platforms, EduGenie democratizes learning by simplifying complex concepts, providing instant question-and-answer interactions, generating personalized quizzes, offering detailed summaries, and tailoring smart learning paths based on individual needs. Its lightweight infrastructure ensures that even users with minimal hardware resources can access high-quality, personalized education without barriers.
Throughout the development of EduGenie, the project achieved key milestones in AI integration, user experience design, and content adaptability. Leveraging advanced generative AI, it transforms static learning into a dynamic and interactive process. The platform's simplicity and clarity cater to learners of all levels—especially those who may find traditional educational content overwhelming or inaccessible. The modularity of the platform further allows for easy future upgrades, while its cloud-based backend ensures scalability and data-driven intelligence.
However, the development journey came with its own set of challenges. Ensuring accuracy in AI-generated responses, maintaining performance across devices, and balancing personalization with general usability were significant hurdles. Overcoming these required continuous testing, fine-tuning AI prompt structures, optimizing the UI for clarity, and addressing data privacy concerns. Yet, these challenges provided valuable learning outcomes—especially in areas like prompt engineering, cloud integration, user-centric design, and scalable architecture.
Looking ahead, EduGenie holds immense potential for enhancement and expansion. One promising direction involves the integration of voice-based interaction, enabling users to learn hands-free using spoken commands and queries—a particularly useful feature for accessibility and multitasking. Multilingual support is another key frontier, helping bridge language barriers and reaching a broader global audience. A mobile application is also envisioned to make learning available anytime, anywhere, with offline features for uninterrupted access.
Furthermore, future iterations of EduGenie could incorporate progress tracking dashboards, allowing users to visualize their learning journey through metrics and insights. The addition of gamified elements such as badges, learning streaks, and challenge-based assessments can boost engagement and motivation. Adaptive learning paths powered by data analytics can guide users more intelligently through content based on their strengths and weaknesses.
From a collaboration perspective, EduGenie can evolve to support group study sessions, teacher or parent dashboards, and integration with Learning Management Systems (LMS) such as Moodle or Google Classroom. Input recognition for images and PDF files can expand how students interact with content, enabling snapshot-based doubt solving and resource summarization. Real-time sync and smart notifications will also improve continuity and interactivity.
In conclusion, EduGenie is not just an AI tool—it’s a foundation for the future of personalized, inclusive, and intelligent education. By bridging gaps in access, comprehension, and adaptability, it redefines the learning experience for digital natives and underserved communities alike. As it continues to evolve, EduGenie is poised to become a comprehensive learning companion for the modern era—smart, scalable, and learner-first.

Submitted by:
Tella Divya Sree
Mentor: Siri
Date: 11/04/2025

Rendaiyum new file create Pannu enakku nalla theliva mela irukkura text project requirements ah nu paththu pannu