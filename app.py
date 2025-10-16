# app.py

import streamlit as st
import json
import os
from datetime import datetime
import tempfile

# CrewAI and LangChain imports
from crewai import Crew, Process
from crewai.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# RAG specific imports
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# PDF Conversion import - ADD Section HERE
from markdown_pdf import MarkdownPdf, Section

# Agent and tool imports
from agents.syllabus_analyst_agent import SyllabusAnalystAgents
from agents.question_generator_agent import QuestionGeneratorAgents
from agents.paper_formatter_agent import PaperFormatterAgents
from tools import get_exam_pattern_tool

# Load API Key at the start of the app
load_dotenv()

# --- Page Configuration ---
st.set_page_config(page_title="AI Mock Paper Generator", layout="wide")
st.title("🎓 AI Mock Paper Generator")

# --- Helper Functions ---
def get_exam_names():
    """Loads the list of exam names from the JSON knowledge base."""
    try:
        with open('mcp_server/exam_patterns.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
        return list(data.keys())
    except FileNotFoundError:
        return []

# --- Sidebar UI ---
with st.sidebar:
    st.header("Upload Reference Materials (Optional)")
    uploaded_files = st.file_uploader(
        "Upload study notes (PDF, TXT)",
        accept_multiple_files=True,
        type=['pdf', 'txt']
    )
    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) ready for RAG!")

    st.header("📄 Paper History")
    paper_dir = "generated_papers"
    if not os.path.exists(paper_dir):
        os.makedirs(paper_dir)
    
    past_papers = sorted([f for f in os.listdir(paper_dir) if f.endswith('.pdf')], reverse=True)
    if not past_papers:
        st.write("No papers generated yet.")
    else:
        for paper_file in past_papers:
            with open(os.path.join(paper_dir, paper_file), "rb") as f:
                st.download_button(
                    label=paper_file,
                    data=f.read(),
                    file_name=paper_file,
                    mime="application/pdf",
                    key=paper_file
                )

# --- Main Interface ---
st.header("Step 1: Select Your Exam")
exam_names = get_exam_names()

if not exam_names:
    st.error("Could not load exam patterns. Make sure 'mcp_server/exam_patterns.json' exists.")
else:
    selected_exam = st.selectbox("Choose an exam:", options=exam_names)

    custom_prompt = st.text_area(
        "Step 2: Add Custom Instructions (Optional)",
        placeholder="e.g., 'Focus on algebra questions.' or 'Generate questions based on my uploaded notes about Indian history.'"
    )

    if st.button("Generate Mock Paper"):
        if selected_exam:
            with st.spinner("The AI crew is assembling your mock paper... 🤖"):
                
                from crewai import LLM

                llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)

                rag_tool = None
                if uploaded_files:
                    all_chunks = []
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                            tmp.write(uploaded_file.getvalue())
                            loader = PyPDFLoader(tmp.name) if tmp.name.endswith(".pdf") else TextLoader(tmp.name)
                            docs = loader.load_and_split(text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100))
                            all_chunks.extend(docs)
                    
                    if all_chunks:
                        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                        vectorstore = Chroma.from_documents(documents=all_chunks, embedding=embeddings)
                        retriever = vectorstore.as_retriever()
                        
                        @tool("Reference Material Tool")
                        def rag_tool(query: str) -> str:
                            """Searches the user's uploaded documents for relevant information to answer a question."""
                            docs = retriever.invoke(query)
                            return "\n".join([doc.page_content for doc in docs])
                        st.info("Created a searchable knowledge base from your files.")

                analyst_agents = SyllabusAnalystAgents()
                generator_agents = QuestionGeneratorAgents()
                formatter_agents = PaperFormatterAgents()

                analyst = analyst_agents.make_analyst_agent(llm)
                generator_tools = [rag_tool] if rag_tool else []
                generator = generator_agents.make_generator_agent(llm, tools=generator_tools)
                formatter = formatter_agents.make_formatter_agent(llm)

                analysis_task = analyst_agents.make_analysis_task(analyst, selected_exam)
                
                question_task_description = (f'Based on the provided exam pattern, generate the specified number of questions for EACH subject. ')
                if custom_prompt:
                    question_task_description += f'Also, follow these custom instructions: "{custom_prompt}" '
                if rag_tool:
                    question_task_description += "If the user's instructions mention their notes, use the 'Reference Material Tool' to search their documents for relevant topics before generating questions."

                question_task = generator_agents.make_question_task(generator, context=[analysis_task])
                question_task.description = question_task_description
                
                formatting_task = formatter_agents.make_formatting_task(formatter, context=[question_task])

                crew = Crew(
                    agents=[analyst, generator, formatter],
                    tasks=[analysis_task, question_task, formatting_task],
                    process=Process.sequential
                )
                result = crew.kickoff()

                st.success("Mock paper generated! Converting to PDF...")
                
                # --- PDF Conversion and Saving ---
                markdown_text = result.raw
                pdf = MarkdownPdf()
                # FIX IS HERE: Wrap the text in a Section object
                pdf.add_section(Section(markdown_text))
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                pdf_filename = f"{selected_exam.replace(' ', '_')}_{timestamp}.pdf"
                pdf_save_path = os.path.join(paper_dir, pdf_filename)
                pdf.save(pdf_save_path)

                # --- Display Results ---
                st.header("Your Mock Paper:")
                st.markdown(markdown_text)

                with open(pdf_save_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF Paper",
                        data=f.read(),
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
                
                st.header("Rate this Paper")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 Thumbs Up"):
                        st.success("Thanks for your feedback!")
                with col2:
                    if st.button("👎 Thumbs Down"):
                        st.warning("We'll try to do better next time. Thanks for the feedback!")