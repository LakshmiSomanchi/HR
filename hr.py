#Streamlit HR System (hr.py)

import streamlit as st
import sqlite3
import datetime
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

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

def init_db():
    with sqlite3.connect(DB) as conn:
        for ddl in TABLES.values():
            conn.execute(ddl)

init_db()

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
    "Interview Assessment", "Post-Joining Uploads",
    "Attendance & Leave Tracker", "Payroll Data Preparation",
    "Exit Management Tracker", "Downloadable Reports",
    "Admin Assets / Travel Requests", "Approvals Workflow"])

# Reuse connection
conn = sqlite3.connect(DB)
c = conn.cursor()

if menu == "Attendance & Leave Tracker":
    st.title("Attendance Tracking")
    with st.form("attendance_form"):
        emp = st.text_input("Employee Name")
        date = st.date_input("Date")
        present = st.checkbox("Present", value=True)
        leave_type = st.selectbox("Leave Type", ["None", "Sick Leave", "Casual Leave", "Earned Leave"])
        if st.form_submit_button("Mark Attendance"):
            c.execute("INSERT INTO attendance (employee, date, present, leave_type) VALUES (?, ?, ?, ?)",
                      (emp, str(date), int(present), leave_type))
            conn.commit()
            st.success("Attendance saved.")

elif menu == "Payroll Data Preparation":
    st.title("Payroll Calculator")
    with st.form("payroll_form"):
        emp = st.text_input("Employee")
        month = st.text_input("Month")
        base = st.number_input("Base Salary", 0.0)
        pf = base * 0.12
        esic = base * 0.0325
        total = base - (pf + esic)
        st.write(f"PF: {pf:.2f} | ESIC: {esic:.2f} | Net: {total:.2f}")
        if st.form_submit_button("Save Payroll"):
            c.execute("INSERT INTO payroll (employee, month, base_salary, pf, esic, total_salary) VALUES (?, ?, ?, ?, ?, ?)",
                      (emp, month, base, pf, esic, total))
            conn.commit()
            st.success("Payroll record saved.")

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

elif menu == "Downloadable Reports":
    st.title("Download Reports")
    for table in ["payroll", "attendance", "exits"]:
        st.markdown(f"#### {table.capitalize()} Report")
        rows = c.execute(f"SELECT * FROM {table}").fetchall()
        if rows:
            st.dataframe(rows)

elif menu == "Admin Assets / Travel Requests":
    st.title("Assets / Travel")
    with st.form("asset_form"):
        emp = st.text_input("Employee")
        asset = st.text_input("Asset/Request")
        status = st.selectbox("Status", ["Assigned", "Returned", "In Process"])
        if st.form_submit_button("Save"):
            c.execute("INSERT INTO assets (employee, asset, status) VALUES (?, ?, ?)", (emp, asset, status))
            conn.commit()
            st.success("Saved.")

elif menu == "Approvals Workflow":
    st.title("Approvals")
    with st.form("approval_form"):
        req_type = st.selectbox("Request Type", ["Leave", "Travel", "Payroll Adjustment"])
        requested_by = st.text_input("Requested By")
        approved_by = st.text_input("Approver")
        status = st.selectbox("Status", ["Pending", "Approved", "Rejected"])
        if st.form_submit_button("Submit Request"):
            c.execute("INSERT INTO approvals (request_type, requested_by, approved_by, status) VALUES (?, ?, ?, ?)",
                      (req_type, requested_by, approved_by, status))
            conn.commit()
            st.success("Approval logged.")

conn.close()

