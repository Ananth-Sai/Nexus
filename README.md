# Nexus AI: Autonomous Operations & Financial Risk Suite

An integrated, enterprise-grade AI prototype addressing two core organizational challenges:
1. **Incoming Request Processing Workflow** (Autonomous triage, intent extraction, multi-branch remediation, and audit logging).
2. **Financial Risk Signal Aggregator** (Multi-source data ingestion, transaction anomaly detection, AML risk scoring, and compliance narrative generation).

---

## 1. Quick Start & Setup

### Prerequisites
- Python 3.10+ installed
- (Optional) `GEMINI_API_KEY` for live generative responses. If not provided, the system automatically falls back to its deterministic rule engine with 100% functionality and offline reliability.

### Installation
```bash
git clone <your-repo-link>
cd A1
python -m pip install -r requirements.txt
```

### Running Locally
```bash
python -m streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### Running Test Suite
```bash
python -m pytest -v test_engines.py
```
*(8 of 8 automated unit & integration tests pass with 0 warnings).*

---

## 2. Deploying to Render (Free Hosting)

To generate a live hosted URL for your evaluation submission:
1. Push this repository to your GitHub account (`git push origin main`).
2. Log into [Render.com](https://render.com) and click **New +** $\rightarrow$ **Web Service**.
3. Connect your repository.
4. Set the following build settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Click **Create Web Service**. Within 2 minutes, Render will issue a public URL (e.g. `https://nexus-ai-suite.onrender.com`) to submit.

---

## 3. Module 1: Incoming Request Processing Workflow

### Objective & Architecture
Replaces manual, slow, and inconsistent customer support dispatching with an autonomous multi-step remediation engine.

```
[Incoming Ticket/Email] ──► [AI Classifier & Entity Extractor]
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
  [Branch A: Billing]          [Branch B: Outage]          [Branch C: Inquiry]
  • Extract Invoice & Amount   • Telemetry Fault Assessment• FAQ / KB Retrieval
  • SLA & Policy Check         • On-Call Engineering Page  • Tier-1 Queue Dispatch
  • Draft Refund Hold Notice   • War-Room Bridge Trigger   • Self-Service Response
  • Route to Tier-2 Finance    • Critical 1-Hour SLA Lock  • Standard 24-Hour SLA
           │                            │                            │
           └────────────────────────────┼────────────────────────────┘
                                        ▼
                         [Audited Execution Ledger]
```

### Verified Scenarios & Example Inputs/Outputs

#### Example 1: Critical Billing Overcharge
* **Input Text:**
  > *"URGENT: I was double-charged on invoice INV-88942 for our enterprise subscription. The charge of $4,950.00 was debited twice from our corporate card this morning. Please reverse immediately!"*
* **Classification Output:** Category: `Billing Dispute` | Urgency: `High` | Entities: `{"invoice_id": "INV-88942", "amount": "$4,950.00"}`
* **Remediation Steps Executed:**
  1. *Entity Validation & Audit Check:* Extracted `INV-88942` and `$4,950.00`. Cross-referenced against ledger.
  2. *SLA & Refund Policy Enforcement:* Confirmed within 60-day policy window.
  3. *Queue Dispatch:* Assigned to `Finance & Billing Tier-2` with 4-hour SLA.
  4. *Customer Notification:* Generated personalized acknowledgment confirming temporary charge hold.
* **Audit Persistence:** Automatically logged with unique UUID to `operations_audit.db`.

#### Example 2: Critical Technical Outage
* **Input Text:**
  > *"CRITICAL EMERGENCY: The Payment Checkout API gateway is returning HTTP 500 Internal Server Errors across all US-East clusters. Error code ERR_GATEWAY_TIMEOUT_504 is spiking to 87%. Escalate immediately!"*
* **Classification Output:** Category: `Technical Escalation` | Urgency: `Critical` | Entities: `{"service": "API", "error_code": "ERR_GATEWAY_TIMEOUT_504"}`
* **Remediation Steps Executed:**
  1. *Telemetry Probe:* Verified high-impact infrastructure fault.
  2. *On-Call Alert:* Paged Site Reliability Engineering (SRE) war-room.
  3. *SLA Lock:* Initiated emergency 1-hour P1 resolution countdown.
  4. *Status Update:* Generated incident update with live status page link.

---

## 4. Module 2: Financial Risk Signal Aggregator

### Objective & Architecture
Empowers AML compliance analysts to synthesize fragmented signals across transactions, account velocity, and external watchlists into a single, prioritized risk profile.

```
[Transaction CSV Records] + [Account Profile] + [External Watchlists/PEP]
                                        │
                                        ▼
                  [Risk Signal Evaluation Engine]
                  • Structuring Rule: $8,500 - $9,999 smurfing patterns
                  • Jurisdiction Rule: FATF grey/black list transfers
                  • Watchlist Rule: OFAC / Interpol / Adverse Media matches
                  • Velocity Rule: Surge on newly onboarded accounts
                                        │
                                        ▼
                 [Consolidated Compliance Profile]
                 • Composite Risk Score (0 - 100)
                 • Priority Tier: Critical / High / Medium / Low
                 • Executive AI Narrative Rationale
                 • Action Banner: SAR Filing / Account Freeze / EDD
```

### Verified Scenarios & Example Inputs/Outputs

#### Scenario A: High-Risk Structuring & Sanctions Match (ACC-9041)
* **Input Records:** 4 transactions between \$9,200 and \$9,800 to Panama and Cayman Islands, plus \$125,000 wire to Switzerland. Account age: 1 month. PEP: True.
* **Output Metrics:**
  * **Risk Score:** `85 / 100` (Critical Tier)
  * **Flagged Signals (4):**
    1. *External Sanctions / Watchlist Alert:* PEP match linked to foreign official (+40 pts).
    2. *Structuring / Smurfing:* Multiple transactions just under the \$10,000 threshold (+30 pts).
    3. *High-Risk Jurisdiction Activity:* Transfers involving FATF-monitored destinations (+25 pts).
    4. *New Account Velocity Surge:* \$163,100 volume within 1st month of opening (+15 pts).
  * **Action Required:** `IMMEDIATE ACCOUNT FREEZE & FILE SUSPICIOUS ACTIVITY REPORT (SAR)`
  * **AI Narrative:**
    > *"Consolidated risk assessment flagged account ACC-9041 (Vanguard Maritime Trade Ltd) at a Critical risk tier with a composite risk score of 85/100. Key drivers include 'External Sanctions / Watchlist Alert', 'Potential Structuring / Smurfing Threshold Evasion', and 'High-Risk Jurisdiction Wire Activity' across 5 transactions totaling $163,100.00. The convergence of structured amounts and adverse profile indicators warrants prioritized compliance review and prompt execution of enhanced due diligence."*

#### Scenario B: Clean Retail Account (ACC-1001)
* **Input Records:** Standard domestic utility payments, coffee purchases, and payroll deposit totaling \$1,719.70.
* **Output Metrics:**
  * **Risk Score:** `0 / 100` (Low Tier)
  * **Flagged Signals:** 0
  * **Action Recommendation:** `STANDARD MONITORING - NO ADVERSE ACTION REQUIRED`

---

## 5. Technology Stack & Key Decisions

| Component | Technology | Rationale |
|---|---|---|
| Frontend UI | Streamlit 1.35+ | High performance, interactive controls, zero JavaScript build bloat, 1-click cloud hosting. |
| Data Validation | Pydantic v2 | Strict schema contracts and type safety across all pipeline steps. |
| Storage & Audit | SQLite3 | Zero-configuration, ACID-compliant local audit persistence. |
| AI / LLM Engine | Hybrid (GenAI + Regex Rules) | Guarantees 100% offline uptime with deterministic accuracy, with seamless LLM enrichment when API key is present. |
| Testing | Pytest | Full regression test suite covering all branches, edge cases, and parsers. |

---

## 6. Repository Structure
```
A1/
├── app.py                     # Multi-page Streamlit application
├── workflow_engine.py         # Request triage, branching & audit engine
├── risk_engine.py             # AML data aggregation, anomaly scoring & narrative engine
├── test_engines.py            # Pytest test suite (8 tests)
├── sample_requests.json       # Mock customer requests for 1-click testing
├── sample_financial_data.csv  # Mock transaction records
├── sample_external_alerts.json# Mock external watchlist hits
├── requirements.txt           # Project dependencies
├── SLIDES_WORKFLOW.md         # 5-Slide presentation deck for Assignment 1
├── SLIDES_RISK.md             # 5-Slide presentation deck for Assignment 2
└── README.md                  # Comprehensive documentation
```

