import streamlit as st
st.set_page_config(page_title="Smart Resume Checker")

from dotenv import load_dotenv
import base64
import os
import io
import pdf2image
from PIL import Image 
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        return [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
    else:
        raise FileNotFoundError("No file uploaded")

st.markdown("""
    <style>
    textarea {
        color: white !important;
        background-color: #2c2f33 !important;
    }
    .stTextArea label {
        color: white !important;
    }
    .stButton button {
        width: 100%;
        border-radius: 8px;
        padding: 10px;
        background-color: #4CAF50;
        color: white;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

st.header("📈 ATS Tracking System")
uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"], help="We only process the first page of your resume")
input_text = st.text_area("Job Description:", key="input")

if uploaded_file is not None:
    st.success("✅ PDF Uploaded Successfully")

st.subheader("🚀 Boost Your Resume Performance")
col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("🔍 Resume Analysis")
    submit3 = st.button("✅ Percentage Match")
with col2:
    submit2 = st.button("💡 Improve Resume")
    submit4 = st.button("🎓 Skill Recommendations")

with st.sidebar:
    st.title("💡 User Guide")
    st.markdown("""
    1. Enter job description in main text area  
    2. Upload PDF resume  
    3. Choose analysis type:
       - 🔍 Full resume analysis  
       - 💡 Improvement suggestions  
       - ✅ ATS match percentage  
       - 🎓 Skill development resources  
    """)
    st.success("Note: Analysis may take 20-30 seconds")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide the percentage match, followed by missing keywords and final thoughts.
"""

input_prompt2 = """
As a professional resume consultant, analyze the provided resume and suggest specific improvements to better align with the job description. 
Focus on formatting, content relevance, and keyword optimization. Provide actionable recommendations in bullet points.
"""

input_prompt4 = """
As a career advisor, identify 3-5 key skills the candidate lacks based on the resume and job description. 
For each skill gap, recommend 2-3 free online learning resources or video tutorials (include full URLs). 
Present in this format:
1. [Skill Name]: 
   - [Resource Name] ([URL])
   - [Resource Name] ([URL])
"""

if submit1:
    if uploaded_file:
        with st.spinner("Analyzing resume..."):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("📝 Analysis Report")
            st.write(response)
    else:
        st.warning("⚠️ Please upload the resume first.")

elif submit3:
    if uploaded_file:
        with st.spinner("Calculating match percentage..."):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("📊 Match Percentage")
            st.write(response)
    else:
        st.warning("⚠️ Please upload the resume first.")

elif submit2:
    if uploaded_file:
        with st.spinner("Analyzing for improvements..."):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt2)
            st.subheader("📌 Improvement Suggestions")
            st.markdown(response, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload the resume first.")

elif submit4:
    if uploaded_file:
        with st.spinner("Finding skill development resources..."):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt4)
            st.subheader("🎯 Skill Development Resources")
            st.markdown(response, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload the resume first.")