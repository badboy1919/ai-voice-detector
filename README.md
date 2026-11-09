# AI Voice Detection API

A **FastAPI** service that classifies a submitted audio clip as **AI-generated** or **human** speech, returning a confidence score and explanation. Built as a spec-driven API implementation with API-key authentication and strict input validation.

## ✨ Features

- **`POST /api/voice-detection`** — base64-encoded MP3 in, classification out
- **API-key auth** — `X-API-Key` header required; invalid/missing key → `401`
- **Language validation** — supported: Tamil, English, Hindi, Malayalam, Telugu → else `400`
- **Format validation** — MP3 only → else `400`
- **Structured responses** — `status`, `language`, `classification`, `confidenceScore`, `explanation`
- **Spec-aligned error model** — uniform `{ status: "error", message }` shape

> ℹ️ Detection logic is a lightweight demonstration (length-based heuristic) implementing the API contract — swap `detect_voice_origin()` with a real model (e.g., audio deepfake classifier) for production use.

## 🛠️ Stack

- **FastAPI** + **Pydantic** models
- Header-based API key dependency injection

## 🚀 Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Interactive docs: `http://127.0.0.1:8000/docs`

## 📨 Example

```bash
curl -X POST "http://127.0.0.1:8000/api/voice-detection" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_test_123456789" \
  -d '{
    "language": "Hindi",
    "audioFormat": "mp3",
    "audioBase64": "SUQzDNAAAA..."
  }'
```

Success response:

```json
{
  "status": "success",
  "language": "Hindi",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.87,
  "explanation": "Consistent robotic frequency and unnatural pitch patterns detected in Hindi audio."
}
```

## 📁 Structure

```
ai-voice-detector/
├── main.py            # FastAPI app, auth, validation, detection logic
├── requirements.txt   # fastapi, uvicorn, pydantic
└── README.md
```

---

*B.Tech CSE (Cybersecurity) · Parul University*
