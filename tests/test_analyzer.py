from src.analyzer import (
    extract_skills,
    calculate_skill_match,
    calculate_text_similarity,
    analyze_resume,
)


def test_extract_skills():
    text = """
    I have experience with Python, SQL, Machine Learning,
    pandas and scikit-learn.
    """

    skills = extract_skills(text)

    assert "python" in skills
    assert "sql" in skills
    assert "machine learning" in skills
    assert "pandas" in skills


def test_skill_match():
    resume = """
    Python developer with experience in SQL and pandas.
    """

    job = """
    Looking for Python, SQL, pandas and Docker experience.
    """

    result = calculate_skill_match(resume, job)

    assert result["score"] == 75
    assert "python" in result["matched"]
    assert "docker" in result["missing"]


def test_similarity():
    resume = "Python machine learning data science"
    job = "Python machine learning engineer"

    score = calculate_text_similarity(resume, job)

    assert score > 0


def test_complete_analysis():
    resume = """
    Python developer with machine learning and SQL experience.
    """

    job = """
    We need a Python developer with machine learning and SQL skills.
    """

    result = analyze_resume(resume, job)

    assert "overall_score" in result
    assert "recommendations" in result
    assert result["overall_score"] > 0