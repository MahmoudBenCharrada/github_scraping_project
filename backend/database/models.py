'''Database Models'''

from pydantic import BaseModel


class User(BaseModel):
    """User model"""

    user_id: int
    username: str


class Repository(BaseModel):
    """Repository model"""

    repo_id: int
    name: str
    url: str
    repo_owner: int