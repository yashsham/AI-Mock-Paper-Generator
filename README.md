# AI Mock Paper Generator 🎓

This project is an advanced, multi-agent AI system designed to help students prepare for major government exams. It provides an interactive web interface where users can select an exam, provide custom instructions, upload their own study materials, and receive a complete, downloadable mock paper in PDF format.

## Features ✨

* **🤖 Autonomous Agent Crew:** A team of three specialized AI agents (Syllabus Analyst, Question Generator, and Paper Formatter) collaborate to build the mock paper from scratch.
* **📚 RAG-Powered Customization:** Users can upload their own study notes (PDFs, text files). The Question Generator Agent uses this material as a reference to create relevant questions, turning it into a personalized study tool.
* **📝 PDF Output:** The final mock paper is converted into a professional, easy-to-share PDF document.
* **⚙️ Custom Prompts:** A dedicated text area allows students to give specific instructions, such as "focus on algebra" or "make the history questions more difficult."
* **🗂️ History Section:** All generated papers are saved, and a history is displayed in the sidebar for easy, one-click downloading of previous sessions.
* **🌐 Interactive UI:** Built with Streamlit for a clean, user-friendly experience.

## Tech Stack 🛠️

* **Agent Framework:** CrewAI
* **LLM & Embeddings:** Google Gemini Pro
* **UI Framework:** Streamlit
* **RAG & Vector Store:** LangChain, ChromaDB
* **PDF Conversion:** markdown-pdf
* **Core Language:** Python

## Setup & Installation ⚙️

**1. Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/AI-Mock-Paper-Generator.git](https://github.com/YOUR_USERNAME/AI-Mock-Paper-Generator.git)
cd AI-Mock-Paper-Generator
```

**2. Create and activate a virtual environment:**
```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up your API Key:**
Create a file named `.env` in the root of the project directory and add your Google API key:
```
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

## How to Run 🚀

Launch the Streamlit web application with the following command:

```bash
streamlit run app.py
```
Navigate to the local URL provided by Streamlit in your web browser.