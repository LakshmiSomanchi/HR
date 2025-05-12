import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="TechnoServe HR Dashboard",
    page_icon="🧑‍💼",
    layout="wide",
)

# Sidebar Logo and Navigation
st.sidebar.image("TechnoServe_logo.png", use_container_width=True)
st.sidebar.title("TechnoServe HR Dashboard")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigate to:",
    [
        "📋 Candidate Tracker",
        "💼 Offer Tracker",
        "👨‍💼 Employee Masterfile",
        "📝 Interview Assessment",
        "📂 Post-Joining Uploads",
        "📊 Attendance & Leave Tracker",
        "💰 Payroll Data Preparation",
        "🚪 Exit Management Tracker",
        "📈 Downloadable Reports",
        "🛠️ Admin Assets / Travel Requests",
        "✅ Approvals Workflow",
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
    st.image("candidate_tracker.jpg", caption="Candidate Management", use_container_width=True)
    name = st.text_input("Candidate Name")
    designation = st.text_input("Designation")
    project = st.text_input("Project")
    location = st.text_input("Location")
    if st.button("Save Candidate"):
        st.success(f"Candidate '{name}' has been successfully saved!")

elif menu == "💼 Offer Tracker":
    # Offer Tracker Module
    st.title("💼 Offer Tracker")
    st.markdown("Manage job offers seamlessly.")
    st.image("offer_tracker.jpg", caption="Offer Management", use_container_width=True)
    candidate = st.text_input("Candidate Name")
    offer_date = st.date_input("Offer Date")
    offered_by = st.text_input("Offered By")
    status = st.selectbox("Status", ["Issued", "Accepted", "Declined"])
    if st.button("Record Offer"):
        st.success(f"Offer for '{candidate}' has been successfully recorded!")

elif menu == "👨‍💼 Employee Masterfile":
    # Employee Masterfile Module
    st.title("👨‍💼 Employee Masterfile")
    st.markdown("Maintain a comprehensive record of employees.")
    st.image("employee_masterfile.jpg", caption="Employee Records", use_container_width=True)
    name = st.text_input("Employee Name")
    join_date = st.date_input("Joining Date")
    department = st.text_input("Department")
    status = st.selectbox("Status", ["Active", "Inactive"])
    if st.button("Add Employee"):
        st.success(f"Employee '{name}' has been successfully added!")

elif menu == "📝 Interview Assessment":
    # Interview Assessment Module
    st.title("📝 Interview Assessment")
    st.markdown("Assess candidates based on their interviews.")
    st.image("interview_assessment.jpg", caption="Interview Evaluation", use_container_width=True)
    candidates = ["John Doe", "Jane Smith", "Mike Johnson"]  # Replace with dynamic data
    selected_candidate = st.selectbox("Select Candidate", candidates)
    date = st.date_input("Interview Date", datetime.today())
    interviewer = st.text_input("Interviewer")
    strengths = st.text_area("Strengths")
    weaknesses = st.text_area("Weaknesses")
    if st.button("Save Assessment"):
        st.success(f"Interview assessment for '{selected_candidate}' has been saved!")
elif menu == "📂 Post-Joining Uploads":
    # Post-Joining Uploads Module
    st.title("📂 Post-Joining Uploads")
    st.markdown("Upload important documents for new joiners.")
    st.image("post_joining_uploads.jpg", caption="Document Uploads", use_container_width=True)
    uploaded_file = st.file_uploader("Upload Document")
    if uploaded_file:
        st.success("Document uploaded successfully!")

elif menu == "📊 Attendance & Leave Tracker":
    # Attendance and Leave Tracker Module
    st.title("📊 Attendance & Leave Tracker")
    st.markdown("Track and manage employee attendance and leave requests.")
    st.image("attendance_tracker.jpg", caption="Attendance Management", use_container_width=True)
    employee = st.text_input("Employee Name")
    date = st.date_input("Date")
    present = st.checkbox("Present", value=True)
    leave_type = st.selectbox("Leave Type", ["None", "Sick Leave", "Casual Leave", "Earned Leave"])
    if st.button("Save Attendance"):
        st.success(f"Attendance for '{employee}' has been successfully recorded!")

elif menu == "💰 Payroll Data Preparation":
    # Payroll Data Preparation Module
    st.title("💰 Payroll Data Preparation")
    st.markdown("Prepare payroll data accurately.")
    st.image("payroll_tracker.jpg", caption="Payroll Management", use_container_width=True)
    employee = st.text_input("Employee Name")
    month = st.text_input("Month")
    base_salary = st.number_input("Base Salary", min_value=0.0, value=0.0)
    pf = base_salary * 0.12
    esic = base_salary * 0.0325
    total_salary = base_salary - (pf + esic)
    st.write(f"PF: {pf}, ESIC: {esic}, Net Salary: {total_salary}")
    if st.button("Save Payroll"):
        st.success(f"Payroll data for '{employee}' has been successfully saved!")

elif menu == "🚪 Exit Management Tracker":
    # Exit Management Tracker Module
    st.title("🚪 Exit Management Tracker")
    st.markdown("Track employee exits and their reasons.")
    st.image("exit_tracker.jpg", caption="Exit Management", use_container_width=True)
    employee = st.text_input("Employee Name")
    exit_date = st.date_input("Exit Date")
    reason = st.text_area("Reason for Exit")
    if st.button("Save Exit"):
        st.success(f"Exit for '{employee}' has been successfully recorded!")

elif menu == "📈 Downloadable Reports":
    # Downloadable Reports Module
    st.title("📈 Downloadable Reports")
    st.markdown("Generate and download reports.")
    st.image("reports.jpg", caption="Reports Dashboard", use_container_width=True)
    report_type = st.selectbox("Select Report", ["Attendance", "Payroll", "Exit"])
    if st.button("Download Report"):
        st.success(f"'{report_type}' report has been downloaded!")

elif menu == "🛠️ Admin Assets / Travel Requests":
    # Admin Assets Module
    st.title("🛠️ Admin Assets / Travel Requests")
    st.markdown("Manage assets and travel requests for employees.")
    st.image("admin_assets.jpg", caption="Asset Management", use_container_width=True)
    employee = st.text_input("Employee Name")
    asset_description = st.text_area("Asset/Request Description")
    if st.button("Save Request"):
        st.success(f"Request for '{employee}' has been successfully saved!")

elif menu == "✅ Approvals Workflow":
    # Approvals Workflow Module
    st.title("✅ Approvals Workflow")
    st.markdown("Manage approval requests.")
    st.image("approvals.jpg", caption="Approval Management", use_container_width=True)
    request_type = st.selectbox("Request Type", ["Leave", "Travel", "Payroll Adjustment"])
    requested_by = st.text_input("Requested By")
    approved_by = st.text_input("Approved By")
    status = st.selectbox("Approval Status", ["Pending", "Approved", "Rejected"])
    if st.button("Submit Request"):
        st.success(f"Approval request for '{request_type}' has been submitted!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 14px; color: grey;">
        Powered by TechnoServe | Enhancing HR Management
    </div>
    """,
    unsafe_allow_html=True,
)
