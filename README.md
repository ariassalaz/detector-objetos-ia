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

pip install -r requirements.txt

python app.py
