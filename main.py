import base64
import random
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="AI Voice Detection API")

# Configuration
API_KEY_CREDENTIAL = "sk_test_123456789" # Isse apna secret key badal lena [cite: 7, 8]
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"] # [cite: 4]

# --- Models ---
class VoiceRequest(BaseModel):
    language: str
    audioFormat: str = "mp3"
    audioBase64: str

class VoiceResponse(BaseModel):
    status: str
    language: str
    classification: str
    confidenceScore: float
    explanation: str

# --- Security Dependency ---
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY_CREDENTIAL:
        raise HTTPException(status_code=401, detail="Invalid API key or malformed request") # [cite: 11]
    return x_api_key

# --- Logic: Detection Mockup ---
def detect_voice_origin(audio_b64: str, lang: str):
    """
    Prototype logic: Real model yahan plug-in hoga.
    Abhi ke liye ye dummy classification return kar raha hai rules follow karte hue.
    """
    # Base64 decode check
    try:
        audio_data = base64.b64decode(audio_b64[:100]) # Testing decoding
    except:
        return "error", 0.0, "Malformed Base64 data"

    # Mock Detection logic 
    choice = random.choice(["AI_GENERATED", "HUMAN"])
    score = round(random.uniform(0.75, 0.99), 2)
    
    explanation = f"Detected {choice} patterns in {lang} audio based on pitch consistency."
    return choice, score, explanation

# --- Endpoint ---
@app.post("/api/voice-detection", response_model=VoiceResponse)
async def voice_detection(request: VoiceRequest, api_key: str = Depends(verify_api_key)):
    # 1. Language Validation [cite: 4]
    if request.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Language '{request.language}' not supported.")

    # 2. Format Validation [cite: 6]
    if request.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=400, detail="Only MP3 format is supported.")

    # 3. Process Detection
    classification, score, reason = detect_voice_origin(request.audioBase64, request.language)

    # 4. Return structured JSON [cite: 9, 10]
    return {
        "status": "success",
        "language": request.language,
        "classification": classification,
        "confidenceScore": score,
        "explanation": reason
    }