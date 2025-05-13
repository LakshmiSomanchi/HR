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
    "employees": """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    "attendance": """
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee TEXT,
            date TEXT,
            present INTEGER,
            leave_type TEXT
        )
    """,
    "post_joining_documents": """
        CREATE TABLE IF NOT EXISTS post_joining_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee TEXT,
            document_name TEXT,
            uploaded_date TEXT
        )
    """,
    "exit_management": """
        CREATE TABLE IF NOT EXISTS exit_management (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee TEXT,
            exit_date TEXT,
            reason TEXT,
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

# Add custom CSS for styling
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

# --- Sidebar and Authentication ---
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

st.sidebar.title("HR Dashboard")
st.sidebar.image("TechnoServe_logo.png", use_container_width=True)

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

menu = st.sidebar.radio(
    "Select Module",
    [
        "Master Tracker", "Employee Masterfiles", "Attendance Tracker",
        "Post-Joining Documents", "Exit Management", "Downloadable Reports"
    ]
)

# Reuse SQLite connection
conn = sqlite3.connect(DB)
c = conn.cursor()

# --- Master Tracker ---
if menu == "Master Tracker":
    st.markdown("<h1 style='color: #04b4ac;'>Master Tracker</h1>", unsafe_allow_html=True)
    employees = c.execute("SELECT * FROM employees").fetchall()
    st.write("### Employee Master Data")
    if employees:
        df = pd.DataFrame(employees, columns=[
            "ID", "Employee Code", "Name", "Designation", "Job Title",
            "Grade", "Date of Joining", "Confirmation Due Date", "Project", "Actual Project"
        ])
        st.dataframe(df)
    else:
        st.info("No employee records found.")

# --- Employee Masterfiles ---
elif menu == "Employee Masterfiles":
    st.markdown("<h1 style='color: #04b4ac;'>Employee Masterfiles</h1>", unsafe_allow_html=True)
    with st.form("employee_form"):
        employee_code = st.text_input("Employee Code")
        name = st.text_input("Employee Name")
        designation = st.text_input("Designation")
        job_title = st.text_input("Job Title")
        grade = st.text_input("Grade")
        doj = st.date_input("Date of Joining")
        confirmation_due_date = st.date_input("Confirmation Due Date")
        project = st.text_input("Project")
        actual_project = st.text_input("Actual Project")
        if st.form_submit_button("Add Employee"):
            c.execute(
                "INSERT INTO employees (employee_code, employee_name, designation, job_title, grade, doj, confirmation_due_date, project, actual_project) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (employee_code, name, designation, job_title, grade, str(doj), str(confirmation_due_date), project, actual_project)
            )
            conn.commit()
            st.success("Employee added successfully!")

# --- Attendance Tracker ---
elif menu == "Attendance Tracker":
    st.markdown("<h1 style='color: #04b4ac;'>Attendance Tracker</h1>", unsafe_allow_html=True)
    with st.form("attendance_form"):
        employee = st.text_input("Employee Name")
        date = st.date_input("Date", datetime.date.today())
        present = st.checkbox("Present")
        leave_type = st.selectbox("Leave Type", ["None", "Sick Leave", "Casual Leave", "Earned Leave"])
        if st.form_submit_button("Mark Attendance"):
            c.execute(
                "INSERT INTO attendance (employee, date, present, leave_type) VALUES (?, ?, ?, ?)",
                (employee, str(date), int(present), leave_type)
            )
            conn.commit()
            st.success("Attendance marked successfully!")

# --- Post-Joining Documents ---
elif menu == "Post-Joining Documents":
    st.markdown("<h1 style='color: #04b4ac;'>Post-Joining Documents</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Employee Documents", type=["pdf", "docx", "xlsx"])
    if uploaded_file:
        with st.form("post_joining_form"):
            employee = st.text_input("Employee Name")
            document_name = st.text_input("Document Name")
            if st.form_submit_button("Save Document"):
                c.execute(
                    "INSERT INTO post_joining_documents (employee, document_name, uploaded_date) VALUES (?, ?, ?)",
                    (employee, document_name, str(datetime.date.today()))
                )
                conn.commit()
                st.success(f"Document '{document_name}' for {employee} saved successfully!")

# --- Exit Management ---
elif menu == "Exit Management":
    st.markdown("<h1 style='color: #04b4ac;'>Exit Management</h1>", unsafe_allow_html=True)
    with st.form("exit_form"):
        employee = st.text_input("Employee Name")
        exit_date = st.date_input("Exit Date")
        reason = st.text_area("Reason for Exit")
        status = st.selectbox("Exit Status", ["Pending", "Completed"])
        if st.form_submit_button("Save Exit Details"):
            c.execute(
                "INSERT INTO exit_management (employee, exit_date, reason, status) VALUES (?, ?, ?, ?)",
                (employee, str(exit_date), reason, status)
            )
            conn.commit()
            st.success("Exit details saved successfully!")

# --- Downloadable Reports ---
elif menu == "Downloadable Reports":
    st.markdown("<h1 style='color: #04b4ac;'>Downloadable Reports</h1>", unsafe_allow_html=True)
    st.write("### Generate and Download Reports")
    employees = c.execute("SELECT * FROM employees").fetchall()
    if employees:
        df = pd.DataFrame(employees, columns=[
            "ID", "Employee Code", "Name", "Designation", "Job Title",
            "Grade", "Date of Joining", "Confirmation Due Date", "Project", "Actual Project"
        ])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Employee Report", data=csv, file_name="employee_report.csv", mime="text/csv")
    else:
        st.info("No data available for download.")
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
