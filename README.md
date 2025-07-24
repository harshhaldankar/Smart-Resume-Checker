# 🎯 Smart Resume Checker

An AI-powered resume analysis tool that helps job seekers optimize their resumes for better ATS (Applicant Tracking System) compatibility and overall improvement.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](your-deployed-app-url-here)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Features

- 📤 **Resume Upload**: Support for PDF resume uploads
- 🔍 **AI-Powered Analysis**: Comprehensive resume analysis using Google Gemini AI
- 💡 **Improvement Suggestions**: Detailed recommendations for resume enhancement
- ✅ **ATS Match Percentage**: Calculate compatibility with Applicant Tracking Systems
- 🎓 **Skill Development Tips**: Personalized skill improvement recommendations
- 🎨 **User-Friendly Interface**: Clean and intuitive Streamlit web interface

## 🎥 Demo

https://github.com/user-attachments/assets/4bd5841d-e99b-41ac-8ba6-2200180375bb


## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: Google Gemini API
- **PDF Processing**: PyPDF2 or similar
- **Python**: 3.8+
- **Deployment**: streamlit Cloud

## 📋 Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher installed
- Google Gemini API key
- Git installed on your system

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/harshhaldankar/Smart-Resume-Checker.git
cd Smart-Resume-Checker
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🔧 Configuration

### Google Gemini API Setup

1. Visit the [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key and add it to your `.env` file

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes |

## 🚀 Deployment

### Deploy on Streamlit Cloud

1. Fork this repository
2. Create a App on [Streamlit Cloud](streamlit.io)
3. Connect your GitHub repository
4. Add your `GOOGLE_API_KEY` in secrets
6. Deploy!

## 📁 Project Structure

```
Smart-Resume-Checker/
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies          
├── .env.example          # Environment variables template
├── README.md             # Project documentation
└── assets/               # Images and demo files
    └── demo.mp4          # Demo video (add this)
```

## 🎯 How It Works

1. **Upload Resume**: Users upload their resume in PDF format
2. **AI Analysis**: The system uses Google Gemini AI to analyze the resume
3. **ATS Scoring**: Calculates compatibility with ATS systems
4. **Recommendations**: Provides detailed improvement suggestions
5. **Skill Analysis**: Identifies skill gaps and development opportunities
6. **Results Display**: Shows comprehensive analysis with visual insights

## 📸 Screenshots

### Main Interface
![Main Interface]<img width="1915" height="852" alt="Screenshot 2025-04-18 025449" src="https://github.com/user-attachments/assets/d4772140-b68d-4d19-9681-7f78ab211750" />


### Analysis Results
![Analysis Results]<img width="1439" height="834" alt="Screenshot 2025-04-18 025749" src="https://github.com/user-attachments/assets/2f02acf6-d8ed-4cff-b496-b4aac6563d7d" />


### ATS Score
![ATS Score]<img width="1403" height="432" alt="Screenshot 2025-04-18 025737" src="https://github.com/user-attachments/assets/d7fde5dd-eae0-46d4-8a5b-97094c68a3a0" />

