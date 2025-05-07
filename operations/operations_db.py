'''Aqui debes construir las operaciones que se te han indicado'''

from data.models import Pet, Task, User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

# Operaciones para Pet (existentes)
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
        if name: pet.name = name
        if species: pet.species = species
        if age: pet.age = age
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

# Operaciones para Task
async def create_task(session: AsyncSession, title: str, description: Optional[str] = None) -> Task:
    task = Task(title=title, description=description)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_task(session: AsyncSession, task_id: int) -> Task:
    return await session.get(Task, task_id)

async def update_task(session: AsyncSession, task_id: int, title: str = None, description: str = None, status: str = None) -> Task:
    task = await session.get(Task, task_id)
    if task:
        if title: task.title = title
        if description: task.description = description
        if status: task.status = status
        await session.commit()
        await session.refresh(task)
    return task

async def delete_task(session: AsyncSession, task_id: int) -> bool:
    task = await session.get(Task, task_id)
    if task:
        await session.delete(task)
        await session.commit()
        return True
    return False

async def get_all_tasks(session: AsyncSession) -> list[Task]:
    result = await session.exec(select(Task))
    return result.all()

# Operaciones para User
async def create_user(session: AsyncSession, username: str, email: str, password: str) -> User:
    user = User(username=username, email=email, password=password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user(session: AsyncSession, user_id: int) -> User:
    return await session.get(User, user_id)

async def delete_user(session: AsyncSession, user_id: int) -> bool:
    user = await session.get(User, user_id)
    if user:
        await session.delete(user)
        await session.commit()
        return True
    return False

async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.exec(select(User))
    return result.all()