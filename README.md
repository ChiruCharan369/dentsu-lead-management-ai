# Dentsu Lead Management AI



## Project Overview

The application exposes three main endpoints:

- `GET /` — health check
- `POST /icp` — returns ICP fields for a company and email
- `POST /translator` — translates lead-related fields into English

Key folders:

- `app/main.py` — FastAPI application startup
- `app/routes/` — API route definitions for ICP and translator services
- `app/services/` — business logic for ICP enrichment and translation
- `app/models/` — Pydantic request/response models
- `app/llm/` — Azure OpenAI client wrapper
- `app/db/` — local SQLite + CSV caching for ICP data
- `app/prompts/` — prompt templates used by the LLM services

## Requirements

Install the Python dependencies from `requirements.txt`.

Recommended environment:

- Python 3.13+
- `FastAPI`
- `uvicorn`
- `python-dotenv`
- `langchain-openai`
- `pydantic`

## Environment Variables

The app loads `.env` values using `python-dotenv`. Common variables include:

- `AZURE_OPENAI_ENDPOINT`
- `OPENAI_API_VERSION`
- `GPT3.5_KEY`
- `GPT4_KEY`
- `GPT4_1_KEY`
- `SERVICE_LINE`
- `BRAND`
- `PROJECT`

If these variables are missing, the Azure OpenAI client cannot initialize correctly.

## Installation

1. Clone the repository.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment.

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies.

```bash
python -m pip install -r requirements.txt
```

## Running the App

Start the FastAPI service with Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The app initializes the ICP cache database and CSV file automatically on startup.

## API Usage

### Health check

```bash
curl http://localhost:8000/
```

Expected response:

```json
{"status":"running"}
```

### ICP Service

Request:

```bash
curl -X POST http://localhost:8000/icp \
  -H "Content-Type: application/json" \
  -d '{"company": "Example Corp", "email": "sales@example.com"}'
```

Response model includes fields such as:

- `ICPIndustry`
- `ICPEmployeesRange`
- `ICPRevenueUSD`
- `ICPFundingType`
- `ICPFundingStage`
- `ICPLinkedInURL`
- `ICPMarketingSignal`
- `ICPFitStatus`
- `ICPFitmentTest`

### Translator Service

Request:

```bash
curl -X POST http://localhost:8000/translator \
  -H "Content-Type: application/json" \
  -d '{"FirstName":"Juan","LastName":"Perez","company":"Acme","JobTitle":"Gerente","Comments":"Necesito detalles."}'
```

Response model includes fields such as:

- `FirstNameEnglish`
- `LastNameEnglish`
- `companyEnglish`
- `JobTitleEnglish`
- `CommentsEnglish`

## Caching Behavior

The ICP service uses a local SQLite cache (`icp_cache.db`) and a CSV mirror (`icp_cache.csv`). Cached entries are valid for 30 days. On startup the application initializes cache storage automatically.

## Notes

- The project uses Azure OpenAI via `app/llm/llm_client.py`.
- The translator route normalizes line endings in `Comments` before invoking the translation flow.
- This repository currently supports two services: `icp` and `translator`.

## License

This repository does not include a formal license file. Add a `LICENSE` if you want to publish it under an open source license.


