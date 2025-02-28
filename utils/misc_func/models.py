from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    username: str
    balance: float
    bot_id: int

    