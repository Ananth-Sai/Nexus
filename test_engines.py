"""
Unit and Integration Tests for Nexus AI Engine Suite
Covers both Workflow Remediation Engine and Financial Risk Signal Aggregator.
"""

import os
import pytest
from workflow_engine import (
    RequestClassifier,
    WorkflowRemediationEngine,
    get_audit_records,
    init_audit_db,
    DB_PATH
)
from risk_engine import (
    FinancialRiskAggregator,
    FlaggedRiskSignal,
    HIGH_RISK_JURISDICTIONS
)


class TestWorkflowRemediationEngine:
    """Tests for Incoming Request Processing Workflow (Assignment 1)."""

    def test_billing_dispute_branch(self):
        text = "Hello, I was charged twice for invoice INV-98124 totaling $149.00. I need a refund immediately!"
        result = WorkflowRemediationEngine.execute(text, sender="sarah@corp.com")
        
        assert result.classification.category == "Billing Dispute"
        assert result.classification.urgency in ["High", "Critical"]
        assert "invoice_id" in result.classification.key_entities
        assert "INV-98124" in result.classification.key_entities["invoice_id"]
        assert len(result.steps_executed) >= 3
        assert "Finance" in result.assigned_queue
        assert result.sla_hours in [4, 12]
        assert "INV-98124" in result.draft_response
        assert result.requires_human_review is True

    def test_technical_escalation_branch(self):
        text = "CRITICAL: The Checkout API server is down with a 500 internal server error! Customers cannot pay!"
        result = WorkflowRemediationEngine.execute(text, sender="monitoring@client.com")
        
        assert result.classification.category == "Technical Escalation"
        assert result.classification.urgency == "Critical"
        assert len(result.steps_executed) >= 3
        assert "Site Reliability Engineering" in result.assigned_queue
        assert result.sla_hours == 1
        assert "Incident ID" in result.draft_response
        assert result.requires_human_review is True

    def test_general_inquiry_branch(self):
        text = "Hi there, could you provide details on what features are included in your business plan?"
        result = WorkflowRemediationEngine.execute(text, sender="lead@prospect.com")
        
        assert result.classification.category == "General Inquiry"
        assert result.classification.urgency == "Normal"
        assert len(result.steps_executed) >= 3
        assert "Customer Support Tier-1" in result.assigned_queue
        assert result.sla_hours == 24
        assert result.requires_human_review is False

    def test_audit_logging_persistence(self):
        test_text = "Test ticket for invoice INV-1122 with amount $500."
        result = WorkflowRemediationEngine.execute(test_text, sender="audit_test@test.com")
        
        records = get_audit_records(limit=10)
        assert len(records) > 0
        latest = records[0]
        assert latest["request_id"] == result.request_id
        assert latest["sender"] == "audit_test@test.com"


class TestFinancialRiskAggregator:
    """Tests for Financial Risk Signal Aggregator (Assignment 2)."""

    def test_structuring_and_jurisdiction_signals(self):
        # 3 transactions just under $10,000 threshold to offshore haven
        transactions = [
            {"tx_id": "TX-101", "amount": 9500.0, "destination_country": "Panama"},
            {"tx_id": "TX-102", "amount": 9800.0, "destination_country": "Panama"},
            {"tx_id": "TX-103", "amount": 9200.0, "destination_country": "Cayman Islands"},
        ]
        account_meta = {
            "account_id": "ACC-7744",
            "customer_name": "Offshore Trade Ltd",
            "jurisdiction": "Panama",
            "pep_status": False,
            "account_tenure_months": 2
        }

        profile = FinancialRiskAggregator.analyze_dataset(transactions, account_meta)

        # Check structuring detection
        signal_rules = [s.rule_name for s in profile.flagged_signals]
        assert any("Structuring" in r for r in signal_rules)
        assert any("High-Risk Jurisdiction" in r for r in signal_rules)
        assert profile.risk_score >= 50
        assert profile.risk_level in ["High", "Critical"]
        assert "Offshore Trade Ltd" in profile.ai_narrative_summary
        assert "SAR" in profile.recommended_action or "OFFICER" in profile.recommended_action

    def test_clean_transaction_profile(self):
        # Normal domestic low-risk transactions
        transactions = [
            {"tx_id": "TX-001", "amount": 120.0, "destination_country": "Domestic"},
            {"tx_id": "TX-002", "amount": 450.0, "destination_country": "Domestic"},
            {"tx_id": "TX-003", "amount": 55.0, "destination_country": "Domestic"},
        ]
        account_meta = {
            "account_id": "ACC-CLEAN-1",
            "customer_name": "John Doe",
            "jurisdiction": "Domestic",
            "pep_status": False,
            "account_tenure_months": 36
        }

        profile = FinancialRiskAggregator.analyze_dataset(transactions, account_meta)

        assert len(profile.flagged_signals) == 0
        assert profile.risk_score == 0
        assert profile.risk_level == "Low"
        assert "STANDARD MONITORING" in profile.recommended_action

    def test_csv_parser(self):
        csv_data = '''tx_id,amount,source_country,destination_country
TX-1,"$9,500.00",USA,Panama
TX-2,1200,UK,Germany
'''
        parsed = FinancialRiskAggregator.parse_csv_transactions(csv_data)
        assert len(parsed) == 2
        assert parsed[0]["amount"] == 9500.0
        assert parsed[1]["amount"] == 1200.0

    def test_natural_language_query_interface(self):
        transactions = [
            {"tx_id": "TX-1", "amount": 9500.0, "destination_country": "Panama"},
            {"tx_id": "TX-2", "amount": 1200.0, "destination_country": "Domestic"},
            {"tx_id": "TX-3", "amount": 9800.0, "destination_country": "Cayman Islands"},
        ]
        
        # Test threshold query
        res1 = FinancialRiskAggregator.query_transactions(transactions, "Show wires over 9000")
        assert res1["total_matched"] == 2
        assert "exceeding $9,000.00" in res1["answer"]

        # Test offshore query
        res2 = FinancialRiskAggregator.query_transactions(transactions, "Which transactions went to offshore havens?")
        assert res2["total_matched"] == 2
        assert "Panama" in res2["answer"] or "Cayman" in res2["answer"]

        # Test total volume query
        res3 = FinancialRiskAggregator.query_transactions(transactions, "What is the total volume?")
        assert res3["total_matched"] == 3
        assert "$20,500.00" in res3["answer"]
