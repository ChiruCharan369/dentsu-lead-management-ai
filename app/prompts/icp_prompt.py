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

========================
DATA SOURCE PRIORITY (USE THESE FIRST)
========================

When verifying company information, prefer data consistent with:

Clearbit → industry, employee count, revenue range, LinkedIn
Apollo.io → employee size, funding, company details
ZoomInfo → company size, revenue, enterprise data
Crunchbase → funding, investors, parent company
LinkedIn → employee size, company profile, industry
People Data Labs → company enrichment data

Use these as reference signals when estimating values.

If multiple sources conflict:
Use the most realistic value based on company size.

Do not invent unrealistic numbers.

========================
DATA SOURCE PRIORITY (USE THESE FIRST)
========================

When verifying company information, prefer data consistent with:

Clearbit → industry, employee count, revenue range, LinkedIn
Apollo.io → employee size, funding, company details
ZoomInfo → company size, revenue, enterprise data
Crunchbase → funding, investors, parent company
LinkedIn → employee size, company profile, industry
People Data Labs → company enrichment data

Use these as reference signals when estimating values.

If multiple sources conflict:
Use the most realistic value based on company size.

Do not invent unrealistic numbers.

Company: {company}

FIELDS TO RETURN:
ICPIndustry
ICPEmployeesRange
ICPRevenueUSD
ICPFundingType
ICPFundingStage
ICPFUndingAmount
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
Revenue must be >= 1M

========================
FINAL DECISION (VERY STRICT)
========================

Evaluate conditions:

A = Industry is NOT Media AND NOT Advertising
B = EmployeesRange is one of (11-50, 51-200, 201-500, 500+)
C = RevenueUSD must be >= 1M

If A AND B AND C are TRUE:
ICPFitmentTest = "ICP Fitment"
ICPFitStatus = "Good Fit"

Otherwise:
ICPFitmentTest = "ICP non Fitment"
ICPFitStatus = "Not Fit"
"""
