from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import uuid

from services.transcription import transcribe_audio
from services.minutes_generator import generate_minutes


# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------

app = FastAPI(
    title="AI Meeting Minutes Generator",
    description="AI-powered system for converting meeting recordings into structured meeting minutes.",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# FOLDERS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Serve uploaded files if needed
app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads"
)


# --------------------------------------------------
# ALLOWED FILE TYPES
# --------------------------------------------------

ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm"
}

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB


# --------------------------------------------------
# HOME API
# --------------------------------------------------

@app.get("/")
async def home():
    return {
        "status": "success",
        "message": "AI Meeting Minutes Generator API is running",
        "version": "1.0.0"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI Meeting Minutes Generator"
    }


# --------------------------------------------------
# PROCESS MEETING
# --------------------------------------------------

@app.post("/process-meeting")
async def process_meeting(file: UploadFile = File(...)):

    # Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a meeting audio or video file."
        )

    # Get extension
    file_extension = Path(file.filename).suffix.lower()

    # Check extension
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file format. "
                "Supported formats: MP3, WAV, M4A, MP4, AVI, MOV, MKV, WEBM."
            )
        )

    # Create unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    file_path = UPLOAD_DIR / unique_filename

    try:

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Check file size
        file_size = file_path.stat().st_size

        if file_size > MAX_FILE_SIZE:
            file_path.unlink(missing_ok=True)

            raise HTTPException(
                status_code=413,
                detail="File is too large. Maximum allowed size is 500 MB."
            )

        if file_size == 0:
            file_path.unlink(missing_ok=True)

            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        # --------------------------------------------------
        # STEP 1: TRANSCRIPTION
        # --------------------------------------------------

        print(f"Processing file: {file.filename}")
        print("Step 1: Transcribing meeting...")

        transcript = transcribe_audio(str(file_path))

        if not transcript:
            raise HTTPException(
                status_code=500,
                detail="Unable to generate transcript from the meeting."
            )

        # --------------------------------------------------
        # STEP 2: GENERATE MEETING MINUTES
        # --------------------------------------------------

        print("Step 2: Generating meeting minutes...")

        minutes = generate_minutes(transcript)

        if not minutes:
            raise HTTPException(
                status_code=500,
                detail="Unable to generate meeting minutes."
            )

        # --------------------------------------------------
        # RESPONSE
        # --------------------------------------------------

        return {
            "status": "success",
            "message": "Meeting processed successfully.",
            "filename": file.filename,
            "transcript": transcript,
            "minutes": minutes
        }

    except HTTPException:
        raise

    except Exception as e:

        print("ERROR:", str(e))

        # Delete uploaded file if processing fails
        if file_path.exists():
            file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"Meeting processing failed: {str(e)}"
        )

    finally:
        await file.close()


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )