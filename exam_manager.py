# exam_manager.py
import streamlit as st
from datetime import datetime

def get_exams():
    """Return the list of exams stored in session state."""
    if "exams" not in st.session_state:
        st.session_state.exams = []
    return st.session_state.exams

def add_exam(subject, exam_date, study_hours, weak_topics):
    """Add a new exam entry."""
    exams = get_exams()
    exams.append({
        "subject": subject,
        "exam_date": exam_date,
        "study_hours": study_hours,
        "weak_topics": weak_topics
    })

def delete_exam(index):
    """Delete an exam entry by index."""
    exams = get_exams()
    if 0 <= index < len(exams):
        exams.pop(index)

def edit_exam(index, subject, exam_date, study_hours, weak_topics):
    """Edit an existing exam entry."""
    exams = get_exams()
    if 0 <= index < len(exams):
        exams[index] = {
            "subject": subject,
            "exam_date": exam_date,
            "study_hours": study_hours,
            "weak_topics": weak_topics
        }
