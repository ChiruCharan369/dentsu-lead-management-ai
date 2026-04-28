ICP_PROMPT = """
ICP PROMPT GUIDELINES

OUTPUT RULES:
- Return ONLY valid JSON
- Use double quotes for all keys and values
- No explanation, notes, markdown, or extra text
- If uncertain, estimate using realistic business signals
- Never leave mandatory fields blank except allowed N/A fields

==================================================
FIELD DEFINITIONS
==================================================

ICPIndustry:
Primary business industry.

Allowed examples:
Technology
Financial Services
Banking
Retail
Manufacturing
Healthcare
Education
Agriculture
Logistics
Real Estate
Hospitality
Consumer Goods
Automotive
Media
Advertising
Energy
Telecommunications

Rules:
- Marketing / agency / branding / ad companies = Advertising
- TV / news / publishing / streaming = Media
- Fintech / payments / lending / wallets = Financial Services
- SaaS / AI / IT / software = Technology

--------------------------------------------------

ICPEmployeesRange:
Allowed values ONLY:

"1-10"
"11-50"
"51-200"
"201-500"
"500+"

Must never be empty.

--------------------------------------------------

ICPRevenueUSD:
Estimated annual revenue in USD.

Allowed format ONLY:
"K" = Thousand
"M" = Million
"B" = Billion

Examples:
"850K"
"4.2M"
"19M"
"240M"
"1.4B"

Rules:
- No raw numbers
- No currency symbols
- Must be realistic
- Must align with employee size + industry
- Use varied values, not repeated defaults

--------------------------------------------------

ICPFundingType:
Allowed values ONLY:

"Bootstrapped"
"Private"
"Public"
"Venture Capital"
"Subsidiary"

--------------------------------------------------

ICPFundingStage:
Allowed values ONLY:

"Seed"
"Series A"
"Series B"
"Series C"
"IPO"
"Mature"

--------------------------------------------------

ICPFUndingAmount:
If known estimated funding amount:
Examples:
"5M"
"22M"
"300K"

Else return ""

--------------------------------------------------

ICPParentCompany:
Parent company name if known.
Else return "N/A"

--------------------------------------------------

ICPLinkedInURL:
Valid LinkedIn company page if confidently known.
Else return "N/A"

--------------------------------------------------

ICPMarketingSignal:
Allowed values ONLY:

"High Engagement"
"Medium Engagement"
"Low Engagement"

Use signals like:
- Ad activity
- Social presence
- Hiring growth
- Brand campaigns
- Website/product activity

--------------------------------------------------

ICPFitStatus:
"Good Fit"
"Not Fit"

ICPFitmentTest:
"ICP Fitment"
"ICP non Fitment"

==================================================
EMPLOYEE ESTIMATION RULES (VERY IMPORTANT)
==================================================

Estimate using REAL company maturity.

1) Tiny local company / new unknown business:
-> "1-10"

2) Small startup / LLP / niche regional company:
-> "11-50"

3) Funded startup / growing company / active SaaS / fintech:
-> "51-200"

4) Established mid-size company / multiple branches:
-> "201-500"

5) Public company / national brand / old enterprise /
large manufacturer / enterprise group:
-> "500+"

CRITICAL RULES:

- Never default to "51-200"
- Famous brands should rarely be below "500+"
- Listed companies should usually be "500+"
- Multi-country operations should usually be "201-500" or "500+"
- Regulated fintech/payment companies should usually be at least "51-200"

==================================================
REVENUE ESTIMATION RULES (CRITICAL)
==================================================

Revenue must strongly match employee scale.

BASELINE GUIDE:

"1-10"
100K to 2M

"11-50"
500K to 8M

"51-200"
3M to 35M

"201-500"
15M to 120M

"500+"
50M to Multi-Billion

INDUSTRY MULTIPLIERS:

- Manufacturing / Banking / Consumer Goods / Payments:
Usually higher revenue

- SaaS / AI startup:
Medium to high depending scale

- Agriculture / services / boutique firms:
Lower to medium

- Public brands:
Can exceed baseline significantly

CRITICAL RULES:

- Do NOT reuse values like 2.5M / 3.2M / 5M repeatedly
- Use realistic variation:
6.8M
11M
27M
73M
410M
1.2B

- If Employees = "500+" rarely below 50M
- If Employees = "1-10" rarely above 5M

==================================================
FUNDING RULES
==================================================

If listed/public company:
FundingType = "Public"
FundingStage = "IPO"

If startup with investors:
FundingType = "Venture Capital"

If owned by parent group:
FundingType = "Subsidiary"

If old private company:
FundingType = "Private"
FundingStage = "Mature"

If small self-owned:
FundingType = "Bootstrapped"

==================================================
MARKETING SIGNAL RULES
==================================================

High Engagement:
- Strong brand visibility
- Frequent campaigns
- Hiring growth
- Consumer presence

Medium Engagement:
- Normal digital presence
- Some growth activity

Low Engagement:
- Minimal public activity

==================================================
ICP FITMENT CONDITIONS
==================================================

Company is ICP Fit ONLY if ALL below are TRUE:

1. Industry is NOT "Media"
2. Industry is NOT "Advertising"
3. EmployeesRange is NOT "1-10"
4. Revenue > 1M USD

==================================================
ICP DECISION LOGIC
==================================================

If all pass:

ICPFitmentTest = "ICP Fitment"
ICPFitStatus = "Good Fit"

Else:

ICPFitmentTest = "ICP non Fitment"
ICPFitStatus = "Not Fit"

==================================================
CONSISTENCY VALIDATION (MANDATORY)
==================================================

Before final output verify:

1. Employees range realistic for known brand
2. Revenue matches employees
3. Revenue not generic repeated number
4. Public company not marked tiny
5. Startup not marked billion revenue unless justified
6. ICP logic correct
7. JSON valid
8. All values use allowed options

If unrealistic -> regenerate internally once.

==================================================
SPECIAL CASES
==================================================

- Fintech / Payments / Wallet / Banking tech:
Usually Financial Services

- Ad agency / media network:
Usually Not Fit by ICP rule

- Large known manufacturer:
Usually 500+ employees

- Unknown company:
Use conservative estimates

==================================================
COMPANY INPUT
==================================================

Company: {company}

"""