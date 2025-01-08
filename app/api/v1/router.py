from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.audio import AudioCreate, BaseResponse, AudioListData, AudioData
from app.api.v1.service import get_audio_files, create_audio_file
from app.database import get_db

router = APIRouter()


@router.get("/audio", response_model=BaseResponse)
def read_audio_files(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a paginated list of audio files.
    """
    total, files = get_audio_files(db, skip=skip, limit=limit)
    return BaseResponse(
        status="success",
        message="Audio files retrieved successfully",
        data=AudioListData(total=total, items=files),
    )


@router.post("/audio", response_model=BaseResponse)
def add_audio_file(audio: AudioCreate, db: Session = Depends(get_db)):
    """
    Add a new audio file.
    """
    created_audio = create_audio_file(db, name=audio.name, description=audio.description)
    return BaseResponse(
        status="success",
        message="Audio file created successfully",
        data=created_audio,
    )
