from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.connection_db import init_db

from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.connection_db import init_db, get_session
from operations.operations_db import create_pet, get_pet, update_pet, delete_pet, get_all_pets
from data.models import Pet
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

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