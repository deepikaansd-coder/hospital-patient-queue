"""Application heading and queue type badge."""

from __future__ import annotations

import customtkinter as ctk

from ui import styles as s


class Header(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkBaseClass) -> None:
        super().__init__(master, fg_color=s.CARD, corner_radius=s.CARD_RADIUS,
                         border_width=1, border_color=s.BORDER)
        self.grid_columnconfigure(1, weight=1)

        icon = ctk.CTkFrame(self, width=52, height=52, fg_color=s.PALE_BLUE,
                            corner_radius=12)
        icon.grid(row=0, column=0, rowspan=2, padx=(22, 16), pady=18)
        icon.grid_propagate(False)
        ctk.CTkLabel(icon, text="✚", font=(s.FONT, 28, "bold"),
                     text_color=s.PRIMARY).pack(expand=True, fill="both")

        ctk.CTkLabel(self, text="Hospital Patient Waiting System",
                     font=s.TITLE_FONT, text_color=s.HEADING, anchor="w"
                     ).grid(row=0, column=1, sticky="ew", pady=(16, 0))
        ctk.CTkLabel(self, text="Queue Management Using FIFO",
                     font=s.BODY_FONT, text_color=s.SECONDARY, anchor="w"
                     ).grid(row=1, column=1, sticky="ew", pady=(0, 17))

        badge = ctk.CTkLabel(self, text="FIFO Queue", font=s.LABEL_FONT,
                             text_color=s.PRIMARY, fg_color=s.PALE_BLUE,
                             corner_radius=8, width=96, height=30)
        badge.grid(row=0, column=2, rowspan=2, padx=(8, 22))
