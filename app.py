"""
app.py - Streamlit frontend for Resume Keyword Matcher
Run with:  streamlit run app.py
"""

import streamlit as st
from matcher import match_resume

# -- Page Config ---------------------------------------------------------------

st.set_page_config(
    page_title="Resume Keyword Matcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -- Custom CSS ----------------------------------------------------------------

st.markdown("""
<style>
/* -- Import Fonts -- */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* -- Root Variables -- */
:root {
    --bg:          #0c0f1a;
    --surface:     #131726;
    --surface2:    #1a1f30;
    --border:      #252a40;
    --accent:      #4f8dff;
    --accent2:     #a78bfa;
    --success:     #34d399;
    --warning:     #fbbf24;
    --danger:      #f87171;
    --text:        #e2e8f0;
    --text-muted:  #64748b;
    --radius:      12px;
}

/* -- Global -- */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="block-container"] { padding-top: 2rem !important; }
.stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    resize: vertical !important;
    transition: border-color 0.2s;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,141,255,0.12) !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.75rem 2.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(79,141,255,0.35) !important;
}
.stButton > button:active { transform: translateY(0) !important; }


label, .stTextArea label {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
hr { border-color: var(--border) !important; }

/* -- Hero -- */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(79,141,255,0.1);
    border: 1px solid rgba(79,141,255,0.3);
    border-radius: 999px;
    padding: 0.25rem 1rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.2rem, 5vw, 3.8rem) !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    background: linear-gradient(135deg, #fff 30%, var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.75rem !important;
}
.hero p {
    color: var(--text-muted) !important;
    font-size: 1.05rem !important;
    max-width: 520px;
    margin: 0 auto !important;
    line-height: 1.6 !important;
}

/* -- Cards -- */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
}
.card-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.6rem;
}

/* -- Score Ring -- */
.score-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2.5rem 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.score-wrapper::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(79,141,255,0.07) 0%, transparent 65%);
    pointer-events: none;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
    background: linear-gradient(135deg, #fff 40%, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.score-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: 0.25rem;
}
.score-verdict {
    margin-top: 1rem;
    padding: 0.4rem 1.2rem;
    border-radius: 999px;
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.06em;
}
.verdict-strong  { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.verdict-good    { background: rgba(251,191,36,0.12); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.verdict-average { background: rgba(251,146,60,0.12); color: #fb923c; border: 1px solid rgba(251,146,60,0.3); }
.verdict-weak    { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }

/* -- Stat Pills -- */
.stat-row { display: flex; gap: 0.75rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.stat-pill {
    flex: 1 1 100px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.stat-pill-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    line-height: 1;
}
.stat-pill-lbl {
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.num-blue   { color: var(--accent); }
.num-green  { color: var(--success); }
.num-red    { color: var(--danger); }

/* -- Progress Bar -- */
.progress-wrap { margin-bottom: 1.5rem; }
.progress-meta { display: flex; justify-content: space-between; margin-bottom: 0.4rem; }
.progress-title { font-family: 'Syne', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; }
.progress-pct { font-size: 0.78rem; color: var(--text-muted); }
.progress-track {
    height: 6px;
    background: var(--border);
    border-radius: 999px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width 0.8s cubic-bezier(0.16,1,0.3,1);
}

/* -- Keyword Tags -- */
.tag-section-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin: 1.2rem 0 0.6rem;
}
.tag-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.5rem; }
.tag {
    display: inline-block;
    border-radius: 6px;
    padding: 0.25rem 0.65rem;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.02em;
    white-space: nowrap;
}
.tag-green  { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.25); }
.tag-red    { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }
.tag-none   { background: var(--surface2); color: var(--text-muted); border: 1px solid var(--border); font-style: italic; font-size: 0.75rem; }

/* -- Category Block -- */
.cat-block {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.3rem;
    margin-bottom: 1rem;
}
.cat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}
.cat-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.cat-chip {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
}
.chip-green { background: rgba(52,211,153,0.15); color: #34d399; }
.chip-red   { background: rgba(248,113,113,0.15); color: #f87171; }
.chip-grey  { background: var(--border); color: var(--text-muted); }

/* -- Divider -- */
.section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}

/* -- Empty state -- */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--text-muted);
}
.empty-icon { font-size: 3rem; margin-bottom: 0.75rem; }
.empty-text { font-size: 0.95rem; }

/* -- Footer -- */
.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.78rem;
    padding: 2.5rem 1rem 1rem;
    letter-spacing: 0.03em;
}
</style>
""", unsafe_allow_html=True)


# -- Hero Section -------------------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-badge">🎯 ATS Keyword Analyzer</div>
    <h1>Resume Keyword<br>Matcher</h1>
    <p>Paste a job description and your resume. Instantly discover what keywords you're missing and how well your resume matches the role.</p>
</div>
""", unsafe_allow_html=True)


# -- Input Columns -------------------------------------------------------------

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="card-label">📋 Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        label="Job Description",
        placeholder="Paste the full job description here...\n\nInclude responsibilities, requirements, and qualifications.",
        height=320,
        label_visibility="collapsed",
        key="jd_input",
    )

with col2:
    st.markdown('<div class="card-label">📄 Your Resume</div>', unsafe_allow_html=True)
    resume = st.text_area(
        label="Resume",
        placeholder="Paste your resume text here...\n\nInclude your skills, experience, education, and projects.",
        height=320,
        label_visibility="collapsed",
        key="resume_input",
    )

st.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.button("Analyze Match →")


# -- Results -------------------------------------------------------------------

if analyze_btn:
    if not job_description.strip() or not resume.strip():
        st.warning("⚠️  Please provide both a job description and a resume.")
    else:
        with st.spinner("Analyzing keywords…"):
            result = match_resume(job_description, resume)

        score      = result["match_score"]
        matched    = result["matched_keywords"]
        missing    = result["missing_keywords"]
        jd_counts  = result["jd_keyword_counts"]
        total_jd   = result["total_jd"]
        total_hit  = result["total_matched"]
        total_miss = total_jd - total_hit

        # Verdict
        if score >= 75:
            verdict_cls, verdict_txt = "verdict-strong",  "Strong Match 🚀"
        elif score >= 50:
            verdict_cls, verdict_txt = "verdict-good",    "Good Match ✅"
        elif score >= 30:
            verdict_cls, verdict_txt = "verdict-average", "Average Match ⚠️"
        else:
            verdict_cls, verdict_txt = "verdict-weak",    "Weak Match ❌"

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('<div class="card-label" style="text-align:center;margin-bottom:1.25rem;">📊 Analysis Results</div>', unsafe_allow_html=True)

        left, right = st.columns([1, 1.8], gap="large")

        # -- Left: Score --
        with left:
            st.markdown(f"""
            <div class="score-wrapper">
                <div class="score-number">{score}%</div>
                <div class="score-label">Match Score</div>
                <div class="score-verdict {verdict_cls}">{verdict_txt}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="stat-row">
                <div class="stat-pill">
                    <div class="stat-pill-num num-blue">{total_jd}</div>
                    <div class="stat-pill-lbl">JD Keywords</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-pill-num num-green">{total_hit}</div>
                    <div class="stat-pill-lbl">Matched</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-pill-num num-red">{total_miss}</div>
                    <div class="stat-pill-lbl">Missing</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Per-category progress bars
            cat_colors = {
                "Technical Skills": "#4f8dff",
                "Soft Skills":       "#a78bfa",
                "Qualifications":    "#34d399",
            }
            for cat in ["Technical Skills", "Soft Skills", "Qualifications"]:
                total = jd_counts[cat]
                hit   = len(matched[cat])
                pct   = round(hit / total * 100) if total > 0 else 0
                color = cat_colors[cat]
                st.markdown(f"""
                <div class="progress-wrap">
                    <div class="progress-meta">
                        <span class="progress-title">{cat}</span>
                        <span class="progress-pct">{hit}/{total}</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill" style="width:{pct}%;background:{color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # -- Right: Keyword Breakdown --
        with right:
            tabs = st.tabs(["🔴 Missing Keywords", "🟢 Matched Keywords"])

            with tabs[0]:
                any_missing = any(missing[c] for c in missing)
                if not any_missing:
                    st.markdown("""
                    <div class="empty-state">
                        <div class="empty-icon">🎉</div>
                        <div class="empty-text">No missing keywords found - great match!</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    for cat in ["Technical Skills", "Soft Skills", "Qualifications"]:
                        kws = missing[cat]
                        chip_cls = "chip-red" if kws else "chip-grey"
                        chip_txt = f"{len(kws)} missing" if kws else "none missing"
                        tags_html = (
                            "".join(f'<span class="tag tag-red">{kw}</span>' for kw in kws)
                            if kws else '<span class="tag tag-none">None missing ✓</span>'
                        )
                        st.markdown(f"""
                        <div class="cat-block">
                            <div class="cat-header">
                                <span class="cat-title">{cat}</span>
                                <span class="cat-chip {chip_cls}">{chip_txt}</span>
                            </div>
                            <div class="tag-row">{tags_html}</div>
                        </div>""", unsafe_allow_html=True)

            with tabs[1]:
                any_matched = any(matched[c] for c in matched)
                if not any_matched:
                    st.markdown("""
                    <div class="empty-state">
                        <div class="empty-icon">😔</div>
                        <div class="empty-text">No matching keywords found. Try enriching your resume with relevant skills.</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    for cat in ["Technical Skills", "Soft Skills", "Qualifications"]:
                        kws = matched[cat]
                        chip_cls = "chip-green" if kws else "chip-grey"
                        chip_txt = f"{len(kws)} matched" if kws else "none matched"
                        tags_html = (
                            "".join(f'<span class="tag tag-green">{kw}</span>' for kw in kws)
                            if kws else '<span class="tag tag-none">None matched</span>'
                        )
                        st.markdown(f"""
                        <div class="cat-block">
                            <div class="cat-header">
                                <span class="cat-title">{cat}</span>
                                <span class="cat-chip {chip_cls}">{chip_txt}</span>
                            </div>
                            <div class="tag-row">{tags_html}</div>
                        </div>""", unsafe_allow_html=True)

        # -- Tips --
        if total_miss > 0:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown('<div class="card-label">💡 Quick Tips</div>', unsafe_allow_html=True)
            tips = []
            if missing["Technical Skills"]:
                top3 = ", ".join(f"`{k}`" for k in missing["Technical Skills"][:3])
                tips.append(f"**Add missing technical skills** - consider adding {top3} to your skills section or project descriptions.")
            if missing["Soft Skills"]:
                ss = ", ".join(f"`{k}`" for k in missing["Soft Skills"][:2])
                tips.append(f"**Mention soft skills** - weave in {ss} through your work experience bullet points.")
            if missing["Qualifications"]:
                q = ", ".join(f"`{k}`" for k in missing["Qualifications"][:2])
                tips.append(f"**Highlight qualifications** - make sure {q} are explicitly stated in your education or summary section.")
            for tip in tips:
                st.markdown(f"- {tip}")

elif not analyze_btn:
    st.markdown("""
    <div class="empty-state" style="padding:2rem 1rem;">
        <div class="empty-icon">⬆️</div>
        <div class="empty-text">Fill in both fields above and click <strong>Analyze Match</strong> to see results.</div>
    </div>
    """, unsafe_allow_html=True)

# -- Footer --------------------------------------------------------------------

st.markdown("""
<div class="footer">
    Resume Keyword Matcher &nbsp;·&nbsp; Built with Python &amp; Streamlit
</div>
""", unsafe_allow_html=True)
