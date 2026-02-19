from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from ..database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(String, primary_key=True, index=True)
    guild_id = Column(String, ForeignKey("guilds.id"), nullable=False)
    name = Column(String, nullable=False)
    color = Column(Integer, default=0)
    position = Column(Integer, default=0)
    permissions = Column(String, default="0")  # Bitfield als String
    managed = Column(Boolean, default=False)
