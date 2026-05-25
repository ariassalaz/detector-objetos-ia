from tkinter import BOTH, YES, X, LEFT, RIGHT, W, NS, NSEW, BOTTOM
import ttkbootstrap as ttk

CLASSES = [
    ("Bache",        "danger"),
    ("Alcantarilla", "primary"),
    ("Red",          "purple"),
    ("Conos",        "warning"),
    ("Ballena",      "success"),
]

CLASS_HEX = {
    "Bache":        "#ef4444",
    "Alcantarilla": "#3b82f6",
    "Red":          "#8b5cf6",
    "Conos":        "#f59e0b",
    "Ballena":      "#10b981",
}


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Detector De Accesibilidad Urbana")
        self.geometry("1100x660")
        self.minsize(900, 560)
        self._build_ui()

    def _build_ui(self):
        self._build_header()

        body = ttk.Frame(self)
        body.pack(fill=BOTH, expand=YES, padx=20, pady=(0, 20))
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_sidebar(body)
        self._build_main(body)
        self._build_statusbar()

    # ── Header ──────────
    def _build_header(self):
        header = ttk.Frame(self, bootstyle="light")
        header.pack(fill=X)

        ttk.Separator(self).pack(fill=X)

        left = ttk.Frame(header, bootstyle="light")
        left.pack(side=LEFT, padx=24, pady=14)

        ttk.Label(
            left,
            text="Detector De Accesibilidad Urbana",
            font=("Segoe UI", 15, "bold"),
            foreground="#000000",
            background=self.style.colors.light,
        ).pack(anchor=W)

    # ── Sidebar ───────────
    def _build_sidebar(self, parent):
        sidebar = ttk.Frame(parent, bootstyle="light", width=210)
        sidebar.grid(row=0, column=0, sticky=NS, padx=(0, 16), pady=16)
        sidebar.pack_propagate(False)

        bg = self.style.colors.light

        # Acciones
        ttk.Label(
            sidebar, text="ACCIONES",
            font=("Segoe UI", 8, "bold"),
            foreground="#000000", background=bg,
        ).pack(anchor=W, padx=16, pady=(18, 6))

        ttk.Button(
            sidebar, text="  Cargar imagen",
            bootstyle="primary-outline", width=22,
            command=lambda: None,
        ).pack(padx=16, pady=3, fill=X)

        ttk.Button(
            sidebar, text="  Detectar",
            bootstyle="success", width=22,
            command=lambda: None,
        ).pack(padx=16, pady=3, fill=X)

        ttk.Separator(sidebar).pack(fill=X, padx=16, pady=14)

        # Clases
        ttk.Label(
            sidebar, text="CLASES",
            font=("Segoe UI", 8, "bold"),
            foreground="#000000", background=bg,
        ).pack(anchor=W, padx=16, pady=(0, 6))

        for name, color_hex in CLASS_HEX.items():
            row = ttk.Frame(sidebar, bootstyle="light")
            row.pack(fill=X, padx=16, pady=3)

            ttk.Label(
                row, text="●", foreground=color_hex,
                background=bg, font=("Segoe UI", 10),
            ).pack(side=LEFT, padx=(0, 8))

            ttk.Label(
                row, text=name,
                font=("Segoe UI", 10),
                foreground="#000000", background=bg,
            ).pack(side=LEFT)


    # ── Área principal ─────────────────────────────────────────────────────────
    def _build_main(self, parent):
        main = ttk.Frame(parent)
        main.grid(row=0, column=1, sticky=NSEW, pady=16)
        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)

        card = ttk.LabelFrame(main, text="Vista previa")
        card.grid(row=0, column=0, sticky=NSEW)
        card.rowconfigure(0, weight=1)
        card.columnconfigure(0, weight=1)

        placeholder = ttk.Frame(card)
        placeholder.grid(row=0, column=0, padx=20, pady=20)

        ttk.Label(
            placeholder,
            text="↑",
            font=("Segoe UI", 52),
            bootstyle="secondary",
        ).pack(pady=(40, 8))

        ttk.Label(
            placeholder,
            text="Carga una imagen para comenzar",
            font=("Segoe UI", 13),
            bootstyle="secondary",
        ).pack()

        ttk.Label(
            placeholder,
            text="JPG  ·  JPEG  ·  PNG",
            font=("Segoe UI", 9),
            bootstyle="secondary",
        ).pack(pady=(4, 16))

        ttk.Button(
            placeholder,
            text="Seleccionar archivo",
            bootstyle="primary-outline",
            command=lambda: None,
        ).pack()

    # ── Status bar ─────────────────────────────────────────────────────────────
    def _build_statusbar(self):
        ttk.Separator(self).pack(fill=X)

        bar = ttk.Frame(self, bootstyle="light")
        bar.pack(fill=X, side=BOTTOM)

if __name__ == "__main__":
    App().mainloop()
