ICP_PROMPT = """
ICP PROMPT GUIDELINES

MISSION:
Generate highly accurate ICP enrichment JSON.
Highest priority is:
1. Correct ICP Fitment logic
2. Realistic revenue
3. Realistic employee size
4. Consistent company classification

==================================================
OUTPUT RULES
==================================================

- Return ONLY valid JSON
- Use double quotes for all keys and values
- No markdown
- No explanation
- No comments
- No extra text
- Never leave mandatory fields blank
- If uncertain, infer carefully from strong business signals

==================================================
FIELDS
==================================================

ICPIndustry:
Choose ONE:

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

Mapping:
- SaaS / AI / Software / IT = Technology
- Payments / Wallet / Fintech / Lending = Financial Services
- Banks = Banking
- Marketing / Agency = Advertising
- TV / Publishing / News / Streaming = Media

--------------------------------------------------

ICPEmployeesRange:
Choose ONE:

"1-10"
"11-50"
"51-200"
"201-500"
"500+"

--------------------------------------------------

ICPRevenueUSD:
Annual revenue estimate in USD.

Allowed format:
"850K"
"1.4M"
"9.7M"
"42M"
"310M"
"2.2B"

Strict:
- No raw numbers
- No $
- No commas
- Must be believable
- Must vary naturally
- Never use repeated defaults

--------------------------------------------------

ICPFundingType:

"Bootstrapped"
"Private"
"Public"
"Venture Capital"
"Subsidiary"

--------------------------------------------------

ICPFundingStage:

"Seed"
"Series A"
"Series B"
"Series C"
"IPO"
"Mature"

--------------------------------------------------

ICPFUndingAmount:
Known / strong estimate else ""

--------------------------------------------------

ICPParentCompany:
Known / strong estimate else ""

--------------------------------------------------

ICPLinkedInURL:
Known valid URL else "N/A"

--------------------------------------------------

ICPMarketingSignal:

"High Engagement"
"Medium Engagement"
"Low Engagement"

--------------------------------------------------

ICPFitStatus:

"Good Fit"
"Not Fit"

ICPFitmentTest:

"ICP Fitment"
"ICP non Fitment"

==================================================
EMPLOYEE ESTIMATION
==================================================

Use actual market presence.

1-10:
Tiny unknown business / freelancer / micro company

11-50:
Small startup / niche local business

51-200:
Growing startup / funded company / active scale-up

201-500:
Established regional business / strong operations

500+:
Large enterprise / public company / global brand

Rules:
- Famous companies usually 500+
- Public companies usually 500+
- Fintech/payment companies usually 51+ minimum

==================================================
REVENUE ESTIMATION (CRITICAL)
==================================================

DO NOT calculate revenue from employee band alone.

Use these factors:

1. Industry economics
2. Product vs services
3. Geography
4. Consumer scale
5. B2B pricing
6. Funding traction
7. Brand size
8. Public filings if known
9. Multi-country operations
10. Company maturity

Examples:

20-person SaaS = 3M to 15M possible
20-person agency = 700K to 4M possible
80-person fintech = 8M to 60M possible
150-person payments firm = 20M to 150M possible
300-person manufacturer = 30M to 400M possible
1000+ public enterprise = 100M to multi-billion

Rules:
- Payments / fintech revenue should not be tiny if scaled
- Public listed brands can be very large
- Unknown micro firms should stay modest
- Use diverse values:
1.3M
2.8M
6.4M
13M
27M
74M
220M
1.7B

==================================================
FUNDING RULES
==================================================

Public listed:
FundingType = "Public"
FundingStage = "IPO"

VC startup:
FundingType = "Venture Capital"

Owned by parent:
FundingType = "Subsidiary"

Established private:
FundingType = "Private"
FundingStage = "Mature"

Tiny founder-run:
FundingType = "Bootstrapped"

==================================================
ICP FITMENT LOGIC (ABSOLUTE PRIORITY)
==================================================

Evaluate EXACTLY these 3 checks:

CHECK 1:
Industry is NOT "Media"
AND Industry is NOT "Advertising"

CHECK 2:
EmployeesRange is NOT "1-10"

CHECK 3:
Revenue strictly greater than 1M USD

Examples:
"900K" = FAIL
"1M" = FAIL
"1.1M" = PASS
"5M" = PASS
">1M" = PASS
--------------------------------------------------

If CHECK1 = PASS
AND CHECK2 = PASS
AND CHECK3 = PASS

Then:

ICPFitmentTest = "ICP Fitment"
ICPFitStatus = "Good Fit"

Else:

ICPFitmentTest = "ICP non Fitment"
ICPFitStatus = "Not Fit"

==================================================
MANDATORY SELF-CHECK BEFORE OUTPUT
==================================================

Recalculate fitment after all fields generated.

Examples:

Technology + 11-50 + 2.4M
= MUST BE FIT

Financial Services + 51-200 + 18M
= MUST BE FIT

Manufacturing + 201-500 + 73M
= MUST BE FIT

Media + 500+ + 800M
= NOT FIT

Advertising + 51-200 + 10M
= NOT FIT

Agriculture + 1-10 + 4M
= NOT FIT

If your generated result violates above logic, FIX it before output.
this is the most critical step. Always ensure final output is logically consistent.
this examples may be counterintuitive but follow the rules strictly.

==================================================
FINAL VALIDATION
==================================================

1. JSON valid
2. Revenue format valid
3. Revenue realistic
4. Revenue not repetitive
5. Employees realistic
6. Fitment logic rechecked LAST
7. No contradictory output

==================================================
COMPANY INPUT
==================================================

Company: {company}

"""