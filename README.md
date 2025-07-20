# 🎯 Smart Resume Checker

An AI-powered resume analysis tool that helps job seekers optimize their resumes for better ATS (Applicant Tracking System) compatibility and overall improvement.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](your-deployed-app-url-here)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

- 📤 **Resume Upload**: Support for PDF resume uploads
- 🔍 **AI-Powered Analysis**: Comprehensive resume analysis using Google Gemini AI
- 💡 **Improvement Suggestions**: Detailed recommendations for resume enhancement
- ✅ **ATS Match Percentage**: Calculate compatibility with Applicant Tracking Systems
- 🎓 **Skill Development Tips**: Personalized skill improvement recommendations
- 🎨 **User-Friendly Interface**: Clean and intuitive Streamlit web interface

## 🎥 Demo

https://github.com/user-attachments/assets/your-demo-video-filename.mp4

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: Google Gemini API
- **PDF Processing**: PyPDF2 or similar
- **Python**: 3.8+
- **Deployment**: Render.com

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

### Deploy on Render.com

1. Fork this repository
2. Create a new Web Service on [Render.com](https://render.com)
3. Connect your GitHub repository
4. Use the provided `render.yaml` configuration
5. Add your `GOOGLE_API_KEY` in Render's Environment Variables
6. Deploy!

### Deploy on Other Platforms

The application can also be deployed on:
- Heroku
- Streamlit Cloud
- Google Cloud Platform
- AWS
- Azure

## 📁 Project Structure

```
Smart-Resume-Checker/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render.com deployment configuration
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

## 🎥 Adding Demo Video

To add a demonstration video to your README:

### Option 1: Upload to GitHub (Recommended)

1. Create a short demo video (2-3 minutes) showing:
   - Uploading a resume
   - Analysis results
   - Key features in action

2. Upload the video to your repository:
   ```bash
   mkdir assets
   # Add your demo.mp4 file to the assets folder
   git add assets/demo.mp4
   git commit -m "Add demo video"
   git push
   ```

3. Update the demo section in README:
   ```markdown
   ## 🎥 Demo
   
   https://github.com/harshhaldankar/Smart-Resume-Checker/assets/demo.mp4
   ```

### Option 2: Use GitHub Releases

1. Create a new release in your GitHub repository
2. Attach your demo video to the release
3. Use the download URL in your README

### Option 3: External Hosting

You can also host your demo video on:
- YouTube (then embed)
- Loom
- Vimeo
- Google Drive (with public access)

Example with YouTube:
```markdown
[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
```

## 📸 Screenshots

Add screenshots of your application here:

```markdown
### Main Interface
![Main Interface](assets/screenshots/main-interface.png)

### Analysis Results
![Analysis Results](assets/screenshots/analysis-results.png)

### ATS Score
![ATS Score](assets/screenshots/ats-score.png)
```
