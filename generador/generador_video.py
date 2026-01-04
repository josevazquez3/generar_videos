"""
Generador de Videos
Módulo que crea los videos usando moviepy con soporte completo para todas las características
"""

import os
from typing import Callable, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

try:
    from moviepy.editor import (
        VideoClip, ImageClip, AudioFileClip, CompositeVideoClip,
        concatenate_videoclips, ColorClip, TextClip, VideoFileClip
    )
    MOVIEPY_DISPONIBLE = True
except ImportError:
    MOVIEPY_DISPONIBLE = False
    print("ADVERTENCIA: moviepy no está instalado. Instalarlo con: pip install moviepy")


class GeneradorVideo:
    """Clase que genera videos a partir de proyectos"""
    
    def __init__(self):
        self.callback_progreso = None
        
    def generar_video(self, 
                     proyecto,
                     ruta_salida: str,
                     resolucion: str = "1920x1080",
                     fps: int = 30,
                     callback_progreso: Optional[Callable] = None) -> bool:
        """
        Genera un video a partir de un proyecto
        
        Args:
            proyecto: Proyecto con la configuración del video
            ruta_salida: Ruta donde guardar el video
            resolucion: Resolución del video (ej: "1920x1080")
            fps: Frames por segundo
            callback_progreso: Función callback para reportar progreso
            
        Returns:
            True si se generó correctamente, False en caso contrario
        """
        if not MOVIEPY_DISPONIBLE:
            print("Error: moviepy no está instalado")
            return False
        
        self.callback_progreso = callback_progreso
        
        try:
            # Parsear resolución
            width, height = map(int, resolucion.split('x'))
            
            # Reportar progreso
            self._reportar_progreso("Iniciando generación de video", 0)
            
            # Crear clip de carátula
            self._reportar_progreso("Creando carátula", 5)
            clip_caratula = self._crear_caratula(proyecto.caratula, width, height)
            
            clips = [clip_caratula]
            
            # Crear clips de fotos
            total_fotos = len(proyecto.fotos)
            for i, foto in enumerate(proyecto.fotos):
                progreso = 10 + (i / total_fotos) * 60
                self._reportar_progreso(f"Procesando foto {i+1}/{total_fotos}", progreso)
                
                clip = self._crear_clip_foto(foto, width, height)
                clips.append(clip)

            # Agregar carátula final (si existe) después de las fotos
            try:
                caratula_final = getattr(proyecto, 'caratula_final', None) or proyecto.caratula
                if caratula_final:
                    self._reportar_progreso("Creando carátula final", 70)
                    clip_final = self._crear_caratula(caratula_final, width, height)
                    clips.append(clip_final)
            except Exception as e:
                print(f"Advertencia: no se pudo crear carátula final: {e}")
            
            # Agregar videos si existen
            if proyecto.videos:
                total_videos = len(proyecto.videos)
                for i, video_info in enumerate(proyecto.videos):
                    progreso = 70 + (i / total_videos) * 10
                    self._reportar_progreso(f"Procesando video {i+1}/{total_videos}", progreso)
                    
                    video_clip = self._crear_clip_video(video_info, width, height)
                    if video_clip:
                        clips.append(video_clip)
            
            # Concatenar todos los clips
            self._reportar_progreso("Uniendo clips", 80)
            video_final = concatenate_videoclips(clips, method="compose")
            
            # Agregar música si existe
            if proyecto.musica and os.path.exists(proyecto.musica.ruta):
                self._reportar_progreso("Agregando música", 85)
                audio = AudioFileClip(proyecto.musica.ruta)
                
                # Ajustar duración del audio al video
                if audio.duration > video_final.duration:
                    audio = audio.subclip(0, video_final.duration)
                else:
                    # Si el audio es más corto, hacer loop
                    if video_final.duration > audio.duration:
                        # Calcular cuántas veces repetir
                        num_loops = int(video_final.duration / audio.duration) + 1
                        audio_loops = [audio] * num_loops
                        from moviepy.editor import concatenate_audioclips
                        audio = concatenate_audioclips(audio_loops)
                        audio = audio.subclip(0, video_final.duration)
                
                # Aplicar fade out al final
                audio = audio.audio_fadeout(2.0)
                video_final = video_final.set_audio(audio)
            
            # Guardar video
            self._reportar_progreso("Renderizando video final", 90)
            video_final.write_videofile(
                ruta_salida,
                fps=fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None,
                preset='medium',
                threads=4
            )
            
            # Cerrar clips para liberar memoria
            for clip in clips:
                clip.close()
            video_final.close()
            if proyecto.musica and os.path.exists(proyecto.musica.ruta):
                audio.close()
            
            self._reportar_progreso("Video generado exitosamente", 100)
            return True
            
        except Exception as e:
            print(f"Error al generar video: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _crear_caratula(self, caratula, width: int, height: int):
        """Crea el clip de la carátula con todos los elementos"""
        # Crear imagen de la carátula
        img = Image.new('RGB', (width, height), color=caratula.color_fondo)
        draw = ImageDraw.Draw(img)
        
        # Cargar fuentes
        font_titulo = self._cargar_fuente(caratula.fuente_titulo, caratula.tamaño_titulo)
        font_subtitulo = self._cargar_fuente(caratula.fuente_subtitulo, caratula.tamaño_subtitulo)
        
        # Calcular posiciones
        y_center = height // 2
        
        # Dibujar título centrado
        bbox_titulo = draw.textbbox((0, 0), caratula.titulo, font=font_titulo)
        titulo_width = bbox_titulo[2] - bbox_titulo[0]
        titulo_height = bbox_titulo[3] - bbox_titulo[1]
        titulo_x = (width - titulo_width) // 2
        titulo_y = y_center - titulo_height - 30
        
        # Sombra del título
        draw.text((titulo_x + 3, titulo_y + 3), caratula.titulo, 
                 fill='#000000', font=font_titulo)
        # Título
        draw.text((titulo_x, titulo_y), caratula.titulo, 
                 fill=caratula.color_titulo, font=font_titulo)
        
        # Dibujar subtítulo si existe
        if caratula.subtitulo:
            bbox_subtitulo = draw.textbbox((0, 0), caratula.subtitulo, font=font_subtitulo)
            subtitulo_width = bbox_subtitulo[2] - bbox_subtitulo[0]
            subtitulo_height = bbox_subtitulo[3] - bbox_subtitulo[1]
            subtitulo_x = (width - subtitulo_width) // 2
            subtitulo_y = titulo_y + titulo_height + 20
            
            # Sombra del subtítulo
            draw.text((subtitulo_x + 2, subtitulo_y + 2), caratula.subtitulo,
                     fill='#000000', font=font_subtitulo)
            # Subtítulo
            draw.text((subtitulo_x, subtitulo_y), caratula.subtitulo,
                     fill=caratula.color_subtitulo, font=font_subtitulo)
        
        # Dibujar cuadro de texto si está habilitado
        if caratula.textbox_enabled and caratula.textbox_text:
            self._dibujar_textbox(img, draw, caratula, width, height)
        
        # Dibujar imágenes adicionales si existen
        if caratula.imagenes_caratula:
            for img_info in caratula.imagenes_caratula:
                try:
                    self._agregar_imagen_caratula(img, img_info, width, height)
                except Exception as e:
                    print(f"Error al agregar imagen a carátula: {e}")
        
        # Convertir a array numpy para moviepy
        img_array = np.array(img)
        
        # Crear clip de imagen con fade in y fade out
        clip = ImageClip(img_array, duration=caratula.duracion)
        clip = clip.fadein(0.5).fadeout(0.5)
        
        return clip
    
    def _dibujar_textbox(self, img, draw, caratula, width, height):
        """Dibuja el cuadro de texto en la carátula"""
        # Configuración del textbox
        margin = 40
        padding = 20
        
        # Cargar fuente para el textbox
        font_tb = self._cargar_fuente(caratula.textbox_font, caratula.textbox_font_size)
        
        # Calcular tamaño del texto
        lines = caratula.textbox_text.split('\n')
        max_line_width = 0
        total_height = 0
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_tb)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            max_line_width = max(max_line_width, line_width)
            total_height += line_height + 5
        
        # Dimensiones del rectángulo
        rect_width = max_line_width + padding * 2
        rect_height = total_height + padding * 2
        
        # Posición del rectángulo
        rect_x = (width - rect_width) // 2
        
        if caratula.textbox_position == 'top':
            rect_y = margin
        elif caratula.textbox_position == 'center':
            rect_y = (height - rect_height) // 2
        else:  # bottom
            rect_y = height - rect_height - margin
        
        # Dibujar rectángulo de fondo
        draw.rectangle(
            [rect_x, rect_y, rect_x + rect_width, rect_y + rect_height],
            fill=caratula.textbox_bg,
            outline='#888888',
            width=caratula.textbox_border
        )
        
        # Dibujar texto línea por línea
        text_y = rect_y + padding
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_tb)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            text_x = rect_x + (rect_width - line_width) // 2
            
            draw.text((text_x, text_y), line, fill=caratula.textbox_text_color, font=font_tb)
            text_y += line_height + 5
    
    def _agregar_imagen_caratula(self, img_base, img_info, width, height):
        """Agrega una imagen adicional a la carátula"""
        ruta = img_info.get('ruta')
        if not ruta or not os.path.exists(ruta):
            return
        
        # Cargar imagen
        img_add = Image.open(ruta)
        if img_add.mode != 'RGBA':
            img_add = img_add.convert('RGBA')
        
        # Escalar imagen
        scale = img_info.get('scale', 100) / 100.0
        new_size = (int(img_add.width * scale), int(img_add.height * scale))
        img_add = img_add.resize(new_size, Image.Resampling.LANCZOS)
        
        # Calcular posición
        position = img_info.get('position', 'center')
        x, y = self._calcular_posicion(position, img_add.size, (width, height))
        
        # Pegar imagen con transparencia
        img_base.paste(img_add, (x, y), img_add if img_add.mode == 'RGBA' else None)
    
    def _calcular_posicion(self, position, img_size, canvas_size):
        """Calcula la posición x, y para una imagen según el nombre de posición"""
        img_w, img_h = img_size
        canvas_w, canvas_h = canvas_size
        margin = 20
        
        positions = {
            'top-left': (margin, margin),
            'top': ((canvas_w - img_w) // 2, margin),
            'top-right': (canvas_w - img_w - margin, margin),
            'left': (margin, (canvas_h - img_h) // 2),
            'center': ((canvas_w - img_w) // 2, (canvas_h - img_h) // 2),
            'right': (canvas_w - img_w - margin, (canvas_h - img_h) // 2),
            'bottom-left': (margin, canvas_h - img_h - margin),
            'bottom': ((canvas_w - img_w) // 2, canvas_h - img_h - margin),
            'bottom-right': (canvas_w - img_w - margin, canvas_h - img_h - margin)
        }
        
        return positions.get(position, positions['center'])
    
    def _crear_clip_foto(self, foto, width: int, height: int):
        """Crea un clip de video a partir de una foto con todos sus efectos"""
        # Cargar y procesar imagen
        img = Image.open(foto.ruta)
        
        # Convertir a RGB si es necesario
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Aplicar rotación
        if foto.rotacion != 0:
            img = img.rotate(-foto.rotacion, expand=True, fillcolor=(0, 0, 0))
        
        # Aplicar brillo
        if foto.brillo != 1.0:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(foto.brillo)
        
        # Aplicar contraste
        if foto.contraste != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(foto.contraste)
        
        # Redimensionar manteniendo aspecto
        img = self._redimensionar_imagen(img, width, height)
        
        # Aplicar marco si está configurado
        if foto.marco:
            img = self._aplicar_marco(img, foto.marco, foto.color_marco)
        
        # Agregar texto si existe
        if foto.texto:
            tamaño = getattr(foto, 'tamaño_texto', None)
            img = self._agregar_texto_foto(img, foto.texto, foto.color_texto, foto.posicion_texto, tamaño)
        
        # Convertir a array numpy
        img_array = np.array(img)
        
        # Crear clip base
        clip = ImageClip(img_array, duration=foto.duracion)
        
        # Aplicar efecto de transición
        clip = self._aplicar_efecto(clip, foto.efecto, width, height)
        
        return clip
    
    def _crear_clip_video(self, video_info, width: int, height: int):
        """Crea un clip a partir de un archivo de video"""
        try:
            ruta = video_info.get('ruta') if isinstance(video_info, dict) else video_info
            
            if not os.path.exists(ruta):
                print(f"Video no encontrado: {ruta}")
                return None
            
            # Cargar video
            clip = VideoFileClip(ruta)
            
            # Redimensionar si es necesario
            if clip.size != (width, height):
                clip = clip.resize((width, height))
            
            return clip
            
        except Exception as e:
            print(f"Error al cargar video {ruta}: {e}")
            return None
    
    def _redimensionar_imagen(self, img: Image.Image, target_width: int, target_height: int) -> Image.Image:
        """Redimensiona una imagen manteniendo el aspect ratio y centrando"""
        img_width, img_height = img.size
        
        # Calcular ratios
        width_ratio = target_width / img_width
        height_ratio = target_height / img_height
        
        # Usar el menor ratio para que la imagen quepa completa
        ratio = min(width_ratio, height_ratio)
        
        # Nuevo tamaño
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        # Redimensionar
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Crear imagen de fondo negro
        background = Image.new('RGB', (target_width, target_height), (0, 0, 0))
        
        # Centrar la imagen redimensionada
        offset_x = (target_width - new_width) // 2
        offset_y = (target_height - new_height) // 2
        
        background.paste(img, (offset_x, offset_y))
        
        return background
    
    def _aplicar_marco(self, img: Image.Image, tipo_marco: str, color: str) -> Image.Image:
        """Aplica un marco a la imagen"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Convertir color hex a RGB
        try:
            color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        except:
            color_rgb = (255, 255, 255)
        
        if tipo_marco == "simple":
            # Marco simple
            grosor = max(10, width // 100)
            for i in range(grosor):
                draw.rectangle([i, i, width-1-i, height-1-i], outline=color_rgb)
            
        elif tipo_marco == "doble":
            # Marco doble
            grosor1 = max(15, width // 80)
            grosor2 = max(5, width // 150)
            
            # Marco exterior
            for i in range(grosor1):
                draw.rectangle([i, i, width-1-i, height-1-i], outline=color_rgb)
            
            # Marco interior
            offset = grosor1 + 5
            for i in range(grosor2):
                draw.rectangle([offset+i, offset+i, width-offset-1-i, height-offset-1-i], 
                              outline=color_rgb)
            
        elif tipo_marco == "sombra":
            # Marco con sombra
            grosor = max(10, width // 100)
            sombra_offset = grosor
            
            # Sombra
            color_sombra = tuple(max(0, c - 80) for c in color_rgb)
            for i in range(grosor):
                draw.rectangle([sombra_offset+i, sombra_offset+i, 
                              width-1+i, height-1+i], outline=color_sombra)
            
            # Marco principal
            for i in range(grosor):
                draw.rectangle([i, i, width-sombra_offset-i, height-sombra_offset-i], 
                              outline=color_rgb)
            
        elif tipo_marco == "relieve":
            # Marco con efecto de relieve 3D
            grosor = max(12, width // 80)
            
            # Sombra oscura (abajo y derecha)
            color_oscuro = tuple(max(0, c - 60) for c in color_rgb)
            for i in range(grosor):
                # Línea inferior
                draw.line([(i, height-1-i), (width-1-i, height-1-i)], fill=color_oscuro, width=1)
                # Línea derecha
                draw.line([(width-1-i, i), (width-1-i, height-1-i)], fill=color_oscuro, width=1)
            
            # Luz clara (arriba e izquierda)
            color_claro = tuple(min(255, c + 60) for c in color_rgb)
            for i in range(grosor):
                # Línea superior
                draw.line([(i, i), (width-1-grosor-i, i)], fill=color_claro, width=1)
                # Línea izquierda
                draw.line([(i, i), (i, height-1-grosor-i)], fill=color_claro, width=1)
            
            # Marco del medio
            mitad = grosor // 2
            for i in range(mitad):
                draw.rectangle([mitad+i, mitad+i, width-mitad-1-i, height-mitad-1-i], 
                              outline=color_rgb)
        
        return img
    
    def _agregar_texto_foto(self, img: Image.Image, texto: str, color: str, posicion: str, font_size: int = None) -> Image.Image:
        """Agrega texto sobre la imagen"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Determinar tamaño de fuente: usar el proporcionado si existe, sino calcular proporcionalmente
        if font_size is None:
            font_size_calc = max(30, width // 30)
        else:
            try:
                font_size_calc = int(font_size)
            except Exception:
                font_size_calc = max(30, width // 30)
        font = self._cargar_fuente("Arial", font_size_calc)
        
        # Calcular posición del texto
        bbox = draw.textbbox((0, 0), texto, font=font)
        texto_width = bbox[2] - bbox[0]
        texto_height = bbox[3] - bbox[1]
        
        # Centrar horizontalmente
        x = (width - texto_width) // 2
        
        # Posicionar verticalmente según configuración
        margin = 50
        if posicion == "top":
            y = margin
        elif posicion == "center":
            y = (height - texto_height) // 2
        else:  # bottom
            y = height - texto_height - margin
        
        # Dibujar rectángulo de fondo semi-transparente
        padding = 15
        bg_bbox = [x - padding, y - padding, 
                   x + texto_width + padding, y + texto_height + padding]
        
        # Crear capa semi-transparente para el fondo del texto
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(bg_bbox, fill=(0, 0, 0, 180))
        
        # Combinar overlay con imagen original
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Dibujar sombra del texto para mejor legibilidad
        shadow_offset = 3
        draw.text((x + shadow_offset, y + shadow_offset), texto, 
                 fill='#000000', font=font)
        
        # Dibujar texto principal
        draw.text((x, y), texto, fill=color, font=font)
        
        return img
    
    def _aplicar_efecto(self, clip, efecto: str, width: int, height: int):
        """Aplica efectos de transición al clip"""
        duracion = clip.duration
        
        if efecto == "fade":
            # Efecto de fundido suave
            clip = clip.fadein(0.8).fadeout(0.8)
            
        elif efecto == "slide_left":
            # Deslizar desde la izquierda
            def pos_func(t):
                if t < 1:
                    return (width * (1 - t), 0)
                return (0, 0)
            clip = clip.set_position(pos_func)
            
        elif efecto == "slide_right":
            # Deslizar desde la derecha
            def pos_func(t):
                if t < 1:
                    return (-width * (1 - t), 0)
                return (0, 0)
            clip = clip.set_position(pos_func)
            
        elif efecto == "slide_up":
            # Deslizar desde arriba
            def pos_func(t):
                if t < 1:
                    return (0, height * (1 - t))
                return (0, 0)
            clip = clip.set_position(pos_func)
            
        elif efecto == "slide_down":
            # Deslizar desde abajo
            def pos_func(t):
                if t < 1:
                    return (0, -height * (1 - t))
                return (0, 0)
            clip = clip.set_position(pos_func)
            
        elif efecto == "zoom":
            # Efecto de zoom progresivo
            def resize_func(t):
                progress = min(t / duracion, 1)
                return 1 + 0.2 * progress
            clip = clip.resize(resize_func)
            
        elif efecto == "zigzag":
            # Movimiento en zigzag
            def pos_zigzag(t):
                progress = t / duracion
                
                if progress < 0.25:
                    # De derecha a izquierda en la parte superior
                    x = width * (1 - progress * 4)
                    y = 0
                elif progress < 0.5:
                    # De arriba a abajo en la izquierda
                    x = 0
                    y = height * ((progress - 0.25) * 4)
                elif progress < 0.75:
                    # De izquierda a derecha en la parte inferior
                    x = width * ((progress - 0.5) * 4)
                    y = height
                else:
                    # De abajo a arriba hacia el centro
                    x = width * (1 - (progress - 0.75) * 4)
                    y = height * (1 - (progress - 0.75) * 4)
                
                return (x, y)
            
            clip = clip.set_position(pos_zigzag)
        
        return clip
    
    def _cargar_fuente(self, nombre: str, tamaño: int):
        """Carga una fuente del sistema"""
        fuentes_disponibles = {
            'Arial': ['arial.ttf', 'Arial.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
            'Helvetica': ['helvetica.ttf', 'Helvetica.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'],
            'Times New Roman': ['times.ttf', 'Times.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'],
            'Courier New': ['cour.ttf', 'Courier.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'],
            'Verdana': ['verdana.ttf', 'Verdana.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
        }
        
        # Obtener lista de rutas posibles para la fuente
        rutas_posibles = fuentes_disponibles.get(nombre, fuentes_disponibles['Arial'])
        
        # Intentar cargar cada ruta
        for ruta in rutas_posibles:
            try:
                return ImageFont.truetype(ruta, tamaño)
            except:
                continue
        
        # Si no se pudo cargar ninguna, usar fuente por defecto
        print(f"No se pudo cargar la fuente {nombre}, usando fuente por defecto")
        return ImageFont.load_default()
    
    def _reportar_progreso(self, mensaje: str, porcentaje: float):
        """Reporta el progreso de la generación"""
        if self.callback_progreso:
            self.callback_progreso(mensaje, porcentaje)
        
        # También imprimir en consola
        print(f"[{porcentaje:.1f}%] {mensaje}")