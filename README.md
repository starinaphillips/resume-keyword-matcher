# Resume Keyword Matcher

A Python tool that compares a job description with a resume, identifies matching and missing keywords, and computes a match score as a percentage. Missing keywords are grouped into three categories: Technical Skills, Soft Skills, and Qualifications. The tool is built with both a Streamlit web interface and a command-line interface.

---

## Table of Contents

- Overview
- Why No Machine Learning
- Tools and Technologies Used
- How Each Tool is Used
- Why Both a Frontend and a CLI
- Project Structure
- How It Works
- How to Run
- Sample Input and Output
- Modification - Download Results as JSON

---

## Overview

When applying for jobs, resumes are often filtered by ATS (Applicant Tracking Systems) that scan for specific keywords from the job description. Many qualified candidates get rejected simply because their resume does not contain the right words, even if they have the right skills.

This tool solves that problem. You paste a job description and your resume, and the tool instantly tells you what percentage of the job description keywords are present in your resume, which keywords you are already covering grouped by category, which keywords are missing from your resume grouped by category, and actionable tips on where and how to add the missing keywords.

The tool requires no internet connection and produces results instantly.

## Tools and Technologies Used

Python 3.8+ is the core programming language. Streamlit is an external library used for the web interface frontend. re is a Python built-in module used for text cleaning and normalization. collections is a Python built-in module used for organizing keyword data by category. argparse is a Python built-in module used for handling command-line arguments for the CLI. VS Code was used as the development environment.


## How Each Tool is Used

**Streamlit**
Streamlit creates the entire web interface you see in the browser. Every visual element such as the two text input boxes, the Analyze Match button, the score card, the progress bars, the matched and missing keyword tags, and the improvement tips is built using Streamlit. Without it there would be no website, just plain Python running in the terminal.

**re (Regular Expressions)**
When you paste text it contains commas, full stops, brackets, and other punctuation. For example the words Python, and Python should be treated as the same keyword. The re module cleans all punctuation from both inputs before matching so that no keywords are missed due to attached symbols.

**collections**
The defaultdict from the collections module is used to organize keywords into their categories as they are being processed. It ensures that even if a category returns no results, the program handles it cleanly without crashing.

**argparse**
This powers the command-line interface. When you run the tool from the terminal with file paths as arguments, argparse reads and processes those arguments and passes the correct files to the matching logic.


## Why Both a Frontend and a CLI

The project was built with two interfaces to serve different types of users and situations.

The Streamlit web interface is the recommended option for most users. It is visual, interactive, and easy to use. You can paste text, see color coded results, and understand the output at a glance without any technical knowledge.

The command-line interface is for users who prefer working in the terminal, want to automate the tool as part of a script, or are working in an environment without a browser. It accepts text files as arguments and prints a clean formatted report directly in the terminal.

Having both interfaces demonstrates that the underlying matching logic in matcher.py is completely independent of how the results are displayed. The same core function powers both interfaces.


## Project Structure


resume-keyword-matcher/
|
|-- app.py               # Streamlit web application and UI
|-- matcher.py           # Core logic: keyword extraction, matching, scoring
|-- cli.py               # Command-line interface
|-- requirements.txt     # Project dependencies
|-- sample_jd.txt        # Sample job description for testing
|-- sample_resume.txt    # Sample resume for testing
|-- README.md            # Project documentation
```

How It Works

**Step 1 - Text Normalization**
Both inputs are converted to lowercase and cleaned using regular expressions to remove punctuation and special characters so that variations of the same word are treated consistently.

**Step 2 - N-gram Generation**
The cleaned text is broken into combinations of 1 to 4 words. This is what allows the tool to detect multi-word keywords such as machine learning, attention to detail, ci/cd, and data structures — not just single words.

**Step 3 - Keyword Dictionary Lookup**
Each word combination is checked against a curated dictionary of 180+ keywords organized into three categories. Technical Skills covers programming languages, frameworks, databases, cloud platforms, DevOps tools, machine learning libraries, and testing tools. Soft Skills covers professional traits such as communication, leadership, teamwork, problem-solving, and time management. Qualifications covers degrees, certifications, and experience levels such as bachelor, master, m.tech, computer science, and years of experience.

**Step 4 - Score Calculation**

Match Score = (Keywords found in resume / Keywords found in job description) x 100
```
The score is based only on keywords that appear in the job description. This means the result reflects how well your resume is tailored to that specific role.

---

## How to Run

Install the dependency:

```bash
pip install -r requirements.txt
```

If pip is not recognized on Windows use:

```bash
python -m pip install -r requirements.txt
```

**Option 1 - Web Interface (Recommended)**

```bash
streamlit run app.py
```

If streamlit is not recognized use:

```bash
python -m streamlit run app.py
```

The app opens automatically in your browser at http://localhost:8501

Steps: Paste the job description into the left text box, paste your resume into the right text box, click Analyze Match, and view your match score, matched keywords, missing keywords, and improvement tips.

**Option 2 - Command-Line Interface**

Interactive mode:
```bash
python cli.py
```

File mode:
```bash
python cli.py --jd sample_jd.txt --resume sample_resume.txt
```



## Sample Input and Output

**Job Description**
```
Requirements:
- Bachelor degree in Computer Science or Software Engineering
- Strong proficiency in Python and Django or Flask
- Experience with PostgreSQL and Redis
- Familiarity with Docker and AWS
- Knowledge of REST APIs and Git
- Experience with CI/CD pipelines
- Strong communication and teamwork skills
- Attention to detail and problem-solving mindset
```

**Resume**
```
Skills     : Python, Django, PostgreSQL, AWS, Docker, Git, REST APIs
Education  : B.Tech in Computer Science
Soft Skills: Communication, teamwork, problem-solving, attention to detail
```

**Output**
```
Match Score : 78.6%
Verdict     : Good Match

JD Keywords : 14
Matched     : 11
Missing     : 3

Technical Skills   [############----]  75%   (9/12)
Soft Skills        [####################] 100%  (3/3)
Qualifications     [####################] 100%  (2/2)

Missing Keywords:
  Technical Skills : redis, flask, ci/cd
  Soft Skills      : none missing
  Qualifications   : none missing

Tips:
  - Consider adding redis, flask, ci/cd to your
    skills section or project descriptions.
```



## Modification - Download Results as JSON

A download button was added to the Streamlit web interface as part of the modification round. After clicking Analyze Match and viewing the results, a Download Results as JSON button appears at the bottom of the page. Clicking it downloads a file called match_results.json to your computer.

The exported JSON file includes the match score, matched keywords per category, missing keywords per category, per-category job description keyword counts, and the total matched and total job description keyword counts.

```json
{
  "match_score": 78.6,
  "total_jd_keywords": 14,
  "total_matched": 11,
  "matched_keywords": {
    "Technical Skills": ["python", "django", "docker", "aws", "git", "rest"],
    "Soft Skills": ["communication", "teamwork", "attention to detail"],
    "Qualifications": ["bachelor", "computer science"]
  },
  "missing_keywords": {
    "Technical Skills": ["redis", "flask", "ci/cd"],
    "Soft Skills": [],
    "Qualifications": []
  },
  "jd_keyword_counts": {
    "Technical Skills": 9,
    "Soft Skills": 3,
    "Qualifications": 2
  }
}
```

The button uses Streamlit's built-in st.download_button with no third party libraries. It only appears after results have been generated and does not affect the existing results layout in any way.

---
