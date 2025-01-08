from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.models.models import AudioFile
from app.schemas.audio import AudioCreate, BaseResponse, AudioListData, AudioData
from app.services.audio_service import  get_all_audio_files, get_audio_file_by_id, get_audio_file_by_name, save_audio_file
from app.database import get_db

router = APIRouter()


@router.get("/file/{audio_id}", response_class=FileResponse)
async def get_audio_file(audio_id: int, db: Session = Depends(get_db)):
    audio = db.query(AudioFile).filter(AudioFile.id == audio_id).first()
    if not audio:
        raise HTTPException(status_code=404, detail="Audio not found.")
    
    # Trả về file từ server
    return FileResponse(audio.path, media_type="audio/mp3")


@router.post("/file", response_model=BaseResponse)
async def upload_audio(file: UploadFile, description: str = "", db: Session = Depends(get_db)):
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only MP3 files are allowed.")
    return await save_audio_file(file, description, db)
@router.get("/", response_model=BaseResponse)
async def get_all_audios(db: Session = Depends(get_db)):
    return get_all_audio_files(db=db)

@router.get("/{audio_id}", response_model=BaseResponse)
async def get_audio_by_id(audio_id: int, db: Session = Depends(get_db)):
    return get_audio_file_by_id(audio_id, db)

@router.get("/name/{audio_name}", response_model=BaseResponse)
async def get_audio_by_name(audio_name: str, db: Session = Depends(get_db)):
    return get_audio_file_by_name(audio_name, db)

