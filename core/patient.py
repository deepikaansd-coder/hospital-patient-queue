"""Patient data stored in the waiting queue."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Patient:
    token: int
    name: str
    age: int
    reason: str
