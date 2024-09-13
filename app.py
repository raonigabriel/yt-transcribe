from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from pydantic import BaseModel

app = FastAPI()

class TranscriptResponse(BaseModel):
    transcript: list

@app.get("/transcript/{video_id}", response_model=TranscriptResponse)
async def get_transcript(video_id: str):
    try:
        # Busca a transcrição nas línguas Português e Inglês
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["pt", "en"])
        return {"transcript": transcript}
    except Exception as e:
        # Em caso de erro, lança uma exceção HTTP 400
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
