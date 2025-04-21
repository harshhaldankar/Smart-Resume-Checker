import streamlit as st
from dotenv import load_dotenv
import base64
import os
import io
import pdf2image
import re
import pandas as pd
import plotly.express as px
from PIL import Image
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set Streamlit to use the dark theme
st.set_page_config(page_title="Smart Resume Dashboard", layout="wide", initial_sidebar_state="expanded")

# Set the default theme to dark mode (using Streamlit's built-in theme config)
st.markdown(
    """
    <style>
    .main {
        background-color: #121212;
        color: white;
    }
    .stButton > button {
        border-radius: 10px;
        padding: 10px 20px;
        background-color: #28a745; /* Green color */
        color: white;
        font-weight: bold;
        border: none;
        width: 100%; /* Ensures all buttons have the same length */
    }
    .stButton > button:hover {
        background-color: #218838; /* Darker green on hover */
    }
    .stTextArea textarea, .stTextInput input {
        background-color: #333;
        color: white;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 10px;
    }
    .stFileUploader .upload-btn-wrapper {
        border-radius: 8px;
        border: 1px dashed #ccc;
        background-color: #444;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper functions
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    images = pdf2image.convert_from_bytes(uploaded_file.read())
    first_page = images[0]
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return [{
        "mime_type": "image/jpeg",
        "data": base64.b64encode(img_byte_arr).decode()
    }]

# Prompts
prompts = {
    "analysis": """
    You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """,
    "match": """
    You are a skilled ATS scanner. Evaluate the resume against the job description. Return only the percentage match as an integer (e.g., 85).
    """,
    "improve": """
    As a professional resume consultant, analyze the provided resume and suggest specific improvements to better align with the job description. 
    Focus on formatting, content relevance, and keyword optimization. Provide actionable recommendations in bullet points.
    """,
    "skills": """
    As a career advisor, identify 3-5 key skills the candidate lacks based on the resume and job description. 
    For each skill gap, recommend 2-3 free online learning resources or video tutorials (include full URLs).
    """,
    "contact": """
    Extract the candidate's name, email, and phone number from this resume.
    Format:
    Name: <name>
    Email: <email>
    Phone: <phone>
    """
}

# Navigation
st.sidebar.title("🧭 Navigation")
mode = st.sidebar.radio("Choose Mode", ["Single Resume Analyzer", "Bulk Resume Ranker"])

if mode == "Single Resume Analyzer":
    st.title("📈 ATS Tracking System")
    st.markdown("Upload a single resume and compare it with your target job.")
    uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"])
    input_text = st.text_area("Job Description")

    col1, col2 = st.columns(2)
    with col1:
        analyze_btn = st.button("🔍 Resume Analysis")
        match_btn = st.button("✅ Percentage Match")
    with col2:
        improve_btn = st.button("💡 Improve Resume")
        skills_btn = st.button("🎓 Skill Recommendations")

    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)

        if analyze_btn:
            with st.spinner("Analyzing resume..."):
                result = get_gemini_response(input_text, pdf_content, prompts["analysis"])
                st.subheader("📝 Analysis Report")
                st.write(result)

        elif match_btn:
            with st.spinner("Calculating match percentage..."):
                result = get_gemini_response(input_text, pdf_content, prompts["match"])
                st.subheader("📊 Match Percentage")
                match_score = int(re.search(r"\d+", result).group())
                st.progress(match_score)
                st.write(f"{match_score}%")

        elif improve_btn:
            with st.spinner("Improving resume..."):
                result = get_gemini_response(input_text, pdf_content, prompts["improve"])
                st.subheader("📌 Recommendations")
                st.markdown(result, unsafe_allow_html=True)

        elif skills_btn:
            with st.spinner("Finding learning resources..."):
                result = get_gemini_response(input_text, pdf_content, prompts["skills"])
                st.subheader("🎯 Skill Development Resources")
                st.markdown(result, unsafe_allow_html=True)

elif mode == "Bulk Resume Ranker":
    st.title("📊 Bulk Resume Ranker")
    st.markdown("Upload multiple resumes and get ranked matches with contact details.")

    job_description = st.text_area("Job Description (for bulk analysis)")
    uploaded_files = st.file_uploader("Upload Resumes (PDFs)", type=["pdf"], accept_multiple_files=True)

    min_score = st.slider("Minimum Match %", 0, 100, 0)

    ranked_candidates = []

    if st.button("🚀 Analyze All Resumes"):
        if not job_description:
            st.warning("Please enter a job description first.")
        elif not uploaded_files:
            st.warning("Please upload at least one resume.")
        else:
            with st.spinner("Processing resumes..."):
                for file in uploaded_files:
                    try:
                        pdf_content = input_pdf_setup(file)
                        match_result = get_gemini_response(job_description, pdf_content, prompts["match"])
                        match = int(re.search(r"\d+", match_result).group())

                        contact_result = get_gemini_response("", pdf_content, prompts["contact"])
                        name = re.search(r"Name:\s*(.*)", contact_result)
                        email = re.search(r"Email:\s*(.*)", contact_result)
                        phone = re.search(r"Phone:\s*(.*)", contact_result)

                        candidate = {
                            "filename": file.name,
                            "match": match,
                            "name": name.group(1).strip() if name else "N/A",
                            "email": email.group(1).strip() if email else "N/A",
                            "phone": phone.group(1).strip() if phone else "N/A",
                        }
                        ranked_candidates.append(candidate)

                    except Exception as e:
                        st.error(f"Error processing {file.name}: {e}")

            ranked_candidates = sorted(ranked_candidates, key=lambda x: x['match'], reverse=True)
            st.success("✅ Bulk analysis complete")

            df = pd.DataFrame(ranked_candidates)
            filtered_df = df[df['match'] >= min_score]

            st.subheader("📋 Ranked Candidates")
            for idx, row in filtered_df.iterrows():
                with st.container():
                    st.markdown(f"### {row['name']}")
                    st.progress(row['match'])
                    st.markdown(f"**Match:** {row['match']}%")
                    st.markdown(f"📧 {row['email']}")
                    st.markdown(f"📱 {row['phone']}")
                    st.markdown("---")

            st.sidebar.title("📇 Contacts")
            for idx, row in filtered_df.iterrows():
                st.sidebar.markdown(f"**{row['name']}**")
                st.sidebar.markdown(f"📧 {row['email']}")
                st.sidebar.markdown(f"📱 {row['phone']}")
                st.sidebar.markdown(f"Match: {row['match']}%")
                st.sidebar.markdown("---")


            # Export results
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="ranked_candidates.csv",
                mime="text/csv"
            )
