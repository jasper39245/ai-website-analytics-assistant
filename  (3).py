"""Part 3: the FastAPI web server that connects everything."""
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ai_helper import ask_ai
from analytics import compute_stats, parse_csv

BASE = Path(__file__).parent
app = FastAPI(title="AI Website Analytics Assistant")
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


@app.get("/")
def home():
    return FileResponse(BASE / "static" / "index.html")


@app.post("/analyze")
async def analyze(
    question: str = Form("Give me an overview and tell me what to improve."),
    file: UploadFile | None = File(None),
):
    # 1. Get the CSV text: uploaded file, or the sample data
    if file is not None and file.filename:
        text = (await file.read()).decode("utf-8", errors="ignore")
    else:
        text = (BASE / "sample_data.csv").read_text()

    # 2. Parse and calculate (code does the maths)
    try:
        stats = compute_stats(parse_csv(text))
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {e}")

    # 3. AI explains the numbers
    answer = ask_ai(stats, question)
    return {"stats": stats, "answer": answer}
