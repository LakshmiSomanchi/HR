# hr.py

import streamlit as st
import sqlite3
import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DB = "hr.db"
ALLOWED_HR_EMAILS = ["rsomanchi@tns.org", "hr2@example.com"]


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            designation TEXT,
            project TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            date TEXT,
            interviewer TEXT,
            strengths TEXT,
            weaknesses TEXT,
            qualification INTEGER,
            experience INTEGER,
            comm_written INTEGER,
            comm_oral INTEGER,
            problem_solving INTEGER,
            team_capabilities INTEGER,
            comparison TEXT,
            final_remarks TEXT,
            decision TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_candidate(name, designation, project, location):
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO candidates (name, designation, project, location) VALUES (?, ?, ?, ?)",
                     (name, designation, project, location))


def get_candidates():
    with sqlite3.connect(DB) as conn:
        return conn.execute("SELECT id, name FROM candidates").fetchall()


def insert_interview(candidate_id, date, interviewer, strengths, weaknesses, qualification, experience,
                     comm_written, comm_oral, problem_solving, team_capabilities, comparison, final_remarks, decision):
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            INSERT INTO interviews (
                candidate_id, date, interviewer, strengths, weaknesses, qualification, experience,
                comm_written, comm_oral, problem_solving, team_capabilities, comparison, final_remarks, decision
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (candidate_id, date, interviewer, strengths, weaknesses, qualification, experience,
              comm_written, comm_oral, problem_solving, team_capabilities, comparison, final_remarks, decision))


def generate_pdf(candidate, form):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Interview Report: {candidate[1]}")
    y = 730
    for k, v in form.items():
        p.drawString(100, y, f"{k}: {v}")
        y -= 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


# App
init_db()
st.title("HR Management Portal")

if "email" not in st.session_state:
    with st.form("auth"):
        email = st.text_input("Enter HR Email")
        if st.form_submit_button("Login"):
            if email in ALLOWED_HR_EMAILS:
                st.session_state["email"] = email
            else:
                st.error("Unauthorized email")
    st.stop()

st.success(f"Logged in as {st.session_state['email']}")

# Add Candidate
st.subheader("Add Candidate")
with st.form("add_candidate"):
    name = st.text_input("Name")
    designation = st.text_input("Designation")
    project = st.text_input("Project")
    location = st.text_input("Location")
    if st.form_submit_button("Save Candidate"):
        insert_candidate(name, designation, project, location)
        st.success(f"Candidate {name} saved.")

# Interview Assessment
st.subheader("Interview Assessment")
candidates = get_candidates()
candidate_dict = {n: i for i, n in candidates}
selected = st.selectbox("Select Candidate", list(candidate_dict.keys()))
if selected:
    cid = candidate_dict[selected]
    with st.form("interview_form"):
        date = st.date_input("Date", datetime.date.today())
        interviewer = st.text_input("Interviewer")
        strengths = st.text_area("Strengths (min 2)")
        weaknesses = st.text_area("Weaknesses (min 2)")
        qualification = st.slider("Qualification", 1, 5, 3)
        experience = st.slider("Experience", 1, 5, 3)
        comm_written = st.slider("Written Communication", 1, 5, 3)
        comm_oral = st.slider("Oral Communication", 1, 5, 3)
        problem_solving = st.slider("Problem Solving", 1, 5, 3)
        team_capabilities = st.slider("Team Capabilities", 1, 5, 3)
        comparison = st.selectbox("Comparison", ["Below Par", "At Par", "Above Par"])
        final_remarks = st.text_area("Final Remarks")
        decision = st.selectbox("Decision", ["Recommended for Hire", "Reject", "On Hold"])
        if st.form_submit_button("Submit Interview"):
            insert_interview(cid, str(date), interviewer, strengths, weaknesses,
                             qualification, experience, comm_written, comm_oral,
                             problem_solving, team_capabilities, comparison, final_remarks, decision)
            pdf_buffer = generate_pdf(
                (cid, selected), {
                    "Date": date, "Interviewer": interviewer,
                    "Strengths": strengths, "Weaknesses": weaknesses,
                    "Qualification": qualification, "Experience": experience,
                    "Comm. Written": comm_written, "Comm. Oral": comm_oral,
                    "Problem Solving": problem_solving, "Team Capabilities": team_capabilities,
                    "Comparison": comparison, "Remarks": final_remarks, "Decision": decision
                }
            )
            st.success("Interview saved.")
            st.download_button("Download Interview PDF", data=pdf_buffer, file_name=f"{selected}_interview.pdf")
