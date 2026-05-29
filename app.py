from pathlib import Path
from tkinter import BOTH, YES, X, LEFT, RIGHT, W, NS, NSEW, BOTTOM, filedialog
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ultralytics import YOLO 
import numpy as np
import os

CLASS_HEX = {
    "Bache":        "#ef4444",
    "Alcantarilla": "#3b82f6",
    "Red":          "#8b5cf6",
    "Conos":        "#f59e0b",
    "Ballena":      "#10b981",
}

TIPS_SEGURIDAD = {
    "Bache":        "Riesgo de daño estructural o caída. Reduce la velocidad inmediatamente!",
    "Alcantarilla": "Peligro de hundimiento o neumático atorado!",
    "Red":          "Zona de obras activa. Mantener distancia por caída de escombros!",
    "Conos":        "Desvío u obstáculo temporal. Cambia de carril con precaución!",
    "Ballena":      "Barrera rígida de seguridad. Con cuidado!",
}


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Detector De Accesibilidad Urbana")
        self.geometry("1100x740") 
        self.minsize(950, 640)
        self._img_ref = None     
        self.current_image = None   
        self.analyzed_image = None  
        
        print("Cargando modelo de IA...")
        self.model = YOLO("models/best.pt")
        
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
        sidebar = ttk.Frame(parent, bootstyle="light", width=230)
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
            command=self._load_image,
        ).pack(padx=16, pady=3, fill=X)

        ttk.Button(
            sidebar, text="  Detectar",
            bootstyle="success", width=22,
            command=self._detect_objects,
        ).pack(padx=16, pady=3, fill=X)

        self.btn_save = ttk.Button(
            sidebar, text="  Guardar resultado",
            bootstyle="secondary", width=22,
            command=self._save_report,
            state="disabled"
        )
        self.btn_save.pack(padx=16, pady=3, fill=X)

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

        ttk.Separator(sidebar).pack(fill=X, padx=16, pady=14)

        # Panel de Resultados 
        self.stats_panel = ttk.LabelFrame(sidebar, text=" Resultados del Análisis ")
        self.stats_panel.pack(fill=X, padx=16, pady=5, side=BOTTOM)
        
        self.lbl_total = ttk.Label(self.stats_panel, text="Objetos: -", font=("Segoe UI", 10))
        self.lbl_total.pack(anchor=W, padx=10, pady=4)
        
        self.lbl_detail = ttk.Label(self.stats_panel, text="Esperando análisis...", font=("Segoe UI", 9), bootstyle="secondary")
        self.lbl_detail.pack(anchor=W, padx=10, pady=(0, 4))

        #Alerta de seguridad dinamica
        self.lbl_tip = ttk.Label(
            self.stats_panel, 
            text="", 
            font=("Segoe UI", 8, "italic"), 
            wraplength=190,  
            justify=LEFT
        )
        self.lbl_tip.pack(anchor=W, padx=10, pady=(4, 8))

    # ── Área principal ─────────────────────────────────────────────────────────
    def _build_main(self, parent):
        main = ttk.Frame(parent)
        main.grid(row=0, column=1, sticky=NSEW, pady=16)
        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)

        self._card = ttk.LabelFrame(main, text="Vista previa")
        self._card.grid(row=0, column=0, sticky=NSEW)
        self._card.rowconfigure(0, weight=1)
        self._card.columnconfigure(0, weight=1)

        # Placeholder
        self._placeholder = ttk.Frame(self._card)
        self._placeholder.grid(row=0, column=0)

        ttk.Label(
            self._placeholder, text="↑",
            font=("Segoe UI", 52), bootstyle="secondary",
        ).pack(pady=(40, 8))
        ttk.Label(
            self._placeholder,
            text="Carga una imagen para comenzar",
            font=("Segoe UI", 13), bootstyle="secondary",
        ).pack()
        ttk.Label(
            self._placeholder, text="JPG  ·  JPEG  ·  PNG",
            font=("Segoe UI", 9), bootstyle="secondary",
        ).pack(pady=(4, 16))
        ttk.Button(
            self._placeholder, text="Seleccionar archivo",
            bootstyle="primary-outline",
            command=self._load_image,
        ).pack()

        self._image_label = ttk.Label(self._card)

    # ── Carga de imagen ───────────────
    def _load_image(self):
        path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png"),
                       ("Todos los archivos", "*.*")],
        )
        if not path:
            return

        self.current_image = Image.open(path)
        self.analyzed_image = None 
        self.btn_save.configure(state="disabled", bootstyle="secondary")
        
        self.lbl_total.configure(text="Objetos: -")
        self.lbl_detail.configure(text="Esperando análisis...", bootstyle="secondary")
        self.lbl_tip.configure(text="") 

        self._display_image(self.current_image)
        self._status_var.set(f"Imagen cargada: {Path(path).name}")

    def _display_image(self, img: Image.Image):
        self.update_idletasks()
        max_w = max(self._card.winfo_width() - 20, 400)
        max_h = max(self._card.winfo_height() - 20, 300)

        img_copy = img.copy()
        img_copy.thumbnail((max_w, max_h), Image.LANCZOS)

        photo = ImageTk.PhotoImage(img_copy)
        self._img_ref = photo  

        self._placeholder.grid_remove()
        self._image_label.configure(image=photo)
        self._image_label.grid(row=0, column=0, padx=10, pady=10)

    # ── Status bar ─────────────────────────────────────────────────────────────
    def _build_statusbar(self):
        ttk.Separator(self).pack(fill=X)

        bar = ttk.Frame(self, bootstyle="light")
        bar.pack(fill=X, side=BOTTOM)

        self._status_var = ttk.StringVar(value="Listo  ·  Sin imagen cargada")
        ttk.Label(
            bar,
            textvariable=self._status_var,
            font=("Segoe UI", 9),
            bootstyle="secondary",
        ).pack(side=LEFT, padx=16, pady=5)

    # ── Detección con YOLOv8 ───────────────────────────────────────────────────
    def _detect_objects(self):
        if self.current_image is None:
            self._status_var.set("Error: Primero carga una imagen para analizar.")
            return

        self._status_var.set("Analizando imagen con IA...")
        self.update_idletasks() 

        # predicción con el modelo
        results = self.model.predict(source=self.current_image, conf=0.25)

        # extraemos tiempos de procesamiento 
        speed_info = results[0].speed
        tiempo_total_ms = speed_info['preprocess'] + speed_info['inference'] + speed_info['postprocess']

        # Conteo de objetos y clases detectadas
        boxes = results[0].boxes
        total_objetos = len(boxes)
        
        conteos = {}
        clase_principal = None
        max_confianza = -1

        if total_objetos > 0:
            for box in boxes:
                cls_id = int(box.cls[0])
                cls_name = results[0].names[cls_id]
                conf = float(box.conf[0])
                
                conteos[cls_name] = conteos.get(cls_name, 0) + 1
                
                #  objeto con la confianza mas alta para mostrar el tip
                if conf > max_confianza:
                    max_confianza = conf
                    clase_principal = cls_name

        self.lbl_total.configure(text=f"Objetos: {total_objetos}")
        if total_objetos > 0:
            texto_detalle = "\n".join([f"• {k}: {v}" for k, v in conteos.items()])
            self.lbl_detail.configure(text=texto_detalle, bootstyle="success")
            
            # tip en base a la clase con mayor confianza
            if clase_principal in TIPS_SEGURIDAD:
                self.lbl_tip.configure(text=TIPS_SEGURIDAD[clase_principal], bootstyle="warning")
        else:
            self.lbl_detail.configure(text="Calle limpia / Sin riesgos", bootstyle="warning")
            self.lbl_tip.configure(text="✨ Vía segura para el tránsito urbano.", bootstyle="success")

        res_plotted = results[0].plot()

        res_rgb = res_plotted[..., ::-1]
        self.analyzed_image = Image.fromarray(res_rgb)

        self._display_image(self.analyzed_image)
        
        #guardar resultado
        self.btn_save.configure(state="normal", bootstyle="info")
        self._status_var.set(f"¡Detección completada con éxito! | Tiempo de procesamiento: {tiempo_total_ms:.1f} ms")

    def _save_report(self):
        if self.analyzed_image is None:
            return
            
        path_guardar = filedialog.asksaveasfilename(
            title="Guardar imagen procesada",
            defaultextension=".jpg",
            filetypes=[("Imagen JPEG", "*.jpg"), ("Imagen PNG", "*.png")],
            initialfile="reporte_obstaculo.jpg"
        )
        
        if path_guardar:
            self.analyzed_image.save(path_guardar)
            self._status_var.set(f"¡Reporte guardado con éxito en: {Path(path_guardar).name}!")


if __name__ == "__main__":
    App().mainloop()