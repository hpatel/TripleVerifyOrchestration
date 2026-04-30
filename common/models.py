<<<<<<< HEAD
from pydantic import BaseModel
from typing import Any, Dict, List

class QueryRequest(BaseModel):
    query: str

class AgentResponse(BaseModel):
=======
from pydantic import BaseModel
from typing import Any, Dict, List

class QueryRequest(BaseModel):
    query: str

class AgentResponse(BaseModel):
>>>>>>> 957bc36 (Moving all config to .env file. Improvig dependency install time by using uv. Fix minor port issues.)
    result: Dict[str, Any]