import streamlit as st
from pypdf import PdfReader
from docx import Document

from src.analyzer import analyze_resume


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_docx_text(uploaded_file):
    document = Document(uploaded_file)

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )


def extract_file_text(uploaded_file):

    if uploaded_file.name.lower().endswith(".pdf"):
        return extract_pdf_text(uploaded_file)

    if uploaded_file.name.lower().endswith(".docx"):
        return extract_docx_text(uploaded_file)

    return ""


st.title("🤖 AI Resume Analyzer")

st.markdown(
    """
    ### Analyze how well your resume matches a job description

    This application uses NLP and machine-learning techniques to:

    - Extract technical skills
    - Compare your resume with a job description
    - Calculate a skill-match score
    - Calculate text similarity
    - Identify missing skills
    - Generate resume improvement recommendations
    """
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Resume")

    uploaded_resume = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"]
    )

with col2:
    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Paste the complete job description..."
    )


if st.button("🚀 Analyze Resume", type="primary"):

    if uploaded_resume is None:
        st.error("Please upload a resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:

        with st.spinner("Analyzing resume..."):

            try:
                resume_text = extract_file_text(uploaded_resume)

                if not resume_text.strip():
                    st.error(
                        "Could not extract text from the uploaded file."
                    )
                    st.stop()

                result = analyze_resume(
                    resume_text,
                    job_description
                )

            except Exception as error:
                st.error(f"Something went wrong: {error}")
                st.stop()

        st.success("Analysis complete!")

        st.divider()

        st.subheader("📊 Results")

        score1, score2, score3 = st.columns(3)

        with score1:
            st.metric(
                "Overall Match",
                f"{result['overall_score']}%"
            )

        with score2:
            st.metric(
                "Skill Match",
                f"{result['score']}%"
            )

        with score3:
            st.metric(
                "Text Similarity",
                f"{result['similarity']}%"
            )

        st.progress(
            min(result["overall_score"] / 100, 1.0)
        )

        st.divider()

        skill_col1, skill_col2 = st.columns(2)

        with skill_col1:
            st.subheader("✅ Matching Skills")

            if result["matched"]:
                for skill in result["matched"]:
                    st.success(skill)
            else:
                st.info("No matching skills detected.")

        with skill_col2:
            st.subheader("⚠️ Missing Skills")

            if result["missing"]:
                for skill in result["missing"]:
                    st.warning(skill)
            else:
                st.success("No major missing skills detected!")

        st.divider()

        st.subheader("🔎 Skills Detected in Resume")

        if result["resume_skills"]:
            st.write(
                ", ".join(result["resume_skills"])
            )
        else:
            st.info("No recognized technical skills detected.")

        st.divider()

        st.subheader("💡 Recommendations")

        for recommendation in result["recommendations"]:
            st.write(f"• {recommendation}")

        st.divider()

        st.subheader("🧠 How the AI/ML system works")

        st.markdown(
            """
            **1. Text extraction**

            The application extracts text from your PDF or DOCX resume.

            **2. Skill extraction**

            Technical skills are detected in the resume and job description.

            **3. Skill matching**

            Resume skills are compared with skills required by the job.

            **4. TF-IDF**

            The resume and job description are converted into numerical
            representations using TF-IDF.

            **5. Cosine similarity**

            Cosine similarity measures how similar the two documents are.

            **6. Final score**

            The final score combines:

            - 60% technical skill match
            - 40% text similarity
            """
        )

        st.divider()

        with st.expander("View extracted resume text"):

            st.text_area(
                "Resume text",
                resume_text,
                height=300
            )