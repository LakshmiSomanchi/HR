# HR System (hr.py)

import streamlit as st
import sqlite3
import datetime
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

DB = "hr.db"
ALLOWED_HR_EMAILS = ["hr1@example.com", "hr2@example.com"]

# Initialize tables
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
    "offers": """
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate TEXT,
            offer_date TEXT,
            offered_by TEXT,
            status TEXT
        )
    """,
    "employees": """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            join_date TEXT,
            department TEXT,
            status TEXT
        )
    """
}

def init_db():
    with sqlite3.connect(DB) as conn:
        for ddl in TABLES.values():
            conn.execute(ddl)

init_db()

# Login
if "email" not in st.session_state:
    with st.form("auth"):
        email = st.text_input("Enter HR Email")
        if st.form_submit_button("Login"):
            if email in ALLOWED_HR_EMAILS:
                st.session_state["email"] = email
            else:
                st.error("Unauthorized email")
    st.stop()

st.sidebar.title("HR Dashboard")
menu = st.sidebar.radio("Select Module", [
    "Candidate Tracker", "Offer Tracker", "Employee Masterfile",
    "Interview Assessment", "Post-Joining Uploads"])

# Candidate Tracker
if menu == "Candidate Tracker":
    st.title("Add Candidate")
    with st.form("add_candidate"):
        name = st.text_input("Name")
        designation = st.text_input("Designation")
        project = st.text_input("Project")
        location = st.text_input("Location")
        if st.form_submit_button("Save Candidate"):
            with sqlite3.connect(DB) as conn:
                conn.execute("INSERT INTO candidates (name, designation, project, location) VALUES (?, ?, ?, ?)",
                             (name, designation, project, location))
            st.success("Candidate added.")

# Offer Tracker
elif menu == "Offer Tracker":
    st.title("Offer Issuance")
    with st.form("offer_form"):
        candidate = st.text_input("Candidate Name")
        offer_date = st.date_input("Offer Date")
        offered_by = st.text_input("Offered By")
        status = st.selectbox("Status", ["Issued", "Accepted", "Declined"])
        if st.form_submit_button("Record Offer"):
            with sqlite3.connect(DB) as conn:
                conn.execute("INSERT INTO offers (candidate, offer_date, offered_by, status) VALUES (?, ?, ?, ?)",
                             (candidate, str(offer_date), offered_by, status))
            st.success("Offer recorded.")

# Employee Masterfile
elif menu == "Employee Masterfile":
    st.title("New Joiner Data")
    with st.form("employee_form"):
        name = st.text_input("Employee Name")
        join_date = st.date_input("Joining Date")
        department = st.text_input("Department")
        status = st.selectbox("Status", ["Active", "Inactive"])
        if st.form_submit_button("Save Record"):
            with sqlite3.connect(DB) as conn:
                conn.execute("INSERT INTO employees (name, join_date, department, status) VALUES (?, ?, ?, ?)",
                             (name, str(join_date), department, status))
            st.success("Employee added.")

# Interview Assessment
elif menu == "Interview Assessment":
    st.title("Interview Assessment")
    with sqlite3.connect(DB) as conn:
        candidates = conn.execute("SELECT id, name FROM candidates").fetchall()
    candidate_dict = {name: cid for cid, name in candidates}
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
                with sqlite3.connect(DB) as conn:
                    conn.execute("""
                        INSERT INTO interviews (
                            candidate_id, date, interviewer, strengths, weaknesses,
                            qualification, experience, comm_written, comm_oral,
                            problem_solving, team_capabilities, comparison, final_remarks, decision
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (cid, str(date), interviewer, strengths, weaknesses,
                          qualification, experience, comm_written, comm_oral,
                          problem_solving, team_capabilities, comparison, final_remarks, decision))
                st.success("Interview submitted.")

                pdf_buffer = BytesIO()
                p = canvas.Canvas(pdf_buffer, pagesize=letter)
                p.drawString(100, 750, f"Interview Report: {selected}")
                y = 730
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
                pdf_buffer.seek(0)

                st.download_button("Download Interview PDF", data=pdf_buffer.getvalue(),
                                   file_name=f"{selected}_interview.pdf")

# Post-Joining Uploads
elif menu == "Post-Joining Uploads":
    st.title("Document Upload")
    uploaded = st.file_uploader("Upload Post-Joining Document", type=["pdf", "docx", "jpg", "png"])
    if uploaded:
        path = os.path.join("uploads", uploaded.name)
        os.makedirs("uploads", exist_ok=True)
        with open(path, "wb") as f:
            f.write(uploaded.read())
        st.success(f"Uploaded to {path}")
