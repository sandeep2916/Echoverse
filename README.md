# EchoVerse Fullstack (FastAPI backend + Static frontend)

## Quick start (Windows PowerShell)

1. Open PowerShell and navigate to the backend folder:
```powershell
cd path\to\echoverse_fullstack\backend
python -m venv .venv
.venv\Scripts\activate.bat   # or Activate.ps1 if policy allows
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in IBM credentials.

3. Run the backend (from backend folder):

```powershell
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

4. Open the frontend: open `frontend/index.html` in your browser (double-click the file). 
If the browser blocks local fetch, run a static server from the frontend folder:

```powershell
cd ..\frontend
python -m http.server 5500
# then visit http://localhost:5500
```

Notes:
- Ensure `WATSONX_PROJECT_ID` and keys are correct.
- For production, secure keys and use HTTPS.
