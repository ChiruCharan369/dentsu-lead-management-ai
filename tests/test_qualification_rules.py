from types import SimpleNamespace
from unittest.mock import patch

from app.services.company_resolver import normalize_company
from app.services.icp_service import get_icp_data
from app.services.intent_service import classify_intent


def test_normalize_company_prefers_provided_company_over_domain():
    assert normalize_company("Acme Corp", "john@contoso.com") == "acme corp"


def test_placeholder_company_name_is_treated_as_empty():
    assert normalize_company("Tech Innovators", "") == ""


def test_empty_company_returns_safe_icp_fallback_without_llm():
    response = get_icp_data("", "")

    assert response.ICPParentCompany == ""
    assert response.ICPFitStatus == "Not Fit"
    assert response.ICPFitmentTest == "ICP non Fitment"


def test_empty_or_no_comment_with_high_revenue_is_qualified():
    with patch("app.services.intent_service.llm.invoke", return_value=SimpleNamespace(content="non qualified")):
        result = classify_intent({
            "company": "Example Corp",
            "Comments": "",
            "ICPRevenueUSD": "5M",
        })

    assert result["result"] == "qualified"
    assert "high revenue" in result["reason"]


def test_service_provider_message_is_rejected_even_if_llm_says_qualified():
    with patch("app.services.intent_service.llm.invoke", return_value=SimpleNamespace(content="qualified")):
        result = classify_intent({
            "comment": "We offer SEO and backlink services to help your agency grow."
        })

    assert result["result"] == "non qualified"
    assert "selling services" in result["reason"]


def test_gibberish_message_is_rejected_even_if_llm_says_qualified():
    with patch("app.services.intent_service.llm.invoke", return_value=SimpleNamespace(content="qualified")):
        result = classify_intent({
            "comment": "asdf qwer zzz"
        })

    assert result["result"] == "non qualified"
    assert "gibberish" in result["reason"]


def test_gibberish_first_or_last_name_is_rejected_before_llm():
    with patch("app.services.intent_service.llm.invoke", return_value=SimpleNamespace(content="qualified")):
        result = classify_intent({
            "FirstName": "BkJJOjbibkexDzHtpHunw",
            "LastName": "PyuSuLoVdOCEflHm",
            "comment": "2026-07-20 19:54:08 (BST) eXVxJIrnoyDeMIhuPVy2026-07-20 19:54:38 (BST) dqXbGKNGxwirKcXSeW *Marketing"
        })

    assert result["result"] == "non qualified"
    assert "sender name" in result["reason"]


def test_placeholder_name_fields_are_rejected_before_llm():
    with patch("app.services.intent_service.llm.invoke", return_value=SimpleNamespace(content="qualified")):
        result = classify_intent({
            "FirstName": "#sym:FirstName",
            "LastName": "#sym:LastName",
            "comment": "This is a placeholder submission"
        })

    assert result["result"] == "non qualified"
    assert "placeholder" in result["reason"]
