'''Aqui debes consignar el modelo que se te indico en el parcial
Escribe aquí el que te corresponde.

'''
from sqlmodel import SQLModel, Field
from typing import Optional

class Pet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    species: str
    age: int