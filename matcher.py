"""
matcher.py - Core keyword extraction and matching logic
"""

import re
from collections import defaultdict

# ── Keyword Dictionaries ─────────────────────────────────────────────────────

TECHNICAL_SKILLS = {
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c", "go", "rust",
    "kotlin", "swift", "ruby", "php", "scala", "r", "matlab", "bash", "shell",
    "perl", "haskell", "lua", "dart", "elixir",
    # Web / Frontend
    "html", "css", "react", "angular", "vue", "nextjs", "nuxtjs", "svelte",
    "bootstrap", "tailwind", "sass", "less", "webpack", "vite", "jquery",
    "redux", "graphql", "rest", "restful", "api",
    # Backend / Frameworks
    "django", "flask", "fastapi", "spring", "nodejs", "express", "rails",
    "laravel", "asp.net", "dotnet", ".net",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle",
    "cassandra", "elasticsearch", "dynamodb", "firebase", "nosql",
    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "github actions", "ci/cd", "devops", "linux", "unix",
    "nginx", "apache", "serverless",
    # ML / Data
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow",
    "pytorch", "keras", "scikit-learn", "pandas", "numpy", "matplotlib",
    "seaborn", "opencv", "huggingface", "transformers", "llm", "langchain",
    "data science", "data analysis", "data engineering", "etl",
    "tableau", "power bi", "spark", "hadoop", "airflow", "dbt",
    # Tools / Version Control
    "git", "github", "gitlab", "bitbucket", "jira", "confluence",
    "postman", "swagger", "figma", "linux",
    # Testing
    "unit testing", "integration testing", "pytest", "jest", "selenium",
    "cypress", "tdd", "bdd",
    # Architectures / Concepts
    "microservices", "distributed systems", "cloud computing", "agile",
    "scrum", "design patterns", "oop", "functional programming", "system design",
    "data structures", "algorithms",
}

SOFT_SKILLS = {
    "communication", "teamwork", "leadership", "problem solving", "problem-solving",
    "critical thinking", "time management", "adaptability", "creativity",
    "collaboration", "attention to detail", "analytical", "organized",
    "self-motivated", "motivated", "proactive", "initiative", "interpersonal",
    "presentation", "negotiation", "conflict resolution", "mentoring", "coaching",
    "decision making", "decision-making", "multitasking", "work ethic",
    "fast learner", "quick learner", "detail-oriented", "results-driven",
    "team player", "cross-functional", "stakeholder management", "empathy",
    "written communication", "verbal communication", "public speaking",
}

QUALIFICATIONS = {
    # Degrees
    "bachelor", "bachelor's", "b.tech", "b.e", "b.sc", "bs", "b.s",
    "master", "master's", "m.tech", "m.e", "m.sc", "ms", "m.s", "mba",
    "phd", "ph.d", "doctorate", "associate degree", "diploma", "certification",
    # Certifications
    "aws certified", "google certified", "microsoft certified", "azure certified",
    "pmp", "cissp", "cpa", "cfa", "gre", "gate",
    # Experience markers
    "years of experience", "year experience", "years experience",
    "entry level", "mid-level", "senior", "junior", "lead", "principal",
    "intern", "internship", "fresher", "graduate",
    # Domain
    "computer science", "information technology", "software engineering",
    "data science", "electrical engineering", "mechanical engineering",
    "mathematics", "statistics",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Lowercase and strip punctuation for comparison."""
    text = text.lower()
    text = re.sub(r"[^\w\s\.\+\#\-/]", " ", text)
    return text


def extract_ngrams(text: str, n: int) -> set:
    """Return all n-grams (as strings) from whitespace-tokenized text."""
    tokens = text.split()
    return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def extract_keywords_from_text(text: str, keyword_set: set) -> set:
    """Return which keywords from keyword_set appear in text."""
    norm = normalize(text)
    found = set()
    # Check single words and multi-word phrases
    all_ngrams = set(norm.split())
    for n in range(2, 5):
        all_ngrams |= extract_ngrams(norm, n)
    for kw in keyword_set:
        if kw in all_ngrams:
            found.add(kw)
    return found


# ── Main Matching Function ────────────────────────────────────────────────────

def match_resume(job_description: str, resume: str) -> dict:
    """
    Compare a job description against a resume.

    Returns
    -------
    dict with keys:
        match_score        : float (0–100)
        matched_keywords   : dict[category -> list[str]]
        missing_keywords   : dict[category -> list[str]]
        jd_keyword_counts  : dict[category -> int]   (total JD keywords per cat)
    """
    categories = {
        "Technical Skills": TECHNICAL_SKILLS,
        "Soft Skills": SOFT_SKILLS,
        "Qualifications": QUALIFICATIONS,
    }

    matched = {}
    missing = {}
    jd_counts = {}

    total_jd = 0
    total_matched = 0

    for cat, kw_set in categories.items():
        jd_kws   = extract_keywords_from_text(job_description, kw_set)
        res_kws  = extract_keywords_from_text(resume, kw_set)

        cat_matched = sorted(jd_kws & res_kws)
        cat_missing = sorted(jd_kws - res_kws)

        matched[cat] = cat_matched
        missing[cat] = cat_missing
        jd_counts[cat] = len(jd_kws)

        total_jd      += len(jd_kws)
        total_matched += len(cat_matched)

    match_score = (total_matched / total_jd * 100) if total_jd > 0 else 0.0

    return {
        "match_score":       round(match_score, 1),
        "matched_keywords":  matched,
        "missing_keywords":  missing,
        "jd_keyword_counts": jd_counts,
        "total_jd":          total_jd,
        "total_matched":     total_matched,
    }
