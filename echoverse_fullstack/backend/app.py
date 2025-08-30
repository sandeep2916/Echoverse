import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from ibm_llm import rewrite_with_tone
from ibm_tts import synthesize_mp3_bytes

app = FastAPI(title="EchoVerse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RewriteRequest(BaseModel):
    text: str
    tone: str

@app.get("/")
def root():
    return HTMLResponse(content="<h2>EchoVerse backend running. See /docs for API</h2>")

@app.post("/api/rewrite")
def api_rewrite(req: RewriteRequest):
    try:
        data = rewrite_with_tone(req.text, req.tone)
        return JSONResponse(data)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/upload-txt")
async def api_upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.txt'):
        return JSONResponse({"error": "Please upload a .txt file."}, status_code=400)
    content = (await file.read()).decode('utf-8', errors='ignore')
    return JSONResponse({"text": content})

@app.post("/api/generate")
async def api_generate(text: str = Form(...), tone: str = Form("Neutral"), voice: str = Form(None)):
    try:
        data = rewrite_with_tone(text, tone)
        mp3 = synthesize_mp3_bytes(data.get('rewrite',''), voice=voice)
        def iterfile():
            yield mp3
        headers = {"Content-Disposition": "attachment; filename=echoverse.mp3"}
        return StreamingResponse(iterfile(), media_type="audio/mpeg", headers=headers)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    host = os.getenv('APP_HOST', '0.0.0.0')
    port = int(os.getenv('APP_PORT', 8000))
    uvicorn.run("backend.app:app", host=host, port=port, reload=True)