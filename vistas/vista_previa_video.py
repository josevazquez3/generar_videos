"""
Vista Previa del Video
Módulo para previsualizar el video antes de generarlo
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageEnhance
import os
from typing import List
import time
import math

class VistaPreviewVideo:
    """Ventana de vista previa del video"""
    
    def __init__(self, parent, proyecto):
        self.proyecto = proyecto
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Vista Previa del Video")
        self.ventana.geometry("1000x700")
        self.ventana.transient(parent)
        
        # Variables de control
        self.frame_actual = 0
        self.total_frames = 0
        self.frames_list = []
        self.reproduciendo = False
        self.paused = False
        self._preview_image_tk = None
        
        self.crear_interfaz()
        self.generar_frames_preview()
        self.mostrar_frame(0)
        
    def crear_interfaz(self):
        """Crea la interfaz de la ventana de preview"""
        # Frame superior - Canvas para mostrar el video
        frame_canvas = ttk.Frame(self.ventana)
        frame_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame_canvas, text="Vista Previa del Video", 
                 font=('Arial', 14, 'bold')).pack(pady=5)
        
        # Canvas para mostrar frames
        self.canvas = tk.Canvas(frame_canvas, width=800, height=450, 
                               bg='black', bd=2, relief=tk.SUNKEN)
        self.canvas.pack(pady=10)
        
        # Frame de controles
        frame_controles = ttk.Frame(self.ventana)
        frame_controles.pack(fill=tk.X, padx=10, pady=5)
        
        # Botones de control
        btn_frame = ttk.Frame(frame_controles)
        btn_frame.pack(pady=5)
        
        self.btn_play = ttk.Button(btn_frame, text="▶️ Reproducir", 
                                   command=self.reproducir)
        self.btn_play.pack(side=tk.LEFT, padx=5)
        
        self.btn_pause = ttk.Button(btn_frame, text="⏸️ Pausar", 
                                    command=self.pausar, state='disabled')
        self.btn_pause.pack(side=tk.LEFT, padx=5)
        
        self.btn_stop = ttk.Button(btn_frame, text="⏹️ Detener", 
                                   command=self.detener, state='disabled')
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="⏮️ Inicio", 
                  command=self.ir_inicio).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="⏭️ Final", 
                  command=self.ir_final).pack(side=tk.LEFT, padx=5)
        
        # Slider de progreso
        progress_frame = ttk.Frame(frame_controles)
        progress_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(progress_frame, text="Progreso:").pack(side=tk.LEFT, padx=5)
        
        self.slider = ttk.Scale(progress_frame, from_=0, to=100, 
                               orient=tk.HORIZONTAL, command=self.on_slider_change)
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.label_tiempo = ttk.Label(progress_frame, text="0:00 / 0:00")
        self.label_tiempo.pack(side=tk.LEFT, padx=5)
        
        # Frame de información
        info_frame = ttk.LabelFrame(self.ventana, text="Información del Video", 
                                    padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        info_text = f"""
        Carátula: {self.proyecto.caratula.duracion}s
        Fotos: {len(self.proyecto.fotos)} ({sum(f.duracion for f in self.proyecto.fotos)}s)
        Videos: {len(self.proyecto.videos)}
        Música: {"Sí" if self.proyecto.musica else "No"}
        Duración Total: {self._calcular_duracion_total()}s
        Resolución: {self.proyecto.resolucion}
        FPS: {self.proyecto.fps}
        """
        
        ttk.Label(info_frame, text=info_text.strip(), 
                 justify=tk.LEFT).pack(anchor=tk.W)
        
        # Botones de acción
        action_frame = ttk.Frame(self.ventana)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="✅ Generar Video", 
                  command=self.confirmar_generacion, 
                  style='Accent.TButton').pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(action_frame, text="❌ Cancelar", 
                  command=self.ventana.destroy).pack(side=tk.RIGHT, padx=5)
        
    def generar_frames_preview(self):
        """Genera frames de preview del video"""
        try:
            width, height = map(int, self.proyecto.resolucion.split('x'))
            preview_width = 800
            preview_height = 450
            
            self.frames_list = []
            
            # Frame de carátula
            print("Generando preview de carátula...")
            frame_caratula = self._generar_frame_caratula(preview_width, preview_height)
            # Duplicar el frame de carátula según su duración (a 2 fps para preview)
            frames_caratula = int(self.proyecto.caratula.duracion * 2)
            for _ in range(frames_caratula):
                self.frames_list.append(frame_caratula.copy())
            
            # Frames de fotos
            for i, foto in enumerate(self.proyecto.fotos):
                print(f"Generando preview de foto {i+1}/{len(self.proyecto.fotos)}...")
                frame_foto = self._generar_frame_foto(foto, preview_width, preview_height)
                # Duplicar el frame según su duración (a 2 fps para preview)
                frames_foto = int(foto.duracion * 2)
                for _ in range(frames_foto):
                    self.frames_list.append(frame_foto.copy())
            
            self.total_frames = len(self.frames_list)
            self.slider.config(to=self.total_frames - 1)
            
            print(f"Preview generado: {self.total_frames} frames")
            
        except Exception as e:
            print(f"Error al generar frames de preview: {e}")
            import traceback
            traceback.print_exc()
    
    def _generar_frame_caratula(self, width, height):
        """Genera un frame de la carátula"""
        caratula = self.proyecto.caratula
        
        # Crear imagen
        img = Image.new('RGB', (width, height), color=caratula.color_fondo)
        draw = ImageDraw.Draw(img)
        
        # Cargar fuentes
        try:
            font_titulo = ImageFont.truetype('arial.ttf', 48)
        except:
            font_titulo = ImageFont.load_default()
        
        try:
            font_subtitulo = ImageFont.truetype('arial.ttf', 24)
        except:
            font_subtitulo = ImageFont.load_default()
        
        # Dibujar título
        bbox_t = draw.textbbox((0, 0), caratula.titulo, font=font_titulo)
        w_t = bbox_t[2] - bbox_t[0]
        h_t = bbox_t[3] - bbox_t[1]
        x_t = (width - w_t) // 2
        y_t = (height // 2) - h_t - 20
        
        # Sombra
        draw.text((x_t + 2, y_t + 2), caratula.titulo, 
                 fill='#000000', font=font_titulo)
        # Título
        draw.text((x_t, y_t), caratula.titulo, 
                 fill=caratula.color_titulo, font=font_titulo)
        
        # Dibujar subtítulo si existe
        if caratula.subtitulo:
            bbox_s = draw.textbbox((0, 0), caratula.subtitulo, font=font_subtitulo)
            w_s = bbox_s[2] - bbox_s[0]
            x_s = (width - w_s) // 2
            y_s = y_t + h_t + 20
            
            # Sombra
            draw.text((x_s + 2, y_s + 2), caratula.subtitulo,
                     fill='#000000', font=font_subtitulo)
            # Subtítulo
            draw.text((x_s, y_s), caratula.subtitulo,
                     fill=caratula.color_subtitulo, font=font_subtitulo)
        
        # Textbox si está habilitado
        if caratula.textbox_enabled and caratula.textbox_text:
            self._dibujar_textbox_preview(img, draw, caratula, width, height)
        
        return img
    
    def _dibujar_textbox_preview(self, img, draw, caratula, width, height):
        """Dibuja el textbox en el frame de carátula"""
        try:
            font = ImageFont.truetype('arial.ttf', 16)
        except:
            font = ImageFont.load_default()
        
        text = caratula.textbox_text
        lines = text.split('\n')
        
        # Calcular dimensiones
        max_w = 0
        total_h = 0
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            max_w = max(max_w, bbox[2] - bbox[0])
            total_h += bbox[3] - bbox[1] + 5
        
        padding = 15
        rect_w = max_w + padding * 2
        rect_h = total_h + padding * 2
        
        # Posición
        rect_x = (width - rect_w) // 2
        
        if caratula.textbox_position == 'top':
            rect_y = 20
        elif caratula.textbox_position == 'center':
            rect_y = (height - rect_h) // 2
        else:
            rect_y = height - rect_h - 20
        
        # Dibujar rectángulo
        draw.rectangle([rect_x, rect_y, rect_x + rect_w, rect_y + rect_h],
                      fill=caratula.textbox_bg, outline='#888888', width=2)
        
        # Dibujar texto
        y = rect_y + padding
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            x = rect_x + (rect_w - w) // 2
            draw.text((x, y), line, fill=caratula.textbox_text_color, font=font)
            y += bbox[3] - bbox[1] + 5
    
    def _generar_frame_foto(self, foto, width, height):
        """Genera un frame de una foto"""
        try:
            # Cargar imagen
            img = Image.open(foto.ruta)
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
            
            # Aplicar marco
            if foto.marco:
                img = self._aplicar_marco_preview(img, foto.marco, foto.color_marco)
            
            # Aplicar texto
            if foto.texto:
                img = self._aplicar_texto_preview(img, foto.texto, 
                                                 foto.color_texto, foto.posicion_texto)
            
            return img
            
        except Exception as e:
            print(f"Error al generar frame de foto: {e}")
            # Retornar imagen negra en caso de error
            return Image.new('RGB', (width, height), (0, 0, 0))
    
    def _redimensionar_imagen(self, img, target_width, target_height):
        """Redimensiona imagen manteniendo aspecto"""
        img_width, img_height = img.size
        
        width_ratio = target_width / img_width
        height_ratio = target_height / img_height
        ratio = min(width_ratio, height_ratio)
        
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        background = Image.new('RGB', (target_width, target_height), (0, 0, 0))
        offset_x = (target_width - new_width) // 2
        offset_y = (target_height - new_height) // 2
        background.paste(img, (offset_x, offset_y))
        
        return background
    
    def _aplicar_marco_preview(self, img, tipo_marco, color):
        """Aplica marco a la imagen"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        try:
            color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        except:
            color_rgb = (255, 255, 255)
        
        if tipo_marco == "simple":
            grosor = max(5, width // 100)
            for i in range(grosor):
                draw.rectangle([i, i, width-1-i, height-1-i], outline=color_rgb)
        
        elif tipo_marco == "doble":
            grosor1 = max(8, width // 80)
            grosor2 = max(3, width // 150)
            for i in range(grosor1):
                draw.rectangle([i, i, width-1-i, height-1-i], outline=color_rgb)
            offset = grosor1 + 2
            for i in range(grosor2):
                draw.rectangle([offset+i, offset+i, width-offset-1-i, 
                              height-offset-1-i], outline=color_rgb)
        
        elif tipo_marco == "sombra":
            grosor = max(5, width // 100)
            sombra = tuple(max(0, c - 80) for c in color_rgb)
            draw.rectangle([grosor, grosor, width-1, height-1], 
                         outline=sombra, width=grosor)
            for i in range(grosor):
                draw.rectangle([i, i, width-grosor-i, height-grosor-i], 
                             outline=color_rgb)
        
        elif tipo_marco == "relieve":
            grosor = max(6, width // 80)
            oscuro = tuple(max(0, c - 50) for c in color_rgb)
            claro = tuple(min(255, c + 50) for c in color_rgb)
            for i in range(grosor):
                draw.line([(i, height-1-i), (width-1-i, height-1-i)], fill=oscuro)
                draw.line([(width-1-i, i), (width-1-i, height-1-i)], fill=oscuro)
                draw.line([(i, i), (width-1-i, i)], fill=claro)
                draw.line([(i, i), (i, height-1-i)], fill=claro)
        
        return img
    
    def _aplicar_texto_preview(self, img, texto, color, posicion):
        """Aplica texto a la imagen"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        try:
            font = ImageFont.truetype('arial.ttf', max(20, width // 30))
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), texto, font=font)
        texto_width = bbox[2] - bbox[0]
        texto_height = bbox[3] - bbox[1]
        
        x = (width - texto_width) // 2
        margin = 30
        
        if posicion == "top":
            y = margin
        elif posicion == "center":
            y = (height - texto_height) // 2
        else:
            y = height - texto_height - margin
        
        # Fondo semi-transparente
        padding = 10
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle([x - padding, y - padding, 
                               x + texto_width + padding, y + texto_height + padding],
                              fill=(0, 0, 0, 180))
        
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Sombra
        draw.text((x + 2, y + 2), texto, fill='#000000', font=font)
        # Texto
        draw.text((x, y), texto, fill=color, font=font)
        
        return img
    
    def mostrar_frame(self, index):
        """Muestra un frame específico"""
        if 0 <= index < self.total_frames:
            self.frame_actual = index
            
            # Obtener frame
            img = self.frames_list[index]
            
            # Convertir a PhotoImage
            self._preview_image_tk = ImageTk.PhotoImage(img)
            
            # Mostrar en canvas
            self.canvas.delete('all')
            self.canvas.create_image(400, 225, image=self._preview_image_tk)
            
            # Actualizar slider
            self.slider.set(index)
            
            # Actualizar tiempo
            tiempo_actual = index / 2  # 2 fps
            tiempo_total = self.total_frames / 2
            self.label_tiempo.config(
                text=f"{self._format_tiempo(tiempo_actual)} / {self._format_tiempo(tiempo_total)}"
            )
    
    def reproducir(self):
        """Inicia la reproducción"""
        if not self.reproduciendo:
            self.reproduciendo = True
            self.paused = False
            self.btn_play.config(state='disabled')
            self.btn_pause.config(state='normal')
            self.btn_stop.config(state='normal')
            self._reproducir_loop()
    
    def _reproducir_loop(self):
        """Loop de reproducción"""
        if self.reproduciendo and not self.paused:
            if self.frame_actual < self.total_frames - 1:
                self.frame_actual += 1
                self.mostrar_frame(self.frame_actual)
                self.ventana.after(500, self._reproducir_loop)  # 2 fps (500ms)
            else:
                self.detener()
    
    def pausar(self):
        """Pausa la reproducción"""
        self.paused = True
        self.btn_play.config(state='normal')
        self.btn_pause.config(state='disabled')
    
    def detener(self):
        """Detiene la reproducción"""
        self.reproduciendo = False
        self.paused = False
        self.frame_actual = 0
        self.mostrar_frame(0)
        self.btn_play.config(state='normal')
        self.btn_pause.config(state='disabled')
        self.btn_stop.config(state='disabled')
    
    def ir_inicio(self):
        """Va al inicio del video"""
        self.detener()
    
    def ir_final(self):
        """Va al final del video"""
        if self.reproduciendo:
            self.detener()
        self.frame_actual = self.total_frames - 1
        self.mostrar_frame(self.frame_actual)
    
    def on_slider_change(self, value):
        """Maneja el cambio en el slider"""
        if not self.reproduciendo or self.paused:
            index = int(float(value))
            self.mostrar_frame(index)
    
    def _calcular_duracion_total(self):
        """Calcula la duración total del proyecto"""
        duracion = self.proyecto.caratula.duracion
        for foto in self.proyecto.fotos:
            duracion += foto.duracion
        return round(duracion, 1)
    
    def _format_tiempo(self, segundos):
        """Formatea segundos a MM:SS"""
        minutos = int(segundos // 60)
        segs = int(segundos % 60)
        return f"{minutos}:{segs:02d}"
    
    def confirmar_generacion(self):
        """Confirma y cierra para generar el video"""
        self.ventana.destroy()
    
    def mostrar(self):
        """Muestra la ventana y espera"""
        self.ventana.wait_window()