import streamlit as st
import matplotlib.pyplot as plt

from chatbot import get_career_advice
from career_engine import recommend
from mbti_model import (
    predict_mbti_quiz,
    predict_mbti_ml
)
from pdf_generator import generate_report

from database import (
    create_tables,
    save_user,
    get_all_users,
    save_session,
    get_sessions
)

# Initialize Database
create_tables()

# MBTI Descriptions
mbti_info = {
    "INTJ": "Strategic Thinker",
    "INTP": "Analytical Innovator",
    "ENTJ": "Natural Leader",
    "ENTP": "Creative Problem Solver",
    "INFJ": "Insightful Mentor",
    "INFP": "Creative Idealist",
    "ENFJ": "Inspirational Leader",
    "ENFP": "Enthusiastic Motivator",
    "ISTJ": "Reliable Organizer",
    "ISFJ": "Supportive Protector",
    "ESTJ": "Efficient Manager",
    "ESFJ": "Community Builder",
    "ISTP": "Practical Problem Solver",
    "ISFP": "Flexible Creator",
    "ESTP": "Energetic Performer",
    "ESFP": "Outgoing Entertainer"
}

# Interest Scores
interest_scores = {
    "AI": 95,
    "Data Science": 90,
    "Web Development": 80,
    "Cyber Security": 85
}

# Career Scope Scores
career_scope = {
    "AI Engineer": 98,
    "ML Engineer": 95,
    "Data Scientist": 92,
    "Data Analyst": 80,
    "Frontend Developer": 75,
    "Full Stack Developer": 88,
    "Security Analyst": 90
}

# -------------------------
# PAGE TITLE
# -------------------------

st.title("🎯 AI Career Counselor")

# -------------------------
# USER DETAILS
# -------------------------

st.header("Basic Information")

name = st.text_input("Name")

education = st.selectbox(
    "Education",
    [
        "10th",
        "12th",
        "Diploma",
        "B.Tech",
        "M.Tech",
        "MBA"
    ]
)

skills = st.text_input(
    "Skills (comma separated)"
)

# -------------------------
# INTERESTS
# -------------------------

st.header("Career Interests")

interests = st.multiselect(
    "Choose Interests",
    [
        "AI",
        "Data Science",
        "Web Development",
        "Cyber Security"
    ]
)

# -------------------------
# MBTI QUIZ
# -------------------------

st.header("Personality Assessment")

q1 = st.radio(
    "1. You prefer",
    [
        "Working Alone",
        "Working in Teams"
    ]
)

q2 = st.radio(
    "2. You make decisions based on",
    [
        "Logic",
        "Emotions"
    ]
)

q3 = st.radio(
    "3. You are usually",
    [
        "Planner",
        "Spontaneous"
    ]
)

q4 = st.radio(
    "4. You enjoy",
    [
        "Deep Thinking",
        "Social Activities"
    ]
)

q5 = st.radio(
    "5. You focus more on",
    [
        "Ideas",
        "Practical Reality"
    ]
)

# -------------------------
# FREE TEXT FOR ML MODEL
# -------------------------

st.subheader("Personality Description")

personality_text = st.text_area(
    "Describe yourself in a few sentences"
)

# -------------------------
# ANALYZE BUTTON
# -------------------------

if st.button("Analyze"):

    if not name:
        st.error("Please enter your name.")
        st.stop()

    # Quiz MBTI
    quiz_mbti = predict_mbti_quiz(
        q1,
        q2,
        q3,
        q4,
        q5
    )

    # ML MBTI
    ml_mbti = "Not Available"
    confidence = 0

    if personality_text.strip():

        try:

            ml_mbti, confidence = predict_mbti_ml(
                personality_text
            )

        except Exception as e:

            st.warning(
                f"ML Model Error: {e}"
            )

    # Final MBTI
    mbti = quiz_mbti

    # Save User
    save_user(
        name,
        education,
        skills,
        mbti
    )

    # Career Recommendations
    careers = recommend(interests)

    recommendation_text = ""

    for role, salary in careers:
        recommendation_text += (
            f"{role} - {salary}\n"
        )

    # GPT Advice
    try:

        gpt_advice = get_career_advice(
            education,
            skills,
            interests,
            mbti
        )

    except Exception as e:

        gpt_advice = (
            f"GPT Error: {str(e)}"
        )

    # Save Session
    try:

        save_session(
            name,
            ",".join(interests),
            mbti,
            recommendation_text,
            gpt_advice
        )

    except Exception:
        pass

    # -------------------------
    # RESULTS
    # -------------------------

    st.success(
        f"Quiz MBTI: {quiz_mbti}"
    )

    st.info(
        mbti_info.get(
            quiz_mbti,
            "Personality Type"
        )
    )

    if ml_mbti != "Not Available":

        st.success(
            f"ML MBTI: {ml_mbti}"
        )

        st.info(
            f"Confidence: {confidence:.2f}%"
        )

    # -------------------------
    # CAREERS
    # -------------------------

    st.subheader(
        "Recommended Careers"
    )

    if careers:

        for role, salary in careers:

            st.metric(
                label=role,
                value=salary
            )

    else:

        st.warning(
            "No recommendations found."
        )

    # -------------------------
    # GPT CAREER COUNSELOR
    # -------------------------

    st.subheader(
        "🤖 AI Career Counselor"
    )

    st.write(
        gpt_advice
    )

    # -------------------------
    # INTEREST GRAPH
    # -------------------------

    if interests:

        st.subheader(
            "📊 Interest Analytics"
        )

        labels = []
        scores = []

        for interest in interests:

            labels.append(interest)

            scores.append(
                interest_scores.get(
                    interest,
                    50
                )
            )

        fig, ax = plt.subplots()

        ax.bar(
            labels,
            scores
        )

        ax.set_title(
            "Interest Strength"
        )

        ax.set_ylabel(
            "Score"
        )

        st.pyplot(fig)

    # -------------------------
    # CAREER SCOPE GRAPH
    # -------------------------

    if careers:

        st.subheader(
            "🚀 Career Scope Analysis"
        )

        career_names = []
        scope_scores = []

        for role, salary in careers:

            career_names.append(role)

            scope_scores.append(
                career_scope.get(
                    role,
                    70
                )
            )

        fig2, ax2 = plt.subplots()

        ax2.barh(
            career_names,
            scope_scores
        )

        ax2.set_title(
            "Future Scope (%)"
        )

        st.pyplot(fig2)

    # -------------------------
    # PDF REPORT
    # -------------------------

    pdf_file = generate_report(
        name,
        mbti,
        careers
    )

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="📄 Download Career Report",
            data=file,
            file_name="career_report.pdf",
            mime="application/pdf"
        )

# -------------------------
# SAVED USERS
# -------------------------

st.markdown("---")

if st.button("Show Saved Users"):

    users = get_all_users()

    st.subheader(
        "Saved Users"
    )

    for user in users:

        st.write(user)

# -------------------------
# SESSION HISTORY
# -------------------------

st.markdown("---")

if st.button("Show Session History"):

    sessions = get_sessions()

    st.subheader(
        "Career Session History"
    )

    for session in sessions:

        st.write(session)