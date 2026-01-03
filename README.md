# Video Maker - Creador de Videos con Fotos y Música

Aplicación desarrollada en Python con Tkinter para crear videos profesionales a partir de fotos y música.

## Características

- ✅ Interfaz gráfica intuitiva con Tkinter
- ✅ Arquitectura MVC (Modelo-Vista-Controlador)
- ✅ Carátula personalizable con títulos y colores
- ✅ Múltiples efectos de transición para fotos
- ✅ Marcos decorativos para fotos (simple, doble, sombra, relieve)
- ✅ Texto sobre las fotos con posicionamiento
- ✅ Integración de música (local o YouTube)
- ✅ Exportación a MP4 compatible con YouTube
- ✅ Gestión completa de fotos (agregar, editar, eliminar, reordenar)
- ✅ Guardar y cargar proyectos

## Requisitos

- Python 3.8 o superior
- Sistema operativo: Windows, Linux o macOS

## Instalación

### 1. Instalar Python

Asegurate de tener Python 3.8 o superior instalado.
```bash
python --version
```

### 2. Instalar dependencias

Abrí la terminal en la carpeta del proyecto y ejecutá:

**Windows:**
```cmd
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
pip3 install -r requirements.txt
```

**Nota para Linux:** También necesitás ImageMagick:
```bash
# Ubuntu/Debian
sudo apt-get install imagemagick

# Fedora
sudo dnf install imagemagick
```

## Uso

### Iniciar la aplicación

**Windows:**
```cmd
python main.py
```

**Linux/macOS:**
```bash
python3 main.py
```

### Crear tu primer video

1. **Nuevo Proyecto**: Click en "📁 Nuevo" o presiona Ctrl+N

2. **Configurar Carátula**: 
   - Ve a la pestaña "📋 Carátula"
   - Ingresa el título y subtítulo
   - Elige los colores de fondo y texto
   - Click en "💾 Guardar Cambios de Carátula"

3. **Agregar Fotos**:
   - Ve a la pestaña "📷 Fotos"
   - Click en "➕ Agregar"
   - Selecciona tus fotos (JPG, PNG, GIF, BMP)
   - Para editar cada foto: seleccioná y click en "✏️ Editar"
   - Configurá: duración, efecto, marco, texto

4. **Agregar Música**:
   - Ve a la pestaña "🎵 Música"
   - Click en "📁 Cargar desde Archivo"
   - Selecciona tu archivo de audio (MP3, WAV, etc.)

5. **Generar Video**:
   - Click en "▶️ Generar Video" o presiona F5
   - Elige dónde guardar el archivo MP4
   - ¡Esperá a que se complete el proceso!

## Efectos de Transición Disponibles

- **fade**: Fundido suave
- **slide_left**: Desliza desde la izquierda
- **slide_right**: Desliza desde la derecha
- **slide_up**: Desliza desde arriba
- **slide_down**: Desliza desde abajo
- **zoom**: Efecto de acercamiento
- **zigzag**: Movimiento en zig-zag

## Tipos de Marco

- **simple**: Marco de línea única
- **doble**: Marco con doble línea
- **sombra**: Marco con efecto de sombra
- **relieve**: Marco con efecto 3D

## Estructura del Proyecto
```
video_maker/
├── main.py                    # Punto de entrada
├── modelo/
│   ├── __init__.py
│   └── modelo.py              # Clases de datos
├── vistas/
│   ├── __init__.py
│   ├── vista_principal.py     # Ventana principal
│   └── dialogo_editar_foto.py # Diálogo de edición
├── controlador/
│   ├── __init__.py
│   └── controlador.py         # Lógica de control
├── validaciones/
│   ├── __init__.py
│   └── validaciones.py        # Validación de datos
├── generador/
│   ├── __init__.py
│   └── generador_video.py     # Generación de videos
├── requirements.txt           # Dependencias
└── README.md                  # Este archivo
```

## Atajos de Teclado

- `Ctrl+N`: Nuevo proyecto
- `Ctrl+O`: Abrir proyecto
- `Ctrl+S`: Guardar proyecto
- `F5`: Generar video

## Formatos Soportados

### Imágenes
- JPG/JPEG
- PNG
- GIF
- BMP
- TIFF

### Audio
- MP3
- WAV
- OGG
- M4A
- AAC
- FLAC

### Video (salida)
- MP4 (H.264 + AAC)

## Resoluciones Disponibles

- **640x480** (SD)
- **1280x720** (HD)
- **1920x1080** (Full HD) ⭐ Recomendado
- **3840x2160** (4K)

## Solución de Problemas

### Error: "moviepy no está instalado"
```bash
pip install moviepy
```

### Error: "No module named 'PIL'"
```bash
pip install Pillow
```

### Error: "ImageMagick no encontrado" (Linux)
```bash
sudo apt-get install imagemagick
```

### El video no tiene audio
- Verificá que el archivo de audio sea válido
- Verificá que el formato sea soportado (MP3, WAV, etc.)

### Las fotos se ven pixeladas
- Usá fotos de alta resolución
- Seleccioná una resolución de video apropiada

## Desarrollador

**José**  
Gerente Administrativo  
Consejo Superior del Colegio de Médicos  
Provincia de Buenos Aires

- Técnico Superior en Analista de Sistemas  
- Técnico Superior en Comercio Exterior

## Licencia

© 2026 - Todos los derechos reservados

---

**Versión**: 1.0  
**Fecha**: Enero 2026
```

5. Guardá (Ctrl+S)

---

### Archivo 4: `.gitignore` (en la carpeta raíz `video_maker`)

1. Click derecho en la carpeta principal `video_maker`
2. New File
3. Nombralo: `.gitignore`
4. Pegá este contenido:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Video Maker specific
temp-audio.m4a

# Test files
test_*.py
test_videos/
test_images/
```

5. Guardá (Ctrl+S)

---

## 🎉 ¡PROYECTO COMPLETO!

Tu estructura final debería verse así en VS Code:
```
video_maker/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── modelo/
│   ├── __init__.py
│   └── modelo.py
├── vistas/
│   ├── __init__.py
│   ├── vista_principal.py
│   └── dialogo_editar_foto.py
├── controlador/
│   ├── __init__.py
│   └── controlador.py
├── validaciones/
│   ├── __init__.py
│   └── validaciones.py
└── generador/
    ├── __init__.py
    └── generador_video.py