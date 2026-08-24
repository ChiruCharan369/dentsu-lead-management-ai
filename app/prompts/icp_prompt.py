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

EMPTY OR INVALID COMPANY (CRITICAL)

If company is:

- empty
- "none", "na", "n/a", "null"
- only symbols or test company names ("test", "abc", "xyz corp")


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
ConfidenceScore
ScoreComment

========================
CRITICAL NORMALIZATION (NEW)
========================

STEP A — CANONICAL ENTITY RESOLUTION (DO THIS FIRST):
- Determine the "CanonicalEntity" behind the input company string.
- Treat the following as the SAME CanonicalEntity:
  * abbreviations ↔ expanded forms
  * brand ↔ product line ↔ business unit name
  * punctuation/case variants
  * common nicknames and regional naming variants
- If the input clearly refers to a SUBSIDIARY / DIVISION / PRODUCT of a larger parent:
  * Keep revenue/employees at the SUBSIDIARY/DIVISION level ONLY if it is a separately operated/reporting business.
  * Otherwise, treat it as the parent’s OPERATING SEGMENT and keep scale consistent with the parent’s overall scale ONLY when the segment is widely known to be massive and inseparable in public perception.
- NEVER let an alias produce a materially different scale for the same CanonicalEntity.

STEP B — PARENT vs ENTITY RULE (NEW):
- ICPParentCompany must reflect ownership.
- ICPRevenueUSD and ICPEmployeesRange must reflect the CanonicalEntity being described (not always the parent).
- If you cannot separate subsidiary/segment financials reliably:
  * Set ICPParentCompany correctly
  * Set ICPRevenueUSD and ICPEmployeesRange to the parent-level scale ONLY if the input is commonly used to mean the overall organization.
  * Otherwise choose a conservative segment-level estimate AND KEEP IT CONSISTENT ACROSS ALIASES.

========================
REALISTIC INFERENCE RULES (CRITICAL)
========================

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
ICPRevenueUSD is strictly greater than 1M USD annually

CHECK 3:
ICPEmployeesRange is NOT less than 10

NOTE — COMPENSATING FACTOR RULE:
- Revenue is the primary pass/fail criteria after industry.
- However, employee count is a compensating factor: if revenue is slightly below the threshold (within 5% below $1M) but employee count meets or exceeds the employee threshold (≥ 10), classify as "Near Fit" instead of automatic non-fit.

NEAR FIT (AMBER) CRITERIA:
1. Revenue is within 5% below the benchmark (i.e., between $950,000 and $1,000,000),
2. Industry criteria are satisfied (CHECK 1),
3. Employee count criteria are satisfied (CHECK 3).

FITMENT RESULT (FINAL):
- If CHECK 1 AND CHECK 2 AND CHECK 3 PASS:
  ICPFitmentTest = "ICP Fitment"
  ICPFitStatus = "Good Fit"
- Else if CHECK 1 PASS and Revenue within 5% below threshold and CHECK 3 PASS:
  ICPFitmentTest = "ICP Near Fitment"
  ICPFitStatus = "Near Fit"
- Else:
  ICPFitmentTest = "ICP non Fitment"
  ICPFitStatus = "Not Fit"

SCORE GUIDANCE:
- `ConfidenceScore`: integer 0-100 where higher means better match to revenue threshold and quality. Use 100 for clearly above threshold; use values in the 70-89 range for Near Fit; below 70 for weak revenue signals.
- `ScoreComment`: short human-readable rationale for the revenue score (e.g., "Revenue 980K (within 2% of threshold); employees strong -> Near Fit").

========================
MANDATORY SELF-CHECK (FINAL STEP) (UPDATED)
========================
- Validate revenue against employee size and industry
- Verify that the output would remain CONSISTENT if the input were a common alias/expanded form of the same CanonicalEntity
- Ensure Parent vs Entity rule is satisfied (ownership vs scale)
- Recalculate ICP fitment LAST
- If any rule breaks, FIX BEFORE OUTPUT


CONSISTENCY OVERRIDE RULE:

If ICPRevenueUSD > 1M
AND ICPEmployeesRange ≥ 10
AND ICPIndustry is not explicitly Media or Advertising by business model,
THEN ICPFitmentTest CANNOT be "ICP non Fitment".

FINAL VALIDATION:
- JSON valid
- Revenue varies per company
- Revenue realistic for industry
- No repeated default values
- Fitment logic verified

COMPANY INPUT:
Company: {company}

"""
