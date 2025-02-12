from pydantic import BaseModel


class JoinGameScheme(BaseModel):
    username: str
