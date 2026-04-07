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
- MUST reflect real company scale
- Large/global brands → ALWAYS "500+"

========================
REVENUE RULE (USD) — EXACT VALUE MODE
========================

Revenue MUST always be returned.
It MUST NOT be empty.

"Unknown" is NOT allowed unless absolutely no signals exist.

========================
DATA PRIORITY
========================

Use sources in order:

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
  - Product pricing
  - Market presence
  - Geography
  - Customer scale

STRICT:
- DO NOT calculate from employee count
- DO NOT guess randomly
- DO NOT default to common values

========================
OUTPUT FORMAT (STRICT)
========================

Return revenue as a SINGLE value in USD using:

K = thousand  
M = million  
B = billion  

Examples of VALID outputs:

750K
2M
7.5M
18M
75M
120M
320M
850M
1.2B
1.8B
3.5B
7B

Rules:

- No commas (e.g., 1,000,000 ❌)
- No currency symbols (e.g., $ ❌)
- No text (e.g., "approx" ❌)
- No ranges (e.g., 1M-5M ❌)
- MUST be a realistic number (not rounded unnecessarily)

========================
SCALE VALIDATION
========================

- Global / luxury / enterprise companies → typically in billions (B)
- Mid-size companies → millions (10M–500M)
- Small companies → thousands to low millions (500K–10M)

STRICT:
- Do NOT underestimate large companies
- Do NOT overestimate small companies

========================
YEAR 2026 ADJUSTMENT
========================

If data is old:
- Increase slightly (10–30%)
- Keep realistic growth

========================
FINAL VALIDATION
========================

Before returning:

- Value MUST be non-empty
- Value MUST match company scale
- Value MUST be properly formatted (K/M/B)
- Value MUST be realistic for 2026

If invalid → RE-CALCULATE

========================
FAILSAFE
========================

If ICPRevenueUSD is empty or unrealistic:
→ Entire response is INVALID

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
ICP FITMENT CONDITIONS
========================

A: Industry NOT Media AND NOT Advertising
B: Employees > 10
C: Revenue >= 1M

========================
FINAL DECISION
========================

If A AND B AND C TRUE:
ICPFitmentTest = "ICP Fitment"
ICPFitStatus = "Good Fit"

Else:
ICPFitmentTest = "ICP non Fitment"
ICPFitStatus = "Not Fit"

========================
FAILSAFE (VERY IMPORTANT)
========================

If ICPRevenueUSD or ICPEmployeesRange is:
- Empty
- Unrealistic
- Not matching company scale

→ Entire response is INVALID

Company: {company}

"""