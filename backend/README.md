# DocMind AI Backend

FastAPI service responsible for document processing, retrieval, generation, authentication-aware API access, and RAG orchestration.

## Local development

Create a virtual environment and install dependencies:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy the environment template:

```powershell
Copy-Item .env.example .env
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

API:

- http://localhost:8000/health
- http://localhost:8000/api/v1/health
- http://localhost:8000/docs
