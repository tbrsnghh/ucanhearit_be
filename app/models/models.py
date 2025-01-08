from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
