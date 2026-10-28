"""Compact queue statistics along the bottom of the window."""

from __future__ import annotations

import customtkinter as ctk

from core.service import QueueStats
from ui import styles as s


class _StatusCard(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkBaseClass, title: str,
                 description: str, color: str) -> None:
        super().__init__(master, fg_color=s.CARD, corner_radius=s.CARD_RADIUS,
                         border_width=1, border_color=s.BORDER)
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text=title, font=s.LABEL_FONT,
                     text_color=s.SECONDARY, anchor="w"
                     ).grid(row=0, column=0, sticky="ew", padx=18, pady=(12, 0))
        self.value = ctk.CTkLabel(self, text="0", font=s.NUMBER_FONT,
                                  text_color=color, anchor="w")
        self.value.grid(row=1, column=0, sticky="ew", padx=18)
        ctk.CTkLabel(self, text=description, font=s.SMALL_FONT,
                     text_color=s.SECONDARY, anchor="w"
                     ).grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 12))


class StatusCards(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkBaseClass) -> None:
        super().__init__(master, fg_color="transparent")
        for column in range(3):
            self.grid_columnconfigure(column, weight=1, uniform="status")

        self.waiting = _StatusCard(self, "Waiting Patients", "Currently in queue", s.PRIMARY)
        self.served = _StatusCard(self, "Patients Served", "Called from queue", s.SUCCESS)
        self.next_token = _StatusCard(self, "Next Token", "At the front of queue", s.HEADING)
        self.waiting.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.served.grid(row=0, column=1, sticky="ew", padx=8)
        self.next_token.grid(row=0, column=2, sticky="ew", padx=(8, 0))

    def update_stats(self, stats: QueueStats) -> None:
        self.waiting.value.configure(text=str(stats.waiting))
        self.served.value.configure(text=str(stats.served))
        self.next_token.value.configure(
            text=f"#{stats.next_token:03d}" if stats.next_token is not None else "—"
        )
