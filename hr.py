import streamlit as st
import sqlite3
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="TechnoServe HR Dashboard",
    page_icon="🧑‍💼",
    layout="wide",
)

# Initialize SQLite connection
conn = sqlite3.connect("hr_management.db")
cursor = conn.cursor()

# Create tables if they don't already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    designation TEXT,
    project TEXT,
    location TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    date TEXT,
    interviewer TEXT,
    strengths TEXT,
    weaknesses TEXT,
    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
)
""")

conn.commit()

# Sidebar Logo and Navigation
st.sidebar.image("TechnoServe_logo.png", use_container_width=True)
st.sidebar.title("TechnoServe HR Dashboard")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigate to:",
    [
        "📋 Candidate Tracker",
        "📝 Interview Assessment",
    ]
)

# Header with logo and welcome text
st.image("technoserve_logo.png", use_container_width=True)
st.title("Welcome to the TechnoServe HR Dashboard")
st.markdown(
    """
    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center;">
        <h3 style="color: #4b8bbe; margin-top: 0;">Streamlining HR Operations for Maximum Efficiency</h3>
        <p style="font-size: 16px; color: #555;">Empowering your organization with tools to manage candidates, employees, attendance, payroll, and more.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

if menu == "📋 Candidate Tracker":
    # Candidate Tracker Module
    st.title("📋 Candidate Tracker")
    st.markdown("Easily track and manage candidates in your recruitment pipeline.")

    # Add Candidate Form
    name = st.text_input("Candidate Name")
    designation = st.text_input("Designation")
    project = st.text_input("Project")
    location = st.text_input("Location")

    if st.button("Save Candidate"):
        cursor.execute(
            """
            INSERT INTO candidates (name, designation, project, location)
            VALUES (?, ?, ?, ?)
            """,
            (name, designation, project, location),
        )
        conn.commit()
        st.success(f"Candidate '{name}' has been successfully saved!")

    # Display Candidates
    st.markdown("### List of Candidates")
    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()
    for candidate in candidates:
        st.write(f"ID: {candidate[0]}, Name: {candidate[1]}, Designation: {candidate[2]}, Project: {candidate[3]}, Location: {candidate[4]}")

elif menu == "📝 Interview Assessment":
    # Interview Assessment Module
    st.title("📝 Interview Assessment")
    st.markdown("Assess candidates based on their interviews.")

    # Fetch Candidates for Selectbox
    cursor.execute("SELECT id, name FROM candidates")
    candidates = cursor.fetchall()
    if candidates:
        candidate_dict = {name: id for id, name in candidates}
        selected_candidate_name = st.selectbox("Select Candidate", list(candidate_dict.keys()))
        selected_candidate_id = candidate_dict[selected_candidate_name]

        # Interview Form
        date = st.date_input("Interview Date", datetime.today())
        interviewer = st.text_input("Interviewer Name")
        strengths = st.text_area("Strengths")
        weaknesses = st.text_area("Weaknesses")

        if st.button("Save Assessment"):
            cursor.execute(
                """
                INSERT INTO interviews (candidate_id, date, interviewer, strengths, weaknesses)
                VALUES (?, ?, ?, ?, ?)
                """,
                (selected_candidate_id, date, interviewer, strengths, weaknesses),
            )
            conn.commit()
            st.success(f"Interview assessment for '{selected_candidate_name}' has been saved!")
    else:
        st.warning("No candidates available. Please add candidates in the Candidate Tracker first.")
