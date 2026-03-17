Resume Keyword Matcher
A lightweight Python tool that compares a job description against a resume, extracts matching and missing keywords, computes a match score as a percentage, and groups results by category. Built with a clean Streamlit web interface and an optional command-line interface.

Table of Contents

Overview
Features
Project Structure
Requirements
Installation
How to Run
How It Works
Sample Input and Output


Overview
When applying for jobs, resumes are often screened by ATS (Applicant Tracking Systems) that look for specific keywords from the job description. This tool helps candidates identify which keywords are present in their resume and which are missing, so they can improve their chances before applying.
The tool requires no internet connection, no external NLP libraries, and no AI models. It uses a curated keyword dictionary and Python built-in string processing to perform fast, transparent, and deterministic keyword matching.

Features

Accepts a job description and a resume as plain text input
Extracts single-word and multi-word keywords such as machine learning, ci/cd, and attention to detail
Categorizes keywords into three groups: Technical Skills, Soft Skills, and Qualifications
Computes a match score as a percentage based on how many job description keywords appear in the resume
Displays matched keywords and missing keywords separately
Shows per-category progress breakdown
Provides actionable suggestions to improve the resume
Clean and responsive Streamlit web interface
Optional command-line interface for terminal users


Project Structure
resume-keyword-matcher/
│
├── app.py                  # Streamlit web application
├── matcher.py              # Core keyword extraction and matching logic
├── cli.py                  # Command-line interface
├── requirements.txt        # Python dependencies
├── sample_jd.txt           # Sample job description for testing
├── sample_resume.txt       # Sample resume for testing
├── .gitignore              # Files to exclude from version control

Requirements

Python 3.8 or higher
Streamlit 1.32.0 or higher

No other external libraries are required. All other modules used (re, collections, argparse) are part of the Python standard library.

How to Run
Option 1 — Streamlit Web Interface (Recommended)
bashstreamlit run app.py
Or if streamlit is not recognized:
bashpython -m streamlit run app.py
The app will open automatically in your browser at http://localhost:8501.
Steps to use the web app:

Paste the job description into the left text box
Paste your resume into the right text box
Click Analyze Match
View your match score, matched keywords, missing keywords, and improvement tips


Option 2 — Command-Line Interface
Interactive mode (paste text directly in the terminal):
bashpython cli.py
File mode (pass text files as arguments):
bashpython cli.py --jd sample_jd.txt --resume sample_resume.txt

How It Works
The matching process follows these steps:
1. Text Normalization
Both the job description and resume are lowercased and lightly cleaned to remove punctuation noise.
2. N-gram Generation
The text is broken into 1 to 4 word n-grams so that multi-word phrases like machine learning, attention to detail, and ci/cd are correctly identified.
3. Keyword Dictionary Lookup
Each n-gram is checked against three curated keyword sets:

Technical Skills — 100+ keywords covering languages, frameworks, databases, cloud platforms, ML tools, DevOps, and more
Soft Skills — 30+ keywords covering communication, leadership, teamwork, and other professional traits
Qualifications — 20+ keywords covering degrees, certifications, and experience levels

4. Score Calculation
Match Score = (Keywords found in resume / Keywords found in job description) x 100
The score only counts keywords that appear in the job description, so the result reflects how well the resume is tailored to that specific role.

Sample Input and Output
Job Description (excerpt)
Requirements:
- Bachelor degree in Computer Science or Software Engineering
- Strong proficiency in Python and Django or Flask
- Experience with PostgreSQL and Redis
- Familiarity with Docker and AWS
- Knowledge of REST API design
- Strong communication and teamwork skills
Resume (excerpt)
Skills     : Python, Django, PostgreSQL, AWS, Docker, Git, REST APIs
Education  : B.Tech in Computer Science
Soft Skills: Communication, teamwork, problem-solving
Output
Match Score  : 78.6%
JD Keywords  : 14
Matched      : 11
Missing      : 3

Technical Skills   [########--------]  60%   (6/10)
Soft Skills        [################]  100%  (2/2)
Qualifications     [####################] 100% (3/3)

Missing Keywords:
  Technical Skills : redis, flask
  Soft Skills      : (none missing)
  Qualifications   : (none missing)
