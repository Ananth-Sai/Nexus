"""
Nexus AI: Operations & Compliance Mission Control
Bespoke interface for:
1. Autonomous Request Triage & Multi-Branch Remediation
2. Financial AML Risk Signal Aggregator & Compliance Terminal
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

# Page Configuration
st.set_page_config(
    page_title="Nexus Operations & Compliance Mission Control",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Bespoke, High-Contrast Console Styling (Anti-Vibe-Coded: No purple, no sparkles, strict 8pt grid)
st.markdown("""
<style>
    /* Global Page Structure */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1380px;
    }

    /* Top Console Header */
    .console-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 20px;
        background: #0f172a;
        color: #f8fafc;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    .console-title {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .console-sub {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 2px;
    }
    .status-pill {
        background: #1e293b;
        color: #38bdf8;
        border: 1px solid #334155;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }

    /* Split-screen panels */
    .panel-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        margin-bottom: 16px;
    }
    .panel-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #0f172a;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 8px;
        margin-bottom: 14px;
    }

    /* Metric Badges */
    .kpi-tile {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px 14px;
        text-align: center;
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-val {
        font-size: 1.45rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 2px;
    }

    /* Vertical Remediation Timeline Stepper */
    .timeline-step {
        display: flex;
        margin-bottom: 12px;
        position: relative;
    }
    .timeline-num {
        flex-shrink: 0;
        width: 30px;
        height: 30px;
        background: #0f172a;
        color: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 12px;
    }
    .timeline-content {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 10px 14px;
        width: 100%;
    }
    .timeline-step-title {
        font-weight: 600;
        font-size: 0.88rem;
        color: #1e293b;
    }
    .timeline-step-desc {
        font-size: 0.82rem;
        color: #475569;
        margin-top: 3px;
        line-height: 1.35;
    }

    /* Semantic Tag Badges */
    .chip-critical {
        background: #fee2e2;
        color: #991b1b;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid #fecaca;
    }
    .chip-high {
        background: #fef3c7;
        color: #92400e;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid #fde68a;
    }
    .chip-normal {
        background: #e0f2fe;
        color: #075985;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid #bae6fd;
    }
    .chip-safe {
        background: #dcfce7;
        color: #166534;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid #bbf7d0;
    }

    /* Action Banner */
    .banner-danger {
        background: #fef2f2;
        border-left: 5px solid #dc2626;
        padding: 12px 16px;
        border-radius: 4px;
        color: #991b1b;
        font-size: 0.88rem;
        margin-bottom: 14px;
    }
    .banner-success {
        background: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 12px 16px;
        border-radius: 4px;
        color: #166534;
        font-size: 0.88rem;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)


def load_sample_requests():
    path = os.path.join(os.path.dirname(__file__), "sample_requests.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# Top Command Bar Header
api_indicator = "Hybrid (GenAI Live)" if os.environ.get("GEMINI_API_KEY") else "Deterministic Rule Engine (Active)"
st.markdown(f"""
<div class="console-header">
    <div>
        <div class="console-title">Nexus Operations & Compliance Mission Control</div>
        <div class="console-sub">Multi-Branch Workflow Orchestration & Financial AML Signal Aggregation</div>
    </div>
    <div class="status-pill">{api_indicator}</div>
</div>
""", unsafe_allow_html=True)

# Primary Module Navigation Switcher
active_tab = st.radio(
    "Active Operational Console:",
    options=[
        "Operational Request Triage & Remediation (Assignment 2)",
        "Financial Risk Signal Aggregator & AML Terminal (Assignment 1)"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# VIEW 1: OPERATIONAL REQUEST TRIAGE & REMEDIATION
# ==============================================================================
if "Operational" in active_tab:
    sample_requests = load_sample_requests()

    # Split-Screen Layout: Left = Intake & Feed; Right = Execution & Telemetry
    left_col, right_col = st.columns([5, 6], gap="large")

    with left_col:
        st.markdown("""
        <div class="panel-card">
            <div class="panel-title">Inbound Request Dispatcher</div>
        </div>
        """, unsafe_allow_html=True)

        st.caption("Select a pre-configured enterprise scenario or submit a custom intake payload:")
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        loaded_scenario = None

        if sample_requests:
            with btn_c1:
                if st.button("Billing Dispute", use_container_width=True):
                    loaded_scenario = sample_requests[0]
            with btn_c2:
                if st.button("Critical 500 Outage", use_container_width=True):
                    loaded_scenario = sample_requests[1]
            with btn_c3:
                if st.button("General Inquiry", use_container_width=True):
                    loaded_scenario = sample_requests[2]

        if loaded_scenario:
            st.session_state["v1_text"] = loaded_scenario["text"]
            st.session_state["v1_sender"] = loaded_scenario["sender"]

        with st.form("triage_form"):
            sender_val = st.text_input(
                "Requester Identity / Channel:",
                value=st.session_state.get("v1_sender", "elena.rostova@acmefinance.com")
            )
            text_val = st.text_area(
                "Raw Request Payload:",
                value=st.session_state.get("v1_text", "URGENT: I was double-charged on invoice INV-88942 for our enterprise subscription. The charge of $4,950.00 was debited twice this morning. Please reverse immediately!"),
                height=130
            )
            dispatch_btn = st.form_submit_button("Trigger Autonomous Triage", type="primary", use_container_width=True)

        # Historical Audit Stream
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="panel-card">
            <div class="panel-title">Operations Audit Ledger</div>
        </div>
        """, unsafe_allow_html=True)
        records = get_audit_records(limit=8)
        if records:
            df = pd.DataFrame(records)[["timestamp", "request_id", "category", "urgency", "assigned_queue", "sla_hours"]]
            st.dataframe(df, use_container_width=True, height=210)
        else:
            st.caption("No historical requests recorded in database yet.")

    with right_col:
        st.markdown("""
        <div class="panel-card">
            <div class="panel-title">Remediation Execution Telemetry</div>
        </div>
        """, unsafe_allow_html=True)

        # Run or use default execution on first load
        req_to_process = text_val if dispatch_btn else st.session_state.get("v1_text", "URGENT: I was double-charged on invoice INV-88942 for $4,950.00. Please reverse immediately!")
        sender_to_process = sender_val if dispatch_btn else st.session_state.get("v1_sender", "elena.rostova@acmefinance.com")

        result = WorkflowRemediationEngine.execute(req_to_process, sender=sender_to_process)

        # KPI Metrics Row
        kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
        urgency_class = "chip-critical" if result.classification.urgency == "Critical" else ("chip-high" if result.classification.urgency == "High" else "chip-normal")

        with kpi_c1:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">Category</div>
                <div class="kpi-val" style="font-size: 1.05rem;">{result.classification.category}</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi_c2:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">Urgency</div>
                <div class="kpi-val"><span class="{urgency_class}">{result.classification.urgency}</span></div>
            </div>
            """, unsafe_allow_html=True)
        with kpi_c3:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">Target Queue</div>
                <div class="kpi-val" style="font-size: 0.95rem;">{result.assigned_queue}</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi_c4:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">SLA Window</div>
                <div class="kpi-val">{result.sla_hours} <span style="font-size: 0.8rem; color: #64748b;">Hrs</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Vertical Execution Stepper
        st.markdown(f"**Branch Invocation:** `{result.remediation_branch}` (Ticket: `{result.request_id}`)")

        for step in result.steps_executed:
            st.markdown(f"""
            <div class="timeline-step">
                <div class="timeline-num">{step.step_number}</div>
                <div class="timeline-content">
                    <div class="timeline-step-title">{step.action_name} <span class="chip-safe" style="float: right;">{step.status}</span></div>
                    <div class="timeline-step-desc">{step.description}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if result.classification.key_entities:
            st.markdown(f"**Extracted Entities:** `{json.dumps(result.classification.key_entities)}`")

        # Tailored Response Draft Card
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown("**Tailored Customer Communication (Prepared for Dispatch):**")
        st.text_area("Draft Communication:", value=result.draft_response, height=170, label_visibility="collapsed")


# ==============================================================================
# VIEW 2: FINANCIAL RISK SIGNAL AGGREGATOR & AML TERMINAL
# ==============================================================================
else:
    st.markdown("""
    <div class="panel-card">
        <div class="panel-title">Financial Crime & AML Risk Assessment Console</div>
    </div>
    """, unsafe_allow_html=True)

    # Preset Loaders
    pcol1, pcol2 = st.columns(2)
    load_high_risk = False
    load_clean = False

    with pcol1:
        if st.button("Load Case A: High-Risk Offshore Structuring & PEP (ACC-9041)", use_container_width=True):
            load_high_risk = True
    with pcol2:
        if st.button("Load Case B: Clean Retail Merchant Account (ACC-1001)", use_container_width=True):
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
        st.session_state["v2_acc"] = "ACC-1001"
        st.session_state["v2_name"] = "Johnathan Mercer"
        st.session_state["v2_pep"] = False
        st.session_state["v2_tenure"] = 36
    elif load_high_risk:
        st.session_state["v2_acc"] = "ACC-9041"
        st.session_state["v2_name"] = "Vanguard Maritime Trade Ltd"
        st.session_state["v2_pep"] = True
        st.session_state["v2_tenure"] = 1

    # Ingestion Controls
    meta_c1, meta_c2, meta_c3, meta_c4 = st.columns(4)
    with meta_c1:
        acc_id_input = st.text_input("Entity Account ID:", value=st.session_state.get("v2_acc", "ACC-9041"))
    with meta_c2:
        name_input = st.text_input("Account Legal Name:", value=st.session_state.get("v2_name", "Vanguard Maritime Trade Ltd"))
    with meta_c3:
        pep_input = st.checkbox("PEP Exposure Flag", value=st.session_state.get("v2_pep", True))
    with meta_c4:
        tenure_input = st.number_input("Account Age (Months):", min_value=1, max_value=240, value=st.session_state.get("v2_tenure", 1))

    # Split-Screen Cockpit
    fin_left, fin_right = st.columns([5, 6], gap="large")

    with fin_left:
        st.markdown("**Structured Transaction Records (CSV Input):**")
        csv_payload = st.text_area("CSV Records:", value=default_csv, height=160, label_visibility="collapsed")
        run_aml_btn = st.button("Synthesize Risk Signals & Score Entity", type="primary", use_container_width=True)

        parsed_txs = FinancialRiskAggregator.parse_csv_transactions(csv_payload)
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown(f"**Normalized Ledger Entries ({len(parsed_txs)} Total):**")
        st.dataframe(pd.DataFrame(parsed_txs), use_container_width=True, height=220)

    with fin_right:
        account_meta = {
            "account_id": acc_id_input,
            "customer_name": name_input,
            "jurisdiction": "Offshore",
            "pep_status": pep_input,
            "account_tenure_months": tenure_input
        }
        profile = FinancialRiskAggregator.analyze_dataset(parsed_txs, account_meta)

        # Risk Scoreboard KPIs
        score_class = "chip-critical" if profile.risk_score >= 70 else ("chip-high" if profile.risk_score >= 45 else ("chip-normal" if profile.risk_score >= 20 else "chip-safe"))
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">Risk Score</div>
                <div class="kpi-val">{profile.risk_score} <span style="font-size: 0.8rem; color: #64748b;">/ 100</span></div>
            </div>
            """, unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">Priority Tier</div>
                <div class="kpi-val"><span class="{score_class}">{profile.risk_level}</span></div>
            </div>
            """, unsafe_allow_html=True)
        with sc3:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">Volume USD</div>
                <div class="kpi-val" style="font-size: 1.15rem;">${profile.total_volume_usd:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        with sc4:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">Alert Count</div>
                <div class="kpi-val">{len(profile.flagged_signals)}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Action Recommendation Callout
        if profile.risk_score >= 45:
            st.markdown(f"""
            <div class="banner-danger">
                <strong>MANDATORY ACTION:</strong> {profile.recommended_action}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="banner-success">
                <strong>COMPLIANCE STATUS:</strong> {profile.recommended_action}
            </div>
            """, unsafe_allow_html=True)

        # AI Compliance Narrative
        st.markdown("**AI Compliance Officer Narrative Rationale:**")
        st.info(profile.ai_narrative_summary)

        # Flagged Signals Breakdown Table
        st.markdown("**Identified Risk Signals & Threat Vectors:**")
        if profile.flagged_signals:
            sig_list = []
            for s in profile.flagged_signals:
                sig_list.append({
                    "Threat Vector": s.rule_name,
                    "Severity": s.severity,
                    "Impact": f"+{s.score_contribution} pts",
                    "Evidence": s.description
                })
            st.dataframe(pd.DataFrame(sig_list), use_container_width=True, height=190)
        else:
            st.success("Zero adverse indicators or anomalous velocity patterns identified.")
