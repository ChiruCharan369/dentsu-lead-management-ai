import re


PUBLIC_EMAIL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "live.com",
    "icloud.com",
    "aol.com",
    "protonmail.com",
    "zoho.com",
    "yandex.com",
    "gmx.com",
}


def extract_domain_from_email(email: str) -> str:

    if not email:
        return ""

    email = email.strip().lower()

    match = re.search(r'@([a-z0-9.-]+\.[a-z]{2,})$', email)

    if not match:
        return ""

    domain = match.group(1)

    return domain


def is_public_email(domain: str) -> bool:

    if not domain:
        return True

    return domain in PUBLIC_EMAIL_DOMAINS


def get_company_from_domain(domain: str) -> str:

    if not domain:
        return ""

    parts = domain.split(".")

    if len(parts) >= 2:
        name = parts[-2]
    else:
        name = parts[0]

    return name.lower()


def _is_placeholder_company(value: str) -> bool:
    if not value:
        return True

    normalized = re.sub(r"[^a-z0-9]+", "", (value or "").strip().lower())
    placeholder_values = {
        "",
        "none",
        "na",
        "n/a",
        "null",
        "test",
        "abc",
        "xyz",
        "sample",
        "example",
        "testcompany",
        "xyzcorp",
        "techinnovators",
        "techinnovatorsinc",
        "innovators",
        "innovatorsinc",
        "techcompany",
    }
    return normalized in placeholder_values or normalized.startswith("techinnovators")


def normalize_company(company: str, email: str) -> str:

    company = (company or "").strip()
    email = (email or "").lower().strip()

    if not _is_placeholder_company(company):
        return company.lower().strip()

    # 1. get domain from email
    domain = extract_domain_from_email(email)

    # 2. if public email and no company → use nothing
    if domain and is_public_email(domain):
        return ""

    # 3. if company email → use domain as fallback
    if domain and not is_public_email(domain):
        name = get_company_from_domain(domain)
        if name:
            return name

    return ""