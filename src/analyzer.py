import re
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "excel",
    "power bi",
    "tableau",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "git",
    "github",
    "linux",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "natural language processing",
    "computer vision",
    "llm",
    "generative ai",
    "langchain",
    "rest api",
    "fastapi",
    "flask",
    "django",
    "streamlit",
}


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text: str) -> List[str]:
    """Find recognized technical skills."""
    cleaned = clean_text(text)

    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, cleaned):
            found.append(skill)

    return sorted(found)


def calculate_skill_match(
    resume_text: str,
    job_text: str
) -> Dict:
    """Compare resume skills against job requirements."""

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))

    if not job_skills:
        return {
            "score": 0,
            "resume_skills": sorted(resume_skills),
            "job_skills": [],
            "matched": [],
            "missing": [],
        }

    matched = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills

    score = round(
        (len(matched) / len(job_skills)) * 100
    )

    return {
        "score": score,
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched": sorted(matched),
        "missing": sorted(missing),
    }


def calculate_text_similarity(
    resume_text: str,
    job_text: str
) -> float:
    """Calculate TF-IDF cosine similarity."""

    if not resume_text.strip() or not job_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(
        [resume_text, job_text]
    )

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]

    return round(float(similarity) * 100, 2)


def generate_recommendations(
    resume_text: str,
    job_text: str,
    missing_skills: List[str]
) -> List[str]:

    recommendations = []

    if missing_skills:
        recommendations.append(
            "Consider adding relevant experience or projects involving: "
            + ", ".join(missing_skills[:8])
            + "."
        )

    if "project" not in clean_text(resume_text):
        recommendations.append(
            "Add 2–3 technical projects with measurable results."
        )

    if not re.search(
        r"\d+%|\$\d+|\d+\+|\d+\s*(users|customers|projects)",
        resume_text.lower()
    ):
        recommendations.append(
            "Add measurable results to your experience bullets."
        )

    if len(resume_text.split()) < 150:
        recommendations.append(
            "Your resume appears short. Consider adding relevant "
            "projects, accomplishments, and technical experience."
        )

    if not recommendations:
        recommendations.append(
            "Your resume has a good basic match. Continue tailoring "
            "your accomplishments to the specific job description."
        )

    return recommendations


def analyze_resume(
    resume_text: str,
    job_text: str
) -> Dict:
    """Run the complete resume analysis."""

    skill_result = calculate_skill_match(
        resume_text,
        job_text
    )

    similarity = calculate_text_similarity(
        clean_text(resume_text),
        clean_text(job_text)
    )

    recommendations = generate_recommendations(
        resume_text,
        job_text,
        skill_result["missing"]
    )

    overall_score = round(
        (skill_result["score"] * 0.60)
        + (similarity * 0.40)
    )

    return {
        **skill_result,
        "similarity": similarity,
        "overall_score": overall_score,
        "recommendations": recommendations,
    }