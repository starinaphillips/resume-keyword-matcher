Resume Keyword Matcher
A Python tool that compares a job description with a resume, identifies matching and missing keywords, and computes a match score as a percentage. Missing keywords are grouped into three categories: Technical Skills, Soft Skills, and Qualifications.

Table of Contents

1.Overview
2.Tools and Technologies Used
3.Project Structure
4.How It Works
5.How to Run
6.Sample Input and Output


Overview
When applying for jobs, resumes are often filtered by ATS (Applicant Tracking Systems) that scan for specific keywords from the job description. Many qualified candidates get rejected simply because their resume does not contain the right words.
This tool helps you identify exactly which keywords are missing from your resume so you can improve it before applying. You paste a job description and your resume, and the tool instantly gives you a match score along with a detailed breakdown of matched and missing keywords by category.

Tools and Technologies Used
1.Python 3.8+: Core programming language
2.Streamlit: Web interface for the frontend
3.re :Text cleaning and normalization 
4.collections: Data handling in keyword processing
5.argparse: Command-line argument parsing
6.VS Code :Development environment

Project Structure
resume-keyword-matcher/
|
|-- app.py               # Streamlit web application
|-- matcher.py           # Keyword extraction and matching logic
|-- cli.py               # Command-line interface
|-- requirements.txt     # Project dependencies
|-- sample_jd.txt        # Sample job description for testing
|-- sample_resume.txt    # Sample resume for testing


How It Works
Step 1 - Text Normalization
Both inputs are converted to lowercase and cleaned using regular expressions to remove punctuation noise.
Step 2 - N-gram Generation
The text is broken into 1 to 4 word combinations so that multi-word keywords like machine learning, attention to detail, and ci/cd are detected correctly.
Step 3 - Keyword Dictionary Lookup
Each word or phrase is checked against a curated dictionary of 180+ keywords across three categories:

Technical Skills: Languages, frameworks, databases, cloud tools, DevOps, ML libraries
Soft Skills: Communication, leadership, teamwork, problem-solving, and more
Qualifications: Degrees, certifications, and experience levels

Step 4 - Score Calculation
Match Score = (Keywords found in resume / Keywords in job description) x 100

How to Run
Install the dependency
bash :pip install -r requirements.txt
Run the web app
bash: streamlit run app.py
Open your browser at http://localhost:8501
Steps:

Paste the job description into the left box
Paste your resume into the right box
Click Analyze Match
View your score, matched keywords, missing keywords, and tips


Sample Input and Output
Job Description (excerpt)
Requirements:
- Bachelor degree in Computer Science
- Proficiency in Python and Django
- Experience with PostgreSQL, Docker, and AWS
- Knowledge of REST APIs and Git
- Strong communication and teamwork skills
Resume (excerpt)
Skills     : Python, Django, PostgreSQL, AWS, Docker, Git, REST APIs
Education  : B.Tech in Computer Science
Soft Skills: Communication, teamwork, problem-solving
Output
Match Score : 78.6%
Verdict     : Good Match

JD Keywords : 14
Matched     : 11
Missing     : 3

Technical Skills   [############----]  75%   (9/12)
Soft Skills        [####################] 100%  (2/2)
Qualifications     [####################] 100%  (2/2)

Missing Keywords:
  Technical Skills : ci/cd, redis, flask
  Soft Skills      : none missing
  Qualifications   : none missing
