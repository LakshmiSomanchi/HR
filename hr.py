import streamlit as st
import sqlite3
import datetime
import os
import pandas as pd
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
    "employees": """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT,
            employee_code TEXT,
            employee_name TEXT,
            designation TEXT,
            job_title TEXT,
            grade TEXT,
            doj TEXT,
            confirmation_due_date TEXT,
            project TEXT,
            actual_project TEXT
        )
    """,
    "approvals": """
        CREATE TABLE IF NOT EXISTS approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee TEXT,
            approval_type TEXT,
            status TEXT
        )
    """,
    "admin_requests": """
        CREATE TABLE IF NOT EXISTS admin_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee TEXT,
            request_type TEXT,
            details TEXT
        )
    """
}

# Initialize the database
def init_db():
    with sqlite3.connect(DB) as conn:
        for ddl in TABLES.values():
            conn.execute(ddl)

init_db()

# Add custom CSS styling for better UI
st.markdown("""
    <style>
        body {
            background-color: #c0f6fb;
            color: #ffffff;
            font-family: Arial, sans-serif;
        }
        .stSidebar {
            background-color: #c0f6fb;
        }
        .stSidebar h1 {
            color: #211C4E;
        }
        .stButton button {
            background-color: #04b4ac;
            color: #ffffff;
            border-radius: 5px;
            border: none;
        }
        .stButton button:hover {
            background-color: #dc6262;
        }
        .stTextInput > div > label {
            color: #04b4ac;
        }
        .stSlider > div > label {
            color: #04b4ac;
        }
        .stSelectbox > div {
            color: #ffffff;
        }
        .stTitle {
            color: #211C4E;
        }
    </style>
""", unsafe_allow_html=True)

# --- Login and Sidebar ---
if "email" not in st.session_state:
    with st.form(key="login_form"):
        st.markdown("<h1 style='color: #04b4ac;'>HR Login</h1>", unsafe_allow_html=True)
        email = st.text_input("Enter HR Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if email in ALLOWED_HR_EMAILS and password == "hrsecure":
                st.session_state["email"] = email
                st.success("Login successful! Redirecting...")
                st.rerun()
                st.stop()
            else:
                st.error("Unauthorized email or password")
    st.stop()

# Sidebar
st.sidebar.title("HR Dashboard")
st.sidebar.image("TechnoServe_logo.png", use_container_width=True)

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

menu = st.sidebar.radio(
    "Select Module",
    [
        "Candidate Tracker", "Offer Tracker", "Employee Masterfile",
        "Interview Assessment", "Post-Joining Uploads",
        "Attendance & Leave Tracker", "Payroll Data Preparation",
        "Exit Management Tracker", "Downloadable Reports",
        "Admin Assets / Travel Requests", "Approvals Workflow",
        "Recruitment Snapshot", "Monthly MIS"
    ]
)

# Reuse SQLite connection
conn = sqlite3.connect(DB)
c = conn.cursor()

# --- Candidate Tracker ---
if menu == "Candidate Tracker":
    st.markdown("<h1 style='color: #04b4ac;'>Candidate Tracker</h1>", unsafe_allow_html=True)
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

# --- Approvals Workflow ---
elif menu == "Approvals Workflow":
    st.markdown("<h1 style='color: #04b4ac;'>Approvals Workflow</h1>", unsafe_allow_html=True)
    approvals = c.execute("SELECT * FROM approvals").fetchall()
    st.write("Pending Approvals:")
    for approval in approvals:
        st.write(f"Approval ID: {approval[0]}, Employee: {approval[1]}, Status: {approval[2]}")

# --- Admin Assets / Travel Requests ---
elif menu == "Admin Assets / Travel Requests":
    st.markdown("<h1 style='color: #04b4ac;'>Admin Assets / Travel Requests</h1>", unsafe_allow_html=True)
    with st.form("asset_form"):
        employee = st.text_input("Employee Name")
        request_type = st.selectbox("Request Type", ["Asset Allocation", "Travel Request"])
        details = st.text_area("Details")
        if st.form_submit_button("Submit Request"):
            c.execute(
                "INSERT INTO admin_requests (employee, request_type, details) VALUES (?, ?, ?)",
                (employee, request_type, details)
            )
            conn.commit()
            st.success("Request submitted successfully!")

# --- Interview Assessment ---
elif menu == "Interview Assessment":
    st.markdown("<h1 style='color: #04b4ac;'>Interview Assessment</h1>", unsafe_allow_html=True)
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
                st.success("Interview saved!")
