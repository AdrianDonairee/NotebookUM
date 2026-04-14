from fastapi import APIRouter
from pydantic import BaseModel
from ..services.ai_service import AIService

router = APIRouter(prefix="/api/ai", tags=["ai"])
ai_service = AIService()


class AIQueryRequest(BaseModel):
    prompt: str = ""


@router.post("/query")
def query(payload: AIQueryRequest):
    prompt = payload.prompt
    response = ai_service.query(prompt)
    return {"response": response}
