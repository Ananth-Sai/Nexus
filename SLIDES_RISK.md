# 5-Slide Presentation Deck: Financial Risk Signal Aggregator
*Format: Presentation Slide Content (Five Slides Structure)*

---

## Slide 1: PROBLEM UNDERSTANDING AND OBJECTIVE

### Headline
Consolidating Fragmented Financial Signals into an Actionable Risk View

### Problem Statement
* Compliance and AML analysts at financial institutions manually review thousands of disconnected transaction alerts, customer KYC profiles, and external watchlists daily.
* Data is siloed: transaction ledgers exist in one system, sanctions watchlists in another, and adverse news alerts in another.
* Manual cross-referencing is slow, leads to high false-positive fatigue, and relies heavily on subjective analyst judgment, creating severe regulatory exposure.

### Core Objectives
1. Ingest structured and unstructured data across multiple sources (transactions, account KYC profiles, external watchlists).
2. Synthesize fragmented risk indicators into an automated multi-signal detection pipeline.
3. Compute a quantitative, transparent **Risk Score (0–100)** and **Priority Ranking** (Critical, High, Medium, Low).
4. Generate an executive **AI Compliance Narrative Rationale** explaining why an account was flagged.
5. Provide actionable recommendations (e.g., Immediate Account Freeze & SAR filing vs. Standard Monitoring).

---

## Slide 2: SOLUTION ARCHITECTURE AND DESIGN FLOW

### System Architecture & Data Flow

```
[Transaction CSV Records] + [Customer KYC Profile] + [External Watchlists/PEP]
                                    │
                                    ▼
                     [Data Normalization & Parser]
                                    │
                                    ▼
                   [Multi-Signal Detection Pipeline]
    ├─ Structuring / Smurfing Rule ($8,500 - $9,999 Threshold Evasion)
    ├─ FATF High-Risk Jurisdiction Wire Rule (Panama, Cayman, etc.)
    ├─ Politically Exposed Person (PEP) Active Exposure Rule
    ├─ Account Velocity Anomaly Rule (Volume surge on new accounts)
    └─ External Watchlist / Sanctions Hit Rule (OFAC / Interpol / Dow Jones)
                                    │
                                    ▼
                    [Composite Risk Scoring Engine]
               (0 - 100 Calibrated Score + Priority Tier)
                                    │
                                    ▼
                [AI Compliance Officer Narrative Generator]
                                    │
                                    ▼
             [Interactive Streamlit Compliance Officer Portal]
```

---

## Slide 3: IMPLEMENTATION HIGHLIGHTS

### Technical Architecture & Logic

* **Multi-Source Data Ingestion:**
  * Handles raw CSV transaction records with robust numerical cleaning (sanitizes commas, currency symbols, and missing fields).
  * Ingests contextual account metadata (tenure, PEP status, jurisdiction) and external watchlist feeds.

* **Quantitative Scoring Matrix:**
  * Each triggered signal carries an explicit, calibrated score contribution:
    * External Sanctions / Watchlist hit: **+40 points**
    * Structuring / Smurfing pattern ($\ge 3$ transactions under \$10K): **+30 points**
    * High-risk offshore jurisdiction transfers: **+25 points**
    * PEP active status: **+20 points**
    * Rapid velocity surge on new accounts ($<3$ months old): **+15 points**
  * Risk Tiers: Critical ($\ge 70$), High ($\ge 45$), Medium ($\ge 20$), Low ($<20$).

* **AI Narrative Generation:**
  * Uses zero-temperature Gemini API prompting (with a deterministic compliance template fallback when offline) to produce a concise 3-sentence executive rationale formatted specifically for compliance auditors.

---

## Slide 4: CHALLENGES AND LEARNINGS

### Key Technical Challenges & Trade-offs

1. **Trade-off: Explainability vs. Black-Box Machine Learning**
   * *Challenge:* Pure neural network anomaly models produce uninterpretable risk scores that fail regulatory compliance audits (e.g., FinCEN / FCA explainability requirements).
   * *Resolution:* Built an additive, rule-attributed scoring engine where every single point in the risk score is mapped directly back to an auditable signal and transaction evidence.

2. **Handling Fragmented Data Formats**
   * *Challenge:* Real-world transactions contain varied currencies, unformatted numbers, and inconsistent country naming conventions.
   * *Resolution:* Implemented a resilient data normalization layer that cleans dirty CSV inputs and handles edge cases gracefully.

3. **False Positive Mitigation**
   * *Challenge:* A single high-value transaction shouldn't trigger an account freeze if the customer has a 5-year clean history.
   * *Resolution:* Factored account tenure and baseline volume into anomaly detection thresholds to prevent false alarms on established corporate accounts.

---

## Slide 5: DEMO SUMMARY AND NEXT STEPS

### Prototype Summary
* Fully functioning, end-to-end prototype deployed on Render / Streamlit.
* Pre-loaded with two contrasting realistic scenarios:
  * **Scenario A:** High-Risk Offshore Structuring & PEP (Score: 85/100, Critical Tier $\rightarrow$ Immediate SAR filing).
  * **Scenario B:** Clean Retail Account (Score: 0/100, Low Tier $\rightarrow$ Standard monitoring).
* Visualized metric cards, flagged signal evidence breakdown, and ingested transaction explorer.

### Next Steps & Future Enhancements
1. **Graph Network Analysis:** Map transaction counterparties using graph databases (Neo4j) to detect cyclical money laundering rings.
2. **Natural Language Query Interface:** Add an AI search bar allowing compliance officers to interrogate transaction history in plain English (*"Show all wires over $5,000 to offshore accounts in November"*).
3. **Automated SAR Generation:** Auto-fill standardized FinCEN Form 111 XML reports ready for regulatory filing.

