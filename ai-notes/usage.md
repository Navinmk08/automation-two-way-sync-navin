AI Usage Notes
----------------

Tools used:
- ChatGPT (OpenAI) — high-level design discussion, README drafting, mapping choices
- GitHub Copilot — code snippet suggestions and small edits

What AI helped with:
- Drafting the README and status mapping text.
- Generating basic client code structure for ClickUp and Google Sheets.

What I changed from AI suggestions:
- AI suggested using ClickUp `external_id` only and not storing `task_id` in the sheet. I kept `task_id` in the sheet for deterministic idempotency and added a lookup by `external_id` to avoid duplicates.

Example prompt (redacted):
"Draft a Python function to list Google Sheet rows and return them as dicts with their row index."  
I verified and adapted the returned code to include `__row` and robust header checks.

Notes:
- I validated all AI-generated code manually and added unit tests and logging. Never commit service account keys or tokens.
