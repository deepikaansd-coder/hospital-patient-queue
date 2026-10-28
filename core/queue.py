"""A linked FIFO queue with constant-time enqueue and dequeue."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from core.patient import Patient


@dataclass
class _Node:
    patient: Patient
    next: Optional[_Node] = None


class PatientQueue:
    def __init__(self) -> None:
        self._front: Optional[_Node] = None
        self._rear: Optional[_Node] = None
        self._size = 0

    def enqueue(self, patient: Patient) -> None:
        node = _Node(patient)
        if self._rear is None:
            self._front = node
        else:
            self._rear.next = node
        self._rear = node
        self._size += 1

    def dequeue(self) -> Optional[Patient]:
        if self._front is None:
            return None
        patient = self._front.patient
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return patient

    def peek(self) -> Optional[Patient]:
        return self._front.patient if self._front is not None else None

    def snapshot(self) -> Tuple[Patient, ...]:
        patients = []
        node = self._front
        while node is not None:
            patients.append(node.patient)
            node = node.next
        return tuple(patients)

    def __len__(self) -> int:
        return self._size
