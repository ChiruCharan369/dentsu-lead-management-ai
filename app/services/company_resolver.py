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


def normalize_company(company: str, email: str) -> str:

    company = (company or "").lower().strip()
    email = (email or "").lower().strip()

    # 1. get domain from email
    domain = extract_domain_from_email(email)

    # 2. if gmail / yahoo / etc → use company
    if domain and is_public_email(domain):

        if company:
            return company

        return ""

    # 3. if company email → use domain
    if domain and not is_public_email(domain):

        name = get_company_from_domain(domain)

        if name:
            return name

    # 4. fallback company
    if company:
        return company

    return ""