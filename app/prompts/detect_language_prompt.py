DETECT_LANGUAGE_PROMPT = """
You will be given one field: Comments.
Detect the language for the field and return a JSON object with the key:
"Comments". Use 2-letter language codes (e.g., "en", "uz", "ru").
Return VALID JSON only and nothing else.

Input values:
Comments: {Comments}
"""
