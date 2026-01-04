"""
Modelo de datos para Video Maker
Maneja la información de fotos, música y configuraciones del video
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional

class Foto:
    """Clase que representa una foto en el proyecto"""
    
    def __init__(self, ruta: str, titulo: str = "", orden: int = 0):
        self.ruta = ruta
        self.titulo = titulo
        self.orden = orden
        self.duracion = 3.0
        self.efecto = "fade"
        self.marco = None
        self.color_marco = "#FFFFFF"
        self.texto = ""
        self.color_texto = "#000000"
        self.posicion_texto = "bottom"
        # Nuevos atributos para edición
        self.brillo = 1.0
        self.contraste = 1.0
        self.rotacion = 0  # 0, 90, 180, 270
        
    def to_dict(self) -> dict:
        """Convierte la foto a diccionario para guardar"""
        return {
            'ruta': self.ruta,
            'titulo': self.titulo,
            'orden': self.orden,
            'duracion': self.duracion,
            'efecto': self.efecto,
            'marco': self.marco,
            'color_marco': self.color_marco,
            'texto': self.texto,
            'color_texto': self.color_texto,
            'posicion_texto': self.posicion_texto,
            'brillo': self.brillo,
            'contraste': self.contraste,
            'rotacion': self.rotacion
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Foto':
        """Crea una foto desde un diccionario"""
        foto = Foto(data['ruta'], data.get('titulo', ''), data.get('orden', 0))
        foto.duracion = data.get('duracion', 3.0)
        foto.efecto = data.get('efecto', 'fade')
        foto.marco = data.get('marco')
        foto.color_marco = data.get('color_marco', '#FFFFFF')
        foto.texto = data.get('texto', '')
        foto.color_texto = data.get('color_texto', '#000000')
        foto.posicion_texto = data.get('posicion_texto', 'bottom')
        foto.brillo = data.get('brillo', 1.0)
        foto.contraste = data.get('contraste', 1.0)
        foto.rotacion = data.get('rotacion', 0)
        return foto


class Musica:
    """Clase que representa música en el proyecto"""
    
    def __init__(self, ruta: str, nombre: str = "", origen: str = "local"):
        self.ruta = ruta
        self.nombre = nombre
        self.origen = origen
        self.url_youtube = ""
        
    def to_dict(self) -> dict:
        """Convierte la música a diccionario"""
        return {
            'ruta': self.ruta,
            'nombre': self.nombre,
            'origen': self.origen,
            'url_youtube': self.url_youtube
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Musica':
        """Crea música desde un diccionario"""
        musica = Musica(data['ruta'], data.get('nombre', ''), data.get('origen', 'local'))
        musica.url_youtube = data.get('url_youtube', '')
        return musica


class Caratula:
    """Clase que representa la carátula del video"""
    
    def __init__(self):
        self.titulo = "Mi Video"
        self.subtitulo = ""
        self.color_fondo = "#000080"
        self.color_titulo = "#FFFFFF"
        self.color_subtitulo = "#CCCCCC"
        self.fuente_titulo = "Arial"
        self.tamaño_titulo = 48
        self.fuente_subtitulo = "Arial"
        self.tamaño_subtitulo = 24
        self.titulo_bold = False
        self.titulo_italic = False
        self.subtitulo_bold = False
        self.subtitulo_italic = False
        # Cuadro de texto
        self.textbox_enabled = False
        self.textbox_text = ""
        self.textbox_text_color = "#000000"
        self.textbox_bg = "#FFFFFF"
        self.textbox_border = 1
        self.textbox_position = "bottom"
        self.textbox_font = "Arial"
        self.textbox_font_size = 18
        self.textbox_font_bold = False
        self.textbox_font_italic = False
        self.duracion = 3.0
        self.imagen_fondo = None
        self.imagenes_caratula = []
        
    def to_dict(self) -> dict:
        """Convierte la carátula a diccionario"""
        return {
            'titulo': self.titulo,
            'subtitulo': self.subtitulo,
            'color_fondo': self.color_fondo,
            'color_titulo': self.color_titulo,
            'color_subtitulo': self.color_subtitulo,
            'textbox_enabled': self.textbox_enabled,
            'textbox_text': self.textbox_text,
            'textbox_text_color': self.textbox_text_color,
            'textbox_bg': self.textbox_bg,
            'textbox_border': self.textbox_border,
            'textbox_position': self.textbox_position,
            'textbox_font': self.textbox_font,
            'textbox_font_size': self.textbox_font_size,
            'textbox_font_bold': self.textbox_font_bold,
            'textbox_font_italic': self.textbox_font_italic,
            'fuente_titulo': self.fuente_titulo,
            'tamaño_titulo': self.tamaño_titulo,
            'titulo_bold': self.titulo_bold,
            'titulo_italic': self.titulo_italic,
            'fuente_subtitulo': self.fuente_subtitulo,
            'tamaño_subtitulo': self.tamaño_subtitulo,
            'subtitulo_bold': self.subtitulo_bold,
            'subtitulo_italic': self.subtitulo_italic,
            'duracion': self.duracion,
            'imagen_fondo': self.imagen_fondo,
            'imagenes_caratula': self.imagenes_caratula
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Caratula':
        """Crea carátula desde un diccionario"""
        caratula = Caratula()
        caratula.titulo = data.get('titulo', 'Mi Video')
        caratula.subtitulo = data.get('subtitulo', '')
        caratula.color_fondo = data.get('color_fondo', '#000080')
        caratula.color_titulo = data.get('color_titulo', '#FFFFFF')
        caratula.color_subtitulo = data.get('color_subtitulo', '#CCCCCC')
        caratula.textbox_enabled = data.get('textbox_enabled', False)
        caratula.textbox_text = data.get('textbox_text', '')
        caratula.textbox_text_color = data.get('textbox_text_color', '#000000')
        caratula.textbox_bg = data.get('textbox_bg', '#FFFFFF')
        caratula.textbox_border = data.get('textbox_border', 1)
        caratula.textbox_position = data.get('textbox_position', 'bottom')
        caratula.textbox_font = data.get('textbox_font', 'Arial')
        caratula.textbox_font_size = data.get('textbox_font_size', 18)
        caratula.textbox_font_bold = data.get('textbox_font_bold', False)
        caratula.textbox_font_italic = data.get('textbox_font_italic', False)
        caratula.fuente_titulo = data.get('fuente_titulo', 'Arial')
        caratula.tamaño_titulo = data.get('tamaño_titulo', 48)
        caratula.titulo_bold = data.get('titulo_bold', False)
        caratula.titulo_italic = data.get('titulo_italic', False)
        caratula.fuente_subtitulo = data.get('fuente_subtitulo', 'Arial')
        caratula.tamaño_subtitulo = data.get('tamaño_subtitulo', 24)
        caratula.subtitulo_bold = data.get('subtitulo_bold', False)
        caratula.subtitulo_italic = data.get('subtitulo_italic', False)
        caratula.duracion = data.get('duracion', 3.0)
        caratula.imagen_fondo = data.get('imagen_fondo')
        caratula.imagenes_caratula = data.get('imagenes_caratula', [])
        return caratula


class ProyectoVideo:
    """Clase que representa un proyecto de video completo"""
    
    def __init__(self, nombre: str = "Nuevo Proyecto"):
        self.nombre = nombre
        self.caratula = Caratula()
        # Carátula final (opcional). Si no se especifica, usar la misma carátula.
        self.caratula_final = Caratula()
        self.fotos: List[Foto] = []
        self.musica: Optional[Musica] = None
        self.videos: List[dict] = []
        self.fecha_creacion = datetime.now()
        self.fecha_modificacion = datetime.now()
        self.ruta_salida = ""
        self.resolucion = "1920x1080"
        self.fps = 30
        
    def agregar_foto(self, foto: Foto):
        """Agrega una foto al proyecto"""
        foto.orden = len(self.fotos)
        self.fotos.append(foto)
        self.fecha_modificacion = datetime.now()
    
    def eliminar_foto(self, indice: int):
        """Elimina una foto del proyecto"""
        if 0 <= indice < len(self.fotos):
            self.fotos.pop(indice)
            for i, foto in enumerate(self.fotos):
                foto.orden = i
            self.fecha_modificacion = datetime.now()
    
    def mover_foto(self, indice_origen: int, indice_destino: int):
        """Mueve una foto de posición"""
        if 0 <= indice_origen < len(self.fotos) and 0 <= indice_destino < len(self.fotos):
            foto = self.fotos.pop(indice_origen)
            self.fotos.insert(indice_destino, foto)
            for i, foto in enumerate(self.fotos):
                foto.orden = i
            self.fecha_modificacion = datetime.now()
    
    def to_dict(self) -> dict:
        """Convierte el proyecto a diccionario"""
        return {
            'nombre': self.nombre,
            'caratula': self.caratula.to_dict(),
            'caratula_final': self.caratula_final.to_dict(),
            'fotos': [f.to_dict() for f in self.fotos],
            'musica': self.musica.to_dict() if self.musica else None,
            'videos': [v for v in self.videos],
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_modificacion': self.fecha_modificacion.isoformat(),
            'ruta_salida': self.ruta_salida,
            'resolucion': self.resolucion,
            'fps': self.fps
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'ProyectoVideo':
        """Crea un proyecto desde un diccionario"""
        proyecto = ProyectoVideo(data.get('nombre', 'Nuevo Proyecto'))
        proyecto.caratula = Caratula.from_dict(data.get('caratula', {}))
        # caratula_final puede no existir en proyectos antiguos
        try:
            proyecto.caratula_final = Caratula.from_dict(data.get('caratula_final', {}))
        except Exception:
            proyecto.caratula_final = Caratula.from_dict(data.get('caratula', {}))
        proyecto.fotos = [Foto.from_dict(f) for f in data.get('fotos', [])]
        if data.get('musica'):
            proyecto.musica = Musica.from_dict(data['musica'])
        proyecto.videos = data.get('videos', [])
        proyecto.fecha_creacion = datetime.fromisoformat(data.get('fecha_creacion', datetime.now().isoformat()))
        proyecto.fecha_modificacion = datetime.fromisoformat(data.get('fecha_modificacion', datetime.now().isoformat()))
        proyecto.ruta_salida = data.get('ruta_salida', '')
        proyecto.resolucion = data.get('resolucion', '1920x1080')
        proyecto.fps = data.get('fps', 30)
        return proyecto


class ModeloVideoMaker:
    """Modelo principal de la aplicación"""
    
    def __init__(self):
        self.proyecto_actual: Optional[ProyectoVideo] = None
        self.proyectos_recientes: List[str] = []
        self.directorio_proyectos = os.path.join(os.path.expanduser("~"), "VideoMaker", "Proyectos")
        self.directorio_temp = os.path.join(os.path.expanduser("~"), "VideoMaker", "Temp")
        self.directorio_salida = os.path.join(os.path.expanduser("~"), "VideoMaker", "Videos")
        
        os.makedirs(self.directorio_proyectos, exist_ok=True)
        os.makedirs(self.directorio_temp, exist_ok=True)
        os.makedirs(self.directorio_salida, exist_ok=True)
        
    def nuevo_proyecto(self, nombre: str = "Nuevo Proyecto"):
        """Crea un nuevo proyecto"""
        self.proyecto_actual = ProyectoVideo(nombre)
        return self.proyecto_actual
    
    def guardar_proyecto(self, ruta: str = None) -> bool:
        """Guarda el proyecto actual"""
        if not self.proyecto_actual:
            return False
        
        try:
            if not ruta:
                nombre_archivo = f"{self.proyecto_actual.nombre}.json"
                ruta = os.path.join(self.directorio_proyectos, nombre_archivo)
            
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(self.proyecto_actual.to_dict(), f, indent=2, ensure_ascii=False)
            
            if ruta not in self.proyectos_recientes:
                self.proyectos_recientes.insert(0, ruta)
                self.proyectos_recientes = self.proyectos_recientes[:10]
            
            return True
        except Exception as e:
            print(f"Error al guardar proyecto: {e}")
            return False
    
    def cargar_proyecto(self, ruta: str) -> bool:
        """Carga un proyecto desde archivo"""
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.proyecto_actual = ProyectoVideo.from_dict(data)
            
            if ruta not in self.proyectos_recientes:
                self.proyectos_recientes.insert(0, ruta)
                self.proyectos_recientes = self.proyectos_recientes[:10]
            
            return True
        except Exception as e:
            print(f"Error al cargar proyecto: {e}")
            return False
    
    def obtener_duracion_total(self) -> float:
        """Calcula la duración total del video"""
        if not self.proyecto_actual:
            return 0.0
        
        duracion = self.proyecto_actual.caratula.duracion
        for foto in self.proyecto_actual.fotos:
            duracion += foto.duracion
        
        return duracion