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


def load_risk_cases():
    path = os.path.join(os.path.dirname(__file__), "sample_risk_cases.json")
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
        <div class="msg-header">{active_req.get('title', 'Customer Inquiry')}</div>
        <strong>From:</strong> {active_req.get('sender', 'user@corp.com')}<br><br>
        {active_req.get('text', '')}
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Custom Query"):
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
    risk_data = load_risk_cases()
    category_names = [cat["category"] for cat in risk_data] if risk_data else []
    category_names.append("Custom Sandbox / Enter Your Own Data")

    st.subheader("Step 1: Select Risk Category & Scenario")
    st.caption("Choose from 30 realistic banking compliance cases (10 per category) or enter custom data:")

    sel_col1, sel_col2 = st.columns([1, 1])

    with sel_col1:
        chosen_cat_name = st.selectbox("Risk Category:", options=category_names, index=0)

    # Find scenarios for category
    current_cat = next((c for c in risk_data if c["category"] == chosen_cat_name), None) if risk_data else None

    if current_cat and current_cat["scenarios"]:
        scenario_titles = [s["title"] for s in current_cat["scenarios"]]
        with sel_col2:
            chosen_scenario_title = st.selectbox("Scenario (10 Available):", options=scenario_titles, index=0)

        selected_case = next(s for s in current_cat["scenarios"] if s["title"] == chosen_scenario_title)

        default_acc_id = selected_case.get("account_id", "ACC-1001")
        default_name = selected_case.get("title", "").split("(")[0].strip()
        default_pep = selected_case.get("pep_status", False)
        default_tenure = selected_case.get("tenure_months", 12)
        default_csv = selected_case.get("csv", "")
        default_clue = selected_case.get("clue", "Evaluate multi-source transaction signals.")
    else:
        # Custom Sandbox mode
        with sel_col2:
            st.caption("Custom Mode Active")
        selected_case = None
        default_acc_id = "ACC-CUSTOM-1"
        default_name = "Apex Horizon Capital LLC"
        default_pep = True
        default_tenure = 2
        default_clue = "Custom user scenario. Test and manipulate parameters below."
        default_csv = (
            "tx_id,amount,source_country,destination_country,tx_type\n"
            "TX-01,9500.00,USA,Panama,WIRE_OUT\n"
            "TX-02,9800.00,USA,Panama,WIRE_OUT\n"
            "TX-03,9600.00,USA,Cayman Islands,WIRE_OUT"
        )

    # KYC Profile Snapshot Card with "What to look for" clue
    st.markdown(f"""
    <div class="msg-preview">
        <div class="msg-header">Client KYC Snapshot & Threat Clue</div>
        <strong>Entity:</strong> {default_name} (<code>{default_acc_id}</code>)<br>
        <strong>What to look for:</strong> <em>{default_clue}</em>
    </div>
    """, unsafe_allow_html=True)

    # Interactive What-If Parameter Controls
    with st.expander("Interactive What-If Controls (Manipulate Profile & CSV Data)", expanded=True):
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            pep_toggle = st.toggle("Politically Exposed Person (PEP Exposure)", value=default_pep)
            acc_id_input = st.text_input("Account Identifier:", value=default_acc_id)
        with p_col2:
            tenure_slider = st.slider("Account Age (Months):", min_value=1, max_value=60, value=min(60, max(1, default_tenure)))
            name_input = st.text_input("Legal Entity Name:", value=default_name)

        csv_editor_text = st.text_area(
            "Transaction Ledger (Smart Auto-Mapping detects any column names e.g. amount, value, dest, etc.):",
            value=default_csv,
            height=120
        )

    # Step 2: Action Button
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.subheader("Step 2: Run Risk Detection Engine")

    if st.button("Evaluate Account Risk", type="primary", width="stretch"):
        with st.spinner("Screening sanctions watchlists, detecting structuring anomalies, and computing composite score..."):
            parsed_txs = FinancialRiskAggregator.parse_csv_transactions(csv_editor_text)
            meta = {
                "account_id": acc_id_input,
                "customer_name": name_input,
                "jurisdiction": "Offshore",
                "pep_status": pep_toggle,
                "account_tenure_months": tenure_slider
            }
            profile = FinancialRiskAggregator.analyze_dataset(parsed_txs, meta)
            st.session_state["risk_profile"] = profile
            st.session_state["risk_evaluated"] = True
            st.session_state["evaluated_txs"] = parsed_txs

    # Step 3: Results display
    if st.session_state.get("risk_evaluated", False) and "risk_profile" in st.session_state:
        profile = st.session_state["risk_profile"]
        parsed_txs = st.session_state.get("evaluated_txs", [])

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

        with st.expander("View Normalized Ledger Table"):
            if parsed_txs:
                st.dataframe(pd.DataFrame(parsed_txs), width="stretch")
            else:
                st.caption("No transaction records parsed.")
    else:
        st.info("Click the **'Evaluate Account Risk'** button above to run the fraud and AML detection engine on this account.")
