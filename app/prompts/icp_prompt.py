ICP_PROMPT = """
STRICT RULES:
- Use double quotes for ALL keys
- Use double quotes for ALL values
- Do NOT miss quotes
- Do NOT add extra fields
- Do NOT add text outside JSON
- JSON must be valid for Python json.loads()

Company: {company}

Fields:
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


ICP FITMENT RULES (VERY STRICT):

Condition 1:
Industry must NOT be Ads, Advertising, Media, Marketing Agency, or News company

Condition 2:
Employees must be > 10

Valid ranges:
11-50
51-200
201-500
500+

Condition 3:
Revenue must be >= 1M USD

INVALID revenue examples:
<1M
500K
200000
Unknown


Decision logic:

If ALL conditions are true:
ICPFitmentTest = "ICP Fitment"

Else:
ICPFitmentTest = "Non ICP Fitment"

Return JSON only.
"""