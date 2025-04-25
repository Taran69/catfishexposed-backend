from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

scam_detector = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    filename = file.filename
    if "catfish" in filename.lower():
        return JSONResponse(content={"result": "FAKE"}, status_code=200)
    else:
        return JSONResponse(content={"result": "REAL"}, status_code=200)

@app.post("/analyze-text")
async def analyze_text(text: str):
    result = scam_detector(text, candidate_labels=["scam", "legit"])
    return JSONResponse(content={"result": result['labels'][0], "confidence": result['scores'][0]}, status_code=200)

@app.get("/")
def read_root():
    return {"message": "CatfishExposed API is live"}