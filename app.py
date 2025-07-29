import numpy as np
import time
import google.generativeai as genai
import random
import pandas as pd
import io
import re
import streamlit as st
from dotenv import load_dotenv
import base64
import os
import pdf2image
import re
import datetime

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="Smart Resume Dashboard", layout="wide", initial_sidebar_state="expanded")

# Dark theme styling
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
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #218838;
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

# Helper function to handle retries
def get_gemini_response_with_retry(input_text, pdf_content, prompt, max_retries=3, backoff_factor=2):
    retries = 0
    while retries < max_retries:
        try:
            # Make the API request
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([input_text, pdf_content[0], prompt])
            return response.text
        except Exception as e:
            if "429" in str(e):  # Check if it's a rate limit error
                retries += 1
                wait_time = backoff_factor ** retries + random.uniform(0, 1)  # Exponential backoff with some randomness
                st.warning(f"Rate limit exceeded, retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                st.error(f"An error occurred: {e}")
                break
    return None

# Helper functions
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
st.sidebar.title("Navigation")
mode = st.sidebar.radio("Choose Mode", ["Single Resume Analyzer", "Bulk Resume Ranker"])

if mode == "Single Resume Analyzer":
    st.title("ATS Tracking System")
    st.markdown("Upload a single resume and compare it with your target job.")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    input_text = st.text_area("Job Description")

    col1, col2 = st.columns(2)
    with col1:
        analyze_btn = st.button("Resume Analysis")
        match_btn = st.button("Percentage Match")
    with col2:
        improve_btn = st.button("Improve Resume")
        skills_btn = st.button("Skill Recommendations")

    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)

        if analyze_btn:
            with st.spinner("Analyzing resume..."):
                result = get_gemini_response_with_retry(input_text, pdf_content, prompts["analysis"])
                st.subheader("Analysis Report")
                st.write(result)

        elif match_btn:
            with st.spinner("Calculating match percentage..."):
                result = get_gemini_response_with_retry(input_text, pdf_content, prompts["match"])
                st.subheader("Match Percentage")
                match_score = int(re.search(r"\d+", result).group())
                st.progress(match_score)
                st.write(f"{match_score}%")

        elif improve_btn:
            with st.spinner("Improving resume..."):
                result = get_gemini_response_with_retry(input_text, pdf_content, prompts["improve"])
                st.subheader("Recommendations")
                st.markdown(result, unsafe_allow_html=True)

        elif skills_btn:
            with st.spinner("Finding learning resources..."):
                result = get_gemini_response_with_retry(input_text, pdf_content, prompts["skills"])
                st.subheader("Skill Development Resources")
                st.markdown(result, unsafe_allow_html=True)

elif mode == "Bulk Resume Ranker":
    st.title("Bulk Resume Ranker")
    st.markdown("Upload multiple resumes and get ranked matches with contact details.")

    MAX_RESUMES = 15
    st.markdown("⚠**Note:** You can upload up to 15 resumes at a time.")

    job_description = st.text_area("Job Description (for bulk analysis)")
    uploaded_files = st.file_uploader("Upload Resumes (PDFs)", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        st.markdown(f"**Total Resumes Uploaded:** {len(uploaded_files)}")
        if len(uploaded_files) > MAX_RESUMES:
            st.error(f"Limit exceeded! Please upload no more than {MAX_RESUMES} resumes.")
            st.stop()

        eta_placeholder = st.empty()

    min_score = st.slider("Minimum Match %", 0, 100, 0)

    # Function to batch process resumes
    def process_resumes_in_batches(uploaded_files, job_description, prompts, batch_size=5):
        ranked_candidates = []
        total_files = len(uploaded_files)
        num_batches = (total_files // batch_size) + (1 if total_files % batch_size > 0 else 0)

        # Process each batch sequentially
        for batch_num in range(num_batches):
            batch_files = uploaded_files[batch_num * batch_size: (batch_num + 1) * batch_size]

            for file in batch_files:
                try:
                    # Read PDF and get the content
                    pdf_content = input_pdf_setup(file)

                    # Get match percentage
                    match_result = get_gemini_response_with_retry(job_description, pdf_content, prompts["match"])
                    if match_result is None:
                        continue
                    match = int(re.search(r"\d+", match_result).group())

                    # Get contact details
                    contact_result = get_gemini_response_with_retry("", pdf_content, prompts["contact"])
                    if contact_result is None:
                        continue

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
                    continue

            # Simulate some delay between batches to avoid hitting rate limits
            time.sleep(10)  # Add a 5-second delay between batches (you can adjust this time)
            ranked_candidates.sort(key=lambda x: x['match'], reverse=True)

    
        return ranked_candidates

    if st.button("Analyze All Resumes"):
        if not job_description:
            st.warning("Please enter a job description first.")
        elif not uploaded_files:
            st.warning("Please upload at least one resume.")
        else:
            with st.spinner("Processing resumes..."):
                start_time = time.time()

                # Process resumes in batches
                ranked_candidates = process_resumes_in_batches(uploaded_files, job_description, prompts)

                st.success("Bulk analysis complete")

                # Create a DataFrame from the ranked candidates
                df = pd.DataFrame(ranked_candidates)
                filtered_df = df[df['match'] >= min_score]

                st.subheader("Ranked Candidates")
                for idx, row in filtered_df.iterrows():
                    with st.container():
                        st.markdown(f"### {row['name']}")
                        st.progress(row['match'])
                        st.markdown(f"**Match:** {row['match']}%")
                        st.markdown(f"{row['email']}")
                        st.markdown(f"{row['phone']}")
                        st.markdown("---")

                st.sidebar.title("Contacts")
                for idx, row in filtered_df.iterrows():
                    st.sidebar.markdown(f"**{row['name']}**")
                    st.sidebar.markdown(f"{row['email']}")
                    st.sidebar.markdown(f"{row['phone']}")
                    st.sidebar.markdown(f"Match: {row['match']}%")
                    st.sidebar.markdown("---")

                # Provide a download option for the results
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="ranked_candidates.csv",
                    mime="text/csv"
                )
