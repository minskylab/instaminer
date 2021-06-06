from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InstaminerPost(BaseModel):
    id: str
    date: datetime
    hashtags: str
    mentions: str
    image_uri: str
    likes: int
    comments: int
    relevance: float
    description: Optional[str]
    comments_content: Optional[str]
