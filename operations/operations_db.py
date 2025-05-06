'''Aqui debes construir las operaciones que se te han indicado'''

from sqlmodel.ext.asyncio.session import AsyncSession
from data.models import Pet
from sqlmodel import select

async def create_pet(session: AsyncSession, name: str, species: str, age: int) -> Pet:
    pet = Pet(name=name, species=species, age=age)
    session.add(pet)
    await session.commit()
    await session.refresh(pet)
    return pet

async def get_pet(session: AsyncSession, pet_id: int) -> Pet:
    return await session.get(Pet, pet_id)

async def update_pet(session: AsyncSession, pet_id: int, name: str = None, species: str = None, age: int = None) -> Pet:
    pet = await session.get(Pet, pet_id)
    if pet:
        if name:
            pet.name = name
        if species:
            pet.species = species
        if age:
            pet.age = age
        await session.commit()
        await session.refresh(pet)
    return pet

async def delete_pet(session: AsyncSession, pet_id: int) -> bool:
    pet = await session.get(Pet, pet_id)
    if pet:
        await session.delete(pet)
        await session.commit()
        return True
    return False

async def get_all_pets(session: AsyncSession) -> list[Pet]:
    result = await session.exec(select(Pet))
    return result.all()