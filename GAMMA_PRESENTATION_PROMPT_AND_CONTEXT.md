# 🎨 NEXUS AI — GAMMA MASTER PROMPT & COMPLETE SLIDE SPECIFICATION
### Formatted Specifically for Gamma.app to Produce Human, Executive-Grade Presentations
*(Both Modules: 1. Customer Operations Triage & 2. Financial AML Risk Engine)*

---

## PART 1: THE EXACT PROMPT TO PASTE INTO GAMMA

When you click **"Create new"** $\rightarrow$ **"Generate"** in Gamma, paste the following prompt into the prompt/instruction box:

```text
You are a Principal Product & Design-Systems Engineer at a Tier-1 Fintech. Create a high-impact, professional 5-slide executive presentation based strictly on the project specification below.

CRITICAL DESIGN & LAYOUT CONSTRAINTS:
1. STRICTLY AVOID repetitive 3-box bulleted cards. Every single slide must use a DISTINCT visual layout:
   - Slide 1: High-impact Split Hero (Bold Problem Statistic on left + 3 Objective Pills on right).
   - Slide 2: Horizontal 4-Step Process Pipeline with connecting arrows (Intake -> AI Triage -> Multi-Branch Remediation -> SQLite Audit Ledger).
   - Slide 3: Two-Column Technical Deep Dive with clear component badges and code/schema callouts.
   - Slide 4: Side-by-Side Comparison Table (Red/Amber "Operational Failure Mode" vs. Emerald "Engineering Resolution").
   - Slide 5: Phased Horizontal Roadmap Timeline (Phase 1: Delivered Prototype -> Phase 2: ERP/ITSM Webhooks -> Phase 3: Graph Intelligence).
2. NO GENERIC AI FILLER: Do not write vague buzzwords ("revolutionary", "game-changing", "seamless"). Use grounded engineering and financial terms (AML/CFT, Pydantic v2, ACID SQLite, OFAC WorldCheck, 0–100 calibrated scoring, FATF grey-lists).
3. COLOR PALETTE: Deep slate navy background (#0f172a), dark container surfaces (#1e293b), tech-blue accents (#3b82f6), crisp white text (#f8fafc), and clear data metrics.
4. ZERO EMOJIS in slide titles or buttons. Use crisp typography and structural tags instead.
```

---

## PART 2: SLIDE-BY-SLIDE SPECIFICATIONS (Paste Into Gamma's Content Window)

---

### DECK A: CUSTOMER REQUEST PROCESSING & MULTI-BRANCH REMEDIATION
*(Incoming Request Processing Workflow — Assignment 2)*

```markdown
# Slide 1: Operational Request Triage — Problem Understanding & Objective
**Headline:** Automating Multi-Channel Customer Inquiries with Autonomous Multi-Branch Remediation

### Left Column: The Operational Crisis (Hero Stat & Context)
- **The Bottleneck:** Operations teams receive an unorganized stream of customer requests across shared inboxes and web portals with unpredictable urgency.
- **Latency Cost:** Manual triage causes 4 to 12-hour response delays, frequently breaching enterprise SLA commitments.
- **Root Failure:** A single generic auto-responder fails because a Billing Dispute, a P1 Server Outage, and a Pricing Inquiry require radically different operational actions.

### Right Column: Core Architectural Objectives
- **Multi-Modal Intake:** Ingest raw customer text, simulated webforms, or structured JSON payloads through a unified API.
- **Hybrid AI Classification:** Gemini 2.5 Flash semantic classification (temperature=0.0) with an instant deterministic regex rule fallback for 100% offline uptime.
- **Autonomous Multi-Branch Remediation:** Execute >= 2 domain-specific downstream actions per category (ERP holds, PagerDuty alerts, knowledge base dispatch).
- **Non-Repudiation Governance:** Persist every triage decision, extracted entity, and action payload into an embedded SQLite audit ledger.

---

# Slide 2: End-to-End System Architecture & Data Flow
**Headline:** From Unstructured Ingestion to Multi-Branch Execution & SQLite Audit Persistence

### Layout: Horizontal 4-Step Pipeline Flow
1. **Intake Layer (Multi-Modal Intake)**
   - Unstructured customer messages, simulated inbox webhooks, or 30 pre-loaded enterprise scenarios across 3 categories.
2. **Triage & Entity Classifier (Dual-Engine)**
   - Primary: Gemini 2.5 Flash zero-shot semantic categorization + regex extraction of Invoices (`INV-XXXX`), Amounts (`$1,450.00`), and Errors (`ERR-502`).
   - Fallback: Deterministic keyword and regex router guarantees zero downtime during API outages.
3. **Multi-Branch Remediation Coordinator (Domain Execution)**
   - **Billing Dispute:** Auto-holds disputed invoice in ERP, provisions temporary customer dispute credit, and drafts resolution notice.
   - **Technical Outage:** Auto-generates P1 Jira/PagerDuty ticket, notifies on-call SRE lead, and attaches live status page URL.
   - **General Inquiry:** Contextual routing to product specialist pod and auto-retrieves relevant knowledge base URLs.
4. **Governance & Audit Ledger (ACID Persistence)**
   - SQLite relational database (`operations_audit.db`) storing `request_id`, category, priority, extracted entities JSON, and ISO 8601 UTC timestamp.

---

# Slide 3: Implementation Highlights & Engineering Rigor
**Headline:** Architectural Guardrails Enforcing 100% Uptime, Strict Contracts, and Zero Collateral Regressions

### Left Card: Hybrid AI & Schema Contracts
- **Strict Pydantic v2 Contracts:** Enforced runtime typing schemas (`RequestClassification`, `RemediationResult`), completely preventing malformed JSON crashes.
- **Deterministic Failover:** If Gemini API credits expire or network drops, deterministic regex rules take over within 1 millisecond.
- **100% Offline Testability:** All 8 unit and integration tests pass completely offline in CI/CD without external API keys.

### Right Card: Enterprise Production UI
- **Guided 3-Step Flow:** Step 1: Scenario Select -> Step 2: One-Click Triage Execution -> Step 3: Executive Results & DB Audit Ledger.
- **Anti-Vibe Design Standards:** Slate surfaces (`#1e293b`), high-contrast text (`#f8fafc`), zero purple gradients, and zero non-functional buttons.
- **Dynamic Module Reloader:** Enforced `importlib.reload` on entry to eliminate Streamlit in-memory bytecode caching errors.

---

# Slide 4: Engineering Challenges, Edge Cases & Trade-offs
**Headline:** Navigating Latency Vulnerabilities, Schema Drift, and Operational Boundaries

### Comparison Table: Challenge vs. Architectural Resolution

| Operational Challenge | Technical Risk | Engineering Resolution in Nexus |
| :--- | :--- | :--- |
| **LLM Latency & Outage Vulnerability** | Cloud AI calls introduce 1.5–3.0s latency and halt operations during provider outages. | Implemented a dual-engine router: deterministic regex pre-filters entities and acts as instant offline failover. |
| **Schema Drift & Hallucinations** | Free-form LLM text frequently omits required operational steps or invents invalid keys. | Bound LLM outputs to Pydantic v2 response schemas with fallback value normalization. |
| **Human-in-the-Loop Liability** | Fully automating financial refunds or server reboots carries legal and business risk. | Designed automated preparation: system drafts emails, flags P1 tickets, and holds invoices, but gates financial payouts for supervisor sign-off. |

---

# Slide 5: Demo Summary, Verification & Production Roadmap
**Headline:** Verified Prototype Capabilities and the Enterprise Scalability Path

### Left Card: Delivered & Verified Today
- **30 Enterprise Scenarios:** 10 Billing, 10 Tech Outage, and 10 General Inquiries running instantly with 1-click test buttons.
- **>= 2 Automated Actions:** Executes 3 downstream actions per branch: ticket generation, credit hold, and customer notification.
- **Immutable SQLite Ledger:** Live inspection expander displays tamper-evident audit logs directly in the UI.
- **100% Automated Test Suite:** Verified via `pytest -v test_engines.py` (8/8 tests passing in ~0.17 seconds).

### Right Column: Phased Production Roadmap
- **Phase 1 (Near-Term Integrations):** Direct webhook ingestion from Zendesk, Freshdesk, and SendGrid inbound email parsers.
- **Phase 2 (Automated ERP Hooks):** Live REST API calls to Stripe Billing for automatic dispute placement and Jira Service Management for incident creation.
- **Phase 3 (Enterprise Concurrency):** Migrate SQLite audit trail to distributed PostgreSQL with connection pooling (PgBouncer) and role-based access control (RBAC).
```

---

### DECK B: FINANCIAL RISK SIGNAL AGGREGATOR & AML FRAUD ENGINE
*(Financial Risk Signal Aggregator — Assignment 1)*

```markdown
# Slide 1: Financial Risk Synthesis — Problem Understanding & Objective
**Headline:** Consolidating Fragmented Financial Signals into a Calibrated 0–100 AML Risk Engine

### Left Column: The Compliance Crisis (Hero Stat & Context)
- **Data Fragmentation:** Transaction ledgers, customer KYC records, and sanctions watchlists exist in isolated banking databases.
- **Alert Fatigue:** Compliance officers manually review thousands of disconnected low-fidelity alerts, resulting in severe human error and missed financial crime.
- **Subjective Decisions:** Without an objective scoring framework, risk assessments vary wildly across compliance analysts, exposing institutions to multi-million dollar regulatory penalties.

### Right Column: Core Architectural Objectives
- **Multi-Source Data Fusion:** Ingest CSV transaction ledgers, account tenure, PEP exposure, and external OFAC watchlists simultaneously.
- **Smart CSV Auto-Mapping:** Automatically detect varied bank column headers (`amt`, `value`, `total`, `dest`) and sanitize dirty monetary strings (`$9,500.00` -> `9500.0`).
- **Calibrated 0–100 Scoring Engine:** Implement an additive, explainable scoring matrix mapped to 4 actionable priority tiers.
- **Natural Language Risk Interrogation:** Provide a conversational ledger search interface enabling analysts to interrogate transaction data in plain English.

---

# Slide 2: Multi-Source Architecture & Signal Detection Flow
**Headline:** Raw Ledger Normalization, Multi-Rule Signal Detection, Composite Scoring, and Conversational Query

### Layout: Horizontal 4-Stage Pipeline Flow
1. **Multi-Source Ingestion & Sanitization**
   - Ingests raw CSV ledger records, customer metadata (tenure, PEP status), and external intelligence feeds (OFAC/WorldCheck watchlists).
   - Smart Auto-Mapping handles messy aliases and regex cleans currency formatting (`$`, commas).
2. **Multi-Signal Detection Matrix (Additive Rules)**
   - **Rule 1 (Sanctions Screen):** External WorldCheck/OFAC watchlist match -> **+40 pts** (Critical).
   - **Rule 2 (PEP Status):** Politically Exposed Person active status -> **+20 pts** (Risk Multiplier).
   - **Rule 3 (Offshore Corridors):** Wire transfers to FATF grey-list jurisdictions (Cayman, Panama, Vanuatu) -> **+25 pts**.
   - **Rule 4 (Structuring / Smurfing):** >= 2 transfers in $8.5k–$10k bracket to evade CTR filing -> **+20 to +30 pts**.
   - **Rule 5 (Velocity Surge):** Volume > $50k on accounts < 3 months old -> **+15 pts** (Mule Account Detection).
3. **Composite Scoring & Action Synthesis**
   - Additive sum clamped strictly to `[0, 100]`: Low (<20), Medium (20-44), High (45-69), Critical (70+).
   - Recommends actionable mandate (e.g. `IMMEDIATE FREEZE & FILE SUSPICIOUS ACTIVITY REPORT (SAR)`).
   - Generates executive 3-sentence AI regulatory narrative explaining root causes.
4. **Natural Language Risk Interrogation**
   - Conversational search box parsing plain-English queries (`Large Wires > $50k`, `Offshore Havens`, `Cash Transactions`, `Total Volume`).
   - Calculates filtered volume metrics and displays formatted sub-tables without hallucinating numbers.

---

# Slide 3: Implementation Highlights & Anti-Vibe Standards
**Headline:** Additive Scoring Integrity, Smart CSV Normalization, and Production-Grade UI

### Left Card: Scoring Integrity & Zero Hallucinations
- **Fully Explainable Additive Scoring:** Every single point in the 0–100 score traces directly back to an immutable transaction ID and rule definition.
- **Strict Boundary Clamping:** Clamped mathematically via `min(100, max(0, raw_score))` preventing score overflow.
- **Zero Regulatory Hallucination:** The AI narrative generator feeds only verified pre-computed signals; it never invents unverified accusations.
- **Smart CSV Parser:** Robust canonical aliasing maps messy column names and strips currencies automatically.

### Right Card: Enterprise Design System
- **Visual Progress Bar:** Real-time visual progress bar color-coded by severity (Emerald -> Amber -> Orange -> Rose).
- **Interactive What-If Sandbox:** Lets analysts manipulate PEP exposure, account age, and ledger rows to observe real-time score shifts.
- **Executive KPI Strip:** Replaced generic notifications with clean metrics: Matches Found (`2 / 5 txs`), Filtered Volume (`$164,000.00`), Share of Volume (`68.0%`).
- **Clean Currency Tables:** Streamlit dataframes format numbers as currency (`$75,000.00`), hide index numbers, and use executive column titles.

---

# Slide 4: Technical Challenges, Edge Cases & Learnings
**Headline:** Resolving Overlapping Query Dimensions, Account Tenure Bias, and Black-Box Audits

### Comparison Table: Challenge vs. Architectural Resolution

| Compliance Challenge | Risk Factor | Engineering Resolution in Nexus |
| :--- | :--- | :--- |
| **Overlapping Query Dimensions** | In Vanguard Maritime, offshore wires were also under $10k. Clicking both filters gave identical results ($38,100), appearing frozen. | Decoupled physical cash from numerical structuring and added 'Large Wires > $50k', making every query dimension completely orthogonal. |
| **Account Tenure Velocity Bias** | Penalizing high transaction volume without age context flags legitimate corporate accounts. | Factored tenure into Rule 5: volume surge penalties apply strictly to accounts < 3 months old, allowing 5-year accounts to transact cleanly. |
| **Explainability vs. Deep Learning** | Complex neural networks produce uninterpretable scores that fail FinCEN/FCA compliance audits. | Built an additive, rule-attributed engine where every point ties directly to verified transactions and regulatory guidelines. |

---

# Slide 5: Demo Summary, Verification & Production Roadmap
**Headline:** Verified AML Prototype Scope and Future Enterprise Roadmap

### Left Card: Delivered & Verified Today
- **30 Banking Scenarios:** Pre-loaded client cases across Sanctions/Havens, Structuring, and Clean Corporate accounts.
- **Multi-Source Aggregation:** Combines transaction CSVs, account tenure, PEP flags, and external sanctions watchlists.
- **What-If Sensitivity Sandbox:** Interactive PEP toggles and tenure sliders enabling live compliance simulation.
- **NL Interrogation Interface:** In-memory natural language query engine computing dynamic volume shares and filtered tables.
- **100% Test Pass Rate:** Verified by 8 automated pytest suites in 0.17 seconds.

### Right Column: Phased Production Roadmap
- **Phase 1 (Streaming Ingestion):** Deploy risk engine as a stateless worker consuming real-time transaction streams from Apache Kafka.
- **Phase 2 (Sliding-Window State):** Track 24-hour, 7-day, and 30-day velocity metrics per account using in-memory Redis sliding windows.
- **Phase 3 (Graph Intelligence & Auto-SAR):** Ingest transaction counterparties into Neo4j graph databases to detect circular smurfing rings, and auto-export pre-filled FinCEN Form 111 SAR packages.
```

---

## PART 3: HOW TO USE THIS IN GAMMA.APP (Step-by-Step)

1. Open [**Gamma.app**](https://gamma.app) (free account).
2. Click **Create New** (top right) $\rightarrow$ select **"Paste in text"**.
3. Under **"What do you want to create?"**, select **Presentation (16:9)**.
4. In the text area:
   - For Deck 1: Copy & paste **PART 1** (Prompt) followed by **DECK A** (Customer Triage).
   - For Deck 2: Copy & paste **PART 1** (Prompt) followed by **DECK B** (Financial Risk).
5. Under **Card by Card Settings**, set the number of cards to **5**.
6. Select a Theme: Choose **"Onyx"**, **"Slate"**, or **"Carbon"** (clean dark tech themes).
7. Click **Generate**!
8. Gamma will generate a presentation with:
   - Real horizontal process flows on Slide 2.
   - Clean 2-column feature breakdowns on Slide 3.
   - Side-by-side comparison tables on Slide 4.
   - Phased roadmap timelines on Slide 5.
9. Click **Share** $\rightarrow$ **Export** $\rightarrow$ **Export to PowerPoint (.pptx)** or **Export to PDF**.
