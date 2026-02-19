"""Import all models so that Base.metadata.create_all() registers them."""
from backend.models.guild import Guild
from backend.models.category import Category
from backend.models.channel import Channel

__all__ = ["Guild", "Category", "Channel"]
