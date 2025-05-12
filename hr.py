import streamlit as st
import sqlite3
import datetime
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

DB = "hr.db"
ALLOWED_HR_EMAILS = ["rsomanchi@tns.org", "hr2@example.com"]

# Database table schema
TABLES = {
    "candidates": """
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            designation TEXT,
            project TEXT,
            location TEXT
        )
    """,
    "interviews": """
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
    """,
    "attendance": """
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee TEXT,
            date TEXT,
            present INTEGER,
            leave_type TEXT
        )
    """,
    "payroll": """
        CREATE TABLE IF NOT EXISTS payroll (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee TEXT,
            month TEXT,
            base_salary REAL,
            pf REAL,
            esic REAL,
            total_salary REAL
        )
    """,
    "exits": """
        CREATE TABLE IF NOT EXISTS exits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee TEXT,
            exit_date TEXT,
            reason TEXT
        )
    """,
    "assets": """
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee TEXT,
            asset TEXT,
            status TEXT
        )
    """,
    "approvals": """
        CREATE TABLE IF NOT EXISTS approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_type TEXT,
            requested_by TEXT,
            approved_by TEXT,
            status TEXT
        )
    """,
}


# Initialize the database
def init_db():
    with sqlite3.connect(DB) as conn:
        for ddl in TABLES.values():
            conn.execute(ddl)


init_db()


# --- Login and Sidebar ---
if "email" not in st.session_state:
    with st.form("auth"):
        email = st.text_input("Enter HR Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if email in ALLOWED_HR_EMAILS and password == "hrsecure":
                st.session_state["email"] = email
            else:
                st.error("Unauthorized email or password")
                st.stop()

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.experimental_rerun()

st.sidebar.title("HR Dashboard")
menu = st.sidebar.radio(
    "Select Module",
    [
        "Candidate Tracker", "Interview Assessment", "Attendance & Leave Tracker",
        "Payroll Data Preparation", "Exit Management Tracker", "Downloadable Reports",
        "Admin Assets / Travel Requests", "Approvals Workflow"
    ]
)

# Reuse connection
conn = sqlite3.connect(DB)
c = conn.cursor()

# --- Candidate Tracker ---
if menu == "Candidate Tracker":
    st.title("Add Candidate")
    with st.form("add_candidate"):
        name = st.text_input("Name")
        designation = st.text_input("Designation")
        project = st.text_input("Project")
        location = st.text_input("Location")
        if st.form_submit_button("Save Candidate"):
            c.execute(
                "INSERT INTO candidates (name, designation, project, location) VALUES (?, ?, ?, ?)",
                (name, designation, project, location)
            )
            conn.commit()
            st.success("Candidate added.")

# --- Interview Assessment ---
elif menu == "Interview Assessment":
    st.title("Interview Assessment")
    candidates = c.execute("SELECT id, name FROM candidates").fetchall()
    candidate_dict = {n: i for i, n in candidates}
    selected = st.selectbox("Select Candidate", list(candidate_dict))
    if selected:
        cid = candidate_dict[selected]
        with st.form("interview_form"):
            date = st.date_input("Date", datetime.date.today())
            interviewer = st.text_input("Interviewer")
            strengths = st.text_area("Strengths")
            weaknesses = st.text_area("Weaknesses")
            qualification = st.slider("Qualification", 1, 5, 3)
            experience = st.slider("Experience", 1, 5, 3)
            comm_written = st.slider("Written Communication", 1, 5, 3)
            comm_oral = st.slider("Oral Communication", 1, 5, 3)
            problem_solving = st.slider("Problem Solving", 1, 5, 3)
            team_capabilities = st.slider("Team Capabilities", 1, 5, 3)
            comparison = st.selectbox("Comparison", ["Below Par", "At Par", "Above Par"])
            final_remarks = st.text_area("Final Remarks")
            decision = st.selectbox("Decision", ["Recommended for Hire", "Reject", "On Hold"])
            if st.form_submit_button("Save Interview"):
                c.execute(
                    """
                    INSERT INTO interviews (candidate_id, date, interviewer, strengths, weaknesses,
                    qualification, experience, comm_written, comm_oral, problem_solving,
                    team_capabilities, comparison, final_remarks, decision)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (cid, str(date), interviewer, strengths, weaknesses, qualification, experience,
                     comm_written, comm_oral, problem_solving, team_capabilities, comparison,
                     final_remarks, decision)
                )
                conn.commit()

                # Generate PDF
                buffer = BytesIO()
                p = canvas.Canvas(buffer, pagesize=letter)
                y = 750
                p.drawString(100, y, f"Interview Report: {selected}")
                y -= 20
                for label, val in {
                    "Date": date, "Interviewer": interviewer,
                    "Strengths": strengths, "Weaknesses": weaknesses,
                    "Qualification": qualification, "Experience": experience,
                    "Comm Written": comm_written, "Comm Oral": comm_oral,
                    "Problem Solving": problem_solving, "Team Capabilities": team_capabilities,
                    "Comparison": comparison, "Remarks": final_remarks, "Decision": decision
                }.items():
                    p.drawString(100, y, f"{label}: {val}")
                    y -= 20
                p.showPage()
                p.save()
                buffer.seek(0)
                st.download_button(
                    "Download Interview PDF", data=buffer.getvalue(),
                    file_name=f"{selected}_interview.pdf"
                )

# --- Exit database connection ---
conn.close()
