"""
Módulo de validaciones para Video Maker
Valida archivos, formatos y datos de entrada
"""

import os
import re
from typing import Tuple, Optional
from PIL import Image

class Validaciones:
    """Clase con métodos estáticos para validación"""
    
    # Extensiones permitidas
    EXTENSIONES_IMAGEN = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    # Ampliado para incluir contenedores y formatos comunes de audio provenientes de descargas
    EXTENSIONES_AUDIO = {'.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac', '.webm', '.opus', '.mp4'}
    EXTENSIONES_VIDEO = {'.mp4', '.avi', '.mov', '.mkv', '.flv'}
    
    @staticmethod
    def validar_archivo_existe(ruta: str) -> Tuple[bool, str]:
        """
        Valida que un archivo exista
        Retorna: (es_valido, mensaje_error)
        """
        if not ruta:
            return False, "La ruta del archivo está vacía"
        
        if not os.path.exists(ruta):
            return False, f"El archivo no existe: {ruta}"
        
        if not os.path.isfile(ruta):
            return False, f"La ruta no corresponde a un archivo: {ruta}"
        
        return True, ""
    
    @staticmethod
    def validar_imagen(ruta: str) -> Tuple[bool, str]:
        """
        Valida que un archivo sea una imagen válida
        Retorna: (es_valido, mensaje_error)
        """
        # Verificar existencia
        existe, mensaje = Validaciones.validar_archivo_existe(ruta)
        if not existe:
            return False, mensaje
        
        # Verificar extensión
        _, extension = os.path.splitext(ruta)
        if extension.lower() not in Validaciones.EXTENSIONES_IMAGEN:
            return False, f"Formato de imagen no soportado: {extension}"
        
        # Intentar abrir la imagen
        try:
            with Image.open(ruta) as img:
                img.verify()
            return True, ""
        except Exception as e:
            return False, f"Error al cargar la imagen: {str(e)}"
    
    @staticmethod
    def validar_audio(ruta: str) -> Tuple[bool, str]:
        """
        Valida que un archivo sea de audio válido
        Retorna: (es_valido, mensaje_error)
        """
        # Verificar existencia
        existe, mensaje = Validaciones.validar_archivo_existe(ruta)
        if not existe:
            return False, mensaje
        
        # Verificar extensión
        _, extension = os.path.splitext(ruta)
        if extension.lower() not in Validaciones.EXTENSIONES_AUDIO:
            return False, f"Formato de audio no soportado: {extension}"
        
        return True, ""
    
    @staticmethod
    def validar_texto(texto: str, min_len: int = 0, max_len: int = 1000) -> Tuple[bool, str]:
        """
        Valida un texto
        Retorna: (es_valido, mensaje_error)
        """
        if texto is None:
            return False, "El texto no puede ser nulo"
        
        if len(texto) < min_len:
            return False, f"El texto debe tener al menos {min_len} caracteres"
        
        if len(texto) > max_len:
            return False, f"El texto no puede exceder {max_len} caracteres"
        
        return True, ""
    
    @staticmethod
    def validar_color_hex(color: str) -> Tuple[bool, str]:
        """
        Valida que un string sea un color hexadecimal válido
        Retorna: (es_valido, mensaje_error)
        """
        if not color:
            return False, "El color está vacío"
        
        # Patrón para color hex: #RRGGBB o #RGB
        patron = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        if not re.match(patron, color):
            return False, f"Color hexadecimal inválido: {color}"
        
        return True, ""
    
    @staticmethod
    def validar_numero(valor, min_val=None, max_val=None, tipo=float) -> Tuple[bool, str]:
        """
        Valida que un valor sea un número válido
        Retorna: (es_valido, mensaje_error)
        """
        try:
            numero = tipo(valor)
        except (ValueError, TypeError):
            return False, f"El valor '{valor}' no es un número válido"
        
        if min_val is not None and numero < min_val:
            return False, f"El valor debe ser mayor o igual a {min_val}"
        
        if max_val is not None and numero > max_val:
            return False, f"El valor debe ser menor o igual a {max_val}"
        
        return True, ""
    
    @staticmethod
    def validar_duracion(duracion: float) -> Tuple[bool, str]:
        """
        Valida la duración de una foto o clip
        Retorna: (es_valido, mensaje_error)
        """
        return Validaciones.validar_numero(duracion, min_val=0.1, max_val=60.0, tipo=float)
    
    @staticmethod
    def validar_url_youtube(url: str) -> Tuple[bool, str]:
        """
        Valida que una URL sea de YouTube
        Retorna: (es_valido, mensaje_error)
        """
        if not url:
            return False, "La URL está vacía"
        
        # Patrones comunes de YouTube
        patrones = [
            r'(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(https?://)?(www\.)?youtu\.be/[\w-]+',
            r'(https?://)?(www\.)?youtube\.com/embed/[\w-]+'
        ]
        
        for patron in patrones:
            if re.match(patron, url):
                return True, ""
        
        return False, "URL de YouTube inválida"
    
    @staticmethod
    def validar_resolucion(resolucion: str) -> Tuple[bool, str]:
        """
        Valida una resolución de video
        Retorna: (es_valido, mensaje_error)
        """
        patron = r'^\d+x\d+$'
        if not re.match(patron, resolucion):
            return False, "Formato de resolución inválido (debe ser WIDTHxHEIGHT)"
        
        partes = resolucion.split('x')
        width = int(partes[0])
        height = int(partes[1])
        
        if width < 640 or height < 480:
            return False, "La resolución mínima es 640x480"
        
        if width > 7680 or height > 4320:  # 8K
            return False, "La resolución máxima es 7680x4320 (8K)"
        
        return True, ""
    
    @staticmethod
    def validar_fps(fps: int) -> Tuple[bool, str]:
        """
        Valida los frames por segundo
        Retorna: (es_valido, mensaje_error)
        """
        fps_validos = [24, 25, 30, 50, 60]
        if fps not in fps_validos:
            return False, f"FPS debe ser uno de: {', '.join(map(str, fps_validos))}"
        
        return True, ""
    
    @staticmethod
    def validar_nombre_archivo(nombre: str) -> Tuple[bool, str]:
        """
        Valida que un nombre de archivo sea válido
        Retorna: (es_valido, mensaje_error)
        """
        if not nombre:
            return False, "El nombre del archivo está vacío"
        
        # Caracteres no permitidos en nombres de archivo
        caracteres_invalidos = r'[<>:"/\\|?*]'
        if re.search(caracteres_invalidos, nombre):
            return False, "El nombre contiene caracteres no permitidos"
        
        if len(nombre) > 255:
            return False, "El nombre del archivo es demasiado largo"
        
        return True, ""
    
    @staticmethod
    def validar_directorio(ruta: str) -> Tuple[bool, str]:
        """
        Valida que un directorio exista o se pueda crear
        Retorna: (es_valido, mensaje_error)
        """
        if not ruta:
            return False, "La ruta del directorio está vacía"
        
        if os.path.exists(ruta):
            if not os.path.isdir(ruta):
                return False, "La ruta existe pero no es un directorio"
            if not os.access(ruta, os.W_OK):
                return False, "No hay permisos de escritura en el directorio"
            return True, ""
        
        # Intentar crear el directorio
        try:
            os.makedirs(ruta, exist_ok=True)
            return True, ""
        except Exception as e:
            return False, f"No se puede crear el directorio: {str(e)}"
    
    @staticmethod
    def obtener_dimensiones_imagen(ruta: str) -> Optional[Tuple[int, int]]:
        """
        Obtiene las dimensiones de una imagen
        Retorna: (width, height) o None si hay error
        """
        try:
            with Image.open(ruta) as img:
                return img.size
        except Exception:
            return None
    
    @staticmethod
    def validar_proyecto(proyecto) -> Tuple[bool, str]:
        """
        Valida que un proyecto esté completo y sea válido
        Retorna: (es_valido, mensaje_error)
        """
        if not proyecto:
            return False, "No hay proyecto cargado"
        
        # Validar nombre del proyecto
        es_valido, mensaje = Validaciones.validar_texto(proyecto.nombre, min_len=1, max_len=100)
        if not es_valido:
            return False, f"Nombre del proyecto inválido: {mensaje}"
        
        # Validar carátula
        if not proyecto.caratula:
            return False, "El proyecto debe tener una carátula"
        
        es_valido, mensaje = Validaciones.validar_texto(proyecto.caratula.titulo, min_len=1)
        if not es_valido:
            return False, f"Título de la carátula inválido: {mensaje}"
        
        # Validar que haya al menos una foto
        if not proyecto.fotos or len(proyecto.fotos) == 0:
            return False, "El proyecto debe tener al menos una foto"
        
        # Validar cada foto
        for i, foto in enumerate(proyecto.fotos):
            es_valido, mensaje = Validaciones.validar_imagen(foto.ruta)
            if not es_valido:
                return False, f"Foto {i+1} inválida: {mensaje}"
        
        # Validar música si existe
        if proyecto.musica:
            es_valido, mensaje = Validaciones.validar_audio(proyecto.musica.ruta)
            if not es_valido:
                return False, f"Música inválida: {mensaje}"
        
        return True, ""