# app.py
import streamlit as st
from datetime import date
from subjects import SUBJECT_TOPICS, add_custom_subject
import exam_manager as em
from planner import generate_study_plan
from calendar_view import show_calendar

st.set_page_config(page_title="AI Study Buddy Planner", layout="wide")
st.title("📚 AI Study Buddy – Multi-Exam Planner\n")
st.caption(
    "A smart planner that builds realistic daily study schedules for your exams. In order generate schedule for multiple exams, Click on Add exam button for each exam and click on generate study plan after making all entries."
)

# ---------------- FRONT-PAGE INPUT ----------------
st.header("Add Exam Details")
subjects_list = list(SUBJECT_TOPICS.keys())
selected_subject = st.selectbox("Select Subject", subjects_list + ["Other (Custom Subject)"])
custom_subject = ""
if selected_subject == "Other (Custom Subject)":
    custom_subject = st.text_input("Custom Subject Name")
    custom_topics_input = st.text_area("Enter Topics (comma-separated)")
    custom_topics = [t.strip() for t in custom_topics_input.split(",") if t.strip()]
else:
    topics = SUBJECT_TOPICS[selected_subject]
    custom_topics = st.multiselect("Select Weak Topics", topics)

exam_date = st.date_input("Exam Date", min_value=date.today())
study_hours = st.number_input("Total Study Hours Needed", min_value=1, max_value=100, step=1)

if st.button("➕ Add Exam"):
    final_subject = custom_subject if selected_subject == "Other (Custom Subject)" else selected_subject
    if selected_subject == "Other (Custom Subject)":
        add_custom_subject(custom_subject, custom_topics)
    em.add_exam(final_subject, exam_date, study_hours, custom_topics)
    st.success(f"Exam added: {final_subject} on {exam_date}")

# ---------------- EXAM TABLE ----------------
st.header("📋 Exams")
exams = em.get_exams()

for idx, e in enumerate(exams):
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 3, 1, 1])
    with col1: st.write(e["subject"])
    with col2: st.write(e["exam_date"])
    with col3: st.write(e["study_hours"])
    with col4: st.write(", ".join(e["weak_topics"]))
    with col5:
        if st.button("🗑 Delete", key=f"del-{idx}"):
            em.delete_exam(idx)
            if "edit_idx" in st.session_state and st.session_state.edit_idx == idx:
                del st.session_state.edit_idx
            st.rerun()
    with col6:
        if st.button("✏️ Edit", key=f"edit-{idx}"):
            st.session_state.edit_idx = idx
            st.session_state.edit_subject = e["subject"]
            st.session_state.edit_date = e["exam_date"]
            st.session_state.edit_hours = e["study_hours"]
            st.session_state.edit_topics = e["weak_topics"]

# ---------------- EDIT FORM ----------------
if "edit_idx" in st.session_state:
    st.markdown("### ✏️ Edit Exam")
    edit_idx = st.session_state.edit_idx
    current_subject = st.session_state.edit_subject

    new_subject = st.text_input("Subject", value=current_subject)

    new_date = st.date_input("Exam Date", value=st.session_state.edit_date)

    new_hours = st.number_input("Study Hours", min_value=1, value=st.session_state.edit_hours)

    # Topics input
    if current_subject in SUBJECT_TOPICS:
        new_topics = st.multiselect(
            "Weak Topics",
            SUBJECT_TOPICS[current_subject],
            default=st.session_state.edit_topics
        )
    else:
        new_topics_input = st.text_area(
            "Weak Topics (comma-separated)",
            value=", ".join(st.session_state.edit_topics)
        )
        new_topics = [t.strip() for t in new_topics_input.split(",") if t.strip()]

    if st.button("💾 Save Changes", key=f"save-{edit_idx}"):
        em.edit_exam(
            edit_idx,
            new_subject,
            new_date,
            new_hours,
            new_topics
        )
        st.success(f"Updated exam: {new_subject} on {new_date}")
        del st.session_state.edit_idx
        st.rerun()

# ---------------- GENERATE PLAN ----------------
if st.button("🎯 Generate Multi-Day Study Plan"):
    exams = em.get_exams()
    if not exams:
        st.warning("Add at least one exam first.")
    else:
        with st.spinner("Generating study plan..."):
            plan_text = generate_study_plan(exams)
            st.session_state.plan = plan_text

# ---------------- CALENDAR VIEW ----------------
if "plan" in st.session_state:
    st.header("📅 Study Plan Calendar")
    show_calendar(st.session_state.plan)