from pydantic import BaseModel
from typing import Optional, Any


class EditorMessage(BaseModel):
    """
    Creating standard for every message traveling through the engine
    """

    type: str
    user_id: str
    content: Optional[Any]



