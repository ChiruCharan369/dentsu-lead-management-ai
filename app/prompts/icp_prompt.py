ICP_PROMPT = """

STRICT OUTPUT RULES:
- Return ONLY valid JSON
- Use double quotes for ALL keys
- Use double quotes for ALL values
- No extra text
- No explanation
- JSON must work with Python json.loads()

IMPORTANT:
Use real-world knowledge about the company.
Use best estimate if exact data not known.
Avoid "Unknown" unless impossible.
Values must be realistic for year 2026.

========================
DATA SOURCE PRIORITY (VERY STRICT)
========================

Use data consistent with these sources in order:

1. ZoomInfo (HIGHEST PRIORITY)
2. Clearbit
3. Apollo.io
4. LinkedIn
5. Crunchbase
6. People Data Labs

Rules:

- If ZoomInfo data exists → use it
- If not → use Clearbit / Apollo / LinkedIn
- If conflict → choose most realistic value
- Never invent unrealistic numbers
- Never give startup revenue as billions
- Never give enterprise revenue as thousands

All values must reflect realistic company size in year 2026.

========================
YEAR 2026 ESTIMATION RULE
========================

If data looks old:

- Increase revenue slightly
- Increase employees slightly
- Keep realistic range
- Do NOT overestimate

Example:
2019 revenue 5M → 2026 = 5M–7M
2020 employees 40 → 2026 = 51-100

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

Detect real industry from company name.

News / Media / TV → Media
Ads / Advertising / Marketing → Advertising
Insurance → Insurance
Bank / Finance → Banking
Software / AI / SaaS / IT → Technology
Retail / Ecommerce → Retail
Manufacturing / Industrial → Manufacturing
Hospital / Pharma → Healthcare
Education / University → Education

Do NOT classify everything as Technology.

========================
EMPLOYEE RANGE RULE
========================

Allowed values:

1-10
11-50
51-200
201-500
500+

Use realistic estimate based on real company size.

========================
REVENUE RULE (USD) — VERY STRICT
========================

Revenue must be estimated using real company data signals.

Priority:

1. ZoomInfo revenue
2. Clearbit revenue
3. Apollo revenue
4. Crunchbase financials
5. LinkedIn + real-world knowledge
6. People Data Labs

Rules:

- DO NOT calculate revenue from employees
- DO NOT use fixed mapping
- DO NOT guess randomly
- Revenue must match real company scale
- Use realistic value for year 2026
- If old data → adjust slightly
- Never overestimate
- Never underestimate big companies

Allowed format:

500K
1M
5M
10M
25M
50M
100M
250M
500M
1B
5B
10B

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

Use realistic guess based on company size and presence.

========================
ICP FITMENT CONDITIONS (ONLY THESE 3)
========================

Condition A:
Industry must NOT be Media
Industry must NOT be Advertising

Condition B:
Employees must be > 10

Allowed:
11-50
51-200
201-500
500+

Condition C:
Revenue must be >= 1M

========================
FINAL DECISION (VERY STRICT)
========================

A = Industry NOT Media AND NOT Advertising
B = EmployeesRange in (11-50, 51-200, 201-500, 500+)
C = Revenue >= 1M

If A AND B AND C TRUE:

ICPFitmentTest = "ICP Fitment"
ICPFitStatus = "Good Fit"

Else:

ICPFitmentTest = "ICP non Fitment"
ICPFitStatus = "Not Fit"

Company: {company}

"""