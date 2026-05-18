import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Health Accreditation & QI Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# Global styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .main {
            background-color: #F7FAFC;
        }

        h1, h2, h3 {
            color: #1F3A5F;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .kpi-card {
            background-color: #FFFFFF;
            padding: 18px;
            border-radius: 14px;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
            border-left: 6px solid #2A9D8F;
            min-height: 115px;
        }

        .kpi-label {
            font-size: 15px;
            color: #5F6B7A;
            margin-bottom: 6px;
        }

        .kpi-value {
            font-size: 30px;
            font-weight: 700;
            color: #1F3A5F;
        }

        .section-note {
            background-color: #EAF4F4;
            padding: 14px;
            border-radius: 10px;
            border-left: 5px solid #2A9D8F;
            color: #234;
            margin-bottom: 18px;
        }

        .small-caption {
            color: #667085;
            font-size: 14px;
        }

        div[data-testid="stMetricValue"] {
            color: #1F3A5F;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------
DATA_DIR = Path("data")


@st.cache_data
def load_data():
    patient_utilization = pd.read_csv(DATA_DIR / "patient_utilization.csv")
    behavioral_health = pd.read_csv(DATA_DIR / "behavioral_health.csv")
    satisfaction_scores = pd.read_csv(DATA_DIR / "satisfaction_scores.csv")
    referrals = pd.read_csv(DATA_DIR / "referrals.csv")
    insurance_utilization = pd.read_csv(DATA_DIR / "insurance_utilization.csv")
    aaahc_tracker = pd.read_csv(DATA_DIR / "aaahc_tracker.csv")
    policy_tracker = pd.read_csv(DATA_DIR / "policy_tracker.csv")
    qi_projects = pd.read_csv(DATA_DIR / "qi_projects.csv")

    patient_utilization["Month"] = pd.to_datetime(patient_utilization["Month"])
    behavioral_health["Month"] = pd.to_datetime(behavioral_health["Month"])
    satisfaction_scores["Month"] = pd.to_datetime(satisfaction_scores["Month"])
    referrals["Month"] = pd.to_datetime(referrals["Month"])
    insurance_utilization["Month"] = pd.to_datetime(insurance_utilization["Month"])

    return {
        "patient_utilization": patient_utilization,
        "behavioral_health": behavioral_health,
        "satisfaction_scores": satisfaction_scores,
        "referrals": referrals,
        "insurance_utilization": insurance_utilization,
        "aaahc_tracker": aaahc_tracker,
        "policy_tracker": policy_tracker,
        "qi_projects": qi_projects
    }


data = load_data()

patient_utilization = data["patient_utilization"]
behavioral_health = data["behavioral_health"]
satisfaction_scores = data["satisfaction_scores"]
referrals = data["referrals"]
insurance_utilization = data["insurance_utilization"]
aaahc_tracker = data["aaahc_tracker"]
policy_tracker = data["policy_tracker"]
qi_projects = data["qi_projects"]


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------
def kpi_card(label, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_note(text):
    st.markdown(
        f"""
        <div class="section-note">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


def status_color(status):
    status = str(status).lower()

    if "complete" in status or "ready" in status:
        return "✅"
    if "progress" in status or "review" in status:
        return "🟡"
    if "not started" in status or "gap" in status:
        return "🔴"

    return "⚪"


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.title("🏥 Health Dashboard")
st.sidebar.caption("Accreditation & Quality Improvement")

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview Dashboard",
        "Patient Utilization Trends",
        "Behavioral Health Metrics",
        "PHQ-9 Trend Tracking",
        "Patient Satisfaction Data",
        "Referral Patterns",
        "Insurance Utilization Trends",
        "Quality Improvement Tracker",
        "AAAHC Accreditation Readiness Tracker",
        "Policy Documentation Tracker"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Demo-safe project using synthetic healthcare operations data only. "
    "No real patient information is included."
)


# ---------------------------------------------------------
# KPI calculations
# ---------------------------------------------------------
total_visits = int(patient_utilization["Total Visits"].sum())
counseling_visits = int(patient_utilization["Counseling Visits"].sum())
medical_visits = int(patient_utilization["Medical Visits"].sum())
avg_satisfaction = round(satisfaction_scores["Average Satisfaction Score"].mean(), 2)

total_referrals = referrals["Total Referrals"].sum()
completed_referrals = referrals["Completed Referrals"].sum()
referral_completion_rate = round((completed_referrals / total_referrals) * 100, 1)

total_insurance_visits = insurance_utilization["Visits Using Insurance"].sum()
total_all_visits = insurance_utilization["Total Visits"].sum()
insurance_utilization_rate = round((total_insurance_visits / total_all_visits) * 100, 1)

ready_count = aaahc_tracker[aaahc_tracker["Current Status"] == "Ready"].shape[0]
aaahc_readiness_percentage = round((ready_count / len(aaahc_tracker)) * 100, 1)

policies_completed = policy_tracker[policy_tracker["Status"] == "Completed"].shape[0]
qi_projects_in_progress = qi_projects[qi_projects["Status"] == "In Progress"].shape[0]


# ---------------------------------------------------------
# Page: Overview
# ---------------------------------------------------------
if page == "Overview Dashboard":
    st.title("Health Accreditation & Quality Improvement Dashboard")
    st.caption("Mock dashboard for Retriever Integrated Health, UMBC")

    section_note(
        "This dashboard brings together operational, behavioral health, satisfaction, referral, "
        "insurance, quality improvement, accreditation, and policy documentation indicators in one place."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("Total Visits", f"{total_visits:,}")
    with col2:
        kpi_card("Counseling Visits", f"{counseling_visits:,}")
    with col3:
        kpi_card("Medical Visits", f"{medical_visits:,}")
    with col4:
        kpi_card("Avg. Satisfaction", f"{avg_satisfaction}/5")

    st.write("")

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        kpi_card("Referral Completion", f"{referral_completion_rate}%")
    with col6:
        kpi_card("Insurance Utilization", f"{insurance_utilization_rate}%")
    with col7:
        kpi_card("AAAHC Readiness", f"{aaahc_readiness_percentage}%")
    with col8:
        kpi_card("Policies Completed", policies_completed)

    st.write("")
    st.subheader("Monthly Visit Trends")

    visit_fig = px.line(
        patient_utilization,
        x="Month",
        y=["Medical Visits", "Counseling Visits", "Wellness Visits"],
        markers=True,
        title="Visits by Service Type"
    )
    visit_fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Visits",
        legend_title="Service Type",
        template="plotly_white"
    )
    st.plotly_chart(visit_fig, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("AAAHC Readiness by Status")
        status_counts = aaahc_tracker["Current Status"].value_counts().reset_index()
        status_counts.columns = ["Current Status", "Count"]

        fig = px.pie(
            status_counts,
            names="Current Status",
            values="Count",
            title="Accreditation Readiness Status"
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("QI Project Status")
        qi_counts = qi_projects["Status"].value_counts().reset_index()
        qi_counts.columns = ["Status", "Count"]

        fig = px.bar(
            qi_counts,
            x="Status",
            y="Count",
            title="Quality Improvement Project Status",
            text="Count"
        )
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Project Status",
            yaxis_title="Number of Projects"
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# Page: Patient Utilization Trends
# ---------------------------------------------------------
elif page == "Patient Utilization Trends":
    st.title("Patient Utilization Trends")
    section_note(
        "This section tracks service volume across medical, counseling, wellness, and after-hours support visits."
    )

    st.dataframe(patient_utilization, use_container_width=True)

    fig = px.line(
        patient_utilization,
        x="Month",
        y=["Medical Visits", "Counseling Visits", "Wellness Visits", "After Hours Calls"],
        markers=True,
        title="Monthly Patient Utilization"
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Volume",
        legend_title="Service Type"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        patient_utilization,
        x="Month",
        y="Total Visits",
        title="Total Monthly Visits",
        text="Total Visits"
    )
    fig2.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Total Visits"
    )
    st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------------
# Page: Behavioral Health Metrics
# ---------------------------------------------------------
elif page == "Behavioral Health Metrics":
    st.title("Behavioral Health Metrics")
    section_note(
        "This section summarizes counseling demand, intake appointments, crisis consultations, and no-show patterns."
    )

    st.dataframe(behavioral_health, use_container_width=True)

    fig = px.line(
        behavioral_health,
        x="Month",
        y=["Counseling Visits", "Initial Intakes", "Crisis Consultations", "No Shows"],
        markers=True,
        title="Behavioral Health Service Trends"
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Count",
        legend_title="Metric"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        behavioral_health,
        x="Month",
        y="No Show Rate",
        title="Monthly Behavioral Health No-Show Rate",
        text="No Show Rate"
    )
    fig2.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="No-Show Rate (%)"
    )
    st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------------
# Page: PHQ-9 Trend Tracking
# ---------------------------------------------------------
elif page == "PHQ-9 Trend Tracking":
    st.title("PHQ-9 Trend Tracking")
    section_note(
        "This demo tracks monthly average PHQ-9 screening scores and the share of students showing improvement. "
        "Scores are synthetic and used only for dashboard demonstration."
    )

    phq_df = behavioral_health[[
        "Month",
        "Average PHQ-9 Score",
        "Students Screened",
        "Students Improved"
    ]].copy()

    phq_df["Improvement Rate"] = round(
        (phq_df["Students Improved"] / phq_df["Students Screened"]) * 100,
        1
    )

    st.dataframe(phq_df, use_container_width=True)

    fig = px.line(
        phq_df,
        x="Month",
        y="Average PHQ-9 Score",
        markers=True,
        title="Average PHQ-9 Score Over Time"
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Average PHQ-9 Score"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        phq_df,
        x="Month",
        y="Improvement Rate",
        title="PHQ-9 Improvement Rate",
        text="Improvement Rate"
    )
    fig2.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Improvement Rate (%)"
    )
    st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------------
# Page: Patient Satisfaction
# ---------------------------------------------------------
elif page == "Patient Satisfaction Data":
    st.title("Patient Satisfaction Data")
    section_note(
        "This section tracks student feedback on access, communication, wait time, privacy, and overall experience."
    )

    st.dataframe(satisfaction_scores, use_container_width=True)

    fig = px.line(
        satisfaction_scores,
        x="Month",
        y=[
            "Average Satisfaction Score",
            "Access Score",
            "Communication Score",
            "Wait Time Score",
            "Privacy Score"
        ],
        markers=True,
        title="Patient Satisfaction Trends"
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Average Score out of 5",
        legend_title="Satisfaction Measure"
    )
    st.plotly_chart(fig, use_container_width=True)

    latest_month = satisfaction_scores.sort_values("Month").iloc[-1]

    st.subheader("Latest Month Snapshot")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Overall Satisfaction", f"{latest_month['Average Satisfaction Score']}/5")
    col2.metric("Access", f"{latest_month['Access Score']}/5")
    col3.metric("Communication", f"{latest_month['Communication Score']}/5")
    col4.metric("Privacy", f"{latest_month['Privacy Score']}/5")


# ---------------------------------------------------------
# Page: Referrals
# ---------------------------------------------------------
elif page == "Referral Patterns":
    st.title("Referral Patterns")
    section_note(
        "This section shows referral volume, completion, pending referrals, and common referral destinations."
    )

    referrals["Completion Rate"] = round(
        (referrals["Completed Referrals"] / referrals["Total Referrals"]) * 100,
        1
    )

    st.dataframe(referrals, use_container_width=True)

    fig = px.line(
        referrals,
        x="Month",
        y=["Total Referrals", "Completed Referrals", "Pending Referrals"],
        markers=True,
        title="Referral Volume and Completion"
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Number of Referrals",
        legend_title="Referral Metric"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        referrals,
        x="Most Common Referral Type",
        y="Total Referrals",
        color="Most Common Referral Type",
        title="Referral Volume by Most Common Referral Type",
        text="Total Referrals"
    )
    fig2.update_layout(
        template="plotly_white",
        xaxis_title="Referral Type",
        yaxis_title="Total Referrals",
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------------
# Page: Insurance Utilization
# ---------------------------------------------------------
elif page == "Insurance Utilization Trends":
    st.title("Insurance Utilization Trends")
    section_note(
        "This section tracks how often visits used insurance and how many visits were self-pay or no-charge."
    )

    insurance_utilization["Insurance Utilization Rate"] = round(
        (insurance_utilization["Visits Using Insurance"] / insurance_utilization["Total Visits"]) * 100,
        1
    )

    st.dataframe(insurance_utilization, use_container_width=True)

    fig = px.line(
        insurance_utilization,
        x="Month",
        y=["Visits Using Insurance", "Self Pay Visits", "No Charge Visits"],
        markers=True,
        title="Insurance and Payment Type Trends"
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Number of Visits",
        legend_title="Visit Type"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        insurance_utilization,
        x="Month",
        y="Insurance Utilization Rate",
        title="Insurance Utilization Rate by Month",
        text="Insurance Utilization Rate"
    )
    fig2.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Insurance Utilization Rate (%)"
    )
    st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------------
# Page: QI Projects
# ---------------------------------------------------------
elif page == "Quality Improvement Tracker":
    st.title("Quality Improvement Tracker")
    section_note(
        "This module supports documentation of quality improvement projects, including aim statements, metrics, targets, current progress, and next steps."
    )

    st.subheader("QI Project Portfolio")

    qi_display = qi_projects.copy()
    qi_display.insert(0, "Indicator", qi_display["Status"].apply(status_color))

    st.dataframe(qi_display, use_container_width=True)

    st.subheader("QI Project Progress")

    progress_df = qi_projects.copy()
    progress_df["Progress Toward Target"] = round(
        (progress_df["Current Value"] / progress_df["Target"]) * 100,
        1
    )

    fig = px.bar(
        progress_df,
        x="Project Name",
        y="Progress Toward Target",
        color="Status",
        title="Progress Toward Target by QI Project",
        text="Progress Toward Target"
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="QI Project",
        yaxis_title="Progress Toward Target (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Project Details")
    selected_project = st.selectbox(
        "Choose a project to review",
        qi_projects["Project Name"]
    )

    project = qi_projects[qi_projects["Project Name"] == selected_project].iloc[0]

    st.markdown(f"### {project['Project Name']}")
    st.write(f"**Aim Statement:** {project['Aim Statement']}")
    st.write(f"**Metric:** {project['Metric']}")
    st.write(f"**Baseline:** {project['Baseline']}")
    st.write(f"**Target:** {project['Target']}")
    st.write(f"**Current Value:** {project['Current Value']}")
    st.write(f"**Status:** {project['Status']}")
    st.write(f"**Next Step:** {project['Next Step']}")


# ---------------------------------------------------------
# Page: AAAHC Tracker
# ---------------------------------------------------------
elif page == "AAAHC Accreditation Readiness Tracker":
    st.title("AAAHC Accreditation Readiness Tracker")
    section_note(
        "This module organizes accreditation readiness work by standard area, evidence needed, current status, gap, priority, and responsible team."
    )

    st.subheader("Readiness Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("AAAHC Readiness", f"{aaahc_readiness_percentage}%")
    col2.metric("Ready Items", ready_count)
    col3.metric("Total Tracked Items", len(aaahc_tracker))

    tracker_display = aaahc_tracker.copy()
    tracker_display.insert(0, "Indicator", tracker_display["Current Status"].apply(status_color))

    st.subheader("Accreditation Readiness Details")
    st.dataframe(tracker_display, use_container_width=True)

    fig = px.bar(
        aaahc_tracker,
        x="Standard Area",
        color="Current Status",
        title="AAAHC Readiness by Standard Area",
        barmode="group"
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Standard Area",
        yaxis_title="Number of Requirements"
    )
    st.plotly_chart(fig, use_container_width=True)

    priority_counts = aaahc_tracker["Priority"].value_counts().reset_index()
    priority_counts.columns = ["Priority", "Count"]

    fig2 = px.pie(
        priority_counts,
        names="Priority",
        values="Count",
        title="Accreditation Gaps by Priority"
    )
    fig2.update_layout(template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------------
# Page: Policy Documentation Tracker
# ---------------------------------------------------------
elif page == "Policy Documentation Tracker":
    st.title("Policy Documentation Tracker")
    section_note(
        "This module uses a plain-language policy documentation format with purpose, scope, status, owner, last updated date, and version control."
    )

    completed = policy_tracker[policy_tracker["Status"] == "Completed"].shape[0]
    in_review = policy_tracker[policy_tracker["Status"] == "In Review"].shape[0]
    draft = policy_tracker[policy_tracker["Status"] == "Draft"].shape[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Policies", len(policy_tracker))
    col2.metric("Completed", completed)
    col3.metric("In Review", in_review)
    col4.metric("Draft", draft)

    policy_display = policy_tracker.copy()
    policy_display.insert(0, "Indicator", policy_display["Status"].apply(status_color))

    st.subheader("Policy Documentation Table")
    st.dataframe(policy_display, use_container_width=True)

    fig = px.bar(
        policy_tracker,
        x="AAAHC Standard Area",
        color="Status",
        title="Policy Status by AAAHC Standard Area",
        barmode="group"
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="AAAHC Standard Area",
        yaxis_title="Number of Policies"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Policy Detail View")
    selected_policy = st.selectbox(
        "Choose a policy to review",
        policy_tracker["Policy Name"]
    )

    policy = policy_tracker[policy_tracker["Policy Name"] == selected_policy].iloc[0]

    st.markdown(f"### {policy['Policy Name']}")
    st.write(f"**AAAHC Standard Area:** {policy['AAAHC Standard Area']}")
    st.write(f"**Purpose:** {policy['Purpose']}")
    st.write(f"**Scope:** {policy['Scope']}")
    st.write(f"**Status:** {policy['Status']}")
    st.write(f"**Owner:** {policy['Owner']}")
    st.write(f"**Last Updated:** {policy['Last Updated']}")
    st.write(f"**Version:** {policy['Version']}")


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.caption(
    "Health Accreditation & Quality Improvement Dashboard | Built with Streamlit, Pandas, and Plotly | "
    "Synthetic demo data only"
)