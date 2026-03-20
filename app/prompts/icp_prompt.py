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

Company: {company}

FIELDS TO RETURN:
ICPIndustry
ICPEmployeesRange
ICPRevenueUSD
ICPFundingType
ICPFundingStage
ICPParentCompany
ICPLinkedInURL
ICPMarketingSignal
ICPFitStatus
ICPFitmentTest


========================
INDUSTRY RULE
========================
Detect real industry from company name.

Examples:
News / Media / TV → Media
Ads / Advertising / Marketing → Advertising
Insurance → Insurance
Bank / Finance → Banking
Software / AI / SaaS / IT → Technology
Retail / Ecommerce → Retail
Manufacturing / Industrial → Manufacturing

Do NOT classify everything as Technology.


========================
EMPLOYEE RULE
========================
Employees must be EXACTLY one of:

11-50
51-200
201-500
500+


========================
REVENUE RULE
========================
Return realistic revenue in USD.

Allowed format:
"500K"
"1M"
"3M"
"10M"
"50M"
"100M"
"1B"

Do NOT use ranges.


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
ICP FITMENT CONDITIONS (ONLY THESE 3)
========================

Condition A:
Industry must NOT be Media or Advertising

Condition B:
Employees must be greater than 10
(valid values: 11-50, 51-200, 201-500, 500+)

Condition C:
Revenue must be 1M or higher


========================
FINAL DECISION (STRICT)
========================

If ALL 3 conditions are TRUE:
ICPFitmentTest = "ICP Fitment"
ICPFitStatus = "Good Fit"

Else:
ICPFitmentTest = "ICP non Fitment"
ICPFitStatus = "Not Fit"


Return JSON only.
"""