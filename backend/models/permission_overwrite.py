from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class PermissionOverwrite(Base):
    __tablename__ = "permission_overwrites"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    channel_id = Column(String, ForeignKey("channels.id"), nullable=False)
    target_id = Column(String, nullable=False)  # Role ID or User ID
    target_type = Column(String, nullable=False)  # 'role' or 'member'
    allow = Column(String, default="0")  # Bitfield
    deny = Column(String, default="0")  # Bitfield
    
    channel = relationship("Channel", back_populates="overwrites")
