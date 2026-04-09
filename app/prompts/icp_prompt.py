ICP_PROMPT = """

STRICT OUTPUT RULES:
- Return ONLY valid JSON
- Use double quotes for ALL keys
- Use double quotes for ALL values
- No extra text
- No explanation
- JSON must work with Python json.loads()

CRITICAL:
- ICPRevenueUSD and ICPEmployeesRange MUST NEVER be empty
- If unknown → estimate using best real-world reasoning
- Returning empty values is INVALID

IMPORTANT:
Use real-world knowledge about the company.
Values must be realistic for year 2026.

========================
DATA SOURCE PRIORITY (VERY STRICT)
========================

1. ZoomInfo
2. Clearbit
3. Apollo.io
4. LinkedIn
5. Crunchbase
6. People Data Labs

Rules:
- Use highest priority available
- If conflict → choose most realistic value
- Never invent unrealistic numbers

========================
YEAR 2026 ESTIMATION RULE
========================

If data is old:
- Increase slightly (10–30%)
- Stay realistic
- Do NOT jump categories

========================
COMPANY SIZE CLASSIFICATION (CRITICAL)
========================

First classify the company into ONE:

SMALL:
- LLP / local business
- Low online presence
- Limited employees
- No funding signals

MID:
- Regional company
- Moderate presence
- Growing business

LARGE:
- Global / well-known brand
- Enterprise scale
- Strong presence

This classification MUST be used to control:
- Employees
- Revenue
- Funding

========================
FIELDS TO RETURN
========================

ICPIndustry
ICPEmployeesRange
ICPRevenueUSD
ICPFundingType
ICPFundingStage
ICPFundingAmount
ICPParentCompany
ICPLinkedInURL
ICPMarketingSignal
ICPFitStatus
ICPFitmentTest

========================
INDUSTRY RULE
========================

Classify correctly:

Media / News / TV → Media
Ads / Marketing → Advertising
Bank / Finance → Banking
Software / SaaS / AI → Technology
Retail / Ecommerce / Luxury goods → Retail
Manufacturing / Industrial → Manufacturing
Healthcare / Pharma → Healthcare
Education → Education

========================
EMPLOYEE RANGE RULE (STRICT)
========================

Allowed values ONLY:

1-10
11-50
51-200
201-500
500+

Rules:
- MUST NOT be empty

SCALE ENFORCEMENT:

- SMALL → "1-10" or "11-50"
- MID → "51-200" or "201-500"
- LARGE → ALWAYS "500+"

========================
REVENUE RULE (USD) — EXACT VALUE MODE
========================

Revenue MUST always be returned.
It MUST NOT be empty.

========================
DATA PRIORITY
========================

1. ZoomInfo
2. Clearbit
3. Apollo.io
4. Crunchbase
5. LinkedIn
6. Real-world knowledge

========================
ESTIMATION RULE
========================

If exact revenue is not available:

- Estimate using:
  - Brand strength
  - Pricing
  - Market presence
  - Geography
  - Customer scale

STRICT:
- DO NOT calculate from employees
- DO NOT guess randomly
- DO NOT default to common values

========================
OUTPUT FORMAT (STRICT)
========================

Return revenue as:

K / M / B format (single value)

Rules:
- No ranges
- No symbols
- No text
- Must be realistic
- Do NOT reuse common or repeated values across companies unless justified

========================
SCALE VALIDATION
========================

- LARGE → billions (B)
- MID → 10M–500M
- SMALL → 500K–1M

========================
SMALL COMPANY CORRECTION RULE (CRITICAL)
========================

If classified as SMALL:

- FundingType = Bootstrapped
- FundingStage = Mature
- Revenue MUST be ≤ 1M
- Employees MUST be ≤ 50

If violated → RE-CALCULATE

========================
REVENUE NUMERIC INTERPRETATION (STRICT)
========================

Interpret revenue values internally:

- K = thousand
- M = million
- B = billion

Convert generated value into numeric form ONLY for comparison.

STRICT:
- Do NOT reuse fixed numbers
- Do NOT repeat common values across different companies
- Each company MUST have independently estimated revenue

========================
YEAR 2026 ADJUSTMENT
========================

- Increase slightly (10–30%)
- Stay realistic

========================
FINAL VALIDATION
========================

Before returning:

- Revenue NOT empty
- Employees NOT empty
- Matches company size classification
- Revenue + Employees consistent

If invalid → RE-CALCULATE

========================
FUNDING RULE
========================

FundingType:
Bootstrapped
Private
Public
Venture Capital
Subsidiary

FundingStage:
Seed
Series A
Series B
Series C
IPO
Mature

========================
MARKETING SIGNAL
========================

High Engagement
Medium Engagement
Low Engagement

========================
FINAL DECISION (HARD LOGIC)
========================

Evaluate strictly using numeric revenue:

A = Industry is NOT "Media" AND NOT "Advertising"
B = ICPEmployeesRange is one of: "11-50", "51-200", "201-500", "500+"
C = Revenue (numeric) ≥ 1,000,000

If ALL (A AND B AND C) are TRUE:
- ICPFitmentTest = "ICP Fitment"
- ICPFitStatus = "Good Fit"

ELSE:
- ICPFitmentTest = "ICP non Fitment"
- ICPFitStatus = "Not Fit"

========================
VALIDATION (CRITICAL)
========================

Before returning:

- Re-check A, B, C using GENERATED values ONLY
- If mismatch → FIX output

========================
FAILSAFE
========================

If ICPRevenueUSD or ICPEmployeesRange is:
- Empty
- Unrealistic
- Not matching company size

→ Entire response is INVALID

Company: {company}

"""