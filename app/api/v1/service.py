from sqlalchemy.orm import Session
from app.models.models import AudioFile


def get_audio_files(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a paginated list of audio files and the total count.
    """
    total = db.query(AudioFile).count()
    files = db.query(AudioFile).offset(skip).limit(limit).all()
    return total, files


def create_audio_file(db: Session, name: str, description: str = None):
    """
    Create a new audio file.
    """
    audio = AudioFile(name=name, description=description)
    db.add(audio)
    db.commit()
    db.refresh(audio)
    return {"id": audio.id, "name": audio.name, "description": audio.description}
