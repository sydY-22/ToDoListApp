from fastapi import APIRouter, HTTPException, status
from api.models.todo import Todo
from api.schemas.todo import GetTodo, CreateTodo, PutTodo


todo_router = APIRouter(prefix="/api", tags=["Todo"])


@todo_router.get("/")
async def all_todos():
    return await GetTodo.from_queryset(Todo.all().order_by("-id"))


@todo_router.get("/{key}")
async def get_todo_by_key(key:int):
    todo = await Todo.get_or_none(id=key)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found!")

    return await GetTodo.from_tortoise_orm(todo)


@todo_router.post("/")
async def create_todo(body: CreateTodo):
    row = await Todo.create(**body.model_dump(exclude_unset=True))
    return await GetTodo.from_tortoise_orm(row)


@todo_router.put("/{key}")
async def update_todo(key:int, body:PutTodo):
    todo = await Todo.get_or_none(id=key)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found!")

    await todo.update_from_dict(body.model_dump(exclude_unset=True))
    await todo.save()

    return await GetTodo.from_tortoise_orm(todo)


@todo_router.delete("/{key}")
async def delete_todo(key:int):
    todo = await Todo.get_or_none(id=key)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found!")
    await todo.delete()
    
    return {"message": "Todo deleted successfully!"}

# test