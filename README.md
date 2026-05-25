# Detector de Objetos Urbanos

Aplicación de escritorio para detección de objetos urbanos usando YOLOv8 y tkinter.
Detecta elementos que afectan la accesibilidad en ciudades como Gómez Palacio y Torreón.

## Clases detectadas

| Clase | Descripción |
|-------|-------------|
| Bache | Hundimiento en el pavimento |
| Alcantarilla | Tapa de alcantarilla en la vía |
| Red | Redes o cables en el suelo |
| Conos | Conos de señalización vial |
| Ballena | Topes de estacionamiento |

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/ariassalaz/detectorObjetosIA.git
cd detectorObjetosIA

# 2. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Cómo ejecutar

### 1. Activar el entorno virtual

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Instalar dependencias (solo la primera vez)

```bash
pip install -r requirements.txt
```

### 3. Iniciar la aplicación

```bash
python app.py
```

Se abrirá la ventana de escritorio del detector.

## Equipo

| Nombre | Matrícula | Rol |
|--------|-----------|-----|
| Ricardo Arias Salazar | 22130809 | Líder técnico |
| María del Carmen Bracho Félix | 221000121 | Procesamiento de datos |
| Santiago Orozco Rimada | 22130840 | Entrenamiento del modelo |
| Sofía Alejandra Gutiérrez Hernández | 22130870 | Evaluación y análisis |
| Daniela María González Lara | 22130812 | Documentación y reporte |
