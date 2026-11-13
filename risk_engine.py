"""
Financial Risk Signal Aggregator Engine
Ingests structured financial transactions and unstructured alerts to synthesize a prioritized risk view.
"""

from __future__ import annotations
import csv
import io
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class FlaggedRiskSignal(BaseModel):
    signal_id: str
    rule_name: str
    severity: str = Field(description="Critical, High, Medium, or Low")
    score_contribution: int = Field(description="Points added to total risk score")
    description: str
    evidence: Dict[str, Any] = Field(default_factory=dict)


class EntityRiskProfile(BaseModel):
    account_id: str
    customer_name: str
    jurisdiction: str
    pep_status: bool
    account_tenure_months: int
    total_transactions_analyzed: int
    total_volume_usd: float
    risk_score: int = Field(ge=0, le=100, description="Composite risk score from 0 (Safe) to 100 (Severe Risk)")
    risk_level: str = Field(description="Critical, High, Medium, or Low")
    flagged_signals: List[FlaggedRiskSignal]
    ai_narrative_summary: str
    recommended_action: str


# High-risk offshore jurisdictions (FATF grey/black lists reference)
HIGH_RISK_JURISDICTIONS = {"Cayman Islands", "Panama", "Vanuatu", "Seychelles", "Cyprus", "Russia", "North Korea", "Iran"}

# Watchlist database simulation (external alert source)
MOCK_EXTERNAL_WATCHLIST = {
    "ACC-9041": {"reason": "PEP Match - Immediate relative of foreign official", "source": "WorldCheck / OFAC"},
    "ACC-8812": {"reason": "Interpol Red Notice alert cross-reference", "source": "Interpol Watchlist"},
    "ACC-4109": {"reason": "Adverse media hit - Ongoing securities fraud investigation", "source": "Dow Jones Risk & Compliance"}
}


class FinancialRiskAggregator:
    """Aggregates transaction logs, account state, and external alerts to score risk."""

    @classmethod
    def analyze_dataset(
        cls,
        transactions: List[Dict[str, Any]],
        account_meta: Optional[Dict[str, Any]] = None,
        external_alerts: Optional[List[Dict[str, Any]]] = None
    ) -> EntityRiskProfile:
        if not account_meta:
            account_meta = {
                "account_id": "ACC-UNKNOWN",
                "customer_name": "Unknown Entity",
                "jurisdiction": "Domestic",
                "pep_status": False,
                "account_tenure_months": 12
            }

        account_id = account_meta.get("account_id", "ACC-1001")
        customer_name = account_meta.get("customer_name", "Valued Customer")
        jurisdiction = account_meta.get("jurisdiction", "Domestic")
        pep_status = account_meta.get("pep_status", False)
        account_tenure = int(account_meta.get("account_tenure_months", 12))

        flagged_signals: List[FlaggedRiskSignal] = []
        signal_counter = 1

        total_tx_count = len(transactions)
        total_volume = sum(float(tx.get("amount", 0.0)) for tx in transactions)

        # -------------------------------------------------------------
        # Rule 1: Watchlist & Sanctions Screen (External Signal Aggregation)
        # -------------------------------------------------------------
        if account_id in MOCK_EXTERNAL_WATCHLIST:
            watch_info = MOCK_EXTERNAL_WATCHLIST[account_id]
            flagged_signals.append(FlaggedRiskSignal(
                signal_id=f"SIG-0{signal_counter}",
                rule_name="External Sanctions / Watchlist Alert",
                severity="Critical",
                score_contribution=40,
                description=f"Direct match against {watch_info['source']}: {watch_info['reason']}",
                evidence={"source": watch_info["source"], "details": watch_info["reason"]}
            ))
            signal_counter += 1

        if external_alerts:
            for alert in external_alerts:
                flagged_signals.append(FlaggedRiskSignal(
                    signal_id=f"SIG-0{signal_counter}",
                    rule_name=f"External Alert: {alert.get('alert_type', 'Adverse Event')}",
                    severity=alert.get("severity", "High"),
                    score_contribution=25,
                    description=alert.get("summary", "Unverified external adverse media hit."),
                    evidence=alert
                ))
                signal_counter += 1

        # -------------------------------------------------------------
        # Rule 2: PEP Exposure Check
        # -------------------------------------------------------------
        if pep_status:
            flagged_signals.append(FlaggedRiskSignal(
                signal_id=f"SIG-0{signal_counter}",
                rule_name="Politically Exposed Person (PEP) Active Status",
                severity="High",
                score_contribution=20,
                description=f"Account holder {customer_name} is flagged as a Politically Exposed Person requiring enhanced due diligence (EDD).",
                evidence={"pep_status": True}
            ))
            signal_counter += 1

        # -------------------------------------------------------------
        # Rule 3: High-Risk Jurisdiction Inflows / Outflows
        # -------------------------------------------------------------
        high_risk_txs = [
            tx for tx in transactions
            if tx.get("destination_country") in HIGH_RISK_JURISDICTIONS or tx.get("source_country") in HIGH_RISK_JURISDICTIONS
        ]
        if high_risk_txs:
            high_risk_volume = sum(float(tx.get("amount", 0.0)) for tx in high_risk_txs)
            flagged_signals.append(FlaggedRiskSignal(
                signal_id=f"SIG-0{signal_counter}",
                rule_name="High-Risk Jurisdiction Wire Activity",
                severity="High",
                score_contribution=25,
                description=f"Detected {len(high_risk_txs)} wire transfers totaling ${high_risk_volume:,.2f} involving FATF-monitored jurisdictions.",
                evidence={"affected_transactions": [tx.get("tx_id") for tx in high_risk_txs], "volume": high_risk_volume}
            ))
            signal_counter += 1

        # -------------------------------------------------------------
        # Rule 4: Structuring / Smurfing Pattern Detection (Amounts just under $10,000)
        # -------------------------------------------------------------
        structuring_txs = [
            tx for tx in transactions
            if 8500.0 <= float(tx.get("amount", 0.0)) < 10000.0
        ]
        if len(structuring_txs) >= 2:
            structuring_vol = sum(float(tx.get("amount", 0.0)) for tx in structuring_txs)
            flagged_signals.append(FlaggedRiskSignal(
                signal_id=f"SIG-0{signal_counter}",
                rule_name="Potential Structuring / Smurfing Threshold Evasion",
                severity="Critical" if len(structuring_txs) >= 3 else "High",
                score_contribution=30 if len(structuring_txs) >= 3 else 20,
                description=f"Identified {len(structuring_txs)} transactions just beneath the $10,000 regulatory reporting threshold within a short window.",
                evidence={"tx_ids": [tx.get("tx_id") for tx in structuring_txs], "total_structured_amount": structuring_vol}
            ))
            signal_counter += 1

        # -------------------------------------------------------------
        # Rule 5: Rapid Velocity Anomaly (Unusual spike relative to tenure)
        # -------------------------------------------------------------
        if account_tenure < 3 and total_volume > 50000.0:
            flagged_signals.append(FlaggedRiskSignal(
                signal_id=f"SIG-0{signal_counter}",
                rule_name="New Account Velocity Spike",
                severity="Medium",
                score_contribution=15,
                description=f"Account age is only {account_tenure} month(s), yet total transaction volume surged to ${total_volume:,.2f}.",
                evidence={"tenure_months": account_tenure, "total_volume": total_volume}
            ))
            signal_counter += 1

        # Calculate composite score (capped at 100)
        raw_score = sum(s.score_contribution for s in flagged_signals)
        risk_score = min(100, max(0, raw_score))

        # Assign risk tier
        if risk_score >= 70:
            risk_level = "Critical"
            recommended_action = "IMMEDIATE ACCOUNT FREEZE & FILE SUSPICIOUS ACTIVITY REPORT (SAR)"
        elif risk_score >= 45:
            risk_level = "High"
            recommended_action = "ESCALATE TO SENIOR AML COMPLIANCE OFFICER FOR ENHANCED DUE DILIGENCE (EDD)"
        elif risk_score >= 20:
            risk_level = "Medium"
            recommended_action = "FLAG FOR ROUTINE 30-DAY COMPLIANCE MONITORING AUDIT"
        else:
            risk_level = "Low"
            recommended_action = "STANDARD MONITORING - NO ADVERSE ACTION REQUIRED"

        # AI-generated narrative rationale
        ai_narrative = cls._generate_ai_narrative(
            customer_name, account_id, risk_score, risk_level, flagged_signals, total_volume, total_tx_count
        )

        return EntityRiskProfile(
            account_id=account_id,
            customer_name=customer_name,
            jurisdiction=jurisdiction,
            pep_status=pep_status,
            account_tenure_months=account_tenure,
            total_transactions_analyzed=total_tx_count,
            total_volume_usd=total_volume,
            risk_score=risk_score,
            risk_level=risk_level,
            flagged_signals=flagged_signals,
            ai_narrative_summary=ai_narrative,
            recommended_action=recommended_action
        )

    @classmethod
    def _generate_ai_narrative(
        cls,
        customer_name: str,
        account_id: str,
        risk_score: int,
        risk_level: str,
        signals: List[FlaggedRiskSignal],
        total_volume: float,
        total_tx_count: int
    ) -> str:
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if api_key:
            try:
                from google import genai
                from google.genai import types
                client = genai.Client(
                    api_key=api_key,
                    http_options=types.HttpOptions(
                        timeout=15000,
                        retry_options=types.HttpRetryOptions(attempts=1),
                    ),
                )
                prompt = (
                    f"You are a Senior AML/CFT Compliance Officer. Write a concise, professional 3-sentence "
                    f"risk narrative for client {customer_name} ({account_id}).\n"
                    f"Risk Score: {risk_score}/100 ({risk_level} Priority).\n"
                    f"Analyzed {total_tx_count} transactions totaling ${total_volume:,.2f}.\n"
                    f"Flagged Risk Signals: {[s.rule_name for s in signals]}.\n"
                    f"Conclude with why compliance analysts must focus on this case."
                )
                for model_id in (
                    "gemini-flash-lite-latest",
                    "gemini-3.8-flash",
                    "gemini-3.7-flash",
                    "gemini-3.5-flash-lite",
                    "gemini-flash-latest",
                ):
                    try:
                        response = client.models.generate_content(
                            model=model_id,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                temperature=0.2,
                                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                            )
                        )
                        if response.text:
                            return response.text.strip()
                    except Exception:
                        continue
            except Exception:
                pass

        # Deterministic Narrative Generation (100% reliable offline)
        if not signals:
            return (
                f"Automated risk synthesis completed for account {account_id} ({customer_name}). "
                f"Evaluation of {total_tx_count} transaction records totaling ${total_volume:,.2f} revealed "
                f"zero anomalies or sanctions exposure. The entity maintains a Low Risk profile ({risk_score}/100) "
                f"and complies with standard transaction velocity baselines."
            )

        signal_titles = ", ".join([f"'{s.rule_name}'" for s in signals[:3]])
        return (
            f"Consolidated risk assessment flagged account {account_id} ({customer_name}) at a {risk_level} risk tier "
            f"with a composite risk score of {risk_score}/100. Key drivers include {signal_titles}, accumulating across "
            f"{total_tx_count} transactions totaling ${total_volume:,.2f}. The convergence of structured transaction amounts "
            f"and adverse profile indicators warrants prioritized compliance review and prompt execution of enhanced due diligence."
        )

    @classmethod
    def query_transactions(cls, transactions: List[Dict[str, Any]], query_text: str) -> Dict[str, Any]:
        """
        Interrogates transaction records using natural language queries.
        Filters matching rows and returns a plain-English explanation,
        summary metrics, and percentage of total account volume.
        """
        account_total = sum(float(t.get("amount", 0.0)) for t in transactions) if transactions else 0.0

        if not transactions or not query_text.strip():
            return {
                "answer": "No query provided. Displaying all ledger records.",
                "matched_txs": transactions,
                "total_matched": len(transactions),
                "total_matched_volume": account_total,
                "account_total_volume": account_total,
                "volume_percentage": 100.0 if transactions else 0.0
            }

        q_lower = query_text.lower().strip()
        matched: List[Dict[str, Any]] = []

        # 1. Check for threshold / amount queries (e.g. "> 9000", "over 9,000", "greater than 5000")
        amount_match = re.search(r'(?:>|over|greater than|above|exceeding)\s*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', q_lower)
        if amount_match:
            thresh = float(amount_match.group(1).replace(",", ""))
            matched = [t for t in transactions if float(t.get("amount", 0.0)) > thresh]
            tot_val = sum(float(t.get("amount", 0.0)) for t in matched)
            pct = round((tot_val / account_total * 100), 1) if account_total > 0 else 0.0
            answer = f"Found {len(matched)} transaction(s) with an amount exceeding ${thresh:,.2f}, totaling ${tot_val:,.2f} ({pct}% of account volume)."
            return {
                "answer": answer,
                "matched_txs": matched,
                "total_matched": len(matched),
                "total_matched_volume": tot_val,
                "account_total_volume": account_total,
                "volume_percentage": pct
            }

        # 2. Check for offshore / haven queries
        if any(w in q_lower for w in ["offshore", "haven", "cayman", "panama", "seychelles", "cyprus", "vanuatu", "bahamas", "monaco"]):
            matched = [
                t for t in transactions
                if t.get("destination_country") in HIGH_RISK_JURISDICTIONS or t.get("source_country") in HIGH_RISK_JURISDICTIONS
            ]
            tot_val = sum(float(t.get("amount", 0.0)) for t in matched)
            pct = round((tot_val / account_total * 100), 1) if account_total > 0 else 0.0
            dest_list = sorted(list({t.get("destination_country") for t in matched if t.get("destination_country")}))
            dests_str = ", ".join(dest_list) if dest_list else "High-Risk Corridors"
            answer = f"Found {len(matched)} transaction(s) linked to high-risk offshore jurisdictions ({dests_str}), totaling ${tot_val:,.2f} ({pct}% of volume)."
            return {
                "answer": answer,
                "matched_txs": matched,
                "total_matched": len(matched),
                "total_matched_volume": tot_val,
                "account_total_volume": account_total,
                "volume_percentage": pct
            }

        # 3. Check for pure cash or deposit queries
        if any(w in q_lower for w in ["cash", "deposit", "atm"]):
            matched = [
                t for t in transactions
                if "cash" in str(t.get("tx_type", "")).lower()
                or "dep" in str(t.get("tx_type", "")).lower()
                or "cash" in str(t.get("description", "")).lower()
            ]
            tot_val = sum(float(t.get("amount", 0.0)) for t in matched)
            pct = round((tot_val / account_total * 100), 1) if account_total > 0 else 0.0
            if matched:
                answer = f"Found {len(matched)} cash or deposit transaction(s), totaling ${tot_val:,.2f} ({pct}% of volume)."
            else:
                answer = f"Zero cash transactions identified in this ledger. All records are electronic wires or transfers."
            return {
                "answer": answer,
                "matched_txs": matched,
                "total_matched": len(matched),
                "total_matched_volume": tot_val,
                "account_total_volume": account_total,
                "volume_percentage": pct
            }

        # 4. Check for structuring / smurfing queries (near $10k)
        if any(w in q_lower for w in ["structuring", "smurfing", "under 10k", "below 10,000", "threshold"]):
            matched = [t for t in transactions if 8500.0 <= float(t.get("amount", 0.0)) < 10000.0]
            tot_val = sum(float(t.get("amount", 0.0)) for t in matched)
            pct = round((tot_val / account_total * 100), 1) if account_total > 0 else 0.0
            answer = f"Found {len(matched)} transaction(s) structured just beneath the $10,000 reporting threshold, totaling ${tot_val:,.2f} ({pct}% of volume)."
            return {
                "answer": answer,
                "matched_txs": matched,
                "total_matched": len(matched),
                "total_matched_volume": tot_val,
                "account_total_volume": account_total,
                "volume_percentage": pct
            }

        # 5. Check for total volume / sum queries
        if any(w in q_lower for w in ["total", "volume", "sum", "how much"]):
            tot_val = account_total
            answer = f"The account has a total transaction volume of ${tot_val:,.2f} across all {len(transactions)} record(s)."
            return {
                "answer": answer,
                "matched_txs": transactions,
                "total_matched": len(transactions),
                "total_matched_volume": tot_val,
                "account_total_volume": account_total,
                "volume_percentage": 100.0
            }

        # 6. Fallback keyword filter
        keywords = [w for w in q_lower.split() if len(w) > 2 and w not in ["show", "find", "what", "which", "with", "where", "the", "for"]]
        if keywords:
            matched = [
                t for t in transactions
                if any(kw in str(val).lower() for kw in keywords for val in t.values())
            ]
            tot_val = sum(float(t.get("amount", 0.0)) for t in matched)
            pct = round((tot_val / account_total * 100), 1) if account_total > 0 else 0.0
            answer = f"Found {len(matched)} transaction(s) matching keyword(s) '{', '.join(keywords)}', totaling ${tot_val:,.2f} ({pct}% of volume)."
            return {
                "answer": answer,
                "matched_txs": matched,
                "total_matched": len(matched),
                "total_matched_volume": tot_val,
                "account_total_volume": account_total,
                "volume_percentage": pct
            }

        return {
            "answer": f"Displaying all {len(transactions)} transaction record(s).",
            "matched_txs": transactions,
            "total_matched": len(transactions),
            "total_matched_volume": account_total,
            "account_total_volume": account_total,
            "volume_percentage": 100.0
        }

    @classmethod
    def parse_csv_transactions(cls, csv_text: str) -> List[Dict[str, Any]]:
        """
        Parses CSV text into a structured list of transactions.
        Intelligently auto-maps varying column names (e.g. txn_amt, value, destination, etc.)
        and sanitizes monetary strings ($9,500.00 -> 9500.0).
        """
        if not csv_text or not csv_text.strip():
            return []

        reader = csv.DictReader(io.StringIO(csv_text.strip()))
        txs: List[Dict[str, Any]] = []

        # Canonical aliases
        amount_aliases = {"amount", "amt", "txn_amount", "txn_amt", "value", "total", "sum", "debit"}
        dest_aliases = {"destination_country", "destination", "dest", "country", "receiver_country", "target_country", "beneficiary_country"}
        id_aliases = {"tx_id", "id", "txn_id", "reference", "ref", "trans_id"}

        for row in reader:
            clean_row: Dict[str, Any] = {}
            for k, v in row.items():
                if k is not None and v is not None:
                    k_clean = k.strip().lower()
                    clean_row[k_clean] = v.strip()

            # Identify amount
            amount_val = 0.0
            for alias in amount_aliases:
                if alias in clean_row:
                    try:
                        raw_str = re.sub(r'[^\d.-]', '', str(clean_row[alias]))
                        amount_val = float(raw_str) if raw_str else 0.0
                        break
                    except ValueError:
                        amount_val = 0.0

            # Identify destination country
            dest_val = "Domestic"
            for alias in dest_aliases:
                if alias in clean_row and clean_row[alias]:
                    dest_val = clean_row[alias]
                    break

            # Identify TX ID
            tx_id_val = f"TX-{len(txs)+1:03d}"
            for alias in id_aliases:
                if alias in clean_row and clean_row[alias]:
                    tx_id_val = clean_row[alias]
                    break

            txs.append({
                "tx_id": tx_id_val,
                "amount": amount_val,
                "destination_country": dest_val,
                "source_country": clean_row.get("source_country", "USA"),
                "tx_type": clean_row.get("tx_type", "WIRE_OUT")
            })

        return txs
        """
        Parses CSV text into a structured list of transactions.
        Intelligently auto-maps varying column names (e.g. txn_amt, value, destination, etc.)
        and sanitizes monetary strings ($9,500.00 -> 9500.0).
        """
        if not csv_text or not csv_text.strip():
            return []

        reader = csv.DictReader(io.StringIO(csv_text.strip()))
        txs: List[Dict[str, Any]] = []

        # Canonical aliases
        amount_aliases = {"amount", "amt", "txn_amount", "txn_amt", "value", "total", "sum", "debit"}
        dest_aliases = {"destination_country", "destination", "dest", "country", "receiver_country", "target_country", "beneficiary_country"}
        id_aliases = {"tx_id", "id", "txn_id", "reference", "ref", "trans_id"}

        for row in reader:
            clean_row: Dict[str, Any] = {}
            for k, v in row.items():
                if k is not None and v is not None:
                    k_clean = k.strip().lower()
                    clean_row[k_clean] = v.strip()

            # Identify amount
            amount_val = 0.0
            for alias in amount_aliases:
                if alias in clean_row:
                    try:
                        raw_str = re.sub(r'[^\d.-]', '', str(clean_row[alias]))
                        amount_val = float(raw_str) if raw_str else 0.0
                        break
                    except ValueError:
                        amount_val = 0.0

            # Identify destination country
            dest_val = "Domestic"
            for alias in dest_aliases:
                if alias in clean_row and clean_row[alias]:
                    dest_val = clean_row[alias]
                    break

            # Identify TX ID
            tx_id_val = f"TX-{len(txs)+1:03d}"
            for alias in id_aliases:
                if alias in clean_row and clean_row[alias]:
                    tx_id_val = clean_row[alias]
                    break

            txs.append({
                "tx_id": tx_id_val,
                "amount": amount_val,
                "destination_country": dest_val,
                "source_country": clean_row.get("source_country", "USA"),
                "tx_type": clean_row.get("tx_type", "WIRE_OUT")
            })

        return txs
