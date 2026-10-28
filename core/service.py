"""Registration, validation, token assignment, and queue statistics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from core.patient import Patient
from core.queue import PatientQueue


@dataclass(frozen=True)
class QueueStats:
    waiting: int
    served: int
    next_token: Optional[int]


class PatientService:
    def __init__(self) -> None:
        self._queue = PatientQueue()
        self._next_token = 1
        self._served = 0

    def register(self, name: str, age_text: str, reason: str) -> Patient:
        name = name.strip()
        age_text = age_text.strip()
        reason = reason.strip()

        if not name:
            raise ValueError("Enter the patient's name.")
        if len(name) > 80:
            raise ValueError("Patient name must be 80 characters or fewer.")
        if not age_text:
            raise ValueError("Enter the patient's age.")
        if not age_text.isdecimal() or len(age_text) > 3:
            raise ValueError("Age must be a whole number from 0 to 120.")
        age = int(age_text)
        if age > 120:
            raise ValueError("Age must be a whole number from 0 to 120.")
        if not reason:
            raise ValueError("Enter a reason for the visit.")
        if len(reason) > 150:
            raise ValueError("Reason for visit must be 150 characters or fewer.")

        patient = Patient(self._next_token, name, age, reason)
        self._queue.enqueue(patient)
        self._next_token += 1
        return patient

    def call_next(self) -> Optional[Patient]:
        patient = self._queue.dequeue()
        if patient is not None:
            self._served += 1
        return patient

    def peek(self) -> Optional[Patient]:
        return self._queue.peek()

    def waiting_patients(self) -> Tuple[Patient, ...]:
        return self._queue.snapshot()

    def stats(self) -> QueueStats:
        first = self._queue.peek()
        return QueueStats(
            waiting=len(self._queue),
            served=self._served,
            next_token=first.token if first is not None else None,
        )
