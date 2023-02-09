
from dataclasses import dataclass
from models.Entity import Entity


@dataclass
class Message:

    sender: Entity
    text: str
