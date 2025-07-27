import streamlit as st
import pymupdf
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import PyPDF2
import pandas as pd
from datetime import datetime


# Load environment variables and API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash-lite")

# Clean text
def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip().lower())

# Extract text using pymupdf
def extract_text_from_pdf(pdf_file):
    text = ""
    doc = pymupdf.open(stream=pdf_file.read(), filetype="pdf")  
    for page in doc:
        text += page.get_text("text")
    return clean_text(text)

# Generate answer
def generate_answers(content, query):
    prompt = f"""
    📄 Based on the following PDF content:
    {content}

    ❓ Question:
    {query}

    ✍️ Please provide a concise and relevant answer.
    """
    try:
        response = model.generate_content(prompt)
        return response.text if response else "No answer generated."
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="📘 PDF Answer Bot")
st.header("📄 HOW TO MAKE MONEY AND BEST SKILLS TO LEARN")
st.write(":My Shagufta Ambreen.I am a dedicated government school teacher with a strong passion for education and continuous learning. Alongside my teaching profession, I am actively exploring the world of Artificial Intelligence to stay aligned with modern advancements in technology. I believe in empowering students not only through academic knowledge but also by preparing them for the future with skills that matter. My journey into AI reflects my commitment to lifelong learning and my desire to bring innovation into the classroom. Through this dual role as an educator and AI learner, I aim to bridge the gap between traditional teaching and emerging technologies.")
st.markdown("---")
st.subheader(" Ask anything ")

with open('skills.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()

# Now store it safely
st.session_state['pdf_content'] = clean_text(full_text)
    
    # Get the number of pages
    #num_pages = len(reader.pages)
    
    # Read text from the first page
page = reader.pages[0]
text = page.extract_text()
 
if 'pdf_content' not in st.session_state or not st.session_state['pdf_content']:
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    st.session_state['pdf_content'] = clean_text(full_text)



    if 'pdf_content' not in st.session_state:
     st.session_state['pdf_content'] = ""
   

user_query = st.text_input("❓ Enter your question:")

#
if st.button("Generate Answer") and st.session_state['pdf_content']:
    content = st.session_state['pdf_content']
    answer = generate_answers(content, user_query)
    st.session_state['generated_answer'] = answer
    st.session_state['user_query'] = user_query
    st.subheader("Generated Answer:")
    st.text(answer)   
     
if 'generated_answer' in st.session_state:
    st.markdown("---")
    st.subheader("📋 Feedback")
    feedback = st.text_input("💭 Was this helpful? Any comments or suggestions?")
    if st.button("Submit Feedback"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        feedback_data = {
            "Timestamp": [timestamp],
            "Question": [st.session_state['user_query']],
            "Answer": [st.session_state['generated_answer']],
            "Feedback": [feedback]
        }

        df = pd.DataFrame(feedback_data)
        file_path = "feedback.xlsx"
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_excel(file_path, index=False)
        st.success("✅ Thank you for your feedback!")
   
            
            
            
            
