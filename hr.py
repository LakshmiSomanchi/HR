# Final Complete Streamlit HR System (hr.py)

import streamlit as st
import sqlite3
import datetime
import os
import io
from io import BytesIO
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="TechnoServe HR Dashboard", page_icon="🧑‍💼", layout="wide")

# Add the TechnoServe logo to the sidebar and main page
st.sidebar.image("technoserve_logo.png", use_column_width=True)
st.sidebar.title("TechnoServe HR Dashboard")
st.sidebar.markdown("---")  # Add a divider for better sidebar UI

# Add a main page header with the logo
st.image("technoserve_logo.png", use_column_width=True)
st.title("Welcome to the TechnoServe HR Dashboard")
st.markdown(
    """
    <div style="background-color: #f0f8ff; padding: 10px; border-radius: 10px;">
        <h3 style="text-align: center; color: #4b8bbe;">Empowering HR Management with Streamlined Solutions</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# Add vertical space
add_vertical_space(2)

# Sidebar navigation
menu = st.sidebar.radio(
    "Select a Module:",
    [
        "Candidate Tracker", "Offer Tracker", "Employee Masterfile",
        "Interview Assessment", "Post-Joining Uploads",
        "Attendance & Leave Tracker", "Payroll Data Preparation",
        "Exit Management Tracker", "Downloadable Reports",
        "Admin Assets / Travel Requests", "Approvals Workflow"
    ]
)

# Additional enhancements for UI customization
st.sidebar.markdown(
    """
    <style>
        .css-1aumxhk {background-color: #d3f8e2 !important; color: #000;}
        .css-17eq0hr {font-size: 18px; font-weight: bold;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Example interactive element for dashboard liveliness
if menu == "Candidate Tracker":
    st.title("📋 Candidate Tracker")
    st.markdown("Track and manage candidates efficiently.")
    name = st.text_input("Candidate Name")
    designation = st.text_input("Designation")
    project = st.text_input("Project")
    location = st.text_input("Location")
    if st.button("Save Candidate"):
        st.success(f"Saved candidate: {name}!")

elif menu == "Offer Tracker":
    st.title("💼 Offer Tracker")
    st.markdown("Manage job offers in a seamless way.")
    candidate = st.text_input("Candidate Name")
    offer_date = st.date_input("Offer Date")
    offered_by = st.text_input("Offered By")
    status = st.selectbox("Status", ["Issued", "Accepted", "Declined"])
    if st.button("Record Offer"):
        st.success(f"Offer recorded for {candidate}!")

# Add a footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 14px; color: grey;">
        Powered by TechnoServe | Enhancing Human Resource Management
    </div>
    """,
    unsafe_allow_html=True,
)


st.sidebar.image("technoserve_logo.png", use_column_width=True)
st.image("technoserve_logo.png", use_column_width=True)

st.title("Welcome to the TechnoServe HR Dashboard")

DB = "hr.db"
ALLOWED_HR_EMAILS = ["rsomanchi@tns.org", "hr2@example.com"]

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
    """
}

# Initialize DB
with sqlite3.connect(DB) as conn:
    for ddl in TABLES.values():
        conn.execute(ddl)

# --- Login ---
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
menu = st.sidebar.radio("Select Module", [
    "Candidate Tracker", "Offer Tracker", "Employee Masterfile",
    "Interview Assessment", "Post-Joining Uploads",
    "Attendance & Leave Tracker", "Payroll Data Preparation",
    "Exit Management Tracker", "Downloadable Reports",
    "Admin Assets / Travel Requests", "Approvals Workflow"])

conn = sqlite3.connect(DB)
c = conn.cursor()

# Candidate Tracker
if menu == "Candidate Tracker":
    st.title("Add Candidate")
    with st.form("add_candidate"):
        name = st.text_input("Name")
        designation = st.text_input("Designation")
        project = st.text_input("Project")
        location = st.text_input("Location")
        if st.form_submit_button("Save Candidate"):
            c.execute("INSERT INTO candidates (name, designation, project, location) VALUES (?, ?, ?, ?)",
                      (name, designation, project, location))
            conn.commit()
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
            c.execute("INSERT INTO offers (candidate, offer_date, offered_by, status) VALUES (?, ?, ?, ?)",
                      (candidate, str(offer_date), offered_by, status))
            conn.commit()
            st.success("Offer recorded.")

# Employee Masterfile
elif menu == "Employee Masterfile":
    st.title("Employee Master")
    with st.form("employee_form"):
        name = st.text_input("Name")
        join_date = st.date_input("Joining Date")
        department = st.text_input("Department")
        status = st.selectbox("Status", ["Active", "Inactive"])
        if st.form_submit_button("Add Employee"):
            c.execute("INSERT INTO employees (name, join_date, department, status) VALUES (?, ?, ?, ?)",
                      (name, str(join_date), department, status))
            conn.commit()
            st.success("Employee added.")

# Interview Assessment
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
                c.execute("""
                    INSERT INTO interviews (candidate_id, date, interviewer, strengths, weaknesses, qualification, experience, comm_written, comm_oral, problem_solving, team_capabilities, comparison, final_remarks, decision)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (cid, str(date), interviewer, strengths, weaknesses, qualification, experience, comm_written, comm_oral, problem_solving, team_capabilities, comparison, final_remarks, decision))
                conn.commit()
                buffer = BytesIO()
                p = canvas.Canvas(buffer, pagesize=letter)
                y = 750
                for label, val in {
                    "Candidate": selected, "Date": date, "Interviewer": interviewer, "Strengths": strengths, "Weaknesses": weaknesses, "Qualification": qualification, "Experience": experience, "Comm. Written": comm_written, "Comm. Oral": comm_oral, "Problem Solving": problem_solving, "Team Capabilities": team_capabilities, "Comparison": comparison, "Remarks": final_remarks, "Decision": decision
                }.items():
                    p.drawString(100, y, f"{label}: {val}")
                    y -= 20
                p.showPage()
                p.save()
                buffer.seek(0)
                st.download_button("Download Interview PDF", data=buffer.getvalue(), file_name=f"{selected}_interview.pdf")

# Post Joining Uploads
elif menu == "Post-Joining Uploads":
    st.title("Upload Post-Joining Documents")
    doc = st.file_uploader("Upload File")
    if doc:
        os.makedirs("uploads", exist_ok=True)
        path = os.path.join("uploads", doc.name)
        with open(path, "wb") as f:
            f.write(doc.read())
        st.success(f"Saved to {path}")

# Attendance
elif menu == "Attendance & Leave Tracker":
    st.title("Attendance Tracking")
    with st.form("attendance_form"):
        emp = st.text_input("Employee")
        date = st.date_input("Date")
        present = st.checkbox("Present", value=True)
        leave = st.selectbox("Leave Type", ["None", "Sick Leave", "Casual Leave", "Earned Leave"])
        if st.form_submit_button("Save Attendance"):
            c.execute("INSERT INTO attendance (employee, date, present, leave_type) VALUES (?, ?, ?, ?)",
                      (emp, str(date), int(present), leave))
            conn.commit()
            st.success("Attendance saved.")

# Payroll
elif menu == "Payroll Data Preparation":
    st.title("Payroll Calculator")
    with st.form("payroll_form"):
        emp = st.text_input("Employee")
        month = st.text_input("Month")
        base = st.number_input("Base Salary", 0.0)
        pf = base * 0.12
        esic = base * 0.0325
        total = base - pf - esic
        st.write(f"PF: {pf:.2f} | ESIC: {esic:.2f} | Net Salary: {total:.2f}")
        if st.form_submit_button("Save Payroll"):
            c.execute("INSERT INTO payroll (employee, month, base_salary, pf, esic, total_salary) VALUES (?, ?, ?, ?, ?, ?)",
                      (emp, month, base, pf, esic, total))
            conn.commit()
            st.success("Payroll record saved.")

# Exit
elif menu == "Exit Management Tracker":
    st.title("Exit Tracker")
    with st.form("exit_form"):
        emp = st.text_input("Employee")
        exit_date = st.date_input("Exit Date")
        reason = st.text_area("Reason")
        if st.form_submit_button("Save Exit"):
            c.execute("INSERT INTO exits (employee, exit_date, reason) VALUES (?, ?, ?)",
                      (emp, str(exit_date), reason))
            conn.commit()
            st.success("Exit recorded.")

# Reports
elif menu == "Downloadable Reports":
    st.title("Reports")
    for table in ["payroll", "attendance", "exits"]:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        st.subheader(table.title())
        st.dataframe(df)

        # Save Excel data to a BytesIO object
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        excel_buffer.seek(0)

        # Use the buffer in the download button
        st.download_button(
            f"Download {table} (Excel)",
            data=excel_buffer,
            file_name=f"{table}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Assets / Travel
elif menu == "Admin Assets / Travel Requests":
    st.title("Assets / Travel")
    with st.form("asset_form"):
        emp = st.text_input("Employee")
        asset = st.text_input("Asset or Request")
        status = st.selectbox("Status", ["Assigned", "Returned", "In Process"])
        if st.form_submit_button("Save"):
            c.execute("INSERT INTO assets (employee, asset, status) VALUES (?, ?, ?)",
                      (emp, asset, status))
            conn.commit()
            st.success("Asset recorded.")

# Approvals
elif menu == "Approvals Workflow":
    st.title("Approvals")
    with st.form("approval_form"):
        req_type = st.selectbox("Request Type", ["Leave", "Travel", "Payroll Adjustment"])
        requested_by = st.text_input("Requested By")
        approved_by = st.text_input("Approved By")
        status = st.selectbox("Status", ["Pending", "Approved", "Rejected"])
        if st.form_submit_button("Submit Request"):
            c.execute("INSERT INTO approvals (request_type, requested_by, approved_by, status) VALUES (?, ?, ?, ?)",
                      (req_type, requested_by, approved_by, status))
            conn.commit()
            st.success("Approval submitted.")

conn.close()
