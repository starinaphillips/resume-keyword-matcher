"""
cli.py - Command-line interface for Resume Keyword Matcher
Usage:
    python cli.py                        # interactive mode
    python cli.py --jd jd.txt --resume cv.txt
"""

import argparse
from matcher import match_resume


RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
DIM    = "\033[2m"
BLUE   = "\033[94m"


def color_score(score: float) -> str:
    """Return the score string wrapped in the appropriate terminal color."""
    if score >= 75:
        return f"{GREEN}{BOLD}{score}%{RESET}"
    elif score >= 50:
        return f"{YELLOW}{BOLD}{score}%{RESET}"
    else:
        return f"{RED}{BOLD}{score}%{RESET}"


def print_tags(keywords: list, color: str) -> None:
    """Print each keyword as a colored bullet, or show (none) if list is empty."""
    if not keywords:
        print(f"  {DIM}(none){RESET}")
    else:
        for kw in keywords:
            print(f"  {color}* {kw}{RESET}")


def run(job_description: str, resume: str) -> None:
    """Run the keyword match and print a formatted results report to the terminal."""
    result = match_resume(job_description, resume)

    score     = result["match_score"]
    matched   = result["matched_keywords"]
    missing   = result["missing_keywords"]
    total_jd  = result["total_jd"]
    total_hit = result["total_matched"]
    total_miss = total_jd - total_hit

    width = 60
    print("\n" + "=" * width)
    print(f"{BOLD}{CYAN}  RESUME KEYWORD MATCHER  -  Results{RESET}")
    print("=" * width)

    print(f"\n  Match Score : {color_score(score)}")
    print(f"  JD Keywords : {BOLD}{total_jd}{RESET}")
    print(f"  Matched     : {GREEN}{total_hit}{RESET}")
    print(f"  Missing     : {RED}{total_miss}{RESET}")

    for cat in ["Technical Skills", "Soft Skills", "Qualifications"]:
        total = result["jd_keyword_counts"][cat]
        hit   = len(matched[cat])
        pct   = round(hit / total * 100) if total > 0 else 0
        progress_bar = "#" * (pct // 5) + "-" * (20 - pct // 5)
        print(f"\n  {BOLD}{cat}{RESET}")
        print(f"  {CYAN}{progress_bar}{RESET} {pct}%  ({hit}/{total})")

    print("\n" + "-" * width)
    print(f"{BOLD}  MATCHED KEYWORDS{RESET}")
    print("-" * width)
    for cat in ["Technical Skills", "Soft Skills", "Qualifications"]:
        print(f"\n  {BLUE}{cat}{RESET}")
        print_tags(matched[cat], GREEN)

    print("\n" + "-" * width)
    print(f"{BOLD}  MISSING KEYWORDS{RESET}")
    print("-" * width)
    for cat in ["Technical Skills", "Soft Skills", "Qualifications"]:
        print(f"\n  {BLUE}{cat}{RESET}")
        print_tags(missing[cat], RED)

    print("\n" + "=" * width + "\n")


def interactive() -> None:
    """Run the matcher in interactive mode, reading input from the terminal."""
    print(f"\n{BOLD}{CYAN}Resume Keyword Matcher - Interactive Mode{RESET}")
    print("Paste text, then press ENTER twice (blank line) to submit.\n")

    print(f"{BOLD}Paste Job Description:{RESET}")
    jd_lines = []
    while True:
        line = input()
        if line == "" and jd_lines and jd_lines[-1] == "":
            break
        jd_lines.append(line)
    job_description = "\n".join(jd_lines).strip()

    print(f"\n{BOLD}Paste Resume:{RESET}")
    res_lines = []
    while True:
        line = input()
        if line == "" and res_lines and res_lines[-1] == "":
            break
        res_lines.append(line)
    resume = "\n".join(res_lines).strip()

    run(job_description, resume)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resume Keyword Matcher CLI")
    parser.add_argument("--jd",     help="Path to job description text file")
    parser.add_argument("--resume", help="Path to resume text file")
    args = parser.parse_args()

    if args.jd and args.resume:
        with open(args.jd, "r", encoding="utf-8") as jd_file:
            jd = jd_file.read()
        with open(args.resume, "r", encoding="utf-8") as resume_file:
            res = resume_file.read()
        run(jd, res)
    else:
        interactive()