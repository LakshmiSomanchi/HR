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
"""
}

# Initialize the database
def init_db():
    with sqlite3.connect(DB) as conn:
        for ddl in TABLES.values():
            conn.execute(ddl)

init_db()

# Add custom CSS styling for dark background with high contrast
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
            color: #04b4ac;
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
            color: #04b4ac;
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
                st.rerun()  # ✅ Restart session
                st.stop()   # ✅ Prevent continuing execution
            else:
                st.error("Unauthorized email or password")
    st.stop()

# ✅ Show sidebar only if logged in
st.sidebar.title("HR Dashboard")
st.sidebar.image("TechnoServe_logo.png", use_container_width=True)

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

# ✅ Single use of sidebar menu
menu = st.sidebar.radio(
    "Select Module",
    [
        "Candidate Tracker", "Offer Tracker", "Employee Masterfile",
        "Interview Assessment", "Post-Joining Uploads",
        "Attendance & Leave Tracker", "Payroll Data Preparation",
        "Exit Management Tracker", "Downloadable Reports",
        "Admin Assets / Travel Requests", "Approvals Workflow"
    ]
)

# Reuse connection
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
            st.success("Attendance marked!")

# --- Payroll Data ---
elif menu == "Payroll Data":
    st.markdown("<h1 style='color: #04b4ac;'>Payroll Data</h1>", unsafe_allow_html=True)
    with st.form("payroll_form"):
        employee = st.text_input("Employee Name")
        month = st.text_input("Month (e.g., May 2025)")
        base_salary = st.number_input("Base Salary", min_value=0.0, step=1000.0)
        pf = base_salary * 0.12
        esic = base_salary * 0.0325
        total_salary = base_salary - (pf + esic)
        st.write(f"PF: {pf}, ESIC: {esic}, Total Salary: {total_salary}")
        if st.form_submit_button("Save Payroll"):
            c.execute(
                "INSERT INTO payroll (employee, month, base_salary, pf, esic, total_salary) VALUES (?, ?, ?, ?, ?, ?)",
                (employee, month, base_salary, pf, esic, total_salary)
            )
            conn.commit()
            st.success("Payroll data saved!")
# ✅ Final Complete Streamlit HR System (hr.py)

# --- Recruitment Snapshot ---
elif menu == "Recruitment Snapshot":
    st.markdown("<h1 style='color: #04b4ac;'>Recruitment Snapshot</h1>", unsafe_allow_html=True)
    st.markdown("### Upload or View Recruitment Snapshot")

    upload_file = st.file_uploader("Upload Recruitment Snapshot Excel", type=["xlsx"])
    if upload_file:
        with open("Recruitment_Snapshot.xlsx", "wb") as f:
            f.write(upload_file.read())
        st.success("Uploaded successfully.")

    if os.path.exists("Recruitment_Snapshot.xlsx"):
        df = pd.read_excel("Recruitment_Snapshot.xlsx", sheet_name="Recruitment Snapshot")

        with st.expander("🔍 Filters"):
            recruiter = st.selectbox("Recruiter", ["All"] + sorted(df["Recruiter"].dropna().unique().tolist()))
            project = st.selectbox("Project", ["All"] + sorted(df["Project"].dropna().unique().tolist()))
            if recruiter != "All":
                df = df[df["Recruiter"] == recruiter]
            if project != "All":
                df = df[df["Project"] == project]

        st.dataframe(df)

        # Key Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Offers Made", int(df["Total Offers Made"].sum()))
        col2.metric("Accepted", int(df["Offer Accepted"].sum()))
        col3.metric("Open Positions", int(df["Positions Open"].sum()))

        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name="recruitment_snapshot.csv", mime="text/csv")
    else:
        st.info("Please upload the 'Recruitment Snapshot' Excel file to begin.")

# --- Monthly MIS ---
elif menu == "Monthly MIS":
    st.markdown("<h1 style='color: #04b4ac;'>Monthly Recruitment Progress</h1>", unsafe_allow_html=True)

    upload_mis = st.file_uploader("Upload Monthly MIS Excel", type=["xlsx"], key="mis")
    if upload_mis:
        with open("Monthly_MIS.xlsx", "wb") as f:
            f.write(upload_mis.read())
        st.success("Uploaded successfully.")

    if os.path.exists("Monthly_MIS.xlsx"):
        df = pd.read_excel("Monthly_MIS.xlsx", sheet_name="Monthly MIS")
        df["Month"] = pd.to_datetime(df["Month"])

        chart_data = df[["Month", "Total Positions", "Open Positions", "Tot No of Positions Closed"]].dropna()
        chart_data.set_index("Month", inplace=True)

        st.line_chart(chart_data)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Monthly MIS", data=csv, file_name="monthly_mis.csv", mime="text/csv")
    else:
        st.info("Please upload the 'Monthly MIS' Excel file to view progress.")
