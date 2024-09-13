from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.exceptions import NoTranscriptFound
from pydantic import BaseModel

app = FastAPI()

class TranscriptResponse(BaseModel):
    transcript: list

@app.get("/transcript/{video_id}", response_model=TranscriptResponse)
async def get_transcript(video_id: str):
    try:
        # Fetch the transcript in Portuguese and English
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["pt", "en"])
        return {"transcript": transcript}
    except NoTranscriptFound:
        # If the video does not have a transcript, return a 404 error
        raise HTTPException(status_code=404, detail="Transcript not found for the given video ID.")
    except Exception as e:
        # For other internal errors, return a 500 error
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
