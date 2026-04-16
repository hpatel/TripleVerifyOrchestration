from pydantic import BaseModel
from typing import Any, Dict, List

class QueryRequest(BaseModel):
    query: str

class AgentResponse(BaseModel):
    result: Dict[str, Any]