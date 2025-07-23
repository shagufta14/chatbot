import streamlit as st
import pymupdf
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import PyPDF2

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
st.markdown("---")
st.subheader("📤 Ask anything ")


with open('money2.pdf', 'rb') as file:
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

if st.button("Generate Answer"):
        if not user_query.strip():
            st.warning("Please enter a valid question.")
        else:
            answer = generate_answers(st.session_state['pdf_content'], user_query)
            st.subheader("🧠 Answer:")
            st.text(answer)
            

# Optional: feedback
st.markdown("### 🙋 Was this answer helpful?")
st.radio("Select an option:", ["👍 Yes", "👎 No"], key="feedback_radio")
st.markdown("### 💡 You can try asking:")
st.markdown("""
- *What are best skills to learn?*  
- *What is scope of this?*  
- *how to make money?*
""")

st.markdown("✅ **Tip:** Start with one skill, master it, and build your income step by step.")
