from typing import List, Dict
from datetime import datetime, timedelta, time
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import streamlit as st
import os
from dotenv import load_dotenv
import random

load_dotenv()

# ---------------- LLM SETUP ----------------
@st.cache_resource
def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY not set. Check your .env file.")
        return None

    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0 
    )

llm = get_llm()

# ---------------- SMART BREAK LOGIC ----------------
def get_smart_break(slot_start: datetime):
    h = slot_start.hour

    if 7 <= h < 8:
        return "Breakfast & Morning Routine", 60
    if 10 <= h < 11:
        return "Short Break / Snack", 15
    if 13 <= h < 14:
        return "Lunch Break", 60
    if 17 <= h < 18:
        return "Evening Snack / Relax", 20
    if 20 <= h < 21:
        return "Dinner Break", 60

    return None, 0

# ---------------- STUDY PLAN GENERATOR ----------------
def generate_study_plan(exams: List[Dict]):

    now = datetime.now().replace(second=0, microsecond=0)
    today = now.date()
    # if very late night, shift planning to next day
    if now.time() >= time(23, 0):
        today = today + timedelta(days=1)
        start_time_today = time(7, 0)
    elif now.time() < time(7, 0):
    # Too early → wait till morning
        start_time_today = time(7, 0)
    else:
    # Normal daytime
        start_time_today = now.time()

    # Normalize exam dates
    for exam in exams:
        if isinstance(exam["exam_date"], datetime):
            exam["exam_date"] = exam["exam_date"].date()

    exams = sorted(exams, key=lambda x: x["exam_date"])
    exam_dates = {e["exam_date"] for e in exams}

    if not exams:
        return "No exams provided."

    plan_messages = []

    current_day = today
    end_day = exams[-1]["exam_date"]
    # -------- GLOBAL TOPIC QUEUE --------
    activities = [
        "Concept revision of",
        "Problem-solving on",
        "Topic-wise practice of",
        "Mixed question practice on",
        "Error analysis of",
        "Formula review of",
        "Light revision of",
        "Mock-style questions on",
        "Time-based practice on"
    ]

    while current_day <= end_day:
        day_text = f"**Study Plan for {current_day.strftime('%d %B %Y')}**\n"

        # -------- EXAM DAY --------
        if current_day in exam_dates:
            day_text += (
                "[EXAM_DAY]\n"
                "Good luck for your exam! 🎉\n"
                "After coming home, take proper rest.\n"
                "Later, lightly review the syllabus for your next exam and "
                "practice a few questions to analyse your current level.\n"
            )
            plan_messages.append(day_text)
            current_day += timedelta(days=1)
            continue

        # -------- START TIME --------
        slot_start = datetime.combine(current_day, start_time_today if current_day == today else time(7, 0))
        end_time = datetime.combine(current_day, time(23, 0))

        # -------- TOPICS POOL --------
        topics_pool = []
        for exam in exams:
            if exam["exam_date"] > current_day:  # only future exams
                topics_pool.extend(exam["weak_topics"])

        if not topics_pool:
            current_day += timedelta(days=1)
            continue

        random.shuffle(topics_pool)  # shuffle to avoid repetition
        topic_pointer = 0
        taken_breaks = set()

        # -------- BUILD DAY --------
        while slot_start < end_time:
            break_name, break_minutes = get_smart_break(slot_start)

            if break_name and break_name not in taken_breaks:
                break_end = min(slot_start + timedelta(minutes=break_minutes), end_time)
                day_text += (
                    f"{slot_start.strftime('%I:%M %p')} - "
                    f"{break_end.strftime('%I:%M %p')}: {break_name}\n"
                )
                taken_breaks.add(break_name)
                slot_start = break_end
                continue

            slot_end = min(slot_start + timedelta(hours=1), end_time)
            topic = topics_pool[topic_pointer % len(topics_pool)]
            topic_pointer += 1
            activity = random.choice(activities)


            day_text += (
                f"{slot_start.strftime('%I:%M %p')} - "
                f"{slot_end.strftime('%I:%M %p')}: {activity}{topic}\n"
            )

            slot_start = slot_end
            

        plan_messages.append(day_text)
        current_day += timedelta(days=1)

    # ---------------- AI ENRICHMENT ----------------
    system_prompt = (
        "You are an intelligent study planner AI.\n"
        "DO NOT add subject or hour headers.\n"
        "DO NOT modify dates or time slots.\n"
        "For each time slot, add 1–2 realistic, human-sounding study activities.\n"
        "Vary activity types naturally across the day.\n"
        "Do NOT repeat the same wording in consecutive slots.\n"
        "For breaks, do NOT add activities.\n"
        "For any day containing [EXAM_DAY], do NOT modify anything.\n"
        "After all days, add a section EXACTLY titled:\n"
        "Last-Minute Exam Tips\n"
        "with bullet points starting with '-'\n"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "\n".join(plan_messages))
    ])

    response = llm.invoke(prompt.format_messages())
    plan_text = response.content.strip()

    # Clean stray markdown
    plan_text = "\n".join(
        line for line in plan_text.splitlines() if line.strip() != "**"
    )

    return plan_text
