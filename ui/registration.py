"""Patient registration form and its inline feedback."""

from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from core.patient import Patient
from ui import styles as s


class RegistrationCard(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkBaseClass,
                 on_add: Callable[[str, str, str], Patient]) -> None:
        super().__init__(master, fg_color=s.CARD, corner_radius=s.CARD_RADIUS,
                         border_width=1, border_color=s.BORDER)
        self._on_add = on_add
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                         scrollbar_button_color=s.BORDER,
                                         scrollbar_button_hover_color=s.SECONDARY)
        content.grid(row=0, column=0, sticky="nsew", padx=16, pady=14)
        content.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(content, text="Patient Registration", font=s.SECTION_FONT,
                     text_color=s.HEADING, anchor="w"
                     ).grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(content, text="Enter patient details to join the waiting queue",
                     font=s.BODY_FONT, text_color=s.SECONDARY, anchor="w",
                     wraplength=320, justify="left"
                     ).grid(row=1, column=0, sticky="ew", pady=(3, 15))

        self.name_entry = self._field(content, 2, "Patient Name", "e.g. Asha Kumar")
        self.age_entry = self._field(content, 4, "Age", "Enter age in years")
        self.reason_entry = self._field(content, 6, "Reason for Visit", "e.g. General consultation")

        ctk.CTkButton(content, text="Add Patient to Queue", command=self._submit,
                      font=s.LABEL_FONT, fg_color=s.PRIMARY,
                      hover_color=s.PRIMARY_HOVER, corner_radius=s.CONTROL_RADIUS,
                      height=42).grid(row=8, column=0, sticky="ew", pady=(17, 0))
        self.message = ctk.CTkLabel(content, text="", font=s.SMALL_FONT,
                                    text_color=s.SECONDARY, anchor="w",
                                    justify="left", wraplength=320)
        self.message.grid(row=9, column=0, sticky="ew", pady=(7, 0))

        self.name_entry.bind("<Return>", self._focus_age)
        self.age_entry.bind("<Return>", self._focus_reason)
        self.reason_entry.bind("<Return>", self._submit)

    @staticmethod
    def _field(parent: ctk.CTkScrollableFrame, row: int,
               label: str, placeholder: str) -> ctk.CTkEntry:
        ctk.CTkLabel(parent, text=label, font=s.LABEL_FONT,
                     text_color=s.HEADING, anchor="w"
                     ).grid(row=row, column=0, sticky="ew", pady=(0, 5))
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder,
                             height=38, font=s.BODY_FONT,
                             fg_color=s.CARD, border_color=s.BORDER,
                             corner_radius=s.CONTROL_RADIUS)
        entry.grid(row=row + 1, column=0, sticky="ew",
                   pady=(0, 12 if row < 6 else 0))
        return entry

    def _focus_age(self, _event: object) -> None:
        self.age_entry.focus_set()

    def _focus_reason(self, _event: object) -> None:
        self.reason_entry.focus_set()

    def _submit(self, _event: object = None) -> None:
        try:
            patient = self._on_add(self.name_entry.get(), self.age_entry.get(),
                                   self.reason_entry.get())
        except ValueError as error:
            self.message.configure(text=str(error), text_color=s.ERROR)
            return

        for entry in (self.name_entry, self.age_entry, self.reason_entry):
            entry.delete(0, "end")
        self.message.configure(text=f"Patient registered successfully — Token #{patient.token:03d}.",
                               text_color=s.SUCCESS)
        self.name_entry.focus_set()
