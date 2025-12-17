# calendar_view.py
import streamlit as st
import re

TIME_REGEX = re.compile(
    r"(\d{1,2}:\d{2}\s*(?:AM|PM)\s*-\s*\d{1,2}:\d{2}\s*(?:AM|PM))",
    re.IGNORECASE
)

def show_calendar(plan_text):
    if not plan_text:
        st.info("No study plan available.")
        return

    # -------- Separate last-minute tips --------
    tips_text = None
    if "Last-Minute Exam Tips" in plan_text:
        plan_text, tips_text = plan_text.split("Last-Minute Exam Tips", 1)

    # -------- Split into day blocks --------
    day_blocks = []
    current_block = []

    for raw_line in plan_text.splitlines():
        line = raw_line.strip()
        if not line or line == "**":
            continue

        if "Study Plan for" in line:
            if current_block:
                day_blocks.append(current_block)
                current_block = []

        current_block.append(line)

    if current_block:
        day_blocks.append(current_block)

    # -------- Render Days --------
    for block in day_blocks:
        title_line = block[0]
        is_exam_day = any("[EXAM_DAY]" in line for line in block)

        title = title_line.replace("**", "").replace("Study Plan for ", "")

        content_html = ""
        exam_lines = []

        for line in block[1:]:
            clean = line.replace("**", "").strip()

            if clean == "[EXAM_DAY]":
                continue

            if is_exam_day:
                exam_lines.append(clean)
                continue

            timing_match = TIME_REGEX.search(clean)
            if timing_match:
                timing = timing_match.group(1)
                clean = clean.replace(
                    timing, f"<b><u>{timing}</u></b>"
                )

            content_html += f"<li>{clean}</li>"

        # -------- BODY --------
        if is_exam_day:
            paragraphs = "".join(
                f"<p style='margin:6px 0;'>{l}</p>" for l in exam_lines if l
            )
            body_html = f"""
            <div style="
                background:#fff3f3;
                border:1px solid #f44336;
                border-radius:12px;
                padding:16px;
                color:##333333;
                font-weight:500;
            ">
                {paragraphs}
            </div>
            """
        else:
            body_html = f"""
            <ul style="line-height:1.7; margin-top:10px;">
                {content_html}
            </ul>
            """

        details_open = "open" if is_exam_day else ""
        border_color = "#f44336" if is_exam_day else "#ddd"
        bg_color = "#ffb300" if is_exam_day else "#fce6e9"

        st.markdown(
            f"""
            <details {details_open} style="
                border:1px solid {border_color};
                border-radius:14px;
                padding:12px;
                margin-bottom:16px;
                background-color:{bg_color};
                color:#000000;
            ">
                <summary style="
                    font-size:18px;
                    font-weight:bold;
                    cursor:pointer;
                ">📅 {title}</summary>
                {body_html}
            </details>
            """,
            unsafe_allow_html=True
        )

    # -------- Tips --------
    if tips_text:
        tips = [
            l.strip().replace("**", "")
            for l in tips_text.splitlines()
            if l.strip()
        ]

        tips_html = "".join(f"<li>{t}</li>" for t in tips)

        st.markdown(
            f"""
            <div style="
                border:2px solid #ff9800;
                border-radius:14px;
                padding:20px;
                margin-top:28px;
                background-color:#fff8e1;
                color:#000000;
            ">
                <h2>⚡ Last-Minute Exam Tips</h2>
                <ul>{tips_html}</ul>
            </div>
            """,
            unsafe_allow_html=True
        )
