"""
Nexus AI Operations & Compliance Suite
Streamlit application hosting both:
1. Incoming Request Processing Workflow Engine
2. Financial Risk Signal Aggregator
"""

import json
import os
import streamlit as st
import pandas as pd
from datetime import datetime

from workflow_engine import (
    WorkflowRemediationEngine,
    get_audit_records,
    init_audit_db
)
from risk_engine import (
    FinancialRiskAggregator,
    HIGH_RISK_JURISDICTIONS
)

# Page configuration
st.set_page_config(
    page_title="Nexus AI | Operations & Risk Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, professional styling adhering to anti-vibe-coded guidelines (no neon purple, strict high contrast)
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }
    
    /* Remediation Step Card */
    .step-box {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #2563eb;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .step-header {
        font-weight: 600;
        color: #1e293b;
        font-size: 0.95rem;
    }
    .step-desc {
        color: #334155;
        font-size: 0.88rem;
        margin-top: 4px;
    }

    /* Severity badges */
    .badge-critical {
        background-color: #fee2e2;
        color: #991b1b;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-high {
        background-color: #fef3c7;
        color: #92400e;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-normal {
        background-color: #e0f2fe;
        color: #0369a1;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-low {
        background-color: #dcfce7;
        color: #166534;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


def load_sample_requests():
    path = os.path.join(os.path.dirname(__file__), "sample_requests.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# -------------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------------
with st.sidebar:
    st.title("Nexus AI Platform")
    st.caption("Autonomous Operations & Compliance Engine")
    st.divider()

    module_choice = st.radio(
        "Select Assignment Module:",
        options=[
            "Module 1: Request Processing Workflow",
            "Module 2: Financial Risk Signal Aggregator"
        ],
        index=0
    )

    st.divider()
    st.markdown("**System Architecture Overview**")
    if "Request" in module_choice:
        st.markdown("""
        * **Domain:** Customer & Operations Triage
        * **Input:** Emails / Forms / Escalations
        * **Decisioning:** Intent & Urgency Classifier
        * **Remediation:** 3 Distinct Branches (>=2 automated actions each)
        * **Persistence:** SQLite Audit Ledger
        """)
    else:
        st.markdown("""
        * **Domain:** Financial AML & Sanctions
        * **Input:** Transactions CSV + Watchlists
        * **Detection:** Structuring, PEP, Velocity, FATF Havens
        * **Output:** Risk Score (0-100) & AI SAR Narrative
        """)

    st.divider()
    api_status = "Connected (Gemini Live)" if os.environ.get("GEMINI_API_KEY") else "Offline Deterministic Mode (Active)"
    st.info(f"AI Engine: **{api_status}**")


# =============================================================
# MODULE 1: INCOMING REQUEST PROCESSING WORKFLOW
# =============================================================
if "Request" in module_choice:
    st.header("Incoming Request Processing Workflow")
    st.caption("Autonomous triage, multi-branch remediation execution, and auditable case management.")

    sample_requests = load_sample_requests()

    st.subheader("1. Request Intake")
    col1, col2, col3 = st.columns(3)

    # Preset loader buttons
    selected_preset = None
    if sample_requests:
        with col1:
            if st.button("Load Preset: Billing Dispute", use_container_width=True):
                selected_preset = sample_requests[0]
        with col2:
            if st.button("Load Preset: Critical 500 Outage", use_container_width=True):
                selected_preset = sample_requests[1]
        with col3:
            if st.button("Load Preset: General Inquiry", use_container_width=True):
                selected_preset = sample_requests[2]

    # Preload fields if preset clicked
    if selected_preset:
        st.session_state["req_text"] = selected_preset["text"]
        st.session_state["req_sender"] = selected_preset["sender"]

    with st.form("workflow_intake_form"):
        sender_email = st.text_input(
            "Requester Contact / Email:",
            value=st.session_state.get("req_sender", "customer.ops@enterprise.com")
        )
        request_body = st.text_area(
            "Incoming Request Message / Body:",
            value=st.session_state.get("req_text", "URGENT: I was double-charged on invoice INV-88942 for $4,950.00 this morning. Please reverse immediately!"),
            height=130
        )
        submit_btn = st.form_submit_button("Execute Remediation Workflow", type="primary")

    if submit_btn and request_body.strip():
        with st.spinner("Analyzing request, classifying intent, and executing remediation steps..."):
            result = WorkflowRemediationEngine.execute(request_body, sender=sender_email)

        st.success(f"Workflow Executed Successfully | Case ID: **{result.request_id}**")

        # Summary KPIs
        st.markdown("### 2. Triage & Classification Metrics")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Detected Category</div>
                <div class="metric-value" style="font-size: 1.3rem;">{result.classification.category}</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi2:
            badge_class = "badge-critical" if result.classification.urgency == "Critical" else ("badge-high" if result.classification.urgency == "High" else "badge-normal")
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Urgency Level</div>
                <div class="metric-value"><span class="{badge_class}">{result.classification.urgency}</span></div>
            </div>
            """, unsafe_allow_html=True)
        with kpi3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Assigned Queue</div>
                <div class="metric-value" style="font-size: 1.2rem;">{result.assigned_queue}</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Resolution SLA</div>
                <div class="metric-value">{result.sla_hours} <span style="font-size: 1rem; color: #64748b;">Hours</span></div>
            </div>
            """, unsafe_allow_html=True)

        if result.classification.key_entities:
            st.caption(f"**Extracted Entities:** {json.dumps(result.classification.key_entities)}")

        # Step by step execution trace
        st.markdown("### 3. Executed Remediation Branch")
        st.info(f"**Active Path:** {result.remediation_branch}")

        for step in result.steps_executed:
            st.markdown(f"""
            <div class="step-box">
                <div class="step-header">Step {step.step_number}: {step.action_name} <span class="badge-low" style="float: right;">{step.status}</span></div>
                <div class="step-desc">{step.description}</div>
            </div>
            """, unsafe_allow_html=True)

        # Tailored Response Draft
        st.markdown("### 4. Tailored Communication Output")
        st.text_area("Generated Draft Response (Ready for Dispatch):", value=result.draft_response, height=180)

    # Historical Audit Trail
    st.divider()
    st.subheader("Historical Operations Audit Log")
    records = get_audit_records(limit=15)
    if records:
        df = pd.DataFrame(records)[["timestamp", "request_id", "category", "urgency", "assigned_queue", "sla_hours", "steps_count"]]
        st.dataframe(df, use_container_width=True)
    else:
        st.caption("No historical records logged yet.")


# =============================================================
# MODULE 2: FINANCIAL RISK SIGNAL AGGREGATOR
# =============================================================
else:
    st.header("Financial Risk Signal Aggregator")
    st.caption("Multi-source risk ingestion, anomaly synthesis, AML scoring, and compliance narrative generation.")

    # Preset datasets
    st.subheader("1. Ingest Financial Data")
    dcol1, dcol2 = st.columns(2)
    use_high_risk_preset = False
    use_clean_preset = False

    with dcol1:
        if st.button("Load Scenario A: Offshore Structuring & PEP (High Risk)", use_container_width=True):
            use_high_risk_preset = True
    with dcol2:
        if st.button("Load Scenario B: Clean Retail Account (Low Risk)", use_container_width=True):
            use_clean_preset = True

    default_csv = (
        "tx_id,amount,currency,source_country,destination_country,tx_type\n"
        "TX-9901,9450.00,USD,USA,Cayman Islands,WIRE_OUT\n"
        "TX-9902,9800.00,USD,USA,Panama,WIRE_OUT\n"
        "TX-9903,9200.00,USD,USA,Cayman Islands,WIRE_OUT\n"
        "TX-9904,9650.00,USD,USA,Panama,WIRE_OUT\n"
        "TX-9905,125000.00,USD,USA,Switzerland,WIRE_OUT"
    )

    if use_clean_preset:
        default_csv = (
            "tx_id,amount,currency,source_country,destination_country,tx_type\n"
            "TX-1001,120.50,USD,USA,USA,ACH_PAYMENT\n"
            "TX-1002,84.20,USD,USA,USA,CARD_PURCHASE\n"
            "TX-1003,1450.00,USD,USA,USA,PAYROLL_DEPOSIT\n"
            "TX-1004,65.00,USD,USA,USA,CARD_PURCHASE"
        )
        st.session_state["risk_acc_id"] = "ACC-1001"
        st.session_state["risk_name"] = "Johnathan Mercer"
        st.session_state["risk_pep"] = False
        st.session_state["risk_tenure"] = 36
    elif use_high_risk_preset:
        st.session_state["risk_acc_id"] = "ACC-9041"
        st.session_state["risk_name"] = "Vanguard Maritime Trade Ltd"
        st.session_state["risk_pep"] = True
        st.session_state["risk_tenure"] = 1

    col_meta1, col_meta2, col_meta3, col_meta4 = st.columns(4)
    with col_meta1:
        acc_id = st.text_input("Account Identifier:", value=st.session_state.get("risk_acc_id", "ACC-9041"))
    with col_meta2:
        cust_name = st.text_input("Entity / Client Name:", value=st.session_state.get("risk_name", "Vanguard Maritime Trade Ltd"))
    with col_meta3:
        is_pep = st.checkbox("Politically Exposed Person (PEP)", value=st.session_state.get("risk_pep", True))
    with col_meta4:
        tenure = st.number_input("Account Age (Months):", min_value=1, max_value=240, value=st.session_state.get("risk_tenure", 1))

    csv_input = st.text_area("Transaction Records (CSV Format):", value=default_csv, height=140)

    run_risk_btn = st.button("Run Risk Assessment & Signal Synthesis", type="primary")

    if run_risk_btn and csv_input.strip():
        transactions = FinancialRiskAggregator.parse_csv_transactions(csv_input)
        account_meta = {
            "account_id": acc_id,
            "customer_name": cust_name,
            "jurisdiction": "Offshore",
            "pep_status": is_pep,
            "account_tenure_months": tenure
        }

        with st.spinner("Synthesizing fragmented signals, scoring risk, and generating rationale..."):
            profile = FinancialRiskAggregator.analyze_dataset(transactions, account_meta)

        st.divider()
        st.subheader("2. Consolidated Risk Assessment")

        # Score & Metric display
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        score_badge = "badge-critical" if profile.risk_score >= 70 else ("badge-high" if profile.risk_score >= 45 else ("badge-normal" if profile.risk_score >= 20 else "badge-low"))

        with mcol1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Composite Risk Score</div>
                <div class="metric-value">{profile.risk_score} <span style="font-size: 1rem; color: #64748b;">/ 100</span></div>
            </div>
            """, unsafe_allow_html=True)
        with mcol2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Priority Tier</div>
                <div class="metric-value"><span class="{score_badge}">{profile.risk_level}</span></div>
            </div>
            """, unsafe_allow_html=True)
        with mcol3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Analyzed Volume</div>
                <div class="metric-value">${profile.total_volume_usd:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        with mcol4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Flagged Signals</div>
                <div class="metric-value">{len(profile.flagged_signals)}</div>
            </div>
            """, unsafe_allow_html=True)

        # Recommended Action Banner
        if profile.risk_score >= 45:
            st.error(f"**Action Required:** {profile.recommended_action}")
        else:
            st.success(f"**Action Recommendation:** {profile.recommended_action}")

        # AI Compliance Narrative
        st.markdown("### 3. AI Compliance Officer Narrative")
        st.info(profile.ai_narrative_summary)

        # Flagged Signals Breakdown
        st.markdown("### 4. Identified Risk Signals & Breakdown")
        if profile.flagged_signals:
            sig_data = []
            for sig in profile.flagged_signals:
                sig_data.append({
                    "Signal ID": sig.signal_id,
                    "Rule / Threat Vector": sig.rule_name,
                    "Severity": sig.severity,
                    "Score Impact": f"+{sig.score_contribution} pts",
                    "Evidence Summary": sig.description
                })
            st.dataframe(pd.DataFrame(sig_data), use_container_width=True)
        else:
            st.success("No anomalies or suspicious transaction patterns detected in this dataset.")

        # Parsed Transactions Table
        with st.expander("View Ingested Transaction Records"):
            st.dataframe(pd.DataFrame(transactions), use_container_width=True)
