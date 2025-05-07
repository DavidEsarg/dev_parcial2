from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from utils.connection_db import init_db, get_session
from operations.operations_db import (
    create_pet, get_pet, update_pet, delete_pet, get_all_pets,
    create_task, get_task, update_task, delete_task, get_all_tasks,
    create_user, get_user, update_user_status, get_users_by_status, get_all_users, delete_user
)
from data.models import Pet, Task, User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional  # Añadir esta línea

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

# Endpoints para Pet
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
@app.post("/users/")
async def create_user_endpoint(username: str, email: str, password: str, session: AsyncSession = Depends(get_session)):
    user = await create_user(session, username, email, password)
    return user

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user(session, user_id)
    return user

@app.put("/users/{user_id}/status")
@app.patch("/users/{user_id}/status")
async def update_user_status_endpoint(user_id: int, status: str, session: AsyncSession = Depends(get_session)):
    user = await update_user_status(session, user_id, status)
    return user

@app.put("/users/{user_id}/make-premium")
@app.patch("/users/{user_id}/make-premium")
async def make_user_premium(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await update_user_status(session, user_id, "premium")
    return user

@app.put("/users/{user_id}/make-inactive")
@app.patch("/users/{user_id}/make-inactive")
async def make_user_inactive(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await update_user_status(session, user_id, "inactive")
    return user

@app.get("/users/inactive")
async def get_inactive_users(session: AsyncSession = Depends(get_session)):
    users = await get_users_by_status(session, "inactive")
    return users

@app.get("/users/premium-inactive")
async def get_premium_and_inactive_users(session: AsyncSession = Depends(get_session)):
    inactive_users = await get_users_by_status(session, "inactive")
    premium_users = await get_users_by_status(session, "premium")
    return {"inactive": inactive_users, "premium": premium_users}

@app.get("/users/")
async def list_users(session: AsyncSession = Depends(get_session)):
    users = await get_all_users(session)
    return users

@app.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: int, session: AsyncSession = Depends(get_session)):
    success = await delete_user(session, user_id)
    return {"success": success}