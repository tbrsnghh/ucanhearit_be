from sqlalchemy.orm import Session
from app.models.models import AudioFile
from uuid import uuid4
from fastapi import HTTPException, Response
import os

from app.schemas.audio import AudioData, AudioListData, BaseResponse

UPLOAD_FOLDER = "uploads/"

async def save_audio_file(file, description: str, db: Session) -> BaseResponse:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Tạo ID duy nhất cho file
    unique_id = str(uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, unique_id + "_" + file.filename)

    # Lưu file lên server
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Lưu thông tin vào database (PostgreSQL)
    audio = AudioFile(
        name=file.filename,
        description=description,
        path=file_path
    )

    # Thêm vào database và commit
    db.add(audio)
    db.commit()
    db.refresh(audio)

    # Trả về phản hồi thành công
    return BaseResponse(
        status="success",
        data=AudioData(id=audio.id, name=audio.name, description=audio.description, path=audio.path).dict(),
        message="File uploaded successfully."
    )
# Lấy file về từ server
async def get_audio_file(audio_id: int, db: Session) -> BaseResponse:
    audio = db.query(AudioFile).filter(AudioFile.id == audio_id).first()
    if not audio:
        raise HTTPException(status_code=404, detail="Audio not found.")
    
    # Đọc nội dung file
    with open(audio.path, "rb") as f:
        file_content = await f.read()
    
    # Trả về file
    return Response(content=file_content, media_type="audio/mp3")
# Lấy tất cả audio files
def get_all_audio_files(db: Session, skip: int = 0, limit: int = 10) -> BaseResponse:
    total = db.query(AudioFile).count()
    files = db.query(AudioFile).offset(skip).limit(limit).all()
    audio_list = [AudioData(id=file.id, name=file.name, description=file.description, path=file.path).dict() for file in files]
    return BaseResponse(
        status="success",
        data=AudioListData(total=total, items=audio_list),
        message="Fetched all audio files."
    )

# Lấy thông tin audio theo ID
def get_audio_file_by_id(audio_id: int, db: Session) -> BaseResponse:
    audio = db.query(AudioFile).filter(AudioFile.id == audio_id).first()
    if not audio:
        raise HTTPException(status_code=404, detail="Audio not found.")
    
    # Trả về thông tin file
    return BaseResponse(
        status="success",
        data=AudioData.from_orm(audio).dict(),
        message="Audio fetched successfully."
    )


# Lấy thông tin audio theo tên
def get_audio_file_by_name(name: str, db: Session) -> BaseResponse:
    audio = db.query(AudioFile).filter(AudioFile.name == name).first()
    if not audio:
        raise HTTPException(status_code=404, detail="Audio not found.")
    
    return BaseResponse(
        status="success",
        data=AudioData.from_orm(audio).dict(),
        message="Audio fetched successfully."
    )
