"""Scrollable queue view and actions."""

from __future__ import annotations

from typing import Callable, Sequence

import customtkinter as ctk

from core.patient import Patient
from ui import styles as s


class QueueDisplayCard(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkBaseClass,
                 on_call: Callable[[], None], on_peek: Callable[[], None]) -> None:
        super().__init__(master, fg_color=s.CARD, corner_radius=s.CARD_RADIUS,
                         border_width=1, border_color=s.BORDER)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        heading = ctk.CTkFrame(self, fg_color="transparent")
        heading.grid(row=0, column=0, sticky="ew", padx=20, pady=(17, 12))
        heading.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(heading, text="Waiting Queue", font=s.SECTION_FONT,
                     text_color=s.HEADING, anchor="w"
                     ).grid(row=0, column=0, sticky="ew")
        self.count_label = ctk.CTkLabel(heading, text="0 waiting", font=s.LABEL_FONT,
                                        text_color=s.PRIMARY, fg_color=s.PALE_BLUE,
                                        corner_radius=8, height=29)
        self.count_label.grid(row=0, column=1, padx=(10, 0), ipadx=10)

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color=s.ROW_ALT,
                                                 corner_radius=9,
                                                 scrollbar_button_color=s.BORDER,
                                                 scrollbar_button_hover_color=s.SECONDARY)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        self.list_frame.grid_columnconfigure(0, weight=1)

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=20, pady=(11, 17))
        footer.grid_columnconfigure((0, 1), weight=1)
        self.call_button = ctk.CTkButton(footer, text="Call Next Patient",
                                         command=on_call, font=s.LABEL_FONT,
                                         fg_color=s.SUCCESS,
                                         hover_color=s.SUCCESS_HOVER,
                                         corner_radius=s.CONTROL_RADIUS, height=40)
        self.call_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.peek_button = ctk.CTkButton(footer, text="Peek Next Patient",
                                         command=on_peek, font=s.LABEL_FONT,
                                         fg_color=s.PALE_BLUE, text_color=s.PRIMARY,
                                         hover_color="#DBEAFE",
                                         corner_radius=s.CONTROL_RADIUS, height=40)
        self.peek_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))
        self.feedback = ctk.CTkLabel(footer, text="", font=s.SMALL_FONT,
                                     text_color=s.SECONDARY, anchor="w",
                                     justify="left", wraplength=460)
        self.feedback.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5, 0))

    def show_feedback(self, text: str) -> None:
        self.feedback.configure(text=text)

    def update_patients(self, patients: Sequence[Patient]) -> None:
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        count = len(patients)
        self.count_label.configure(text=f"{count} waiting")
        state = "normal" if count else "disabled"
        self.call_button.configure(state=state)
        self.peek_button.configure(state=state)

        if not patients:
            empty = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            empty.grid(row=0, column=0, sticky="ew", pady=55)
            ctk.CTkLabel(empty, text="○", font=(s.FONT, 30),
                         text_color=s.SECONDARY).pack()
            ctk.CTkLabel(empty, text="No patients waiting",
                         font=(s.FONT, 17, "bold"),
                         text_color=s.HEADING).pack(pady=(4, 2))
            ctk.CTkLabel(empty, text="Register a patient to begin the queue.",
                         font=s.BODY_FONT, text_color=s.SECONDARY).pack()
            return

        columns = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        columns.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 5))
        self._configure_columns(columns)
        for column, title in enumerate(("TOKEN", "PATIENT", "AGE", "REASON FOR VISIT")):
            ctk.CTkLabel(columns, text=title, font=(s.FONT, 11, "bold"),
                         text_color=s.SECONDARY, anchor="w"
                         ).grid(row=0, column=column, sticky="ew", padx=4)

        for index, patient in enumerate(patients, start=1):
            self._patient_row(index, patient)

    @staticmethod
    def _configure_columns(frame: ctk.CTkFrame) -> None:
        frame.grid_columnconfigure(0, minsize=60)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, minsize=42)
        frame.grid_columnconfigure(3, weight=2)

    def _patient_row(self, index: int, patient: Patient) -> None:
        row = ctk.CTkFrame(self.list_frame, fg_color=s.CARD,
                           corner_radius=8, border_width=1,
                           border_color=s.BORDER)
        row.grid(row=index, column=0, sticky="ew", padx=5, pady=4)
        self._configure_columns(row)

        token_frame = ctk.CTkFrame(row, fg_color="transparent")
        token_frame.grid(row=0, column=0, sticky="w", padx=(9, 2), pady=9)
        ctk.CTkLabel(token_frame, text=f"#{patient.token:03d}",
                     font=s.LABEL_FONT, text_color=s.PRIMARY,
                     anchor="w").pack(anchor="w")
        if index == 1:
            ctk.CTkLabel(token_frame, text="FRONT", font=(s.FONT, 10, "bold"),
                         text_color=s.SUCCESS, fg_color=s.PALE_GREEN,
                         corner_radius=5, height=19, width=48).pack(anchor="w", pady=(3, 0))

        ctk.CTkLabel(row, text=patient.name, font=s.BODY_FONT,
                     text_color=s.HEADING, wraplength=135,
                     justify="left", anchor="w"
                     ).grid(row=0, column=1, sticky="ew", padx=4, pady=9)
        ctk.CTkLabel(row, text=str(patient.age), font=s.BODY_FONT,
                     text_color=s.SECONDARY, anchor="w"
                     ).grid(row=0, column=2, sticky="ew", padx=4, pady=9)
        ctk.CTkLabel(row, text=patient.reason, font=s.BODY_FONT,
                     text_color=s.SECONDARY, wraplength=150,
                     justify="left", anchor="w"
                     ).grid(row=0, column=3, sticky="ew", padx=(4, 9), pady=9)
