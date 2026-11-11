"""
Nexus AI: Operations & Risk Suite
Clean, Guided 3-Step Interface (Dark & Light Theme Adaptive)
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

# High-contrast CSS guaranteed to be readable on dark & light modes
CUSTOM_CSS = """
<style>
    .block-container {
        max-width: 860px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Universal High-Contrast Dark Card Surface */
    .card-surface {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 18px 20px;
        margin-bottom: 16px;
        color: #f8fafc;
    }
    
    /* Message Preview Box */
    .msg-preview {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 16px 18px;
        color: #f1f5f9;
        font-size: 0.92rem;
        line-height: 1.5;
        margin-top: 10px;
        margin-bottom: 14px;
        white-space: pre-wrap;
    }
    .msg-header {
        font-size: 0.82rem;
        font-weight: 700;
        color: #38bdf8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }

    /* Result Banner */
    .banner-critical {
        background: #450a0a;
        border: 1px solid #991b1b;
        border-left: 6px solid #ef4444;
        border-radius: 6px;
        padding: 16px 20px;
        color: #fef2f2;
        margin-bottom: 16px;
    }
    .banner-high {
        background: #451a03;
        border: 1px solid #92400e;
        border-left: 6px solid #f59e0b;
        border-radius: 6px;
        padding: 16px 20px;
        color: #fffbeb;
        margin-bottom: 16px;
    }
    .banner-normal {
        background: #064e3b;
        border: 1px solid #065f46;
        border-left: 6px solid #10b981;
        border-radius: 6px;
        padding: 16px 20px;
        color: #ecfdf5;
        margin-bottom: 16px;
    }
    .banner-title {
        font-size: 1.15rem;
        font-weight: 700;
    }
    .banner-sub {
        font-size: 0.9rem;
        margin-top: 4px;
        opacity: 0.95;
    }

    /* Step Item with Bright Text */
    .action-step {
        display: flex;
        align-items: flex-start;
        padding: 12px 14px;
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .step-circle {
        width: 26px;
        height: 26px;
        background: #38bdf8;
        color: #0f172a;
        font-size: 0.82rem;
        font-weight: 800;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 14px;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .step-circle-red {
        width: 26px;
        height: 26px;
        background: #ef4444;
        color: #ffffff;
        font-size: 0.85rem;
        font-weight: 800;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 14px;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .step-header-text {
        font-size: 0.95rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .step-detail-text {
        font-size: 0.88rem;
        color: #cbd5e1;
        margin-top: 3px;
        line-height: 1.4;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def load_category_scenarios():
    path = os.path.join(os.path.dirname(__file__), "sample_requests.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# Top Header
st.title("Nexus Operations & Risk Platform")
st.caption("Select an assignment module below to test its autonomous decisioning in 3 simple steps.")

# Module Selector
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
    scenario_groups = load_category_scenarios()

    st.subheader("Step 1: Pick a Request Category & Scenario")
    st.caption("Click any category below. Clicking multiple times will cycle through realistic sample questions:")

    col1, col2, col3 = st.columns(3)

    # Initialize cycling counters in session_state
    if "billing_idx" not in st.session_state:
        st.session_state["billing_idx"] = 0
    if "tech_idx" not in st.session_state:
        st.session_state["tech_idx"] = 0
    if "gen_idx" not in st.session_state:
        st.session_state["gen_idx"] = 0

    chosen_category = None
    chosen_scenario = None

    b_total = len(scenario_groups[0]["scenarios"]) if scenario_groups else 10
    t_total = len(scenario_groups[1]["scenarios"]) if len(scenario_groups) > 1 else 10
    g_total = len(scenario_groups[2]["scenarios"]) if len(scenario_groups) > 2 else 10

    with col1:
        if st.button("Billing Dispute", width="stretch"):
            if scenario_groups:
                b_list = scenario_groups[0]["scenarios"]
                st.session_state["billing_idx"] = (st.session_state["billing_idx"] + 1) % len(b_list)
                chosen_scenario = b_list[st.session_state["billing_idx"]]
                st.session_state["active_req"] = chosen_scenario
                st.session_state["workflow_executed"] = False
                st.rerun()

    with col2:
        if st.button("System Outage", width="stretch"):
            if len(scenario_groups) > 1:
                t_list = scenario_groups[1]["scenarios"]
                st.session_state["tech_idx"] = (st.session_state["tech_idx"] + 1) % len(t_list)
                chosen_scenario = t_list[st.session_state["tech_idx"]]
                st.session_state["active_req"] = chosen_scenario
                st.session_state["workflow_executed"] = False
                st.rerun()

    with col3:
        if st.button("General Inquiry", width="stretch"):
            if len(scenario_groups) > 2:
                g_list = scenario_groups[2]["scenarios"]
                st.session_state["gen_idx"] = (st.session_state["gen_idx"] + 1) % len(g_list)
                chosen_scenario = g_list[st.session_state["gen_idx"]]
                st.session_state["active_req"] = chosen_scenario
                st.session_state["workflow_executed"] = False
                st.rerun()

    # Default request on first load
    if "active_req" not in st.session_state:
        if scenario_groups:
            st.session_state["active_req"] = scenario_groups[0]["scenarios"][0]
        else:
            st.session_state["active_req"] = {
                "title": "Duplicate Corporate Charge ($4,950)",
                "sender": "elena.rostova@acmefinance.com",
                "text": "URGENT: I was double-charged on invoice INV-88942 for our subscription. Please reverse immediately!"
            }

    active_req = st.session_state["active_req"]

    # Preview card
    st.markdown(f"""
    <div class="msg-preview">
        <div class="msg-header">Selected Scenario: {active_req.get('title', 'Customer Inquiry')}</div>
        <strong>From:</strong> {active_req.get('sender', 'user@corp.com')}<br><br>
        {active_req.get('text', '')}
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Optional: Manually Edit Message Text Before Processing"):
        custom_sender = st.text_input("Sender Email:", value=active_req.get("sender", ""))
        custom_text = st.text_area("Message Content:", value=active_req.get("text", ""), height=100)
        if st.button("Update Custom Text"):
            st.session_state["active_req"] = {"title": "Custom Modified Ticket", "sender": custom_sender, "text": custom_text}
            st.session_state["workflow_executed"] = False
            st.rerun()

    # Step 2: Action Button
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.subheader("Step 2: Run Automated Triage")
    
    if st.button("Process & Execute Workflow", type="primary", width="stretch"):
        with st.spinner("Analyzing intent, classifying urgency, and dispatching remediation branch..."):
            result = WorkflowRemediationEngine.execute(
                active_req["text"],
                sender=active_req.get("sender", "customer@enterprise.com")
            )
            st.session_state["last_result"] = result
            st.session_state["workflow_executed"] = True

    # Step 3: Results display
    if st.session_state.get("workflow_executed", False) and "last_result" in st.session_state:
        result = st.session_state["last_result"]

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.subheader("Step 3: What the System Did")

        if result.classification.urgency == "Critical":
            b_class = "banner-critical"
        elif result.classification.urgency == "High":
            b_class = "banner-high"
        else:
            b_class = "banner-normal"

        st.markdown(f"""
        <div class="{b_class}">
            <div class="banner-title">Category: {result.classification.category} ({result.classification.urgency} Urgency)</div>
            <div class="banner-sub">
                Assigned Team: <strong>{result.assigned_queue}</strong> &bull; 
                Resolution Window: <strong>{result.sla_hours} Hours</strong> &bull; 
                Case ID: <code>{result.request_id}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Automated Remediation Steps Executed:**")
        for step in result.steps_executed:
            st.markdown(f"""
            <div class="action-step">
                <div class="step-circle">{step.step_number}</div>
                <div>
                    <div class="step-header-text">{step.action_name}</div>
                    <div class="step-detail-text">{step.description}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown("**AI-Generated Response (Drafted & Ready to Dispatch):**")
        st.markdown(f'<div class="msg-preview">{result.draft_response}</div>', unsafe_allow_html=True)

        with st.expander("View Past Processed Tickets (Audit Trail)"):
            records = get_audit_records(limit=10)
            if records:
                df = pd.DataFrame(records)[["timestamp", "request_id", "category", "urgency", "assigned_queue", "sla_hours"]]
                st.dataframe(df, width="stretch")
    else:
        st.info("Click the **'Process & Execute Workflow'** button above to run the triage engine on the selected scenario.")


# ==============================================================================
# TAB 2: FINANCIAL RISK AGGREGATOR (ASSIGNMENT 1)
# ==============================================================================
else:
    st.subheader("Step 1: Pick a Client Account Case")
    st.caption("Select a scenario to evaluate its transaction patterns:")

    c_col1, c_col2 = st.columns(2)

    high_risk_csv = (
        "tx_id,amount,currency,source_country,destination_country,tx_type\n"
        "TX-9901,9450.00,USD,USA,Cayman Islands,WIRE_OUT\n"
        "TX-9902,9800.00,USD,USA,Panama,WIRE_OUT\n"
        "TX-9903,9200.00,USD,USA,Cayman Islands,WIRE_OUT\n"
        "TX-9904,9650.00,USD,USA,Panama,WIRE_OUT\n"
        "TX-9905,125000.00,USD,USA,Switzerland,WIRE_OUT"
    )

    clean_csv = (
        "tx_id,amount,currency,source_country,destination_country,tx_type\n"
        "TX-1001,120.50,USD,USA,USA,ACH_PAYMENT\n"
        "TX-1002,84.20,USD,USA,USA,CARD_PURCHASE\n"
        "TX-1003,1450.00,USD,USA,USA,PAYROLL_DEPOSIT\n"
        "TX-1004,65.00,USD,USA,USA,CARD_PURCHASE"
    )

    pep_csv = (
        "tx_id,amount,currency,source_country,destination_country,tx_type\n"
        "TX-701,48000.00,USD,USA,Cyprus,WIRE_OUT\n"
        "TX-702,65000.00,USD,USA,Seychelles,WIRE_OUT\n"
        "TX-703,9800.00,USD,USA,Panama,WIRE_OUT"
    )

    velocity_csv = (
        "tx_id,amount,currency,source_country,destination_country,tx_type\n"
        "TX-801,25000.00,USD,USA,USA,WIRE_IN\n"
        "TX-802,32000.00,USD,USA,USA,WIRE_OUT\n"
        "TX-803,12000.00,USD,USA,USA,CARD_PAYMENT"
    )

    structuring_csv = (
        "tx_id,amount,currency,source_country,destination_country,tx_type\n"
        "TX-501,9900.00,USD,USA,USA,WIRE_OUT\n"
        "TX-502,9850.00,USD,USA,USA,WIRE_OUT\n"
        "TX-503,9750.00,USD,USA,USA,WIRE_OUT\n"
        "TX-504,9920.00,USD,USA,USA,WIRE_OUT"
    )

    corporate_csv = (
        "tx_id,amount,currency,source_country,destination_country,tx_type\n"
        "TX-301,42500.00,USD,USA,USA,PAYROLL_OUT\n"
        "TX-302,15400.00,USD,USA,Germany,VENDOR_PAYMENT\n"
        "TX-303,8900.00,USD,USA,UK,VENDOR_PAYMENT\n"
        "TX-304,62000.00,USD,USA,USA,CLIENT_DEPOSIT"
    )

    with c_col1:
        if st.button("Offshore Structuring & Sanctions (Critical)", width="stretch"):
            st.session_state["f_acc"] = "ACC-9041"
            st.session_state["f_name"] = "Vanguard Maritime Trade Ltd"
            st.session_state["f_pep"] = True
            st.session_state["f_tenure"] = 1
            st.session_state["f_csv"] = high_risk_csv
            st.session_state["risk_evaluated"] = False
            st.rerun()

        if st.button("PEP Foreign Official Entity (High Risk)", width="stretch"):
            st.session_state["f_acc"] = "ACC-4109"
            st.session_state["f_name"] = "Eurasia Capital Partners LLC"
            st.session_state["f_pep"] = True
            st.session_state["f_tenure"] = 8
            st.session_state["f_csv"] = pep_csv
            st.session_state["risk_evaluated"] = False
            st.rerun()

        if st.button("Cash Smurfing Just Below $10K (High Risk)", width="stretch"):
            st.session_state["f_acc"] = "ACC-5521"
            st.session_state["f_name"] = "Metro Cash Distribution LLC"
            st.session_state["f_pep"] = False
            st.session_state["f_tenure"] = 5
            st.session_state["f_csv"] = structuring_csv
            st.session_state["risk_evaluated"] = False
            st.rerun()

    with c_col2:
        if st.button("Clean Everyday Account (Low Risk)", width="stretch"):
            st.session_state["f_acc"] = "ACC-1001"
            st.session_state["f_name"] = "Johnathan Mercer"
            st.session_state["f_pep"] = False
            st.session_state["f_tenure"] = 36
            st.session_state["f_csv"] = clean_csv
            st.session_state["risk_evaluated"] = False
            st.rerun()

        if st.button("New Account Velocity Spike (Medium Risk)", width="stretch"):
            st.session_state["f_acc"] = "ACC-8812"
            st.session_state["f_name"] = "Rapid Logistics Express"
            st.session_state["f_pep"] = False
            st.session_state["f_tenure"] = 1
            st.session_state["f_csv"] = velocity_csv
            st.session_state["risk_evaluated"] = False
            st.rerun()

        if st.button("Established Corporate Vendor Operations (Low Risk)", width="stretch"):
            st.session_state["f_acc"] = "ACC-3302"
            st.session_state["f_name"] = "Midwest Manufacturing Corp"
            st.session_state["f_pep"] = False
            st.session_state["f_tenure"] = 48
            st.session_state["f_csv"] = corporate_csv
            st.session_state["risk_evaluated"] = False
            st.rerun()

    acc_id = st.session_state.get("f_acc", "ACC-9041")
    acc_name = st.session_state.get("f_name", "Vanguard Maritime Trade Ltd")
    is_pep = st.session_state.get("f_pep", True)
    tenure = st.session_state.get("f_tenure", 1)
    csv_text = st.session_state.get("f_csv", high_risk_csv)

    st.markdown(f"""
    <div class="msg-preview">
        <div class="msg-header">Selected Client Profile</div>
        <strong>Account Name:</strong> {acc_name} (<code>{acc_id}</code>)<br>
        <strong>Account Age:</strong> {tenure} month(s)<br>
        <strong>Politically Exposed Person (PEP):</strong> {'Yes (High-Risk Category)' if is_pep else 'No (Standard Retail)'}
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Review Raw Bank Ledger Data (CSV)"):
        st.text_area("Transaction Records:", value=csv_text, height=120, disabled=True)

    # Step 2: Action Button
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.subheader("Step 2: Run Risk Detection")
    
    if st.button("Evaluate Account Risk", type="primary", width="stretch"):
        with st.spinner("Screening sanctions watchlists, detecting structuring anomalies, and computing composite score..."):
            parsed_txs = FinancialRiskAggregator.parse_csv_transactions(csv_text)
            meta = {
                "account_id": acc_id,
                "customer_name": acc_name,
                "jurisdiction": "Offshore",
                "pep_status": is_pep,
                "account_tenure_months": tenure
            }
            profile = FinancialRiskAggregator.analyze_dataset(parsed_txs, meta)
            st.session_state["risk_profile"] = profile
            st.session_state["risk_evaluated"] = True

    # Step 3: Results display
    if st.session_state.get("risk_evaluated", False) and "risk_profile" in st.session_state:
        profile = st.session_state["risk_profile"]

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.subheader("Step 3: Risk Assessment Results")

        if profile.risk_score >= 70:
            b_class = "banner-critical"
        elif profile.risk_score >= 45:
            b_class = "banner-high"
        else:
            b_class = "banner-normal"

        st.markdown(f"""
        <div class="{b_class}">
            <div class="banner-title">Risk Score: {profile.risk_score} / 100 ({profile.risk_level} Priority)</div>
            <div class="banner-sub">
                Total Volume Analyzed: <strong>${profile.total_volume_usd:,.2f}</strong> across <strong>{profile.total_transactions_analyzed} transactions</strong><br>
                <strong>Mandatory Next Step:</strong> {profile.recommended_action}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Simplified Explanation of the AI Summary
        st.markdown("**AI Summary: Why Was This Flagged?**")
        st.caption("A plain-English explanation generated for the compliance officer detailing the primary risk drivers:")
        st.info(profile.ai_narrative_summary)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        if profile.flagged_signals:
            st.markdown("**Specific Red Flags Identified:**")
            for sig in profile.flagged_signals:
                st.markdown(f"""
                <div class="action-step">
                    <div class="step-circle-red">!</div>
                    <div>
                        <div class="step-header-text">{sig.rule_name} (+{sig.score_contribution} pts)</div>
                        <div class="step-detail-text">{sig.description}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No anomalies or red flags detected in this account.")

        with st.expander("View Ingested Transactions Table"):
            st.dataframe(pd.DataFrame(FinancialRiskAggregator.parse_csv_transactions(csv_text)), width="stretch")
    else:
        st.info("Click the **'Evaluate Account Risk'** button above to run the fraud and AML detection engine on this account.")
