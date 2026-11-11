"""
Nexus AI: Operations & Risk Suite
Clean, Guided 3-Step Interface:
1. Operational Request Triage (Assignment 2)
2. Financial AML Risk Aggregator (Assignment 1)
"""

import json
import os
import streamlit as st
import pandas as pd

from workflow_engine import (
    WorkflowRemediationEngine,
    get_audit_records
)
from risk_engine import (
    FinancialRiskAggregator
)

# Page Setup
st.set_page_config(
    page_title="Nexus AI | Operations & Risk Platform",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Minimal, clean, calm styling (Anti-vibe-coded: disciplined colors, no sensory overload, clear hierarchy)
CUSTOM_CSS = """
<style>
    /* Max width centered container to prevent eye strain / clutter */
    .block-container {
        max-width: 860px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Clean Card Container */
    .nexus-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 22px 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 6px;
    }
    .card-sub {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 16px;
    }

    /* Result Banner */
    .result-banner-critical {
        background-color: #fef2f2;
        border-left: 5px solid #dc2626;
        padding: 16px 20px;
        border-radius: 6px;
        margin-bottom: 18px;
    }
    .result-banner-high {
        background-color: #fffbeb;
        border-left: 5px solid #d97706;
        padding: 16px 20px;
        border-radius: 6px;
        margin-bottom: 18px;
    }
    .result-banner-normal {
        background-color: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 16px 20px;
        border-radius: 6px;
        margin-bottom: 18px;
    }
    .banner-heading {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
    }
    .banner-detail {
        font-size: 0.9rem;
        color: #334155;
        margin-top: 4px;
    }

    /* Clean Step Checklist */
    .step-item {
        display: flex;
        align-items: flex-start;
        padding: 10px 0;
        border-bottom: 1px solid #f1f5f9;
    }
    .step-item:last-child {
        border-bottom: none;
    }
    .step-badge {
        background: #0f172a;
        color: #ffffff;
        font-size: 0.75rem;
        font-weight: 700;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 14px;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .step-name {
        font-size: 0.92rem;
        font-weight: 600;
        color: #1e293b;
    }
    .step-desc {
        font-size: 0.84rem;
        color: #475569;
        margin-top: 2px;
    }

    /* Email Preview Box */
    .email-box {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 16px 20px;
        font-family: inherit;
        font-size: 0.88rem;
        color: #1e293b;
        white-space: pre-wrap;
        line-height: 1.5;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def load_sample_requests():
    path = os.path.join(os.path.dirname(__file__), "sample_requests.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# Top Title
st.title("Nexus Operations & Risk Platform")
st.caption("Select an assignment module below to test its autonomous decisioning in 3 simple steps.")

# Simple tab switcher
active_tab = st.radio(
    "Choose Module:",
    options=[
        "1. Customer Request Processing Workflow",
        "2. Financial Risk Signal Aggregator"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()


# ==============================================================================
# TAB 1: CUSTOMER REQUEST WORKFLOW (ASSIGNMENT 2)
# ==============================================================================
if "Customer" in active_tab:
    sample_requests = load_sample_requests()

    st.subheader("Step 1: Pick a Customer Request")
    st.caption("Click any preset scenario to load a realistic inbound message:")

    col1, col2, col3 = st.columns(3)
    preset_choice = None

    if sample_requests:
        with col1:
            if st.button("💳 Billing Dispute", width="stretch"):
                preset_choice = sample_requests[0]
        with col2:
            if st.button("🚨 System Outage", width="stretch"):
                preset_choice = sample_requests[1]
        with col3:
            if st.button("❓ General Inquiry", width="stretch"):
                preset_choice = sample_requests[2]

    if preset_choice:
        st.session_state["req_text"] = preset_choice["text"]
        st.session_state["req_sender"] = preset_choice["sender"]

    current_text = st.session_state.get(
        "req_text",
        "URGENT: I was double-charged on invoice INV-88942 for our subscription. The amount of $4,950.00 was debited twice this morning. Please reverse immediately!"
    )
    current_sender = st.session_state.get("req_sender", "elena.rostova@acmefinance.com")

    with st.expander("Review / Edit Incoming Message Details", expanded=False):
        current_sender = st.text_input("Sender Email:", value=current_sender)
        current_text = st.text_area("Message Body:", value=current_text, height=100)

    st.markdown(
        f'<div class="email-box"><strong>From:</strong> {current_sender}<br><br>{current_text}</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.subheader("Step 2: Run Automated Triage")
    run_btn = st.button("Process & Execute Workflow", type="primary", width="stretch")

    # Run analysis
    result = WorkflowRemediationEngine.execute(current_text, sender=current_sender)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.subheader("Step 3: What the System Did")

    # Banner Class
    if result.classification.urgency == "Critical":
        banner_class = "result-banner-critical"
    elif result.classification.urgency == "High":
        banner_class = "result-banner-high"
    else:
        banner_class = "result-banner-normal"

    st.markdown(f"""
    <div class="{banner_class}">
        <div class="banner-heading">{result.classification.category} ({result.classification.urgency} Urgency)</div>
        <div class="banner-detail">
            Assigned to: <strong>{result.assigned_queue}</strong> | 
            Resolution SLA: <strong>{result.sla_hours} Hours</strong> | 
            Ticket ID: <code>{result.request_id}</code>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Actions Checklist
    st.markdown("**Automated Actions Executed:**")
    for step in result.steps_executed:
        st.markdown(f"""
        <div class="step-item">
            <div class="step-badge">{step.step_number}</div>
            <div>
                <div class="step-name">{step.action_name}</div>
                <div class="step-desc">{step.description}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Generated response
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown("**AI-Drafted Reply (Ready to Send):**")
    st.markdown(f'<div class="email-box">{result.draft_response}</div>', unsafe_allow_html=True)

    # Tucked away audit trail
    with st.expander("View Past Processed Tickets (Audit Trail)"):
        records = get_audit_records(limit=10)
        if records:
            df = pd.DataFrame(records)[["timestamp", "request_id", "category", "urgency", "assigned_queue", "sla_hours"]]
            st.dataframe(df, width="stretch")


# ==============================================================================
# TAB 2: FINANCIAL RISK AGGREGATOR (ASSIGNMENT 1)
# ==============================================================================
else:
    st.subheader("Step 1: Pick a Client Account Case")
    st.caption("Select a scenario to evaluate its transaction patterns:")

    c_col1, c_col2 = st.columns(2)
    load_high = False
    load_clean = False

    with c_col1:
        if st.button("🚨 Suspicious Offshore Account (High Risk)", width="stretch"):
            load_high = True
    with c_col2:
        if st.button("✅ Normal Everyday Account (Low Risk)", width="stretch"):
            load_clean = True

    default_csv = (
        "tx_id,amount,currency,source_country,destination_country,tx_type\n"
        "TX-9901,9450.00,USD,USA,Cayman Islands,WIRE_OUT\n"
        "TX-9902,9800.00,USD,USA,Panama,WIRE_OUT\n"
        "TX-9903,9200.00,USD,USA,Cayman Islands,WIRE_OUT\n"
        "TX-9904,9650.00,USD,USA,Panama,WIRE_OUT\n"
        "TX-9905,125000.00,USD,USA,Switzerland,WIRE_OUT"
    )

    if load_clean:
        default_csv = (
            "tx_id,amount,currency,source_country,destination_country,tx_type\n"
            "TX-1001,120.50,USD,USA,USA,ACH_PAYMENT\n"
            "TX-1002,84.20,USD,USA,USA,CARD_PURCHASE\n"
            "TX-1003,1450.00,USD,USA,USA,PAYROLL_DEPOSIT\n"
            "TX-1004,65.00,USD,USA,USA,CARD_PURCHASE"
        )
        st.session_state["f_acc"] = "ACC-1001"
        st.session_state["f_name"] = "Johnathan Mercer"
        st.session_state["f_pep"] = False
        st.session_state["f_tenure"] = 36
        st.session_state["f_csv"] = default_csv
    elif load_high:
        st.session_state["f_acc"] = "ACC-9041"
        st.session_state["f_name"] = "Vanguard Maritime Trade Ltd"
        st.session_state["f_pep"] = True
        st.session_state["f_tenure"] = 1
        st.session_state["f_csv"] = default_csv

    acc_id = st.session_state.get("f_acc", "ACC-9041")
    acc_name = st.session_state.get("f_name", "Vanguard Maritime Trade Ltd")
    is_pep = st.session_state.get("f_pep", True)
    tenure = st.session_state.get("f_tenure", 1)
    csv_text = st.session_state.get("f_csv", default_csv)

    with st.expander("Review / Edit Account & Transaction Records", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            acc_id = st.text_input("Account ID:", value=acc_id)
            acc_name = st.text_input("Client Name:", value=acc_name)
        with c2:
            is_pep = st.checkbox("Politically Exposed Person (PEP)", value=is_pep)
            tenure = st.number_input("Account Age (Months):", value=tenure, min_value=1)
        csv_text = st.text_area("Transactions (CSV):", value=csv_text, height=120)

    st.markdown(f"""
    <div class="email-box">
        <strong>Account:</strong> {acc_name} (<code>{acc_id}</code>)<br>
        <strong>Profile:</strong> Account Age: {tenure} month(s) | PEP Flag: {'Yes (High-Risk Person)' if is_pep else 'No'}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.subheader("Step 2: Run Risk Detection")
    run_risk_btn = st.button("Evaluate Account Risk", type="primary", width="stretch")

    # Parse and compute
    txs = FinancialRiskAggregator.parse_csv_transactions(csv_text)
    account_meta = {
        "account_id": acc_id,
        "customer_name": acc_name,
        "jurisdiction": "Offshore",
        "pep_status": is_pep,
        "account_tenure_months": tenure
    }
    profile = FinancialRiskAggregator.analyze_dataset(txs, account_meta)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.subheader("Step 3: Risk Assessment Results")

    # Score Banner
    if profile.risk_score >= 70:
        b_class = "result-banner-critical"
    elif profile.risk_score >= 45:
        b_class = "result-banner-high"
    else:
        b_class = "result-banner-normal"

    st.markdown(f"""
    <div class="{b_class}">
        <div class="banner-heading">Risk Score: {profile.risk_score} / 100 ({profile.risk_level} Priority)</div>
        <div class="banner-detail">
            Total Volume Analyzed: <strong>${profile.total_volume_usd:,.2f}</strong> across <strong>{profile.total_transactions_analyzed} transactions</strong><br>
            <strong>Recommended Action:</strong> {profile.recommended_action}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Narrative Rationale
    st.markdown("**Compliance Analyst Rationale:**")
    st.info(profile.ai_narrative_summary)

    # Red Flags Found
    if profile.flagged_signals:
        st.markdown("**Specific Red Flags Identified:**")
        for sig in profile.flagged_signals:
            st.markdown(f"""
            <div class="step-item">
                <div class="step-badge" style="background: #dc2626;">!</div>
                <div>
                    <div class="step-name">{sig.rule_name} (+{sig.score_contribution} pts)</div>
                    <div class="step-desc">{sig.description}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No anomalies or red flags detected in this account.")

    # Ingested transactions tucked in an expander
    with st.expander("View Raw Bank Statement Records"):
        st.dataframe(pd.DataFrame(txs), width="stretch")
