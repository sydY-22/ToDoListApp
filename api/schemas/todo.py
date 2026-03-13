from pydantic import BaseModel, Field
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from api.models.todo import Todo


GetTodo = pydantic_model_creator(Todo, name="Todo")

class CreateTodo(BaseModel):
    task: str = Field(..., max_length=100)
    done:bool=False


class PutTodo(BaseModel):
    task:Optional[str] = Field(None, max_length=100)
    done:Optional[bool]

