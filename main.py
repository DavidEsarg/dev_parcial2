from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.connection_db import init_db

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from utils.connection_db import init_db, get_session
from operations.operations_db import (
    create_pet, get_pet, update_pet, delete_pet, get_all_pets,
    create_task, get_task, update_task, delete_task, get_all_tasks,
    create_user, get_user, delete_user, get_all_users
)
from data.models import Pet, Task, User
from sqlalchemy.ext.asyncio import AsyncSession

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Endpoints para Pet (existentes)
@app.post("/pets/")
async def create_new_pet(name: str, species: str, age: int, session: AsyncSession = Depends(get_session)):
    pet = await create_pet(session, name, species, age)
    return pet

@app.get("/pets/{pet_id}")
async def read_pet(pet_id: int, session: AsyncSession = Depends(get_session)):
    pet = await get_pet(session, pet_id)
    return pet

@app.put("/pets/{pet_id}")
async def update_existing_pet(pet_id: int, name: str = None, species: str = None, age: int = None, session: AsyncSession = Depends(get_session)):
    pet = await update_pet(session, pet_id, name, species, age)
    return pet

@app.delete("/pets/{pet_id}")
async def delete_existing_pet(pet_id: int, session: AsyncSession = Depends(get_session)):
    success = await delete_pet(session, pet_id)
    return {"success": success}

@app.get("/pets/")
async def read_all_pets(session: AsyncSession = Depends(get_session)):
    pets = await get_all_pets(session)
    return pets

# Endpoints para Task
@app.get("/tasks/")
async def list_tasks(session: AsyncSession = Depends(get_session)):
    tasks = await get_all_tasks(session)
    return tasks

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await get_task(session, task_id)
    return task

@app.post("/tasks/")
async def create_task_endpoint(title: str, description: Optional[str] = None, session: AsyncSession = Depends(get_session)):
    task = await create_task(session, title, description)
    return task

@app.put("/tasks/{task_id}")
async def update_task_endpoint(task_id: int, title: str = None, description: str = None, status: str = None, session: AsyncSession = Depends(get_session)):
    task = await update_task(session, task_id, title, description, status)
    return task

@app.patch("/tasks/{task_id}")
async def patch_task_endpoint(task_id: int, status: str = None, session: AsyncSession = Depends(get_session)):
    task = await update_task(session, task_id, status=status)
    return task

@app.delete("/tasks/{task_id}")
async def delete_task_endpoint(task_id: int, session: AsyncSession = Depends(get_session)):
    success = await delete_task(session, task_id)
    return {"success": success}

# Endpoints para User
@app.get("/users/")
async def list_users(session: AsyncSession = Depends(get_session)):
    users = await get_all_users(session)
    return users

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user(session, user_id)
    return user

@app.post("/users/")
async def create_user_endpoint(username: str, email: str, password: str, session: AsyncSession = Depends(get_session)):
    user = await create_user(session, username, email, password)
    return user

@app.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: int, session: AsyncSession = Depends(get_session)):
    success = await delete_user(session, user_id)
    return {"success": success}