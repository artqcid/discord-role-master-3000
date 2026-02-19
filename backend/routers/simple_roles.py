from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["SimpleRoles"])

@router.get("/simple-roles")
async def get_simple_roles():
    logger.info("Simple Roles Endpoint HIT!")
    return [{"id": "1", "name": "Simple Role", "color": 0xFFFFFF}]
