ICP_PROMPT = """
MISSION:
Generate realistic, company-specific ICP enrichment JSON.
Each company must have its own revenue and scale inferred independently.

OUTPUT RULES:
- Return ONLY valid JSON
- Double quotes only
- No markdown, comments, explanations, or extra text
- Do NOT add or remove fields
- Never leave mandatory fields blank
- Revenue and funding must be USD strings using K / M / B only

MANDATORY OUTPUT FIELDS (ONLY):
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

REALISTIC INFERENCE RULES (CRITICAL):

EMPLOYEES ↔ REVENUE SANITY:
- Revenue MUST scale logically with employee size
- Avoid extreme per-employee revenue unless industry justifies it
- Service-based industries have lower revenue density than product companies

INDUSTRY CONSTRAINTS (ENFORCED):
- Advertising, Marketing, Media, Consulting:
  Revenue is service-based, not product-scale
- Manufacturing:
  Revenue grows gradually with scale
- Technology / SaaS / Platforms:
  Higher revenue potential, but avoid extremes without clear signals
- FinTech:
  Conservative revenue unless enterprise-scale signals exist

UNCERTAINTY RULE:
- When data is weak → choose conservative but non-trivial revenue
- Never default all companies to the same revenue
- Never use placeholder values repeatedly

FUNDING RULES:
- Do NOT assume funding unless clearly implied
- If unclear → FundingType = "N/A", FundingStage = "N/A", FundingAmount = "N/A"

ICP FITMENT LOGIC (ABSOLUTE):

CHECK 1:
ICPIndustry is NOT "Media"
AND ICPIndustry is NOT "Advertising"

CHECK 2:
ICPEmployeesRange is NOT less than 10

CHECK 3:
ICPRevenueUSD is strictly greater than 1M USD annually

FITMENT RESULT:
If ALL checks PASS:
ICPFitmentTest = "ICP Fitment"
ICPFitStatus = "Good Fit"
Else:
ICPFitmentTest = "ICP non Fitment"
ICPFitStatus = "Not Fit"

MANDATORY SELF-CHECK (FINAL STEP):
- Validate revenue against employee size and industry
- Recalculate ICP fitment LAST
- If any rule breaks, FIX BEFORE OUTPUT

FINAL VALIDATION:
- JSON valid
- Revenue varies per company
- Revenue realistic for industry
- No repeated default values
- Fitment logic verified

COMPANY INPUT:
Company: {company}

"""