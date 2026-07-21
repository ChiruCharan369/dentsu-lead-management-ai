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

    assert result == "qualified"


def test_service_provider_message_is_rejected_even_if_llm_says_qualified():
    with patch("app.services.intent_service.llm.invoke", return_value=SimpleNamespace(content="qualified")):
        result = classify_intent({
            "comment": "We offer SEO and backlink services to help your agency grow."
        })

    assert result == "non qualified"


def test_gibberish_message_is_rejected_even_if_llm_says_qualified():
    with patch("app.services.intent_service.llm.invoke", return_value=SimpleNamespace(content="qualified")):
        result = classify_intent({
            "comment": "asdf qwer zzz"
        })

    assert result == "non qualified"
