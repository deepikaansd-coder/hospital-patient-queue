"""Main window and coordination between the UI and core service."""

from typing import Optional

import customtkinter as ctk

from core.patient import Patient
from core.service import PatientService
from ui import styles as s
from ui.header import Header
from ui.queue_display import QueueDisplayCard
from ui.registration import RegistrationCard
from ui.status_cards import StatusCards


class HospitalApp(ctk.CTk):
    def __init__(self, service: Optional[PatientService] = None) -> None:
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        super().__init__()
        self.title("Hospital Patient Waiting System")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(fg_color=s.BACKGROUND)
        self._service = service or PatientService()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        Header(self).grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=20)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=43, uniform="main")
        main.grid_columnconfigure(1, weight=57, uniform="main")

        self.registration = RegistrationCard(main, self._register_patient)
        self.registration.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.queue_display = QueueDisplayCard(main, self._call_next, self._peek_next)
        self.queue_display.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self.status_cards = StatusCards(self)
        self.status_cards.grid(row=2, column=0, sticky="ew", padx=20, pady=(12, 20))
        self._refresh()

    def _refresh(self) -> None:
        self.queue_display.update_patients(self._service.waiting_patients())
        self.status_cards.update_stats(self._service.stats())

    def _register_patient(self, name: str, age: str, reason: str) -> Patient:
        patient = self._service.register(name, age, reason)
        self._refresh()
        self.queue_display.show_feedback("")
        return patient

    def _call_next(self) -> None:
        patient = self._service.call_next()
        if patient is None:
            self.queue_display.show_feedback("No patients are waiting.")
        else:
            self.queue_display.show_feedback(
                f"Calling Token #{patient.token:03d} — {patient.name}"
            )
        self._refresh()

    def _peek_next(self) -> None:
        patient = self._service.peek()
        if patient is None:
            self.queue_display.show_feedback("No patients are waiting.")
        else:
            self.queue_display.show_feedback(
                f"Next: Token #{patient.token:03d} — {patient.name}"
            )
