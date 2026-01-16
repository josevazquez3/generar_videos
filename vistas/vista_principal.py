"""
Vista Principal de Video Maker - Versión FINAL Y COMPLETA
Header moderno + TODAS las funcionalidades (Carátula y Carátula Final idénticas)
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFont
import time
import os


class VistaPrincipal:
    """Vista principal con diseño híbrido moderno"""
    
    def __init__(self, root: tk.Tk):
        print('DEBUG: VistaPrincipal.__init__ - start (versión híbrida completa)')
        self.root = root
        self.root.title("Video Maker Pro - Creador de Videos Profesional")
        self.root.geometry("1400x900")
        
        # Colores modernos
        self.colors = {
            'bg_dark': '#1e1e1e',
            'bg_medium': '#2d2d2d',
            'bg_light': '#3d3d3d',
            'accent': '#0078d4',
            'accent_hover': '#106ebe',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'success': '#28a745',
            'danger': '#dc3545'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        self.configurar_estilos()
        
        # Callbacks
        self.callback_nuevo_proyecto = None
        self.callback_abrir_proyecto = None
        self.callback_guardar_proyecto = None
        self.callback_agregar_foto = None
        self.callback_eliminar_foto = None
        self.callback_editar_foto = None
        self.callback_mover_foto_arriba = None
        self.callback_mover_foto_abajo = None
        self.callback_agregar_musica = None
        self.callback_eliminar_musica = None
        self.callback_agregar_video = None
        self.callback_eliminar_video = None
        self.callback_editar_caratula = None
        self.callback_editar_caratula_final = None
        self.callback_generar_video = None
        self.callback_aplicar_edicion_foto = None
        self.callback_agregar_imagen_caratula = None
        self.callback_eliminar_imagen_caratula = None
        self.callback_actualizar_imagen_caratula = None
        self.callback_vista_previa = None
        self.callback_descargar_youtube = None
        
        # Variables internas
        self._fotos = []
        self._imagenes_items = []
        self._original_image = None
        self._current_image = None
        self._preview_image_tk = None
        self._caratula_preview_tk = None
        self._caratula_final_preview_tk = None
        self._imagen_preview_tk = None
        self._anim_after_id = None
        self._anim_state = None
        
        self.crear_header_moderno()
        self.crear_panel_principal()
        self.crear_barra_estado()
        
        print('DEBUG: VistaPrincipal.__init__ - end')
    
    def configurar_estilos(self):
        """Configura los estilos de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 12, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'))
    
    def crear_header_moderno(self):
        """Crea el header moderno con Canvas"""
        header_frame = tk.Frame(self.root, bg=self.colors['bg_dark'], height=70)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        header_frame.pack_propagate(False)
        
        self.header_canvas = tk.Canvas(header_frame, height=70, bg=self.colors['accent'], highlightthickness=0)
        self.header_canvas.pack(fill=tk.BOTH, expand=True)
        
        for i in range(70):
            factor = i / 70
            color = self.interpolar_color('#0078d4', '#005a9e', factor)
            self.header_canvas.create_line(0, i, 2000, i, fill=color, tags="header_bg")
        
        self.header_canvas.create_oval(20, 15, 60, 55, fill="#ffffff", outline="", tags="logo")
        self.header_canvas.create_text(40, 35, text="VM", font=("Arial", 18, "bold"),
                                       fill=self.colors['accent'], tags="logo_text")
        self.header_canvas.create_text(80, 35, text="Video Maker Pro",
                                       font=("Segoe UI", 24, "bold"),
                                       fill=self.colors['text_primary'],
                                       anchor="w", tags="title")
        
        self.crear_boton_header(1260, 20, "📁 Nuevo", self.on_nuevo_proyecto)
        self.crear_boton_header(1130, 20, "📂 Abrir", self.on_abrir_proyecto)
        self.crear_boton_header(1000, 20, "💾 Guardar", self.on_guardar_proyecto)
        self.crear_boton_header(850, 20, "▶️ Generar Video", self.on_generar_video, 
                               color=self.colors['success'])
    
    def crear_boton_header(self, x, y, texto, comando, color=None):
        """Crea un botón moderno en el header"""
        if color is None:
            color = self.colors['bg_light']
        
        w, h = 120, 35
        btn_id = self.header_canvas.create_rectangle(x, y, x+w, y+h, fill=color, outline="", tags=("btn_header", texto))
        txt_id = self.header_canvas.create_text(x+w/2, y+h/2, text=texto, font=("Segoe UI", 10, "bold"),
            fill=self.colors['text_primary'], tags=("btn_header", texto))
        
        for tag in [btn_id, txt_id]:
            self.header_canvas.tag_bind(tag, "<Enter>",
                lambda e, b=btn_id: self.header_canvas.itemconfig(b, fill=self.colors['accent_hover']))
            self.header_canvas.tag_bind(tag, "<Leave>",
                lambda e, b=btn_id, c=color: self.header_canvas.itemconfig(b, fill=c))
            self.header_canvas.tag_bind(tag, "<Button-1>", lambda e, cmd=comando: cmd())
    
    def interpolar_color(self, color1: str, color2: str, t: float) -> str:
        """Interpola entre dos colores hexadecimales"""
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def crear_panel_principal(self):
        """Crea el panel principal con pestañas"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.crear_pestana_fotos()
        self.crear_pestana_caratula()
        self.crear_pestana_caratula_final()
        self.crear_pestana_musica()
        self.crear_pestana_videos()
        self.crear_pestana_configuracion()
    
    def crear_pestana_fotos(self):
        """Crea la pestaña de fotos"""
        frame_fotos = ttk.Frame(self.notebook)
        self.notebook.add(frame_fotos, text="📷 Fotos")
        
        panel_izq = ttk.Frame(frame_fotos, width=350)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        panel_izq.pack_propagate(False)
        
        ttk.Label(panel_izq, text="Lista de Fotos", style='Title.TLabel').pack(anchor=tk.W, pady=5)
        
        frame_lista = ttk.Frame(panel_izq)
        frame_lista.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_fotos = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, 
                                        font=('Arial', 10), selectmode=tk.SINGLE)
        self.listbox_fotos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_fotos.yview)
        self.listbox_fotos.bind('<<ListboxSelect>>', lambda e: self._on_select_foto())
        
        frame_botones = ttk.Frame(panel_izq)
        frame_botones.pack(fill=tk.X, pady=5)
        
        ttk.Button(frame_botones, text="➕", width=3, command=self.on_agregar_foto).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="✏️", width=3, command=self.on_editar_foto).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🗑️", width=3, command=self.on_eliminar_foto).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="⬆️", width=3, command=self.on_mover_foto_arriba).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="⬇️", width=3, command=self.on_mover_foto_abajo).pack(side=tk.LEFT, padx=2)
        
        panel_der = ttk.Frame(frame_fotos)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(panel_der, text="Vista Previa", style='Title.TLabel').pack(anchor=tk.W, pady=5)
        
        self.canvas_foto_preview = tk.Canvas(panel_der, width=600, height=450, bd=2, 
                                            relief=tk.SUNKEN, bg='#ffffff')
        self.canvas_foto_preview.pack(pady=10)
        
        props_frame = ttk.LabelFrame(panel_der, text="Propiedades", padding=10)
        props_frame.pack(fill=tk.X, pady=5)
        
        info_frame = ttk.Frame(props_frame)
        info_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(info_frame, text="Título:").pack(side=tk.LEFT, padx=5)
        self.label_foto_titulo = ttk.Label(info_frame, text="-", font=('Arial', 10, 'bold'))
        self.label_foto_titulo.pack(side=tk.LEFT, padx=5)
        
        info_frame2 = ttk.Frame(props_frame)
        info_frame2.pack(fill=tk.X, pady=2)
        
        ttk.Label(info_frame2, text="Duración:").pack(side=tk.LEFT, padx=5)
        self.label_foto_duracion = ttk.Label(info_frame2, text="-")
        self.label_foto_duracion.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(info_frame2, text="Efecto:").pack(side=tk.LEFT, padx=15)
        self.label_foto_efecto = ttk.Label(info_frame2, text="-")
        self.label_foto_efecto.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(props_frame, text="✏️ Editar Foto", 
                  command=self.on_editar_foto).pack(pady=10)
    
    def _on_select_foto(self):
        """Manejador de selección de foto"""
        sel = self.listbox_fotos.curselection()
        if not sel:
            return
        
        idx = sel[0]
        try:
            foto = self._fotos[idx]
            self._mostrar_preview_foto(foto)
            self.label_foto_titulo.config(text=foto.titulo or "Sin título")
            self.label_foto_duracion.config(text=f"{foto.duracion}s")
            self.label_foto_efecto.config(text=foto.efecto or "Ninguno")
        except Exception as e:
            print(f"Error: {e}")
    
    def _mostrar_preview_foto(self, foto):
        """Muestra preview de foto con soporte de efectos animados"""
        try:
            # Cancelar cualquier animación previa
            self._stop_animation()

            if not foto.ruta or not os.path.exists(foto.ruta):
                self.canvas_foto_preview.delete('all')
                self.canvas_foto_preview.create_text(300, 225,
                                                     text="Archivo no encontrado", 
                                                     fill='red', font=('Arial', 12))
                return
            
            img = Image.open(foto.ruta)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Aplicar edición básica
            if foto.rotacion != 0:
                img = img.rotate(-foto.rotacion, expand=True)
            if foto.brillo != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(foto.brillo)
            if foto.contraste != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(foto.contraste)

            # Preparar imagen base ajustada al canvas
            base = img.copy()
            base.thumbnail((580, 430), Image.Resampling.LANCZOS)

            efecto = (foto.efecto or '').strip()
            if efecto and efecto != 'ninguno':
                # Generar frames de animación según el efecto seleccionado
                frames = self._generate_effect_frames(base, efecto, steps=30)
                if frames:
                    self._anim_state = {"frames": frames, "index": 0}
                    self.canvas_foto_preview.delete('all')
                    # Comenzar animación
                    self._animate_preview_frames()
                    return
            
            # Modo estático (sin efecto)
            self._preview_image_tk = ImageTk.PhotoImage(base)
            self.canvas_foto_preview.delete('all')
            self.canvas_foto_preview.create_image(300, 225, image=self._preview_image_tk)
            
        except Exception as e:
            print(f"Error: {e}")

    def _stop_animation(self):
        """Detiene cualquier animación activa en la vista previa"""
        try:
            if self._anim_after_id is not None:
                self.root.after_cancel(self._anim_after_id)
        except Exception:
            pass
        self._anim_after_id = None
        self._anim_state = None

    def _generate_effect_frames(self, base_img, efecto: str, steps: int = 30):
        """Genera una lista de frames PIL aplicando el efecto indicado"""
        try:
            canvas_w, canvas_h = 600, 450
            # Asegurar tamaño base
            w, h = base_img.size
            # Fondo blanco para la vista previa
            def compose(img, dx=0, dy=0):
                bg = Image.new('RGB', (canvas_w, canvas_h), '#ffffff')
                x = (canvas_w - img.size[0]) // 2 + dx
                y = (canvas_h - img.size[1]) // 2 + dy
                bg.paste(img, (x, y))
                return bg

            frames = []
            for i in range(steps):
                t = i / max(steps - 1, 1)
                if efecto == 'fade':
                    # Fundido desde negro a imagen
                    black = Image.new('RGB', base_img.size, '#000000')
                    blended = Image.blend(black, base_img, t)
                    frames.append(compose(blended))
                elif efecto == 'slide_left':
                    dx = int((1.0 - t) * (-canvas_w // 2))
                    frames.append(compose(base_img, dx=dx, dy=0))
                elif efecto == 'slide_right':
                    dx = int((1.0 - t) * (canvas_w // 2))
                    frames.append(compose(base_img, dx=dx, dy=0))
                elif efecto == 'slide_up':
                    dy = int((1.0 - t) * (-canvas_h // 2))
                    frames.append(compose(base_img, dx=0, dy=dy))
                elif efecto == 'slide_down':
                    dy = int((1.0 - t) * (canvas_h // 2))
                    frames.append(compose(base_img, dx=0, dy=dy))
                elif efecto == 'zoom':
                    # Zoom suave hacia adentro (1.0 -> 1.15)
                    scale = 1.0 + 0.15 * t
                    zw = max(1, int(w * scale))
                    zh = max(1, int(h * scale))
                    zimg = base_img.resize((zw, zh), Image.Resampling.LANCZOS)
                    frames.append(compose(zimg))
                elif efecto == 'zigzag':
                    # Movimiento en zig-zag
                    amplitude = 20
                    dx = int((amplitude) * (1 if (i // 3) % 2 == 0 else -1))
                    dy = int(amplitude * (0.5 - t))
                    frames.append(compose(base_img, dx=dx, dy=dy))
                else:
                    frames.append(compose(base_img))
            return frames
        except Exception as e:
            print(f"Error generando frames de efecto: {e}")
            return []

    def _animate_preview_frames(self):
        """Bucle de animación para reproducir frames en el canvas de la vista previa"""
        try:
            if not self._anim_state or not self._anim_state.get('frames'):
                return
            frames = self._anim_state['frames']
            idx = self._anim_state.get('index', 0)
            img = frames[idx % len(frames)]
            self._preview_image_tk = ImageTk.PhotoImage(img)
            self.canvas_foto_preview.delete('all')
            self.canvas_foto_preview.create_image(300, 225, image=self._preview_image_tk)
            self._anim_state['index'] = (idx + 1) % len(frames)
            # ~30 FPS
            self._anim_after_id = self.root.after(33, self._animate_preview_frames)
        except Exception as e:
            print(f"Error en animación de preview: {e}")
            self._stop_animation()
    
    def crear_pestana_caratula(self):
        """Crea la pestaña de carátula CON VISTA PREVIA"""
        frame_caratula = ttk.Frame(self.notebook)
        self.notebook.add(frame_caratula, text="📋 Carátula")

        container = ttk.Frame(frame_caratula)
        container.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(container, width=500)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = ttk.Frame(container, width=600)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        right.pack_propagate(False)

        canvas = tk.Canvas(left)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.crear_campos_caratula(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Label(right, text="Vista Previa en Tiempo Real", style='Title.TLabel').pack(pady=5)
        
        self.canvas_caratula_preview = tk.Canvas(right, width=560, height=420, 
                                                bd=2, relief=tk.SUNKEN, bg='#ffffff')
        self.canvas_caratula_preview.pack(pady=10)
        
        ttk.Button(right, text="🔍 Vista Previa Grande", 
                  command=self._show_caratula_preview_window).pack(pady=5)
    
    def crear_campos_caratula(self, parent):
        """Crea campos de carátula"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Título:").pack(anchor=tk.W)
        self.entry_titulo_caratula = ttk.Entry(frame, font=('Arial', 12))
        self.entry_titulo_caratula.pack(fill=tk.X, pady=2)
        self.entry_titulo_caratula.insert(0, "Mi Video")
        self.entry_titulo_caratula.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        frame_font = ttk.Frame(parent)
        frame_font.pack(fill=tk.X, padx=10, pady=2)
        ttk.Label(frame_font, text="Estilo Título:").pack(anchor=tk.W)
        
        sub = ttk.Frame(frame_font)
        sub.pack(fill=tk.X)
        
        self.combo_titulo_family = ttk.Combobox(sub, values=['Arial','Helvetica','Times New Roman',
                                                              'Courier New','Verdana'], 
                                               width=16, state='readonly')
        self.combo_titulo_family.pack(side=tk.LEFT)
        self.combo_titulo_family.set('Arial')
        self.combo_titulo_family.bind('<<ComboboxSelected>>', lambda e: self._update_caratula_preview())
        
        self.spin_titulo_size = ttk.Spinbox(sub, from_=8, to=72, width=5)
        self.spin_titulo_size.pack(side=tk.LEFT, padx=6)
        self.spin_titulo_size.set(48)
        self.spin_titulo_size.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        self.var_titulo_bold = tk.IntVar()
        self.var_titulo_italic = tk.IntVar()
        
        ttk.Checkbutton(sub, text='Negrita', variable=self.var_titulo_bold, 
                       command=self._update_caratula_preview).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(sub, text='Cursiva', variable=self.var_titulo_italic, 
                       command=self._update_caratula_preview).pack(side=tk.LEFT, padx=6)
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Subtítulo:").pack(anchor=tk.W)
        self.entry_subtitulo_caratula = ttk.Entry(frame, font=('Arial', 10))
        self.entry_subtitulo_caratula.pack(fill=tk.X, pady=2)
        self.entry_subtitulo_caratula.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        frame_font_sub = ttk.Frame(parent)
        frame_font_sub.pack(fill=tk.X, padx=10, pady=2)
        ttk.Label(frame_font_sub, text="Estilo Subtítulo:").pack(anchor=tk.W)
        
        sub2 = ttk.Frame(frame_font_sub)
        sub2.pack(fill=tk.X)
        
        self.combo_subtitulo_family = ttk.Combobox(sub2, values=['Arial','Helvetica','Times New Roman',
                                                                  'Courier New','Verdana'], 
                                                  width=16, state='readonly')
        self.combo_subtitulo_family.pack(side=tk.LEFT)
        self.combo_subtitulo_family.set('Arial')
        self.combo_subtitulo_family.bind('<<ComboboxSelected>>', lambda e: self._update_caratula_preview())
        
        self.spin_subtitulo_size = ttk.Spinbox(sub2, from_=8, to=72, width=5)
        self.spin_subtitulo_size.pack(side=tk.LEFT, padx=6)
        self.spin_subtitulo_size.set(24)
        self.spin_subtitulo_size.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        self.var_subtitulo_bold = tk.IntVar()
        self.var_subtitulo_italic = tk.IntVar()
        
        ttk.Checkbutton(sub2, text='Negrita', variable=self.var_subtitulo_bold, 
                       command=self._update_caratula_preview).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(sub2, text='Cursiva', variable=self.var_subtitulo_italic, 
                       command=self._update_caratula_preview).pack(side=tk.LEFT, padx=6)
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color de Fondo:").pack(anchor=tk.W)
        frame_color = ttk.Frame(frame)
        frame_color.pack(fill=tk.X)
        
        self.entry_color_fondo = ttk.Entry(frame_color, width=10)
        self.entry_color_fondo.pack(side=tk.LEFT, pady=2)
        self.entry_color_fondo.insert(0, "#000080")
        self.entry_color_fondo.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        self.btn_color_fondo = tk.Button(frame_color, text="🎨", width=3, 
                                         command=self.elegir_color_fondo)
        self.btn_color_fondo.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_fondo = tk.Canvas(frame_color, width=34, height=20, 
                                            bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_fondo.create_rectangle(1, 1, 33, 19, fill="#000080", 
                                                  outline="#888888", tags=('preview',))
        self.preview_color_fondo.pack(side=tk.LEFT, padx=5, pady=2)
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color del Título:").pack(anchor=tk.W)
        frame_color = ttk.Frame(frame)
        frame_color.pack(fill=tk.X)
        
        self.entry_color_titulo = ttk.Entry(frame_color, width=10)
        self.entry_color_titulo.pack(side=tk.LEFT, pady=2)
        self.entry_color_titulo.insert(0, "#FFFFFF")
        self.entry_color_titulo.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        self.btn_color_titulo = tk.Button(frame_color, text="🎨", width=3, 
                                          command=self.elegir_color_titulo)
        self.btn_color_titulo.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_titulo = tk.Canvas(frame_color, width=34, height=20, 
                                             bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_titulo.create_rectangle(1, 1, 33, 19, fill="#FFFFFF", 
                                                   outline="#888888", tags=('preview',))
        self.preview_color_titulo.pack(side=tk.LEFT, padx=5, pady=2)
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color del Subtítulo:").pack(anchor=tk.W)
        frame_color_sub = ttk.Frame(frame)
        frame_color_sub.pack(fill=tk.X)
        
        self.entry_color_subtitulo = ttk.Entry(frame_color_sub, width=10)
        self.entry_color_subtitulo.pack(side=tk.LEFT, pady=2)
        self.entry_color_subtitulo.insert(0, "#CCCCCC")
        self.entry_color_subtitulo.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        self.btn_color_subtitulo = tk.Button(frame_color_sub, text="🎨", width=3, 
                                            command=self.elegir_color_subtitulo)
        self.btn_color_subtitulo.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_subtitulo = tk.Canvas(frame_color_sub, width=34, height=20, 
                                                bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_subtitulo.create_rectangle(1, 1, 33, 19, fill="#cccccc", 
                                                      outline="#888888", tags=('preview',))
        self.preview_color_subtitulo.pack(side=tk.LEFT, padx=5, pady=2)
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Duración (segundos):").pack(anchor=tk.W)
        self.spinbox_duracion_caratula = ttk.Spinbox(frame, from_=1, to=10, increment=0.5, width=10)
        self.spinbox_duracion_caratula.pack(anchor=tk.W, pady=2)
        self.spinbox_duracion_caratula.set(3.0)
        
        frame_tb_enable = ttk.Frame(parent)
        frame_tb_enable.pack(fill=tk.X, padx=10, pady=2)
        
        self.var_textbox_enabled = tk.IntVar()
        ttk.Checkbutton(frame_tb_enable, text='Habilitar cuadro de texto', 
                       variable=self.var_textbox_enabled, 
                       command=lambda: [self._toggle_textbox_controls(), 
                                      self._update_caratula_preview()]).pack(anchor=tk.W)
        
        self.frame_textbox_controls = ttk.Frame(parent)
        self.frame_textbox_controls.pack(fill=tk.X, padx=10, pady=2)
        
        ttk.Label(self.frame_textbox_controls, text='Texto:').pack(anchor=tk.W)
        self.textbox_text = tk.Text(self.frame_textbox_controls, height=3)
        self.textbox_text.pack(fill=tk.X, pady=2)
        self.textbox_text.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        frame_tb_pos = ttk.Frame(self.frame_textbox_controls)
        frame_tb_pos.pack(fill=tk.X, pady=2)
        
        ttk.Label(frame_tb_pos, text='Posición:').pack(side=tk.LEFT)
        self.combo_textbox_position = ttk.Combobox(frame_tb_pos, 
                                                   values=['top','center','bottom'], 
                                                   width=10, state='readonly')
        self.combo_textbox_position.pack(side=tk.LEFT, padx=6)
        self.combo_textbox_position.set('bottom')
        self.combo_textbox_position.bind('<<ComboboxSelected>>', 
                                         lambda e: self._update_caratula_preview())
        
        frame_tb_colors = ttk.Frame(self.frame_textbox_controls)
        frame_tb_colors.pack(fill=tk.X, pady=4)
        
        ttk.Label(frame_tb_colors, text='Color Texto:').pack(anchor=tk.W)
        row = ttk.Frame(frame_tb_colors)
        row.pack(fill=tk.X)
        
        self.entry_textbox_text_color = ttk.Entry(row, width=10)
        self.entry_textbox_text_color.pack(side=tk.LEFT)
        self.entry_textbox_text_color.insert(0, "#000000")
        self.entry_textbox_text_color.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        tk.Button(row, text='🎨', width=3, 
                 command=self.elegir_color_textbox_text_color).pack(side=tk.LEFT, padx=6)
        
        ttk.Label(frame_tb_colors, text='Color Fondo:').pack(anchor=tk.W, pady=(5,0))
        row2 = ttk.Frame(frame_tb_colors)
        row2.pack(fill=tk.X)
        
        self.entry_textbox_bg = ttk.Entry(row2, width=10)
        self.entry_textbox_bg.pack(side=tk.LEFT)
        self.entry_textbox_bg.insert(0, "#FFFFFF")
        self.entry_textbox_bg.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        tk.Button(row2, text='🎨', width=3, 
                 command=self.elegir_color_textbox_bg).pack(side=tk.LEFT, padx=6)
        
        self._toggle_textbox_controls()
        
        ttk.Button(parent, text="💾 Guardar Cambios de Carátula",
                  command=self.on_editar_caratula).pack(pady=20, padx=10)
    
    def _update_caratula_preview(self):
        """Actualiza vista previa de carátula"""
        try:
            self.canvas_caratula_preview.update_idletasks()
            w = self.canvas_caratula_preview.winfo_width() or 560
            h = self.canvas_caratula_preview.winfo_height() or 420
            
            color_fondo = self.entry_color_fondo.get() or '#000080'
            if not color_fondo.startswith('#'):
                color_fondo = f'#{color_fondo}'
            
            img = Image.new('RGB', (w, h), color_fondo)
            draw = ImageDraw.Draw(img)
            
            titulo = self.entry_titulo_caratula.get() or 'Mi Video'
            try:
                size_t = int(self.spin_titulo_size.get())
            except:
                size_t = 48
            
            try:
                font_t = ImageFont.truetype('arial.ttf', size_t)
            except:
                font_t = ImageFont.load_default()
            
            color_titulo = self.entry_color_titulo.get() or '#FFFFFF'
            bbox_t = draw.textbbox((0, 0), titulo, font=font_t)
            w_t = bbox_t[2] - bbox_t[0]
            h_t = bbox_t[3] - bbox_t[1]
            draw.text(((w - w_t)//2, h//3), titulo, fill=color_titulo, font=font_t)
            
            subtitulo = self.entry_subtitulo_caratula.get()
            if subtitulo:
                try:
                    size_s = int(self.spin_subtitulo_size.get())
                except:
                    size_s = 24
                
                try:
                    font_s = ImageFont.truetype('arial.ttf', size_s)
                except:
                    font_s = ImageFont.load_default()
                
                color_subtitulo = self.entry_color_subtitulo.get() or '#CCCCCC'
                bbox_s = draw.textbbox((0, 0), subtitulo, font=font_s)
                w_s = bbox_s[2] - bbox_s[0]
                draw.text(((w - w_s)//2, h//3 + h_t + 20), subtitulo, 
                         fill=color_subtitulo, font=font_s)
            
            if self.var_textbox_enabled.get():
                tb_text = self.textbox_text.get('1.0', 'end').strip()
                if tb_text:
                    bg = self.entry_textbox_bg.get() or '#FFFFFF'
                    color = self.entry_textbox_text_color.get() or '#000000'
                    position = self.combo_textbox_position.get()
                    
                    rect_h = 100
                    margin = 20
                    
                    if position == 'top':
                        rect_y = margin
                    elif position == 'center':
                        rect_y = (h - rect_h)//2
                    else:
                        rect_y = h - rect_h - margin
                    
                    draw.rectangle([margin, rect_y, w-margin, rect_y+rect_h], 
                                 fill=bg, outline='#888888', width=2)
                    
                    try:
                        font_tb = ImageFont.truetype('arial.ttf', 16)
                    except:
                        font_tb = ImageFont.load_default()
                    
                    draw.text((margin+10, rect_y+10), tb_text, fill=color, font=font_tb)
            
            self._caratula_preview_tk = ImageTk.PhotoImage(img)
            self.canvas_caratula_preview.delete('all')
            self.canvas_caratula_preview.create_image(w//2, h//2, image=self._caratula_preview_tk)
            
        except Exception as e:
            print(f"Error preview: {e}")
    
    def _toggle_textbox_controls(self):
        """Muestra/oculta controles textbox"""
        if self.var_textbox_enabled.get():
            self.frame_textbox_controls.pack(fill=tk.X, padx=10, pady=2)
        else:
            self.frame_textbox_controls.pack_forget()
    
    def _show_caratula_preview_window(self):
        """Vista previa grande"""
        try:
            W, H = 1280, 720
            color_fondo = self.entry_color_fondo.get() or '#000080'
            if not color_fondo.startswith('#'):
                color_fondo = f'#{color_fondo}'
            
            img = Image.new('RGB', (W, H), color_fondo)
            draw = ImageDraw.Draw(img)
            
            titulo = self.entry_titulo_caratula.get() or 'Mi Video'
            try:
                size_t = int(self.spin_titulo_size.get()) * 2
            except:
                size_t = 96
            
            try:
                font_t = ImageFont.truetype('arial.ttf', size_t)
            except:
                font_t = ImageFont.load_default()
            
            color_titulo = self.entry_color_titulo.get() or '#FFFFFF'
            bbox_t = draw.textbbox((0, 0), titulo, font=font_t)
            w_t = bbox_t[2] - bbox_t[0]
            h_t = bbox_t[3] - bbox_t[1]
            draw.text(((W - w_t)//2, H//3), titulo, fill=color_titulo, font=font_t)
            
            subtitulo = self.entry_subtitulo_caratula.get()
            if subtitulo:
                try:
                    size_s = int(self.spin_subtitulo_size.get()) * 2
                except:
                    size_s = 48
                try:
                    font_s = ImageFont.truetype('arial.ttf', size_s)
                except:
                    font_s = ImageFont.load_default()
                color_subtitulo = self.entry_color_subtitulo.get() or '#CCCCCC'
                bbox_s = draw.textbbox((0, 0), subtitulo, font=font_s)
                w_s = bbox_s[2] - bbox_s[0]
                draw.text(((W - w_s)//2, H//3 + h_t + 40), subtitulo, 
                         fill=color_subtitulo, font=font_s)
            
            if self.var_textbox_enabled.get():
                tb_text = self.textbox_text.get('1.0', 'end').strip()
                if tb_text:
                    bg = self.entry_textbox_bg.get() or '#FFFFFF'
                    color = self.entry_textbox_text_color.get() or '#000000'
                    position = self.combo_textbox_position.get()
                    rect_h = 150
                    margin = 40
                    if position == 'top':
                        rect_y = margin
                    elif position == 'center':
                        rect_y = (H - rect_h)//2
                    else:
                        rect_y = H - rect_h - margin
                    draw.rectangle([margin, rect_y, W-margin, rect_y+rect_h], 
                                 fill=bg, outline='#888888', width=3)
                    try:
                        font_tb = ImageFont.truetype('arial.ttf', 24)
                    except:
                        font_tb = ImageFont.load_default()
                    draw.text((margin+20, rect_y+20), tb_text, fill=color, font=font_tb)
            
            win = tk.Toplevel(self.root)
            win.title('Vista Previa Grande - Carátula')
            win.geometry('1000x600')
            
            canvas_prev = tk.Canvas(win, width=980, height=550)
            canvas_prev.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            img.thumbnail((980, 550), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            
            canvas_prev.create_image(490, 275, image=img_tk)
            canvas_prev.image = img_tk
            
            ttk.Button(win, text='Cerrar', command=win.destroy).pack(pady=10)
        except Exception as e:
            print(f"Error: {e}")
    
    def elegir_color_fondo(self):
        color = colorchooser.askcolor(title="Color de fondo", 
                                     initialcolor=self.entry_color_fondo.get() or '#000080')
        if color and color[1]:
            self.entry_color_fondo.delete(0, tk.END)
            self.entry_color_fondo.insert(0, color[1])
            self.preview_color_fondo.itemconfig('preview', fill=color[1])
            self._update_caratula_preview()

    def elegir_color_titulo(self):
        color = colorchooser.askcolor(title="Color del título", 
                                     initialcolor=self.entry_color_titulo.get() or '#FFFFFF')
        if color and color[1]:
            self.entry_color_titulo.delete(0, tk.END)
            self.entry_color_titulo.insert(0, color[1])
            self.preview_color_titulo.itemconfig('preview', fill=color[1])
            self._update_caratula_preview()

    def elegir_color_subtitulo(self):
        color = colorchooser.askcolor(title="Color del subtítulo", 
                                     initialcolor=self.entry_color_subtitulo.get() or '#CCCCCC')
        if color and color[1]:
            self.entry_color_subtitulo.delete(0, tk.END)
            self.entry_color_subtitulo.insert(0, color[1])
            self.preview_color_subtitulo.itemconfig('preview', fill=color[1])
            self._update_caratula_preview()
    
    def elegir_color_textbox_text_color(self):
        color = colorchooser.askcolor(title="Color del texto", 
                                     initialcolor=self.entry_textbox_text_color.get() or '#000000')
        if color and color[1]:
            self.entry_textbox_text_color.delete(0, tk.END)
            self.entry_textbox_text_color.insert(0, color[1])
            self._update_caratula_preview()

    def elegir_color_textbox_bg(self):
        color = colorchooser.askcolor(title="Color de fondo", 
                                     initialcolor=self.entry_textbox_bg.get() or '#FFFFFF')
        if color and color[1]:
            self.entry_textbox_bg.delete(0, tk.END)
            self.entry_textbox_bg.insert(0, color[1])
            self._update_caratula_preview()
    
    def crear_pestana_caratula_final(self):
        """Crea pestaña carátula FINAL - IDENTICA A CARATULA"""
        frame_caratula = ttk.Frame(self.notebook)
        self.notebook.add(frame_caratula, text="📋 Carátula Final")

        container = ttk.Frame(frame_caratula)
        container.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(container, width=500)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = ttk.Frame(container, width=600)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        right.pack_propagate(False)

        canvas = tk.Canvas(left)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.crear_campos_caratula_final(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Label(right, text="Vista Previa Carátula Final", style='Title.TLabel').pack(pady=5)
        
        self.canvas_caratula_final_preview = tk.Canvas(right, width=560, height=420, 
                                                bd=2, relief=tk.SUNKEN, bg='#ffffff')
        self.canvas_caratula_final_preview.pack(pady=10)
        
        ttk.Button(right, text="🔍 Vista Previa Grande", 
                  command=self._show_caratula_final_preview_window).pack(pady=5)
    
    def crear_campos_caratula_final(self, parent):
        """Crea campos de carátula FINAL - COPIA EXACTA"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Título (Final):").pack(anchor=tk.W)
        self.entry_titulo_caratula_final = ttk.Entry(frame, font=('Arial', 12))
        self.entry_titulo_caratula_final.pack(fill=tk.X, pady=2)
        self.entry_titulo_caratula_final.insert(0, "Fin")
        self.entry_titulo_caratula_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())
        
        frame_font = ttk.Frame(parent)
        frame_font.pack(fill=tk.X, padx=10, pady=2)
        ttk.Label(frame_font, text="Estilo Título (Final):").pack(anchor=tk.W)
        
        sub = ttk.Frame(frame_font)
        sub.pack(fill=tk.X)
        
        self.combo_titulo_family_final = ttk.Combobox(sub, values=['Arial','Helvetica','Times New Roman', 'Courier New','Verdana'], width=16, state='readonly')
        self.combo_titulo_family_final.pack(side=tk.LEFT)
        self.combo_titulo_family_final.set('Arial')
        self.combo_titulo_family_final.bind('<<ComboboxSelected>>', lambda e: self._update_caratula_final_preview())
        
        self.spin_titulo_size_final = ttk.Spinbox(sub, from_=8, to=72, width=5)
        self.spin_titulo_size_final.pack(side=tk.LEFT, padx=6)
        self.spin_titulo_size_final.set(48)
        self.spin_titulo_size_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())
        
        self.var_titulo_bold_final = tk.IntVar()
        self.var_titulo_italic_final = tk.IntVar()
        
        ttk.Checkbutton(sub, text='Negrita', variable=self.var_titulo_bold_final, command=self._update_caratula_final_preview).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(sub, text='Cursiva', variable=self.var_titulo_italic_final, command=self._update_caratula_final_preview).pack(side=tk.LEFT, padx=6)
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Subtítulo (Final):").pack(anchor=tk.W)
        self.entry_subtitulo_caratula_final = ttk.Entry(frame, font=('Arial', 10))
        self.entry_subtitulo_caratula_final.pack(fill=tk.X, pady=2)
        self.entry_subtitulo_caratula_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())
        
        frame_font_sub = ttk.Frame(parent)
        frame_font_sub.pack(fill=tk.X, padx=10, pady=2)
        ttk.Label(frame_font_sub, text="Estilo Subtítulo (Final):").pack(anchor=tk.W)
        
        sub2 = ttk.Frame(frame_font_sub)
        sub2.pack(fill=tk.X)
        
        self.combo_subtitulo_family_final = ttk.Combobox(sub2, values=['Arial','Helvetica','Times New Roman', 'Courier New','Verdana'], width=16, state='readonly')
        self.combo_subtitulo_family_final.pack(side=tk.LEFT)
        self.combo_subtitulo_family_final.set('Arial')
        self.combo_subtitulo_family_final.bind('<<ComboboxSelected>>', lambda e: self._update_caratula_final_preview())
        
        self.spin_subtitulo_size_final = ttk.Spinbox(sub2, from_=8, to=72, width=5)
        self.spin_subtitulo_size_final.pack(side=tk.LEFT, padx=6)
        self.spin_subtitulo_size_final.set(24)
        self.spin_subtitulo_size_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())
        
        self.var_subtitulo_bold_final = tk.IntVar()
        self.var_subtitulo_italic_final = tk.IntVar()
        
        ttk.Checkbutton(sub2, text='Negrita', variable=self.var_subtitulo_bold_final, command=self._update_caratula_final_preview).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(sub2, text='Cursiva', variable=self.var_subtitulo_italic_final, command=self._update_caratula_final_preview).pack(side=tk.LEFT, padx=6)
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color de Fondo (Final):").pack(anchor=tk.W)
        frame_color = ttk.Frame(frame)
        frame_color.pack(fill=tk.X)
        
        self.entry_color_fondo_final = ttk.Entry(frame_color, width=10)
        self.entry_color_fondo_final.pack(side=tk.LEFT, pady=2)
        self.entry_color_fondo_final.insert(0, "#000080")
        self.entry_color_fondo_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())
        
        self.btn_color_fondo_final = tk.Button(frame_color, text="🎨", width=3, command=self.elegir_color_fondo_final)
        self.btn_color_fondo_final.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_fondo_final = tk.Canvas(frame_color, width=34, height=20, bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_fondo_final.create_rectangle(1, 1, 33, 19, fill="#000080", outline="#888888", tags=('preview',))
        self.preview_color_fondo_final.pack(side=tk.LEFT, padx=5, pady=2)
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color del Título (Final):").pack(anchor=tk.W)
        frame_color = ttk.Frame(frame)
        frame_color.pack(fill=tk.X)
        
        self.entry_color_titulo_final = ttk.Entry(frame_color, width=10)
        self.entry_color_titulo_final.pack(side=tk.LEFT, pady=2)
        self.entry_color_titulo_final.insert(0, "#FFFFFF")
        self.entry_color_titulo_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())
        
        self.btn_color_titulo_final = tk.Button(frame_color, text="🎨", width=3, command=self.elegir_color_titulo_final)
        self.btn_color_titulo_final.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_titulo_final = tk.Canvas(frame_color, width=34, height=20, bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_titulo_final.create_rectangle(1, 1, 33, 19, fill="#FFFFFF", outline="#888888", tags=('preview',))
        self.preview_color_titulo_final.pack(side=tk.LEFT, padx=5, pady=2)
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color del Subtítulo (Final):").pack(anchor=tk.W)
        frame_color_sub = ttk.Frame(frame)
        frame_color_sub.pack(fill=tk.X)
        
        self.entry_color_subtitulo_final = ttk.Entry(frame_color_sub, width=10)
        self.entry_color_subtitulo_final.pack(side=tk.LEFT, pady=2)
        self.entry_color_subtitulo_final.insert(0, "#CCCCCC")
        self.entry_color_subtitulo_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())
        
        self.btn_color_subtitulo_final = tk.Button(frame_color_sub, text="🎨", width=3, command=self.elegir_color_subtitulo_final)
        self.btn_color_subtitulo_final.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_subtitulo_final = tk.Canvas(frame_color_sub, width=34, height=20, bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_subtitulo_final.create_rectangle(1, 1, 33, 19, fill="#cccccc", outline="#888888", tags=('preview',))
        self.preview_color_subtitulo_final.pack(side=tk.LEFT, padx=5, pady=2)
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Duración (segundos):").pack(anchor=tk.W)
        self.spinbox_duracion_caratula_final = ttk.Spinbox(frame, from_=1, to=10, increment=0.5, width=10)
        self.spinbox_duracion_caratula_final.pack(anchor=tk.W, pady=2)
        self.spinbox_duracion_caratula_final.set(3.0)
        
        frame_tb_enable = ttk.Frame(parent)
        frame_tb_enable.pack(fill=tk.X, padx=10, pady=2)
        
        self.var_textbox_enabled_final = tk.IntVar()
        ttk.Checkbutton(frame_tb_enable, text='Habilitar cuadro de texto', variable=self.var_textbox_enabled_final, command=lambda: [self._toggle_textbox_controls_final(), self._update_caratula_final_preview()]).pack(anchor=tk.W)
        
        self.frame_textbox_controls_final = ttk.Frame(parent)
        self.frame_textbox_controls_final.pack(fill=tk.X, padx=10, pady=2)
        
        ttk.Label(self.frame_textbox_controls_final, text='Texto:').pack(anchor=tk.W)
        self.textbox_text_final = tk.Text(self.frame_textbox_controls_final, height=3)
        self.textbox_text_final.pack(fill=tk.X, pady=2)
        self.textbox_text_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())
        
        frame_tb_pos = ttk.Frame(self.frame_textbox_controls_final)
        frame_tb_pos.pack(fill=tk.X, pady=2)
        
        ttk.Label(frame_tb_pos, text='Posición:').pack(side=tk.LEFT)
        self.combo_textbox_position_final = ttk.Combobox(frame_tb_pos, values=['top','center','bottom'], width=10, state='readonly')
        self.combo_textbox_position_final.pack(side=tk.LEFT, padx=6)
        self.combo_textbox_position_final.set('bottom')
        self.combo_textbox_position_final.bind('<<ComboboxSelected>>', lambda e: self._update_caratula_final_preview())
        
        frame_tb_colors = ttk.Frame(self.frame_textbox_controls_final)
        frame_tb_colors.pack(fill=tk.X, pady=4)
        
        ttk.Label(frame_tb_colors, text='Color Texto:').pack(anchor=tk.W)
        row = ttk.Frame(frame_tb_colors)
        row.pack(fill=tk.X)
        
        self.entry_textbox_text_color_final = ttk.Entry(row, width=10)
        self.entry_textbox_text_color_final.pack(side=tk.LEFT)
        self.entry_textbox_text_color_final.insert(0, "#000000")
        self.entry_textbox_text_color_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())
        
        tk.Button(row, text='🎨', width=3, command=self.elegir_color_textbox_text_color_final).pack(side=tk.LEFT, padx=6)
        
        ttk.Label(frame_tb_colors, text='Color Fondo:').pack(anchor=tk.W, pady=(5,0))
        row2 = ttk.Frame(frame_tb_colors)
        row2.pack(fill=tk.X)
        
        self.entry_textbox_bg_final = ttk.Entry(row2, width=10)
        self.entry_textbox_bg_final.pack(side=tk.LEFT)
        self.entry_textbox_bg_final.insert(0, "#FFFFFF")
        self.entry_textbox_bg_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())
        
        tk.Button(row2, text='🎨', width=3, command=self.elegir_color_textbox_bg_final).pack(side=tk.LEFT, padx=6)
        
        self._toggle_textbox_controls_final()
        
        ttk.Button(parent, text="💾 Guardar Cambios de Carátula Final", command=self.on_editar_caratula_final).pack(pady=20, padx=10)
    
    def _update_caratula_final_preview(self):
        """Actualiza preview carátula final"""
        try:
            self.canvas_caratula_final_preview.update_idletasks()
            w = self.canvas_caratula_final_preview.winfo_width() or 560
            h = self.canvas_caratula_final_preview.winfo_height() or 420
            
            color_fondo = self.entry_color_fondo_final.get() or '#000080'
            if not color_fondo.startswith('#'):
                color_fondo = f'#{color_fondo}'
            
            img = Image.new('RGB', (w, h), color_fondo)
            draw = ImageDraw.Draw(img)
            
            titulo = self.entry_titulo_caratula_final.get() or 'Fin'
            try:
                size_t = int(self.spin_titulo_size_final.get())
            except:
                size_t = 48
            
            try:
                font_t = ImageFont.truetype('arial.ttf', size_t)
            except:
                font_t = ImageFont.load_default()
            
            color_titulo = self.entry_color_titulo_final.get() or '#FFFFFF'
            bbox_t = draw.textbbox((0, 0), titulo, font=font_t)
            w_t = bbox_t[2] - bbox_t[0]
            h_t = bbox_t[3] - bbox_t[1]
            draw.text(((w - w_t)//2, h//3), titulo, fill=color_titulo, font=font_t)
            
            subtitulo = self.entry_subtitulo_caratula_final.get()
            if subtitulo:
                try:
                    size_s = int(self.spin_subtitulo_size_final.get())
                except:
                    size_s = 24
                
                try:
                    font_s = ImageFont.truetype('arial.ttf', size_s)
                except:
                    font_s = ImageFont.load_default()
                
                color_subtitulo = self.entry_color_subtitulo_final.get() or '#CCCCCC'
                bbox_s = draw.textbbox((0, 0), subtitulo, font=font_s)
                w_s = bbox_s[2] - bbox_s[0]
                draw.text(((w - w_s)//2, h//3 + h_t + 20), subtitulo, fill=color_subtitulo, font=font_s)
            
            if self.var_textbox_enabled_final.get():
                tb_text = self.textbox_text_final.get('1.0', 'end').strip()
                if tb_text:
                    bg = self.entry_textbox_bg_final.get() or '#FFFFFF'
                    color = self.entry_textbox_text_color_final.get() or '#000000'
                    position = self.combo_textbox_position_final.get()
                    rect_h = 100
                    margin = 20
                    if position == 'top':
                        rect_y = margin
                    elif position == 'center':
                        rect_y = (h - rect_h)//2
                    else:
                        rect_y = h - rect_h - margin
                    draw.rectangle([margin, rect_y, w-margin, rect_y+rect_h], fill=bg, outline='#888888', width=2)
                    try:
                        font_tb = ImageFont.truetype('arial.ttf', 16)
                    except:
                        font_tb = ImageFont.load_default()
                    draw.text((margin+10, rect_y+10), tb_text, fill=color, font=font_tb)
            
            self._caratula_final_preview_tk = ImageTk.PhotoImage(img)
            self.canvas_caratula_final_preview.delete('all')
            self.canvas_caratula_final_preview.create_image(w//2, h//2, image=self._caratula_final_preview_tk)
        except Exception as e:
            print(f"Error: {e}")

    def _toggle_textbox_controls_final(self):
        if self.var_textbox_enabled_final.get():
            self.frame_textbox_controls_final.pack(fill=tk.X, padx=10, pady=2)
        else:
            self.frame_textbox_controls_final.pack_forget()

    def _show_caratula_final_preview_window(self):
        try:
            W, H = 1280, 720
            color_fondo = self.entry_color_fondo_final.get() or '#000080'
            if not color_fondo.startswith('#'):
                color_fondo = f'#{color_fondo}'
            img = Image.new('RGB', (W, H), color_fondo)
            draw = ImageDraw.Draw(img)
            
            titulo = self.entry_titulo_caratula_final.get() or 'Fin'
            try:
                size_t = int(self.spin_titulo_size_final.get()) * 2
            except:
                size_t = 96
            
            try:
                font_t = ImageFont.truetype('arial.ttf', size_t)
            except:
                font_t = ImageFont.load_default()
            
            color_titulo = self.entry_color_titulo_final.get() or '#FFFFFF'
            bbox_t = draw.textbbox((0, 0), titulo, font=font_t)
            w_t = bbox_t[2] - bbox_t[0]
            h_t = bbox_t[3] - bbox_t[1]
            draw.text(((W - w_t)//2, H//3), titulo, fill=color_titulo, font=font_t)
            
            subtitulo = self.entry_subtitulo_caratula_final.get()
            if subtitulo:
                try:
                    size_s = int(self.spin_subtitulo_size_final.get()) * 2
                except:
                    size_s = 48
                try:
                    font_s = ImageFont.truetype('arial.ttf', size_s)
                except:
                    font_s = ImageFont.load_default()
                color_subtitulo = self.entry_color_subtitulo_final.get() or '#CCCCCC'
                bbox_s = draw.textbbox((0, 0), subtitulo, font=font_s)
                w_s = bbox_s[2] - bbox_s[0]
                draw.text(((W - w_s)//2, H//3 + h_t + 40), subtitulo, fill=color_subtitulo, font=font_s)

            if self.var_textbox_enabled_final.get():
                tb_text = self.textbox_text_final.get('1.0', 'end').strip()
                if tb_text:
                    bg = self.entry_textbox_bg_final.get() or '#FFFFFF'
                    color = self.entry_textbox_text_color_final.get() or '#000000'
                    position = self.combo_textbox_position_final.get()
                    rect_h = 150
                    margin = 40
                    if position == 'top':
                        rect_y = margin
                    elif position == 'center':
                        rect_y = (H - rect_h)//2
                    else:
                        rect_y = H - rect_h - margin
                    draw.rectangle([margin, rect_y, W-margin, rect_y+rect_h], fill=bg, outline='#888888', width=3)
                    try:
                        font_tb = ImageFont.truetype('arial.ttf', 24)
                    except:
                        font_tb = ImageFont.load_default()
                    draw.text((margin+20, rect_y+20), tb_text, fill=color, font=font_tb)

            win = tk.Toplevel(self.root)
            win.title('Vista Previa Grande - Carátula Final')
            win.geometry('1000x600')
            
            canvas_prev = tk.Canvas(win, width=980, height=550)
            canvas_prev.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            img.thumbnail((980, 550), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            
            canvas_prev.create_image(490, 275, image=img_tk)
            canvas_prev.image = img_tk
            
            ttk.Button(win, text='Cerrar', command=win.destroy).pack(pady=10)
        except Exception as e:
            print(f"Error: {e}")

    def elegir_color_fondo_final(self):
        color = colorchooser.askcolor(title="Color de fondo (Final)", initialcolor=self.entry_color_fondo_final.get() or '#000080')
        if color and color[1]:
            self.entry_color_fondo_final.delete(0, tk.END)
            self.entry_color_fondo_final.insert(0, color[1])
            self.preview_color_fondo_final.itemconfig('preview', fill=color[1])
            self._update_caratula_final_preview()

    def elegir_color_titulo_final(self):
        color = colorchooser.askcolor(title="Color del título (Final)", initialcolor=self.entry_color_titulo_final.get() or '#FFFFFF')
        if color and color[1]:
            self.entry_color_titulo_final.delete(0, tk.END)
            self.entry_color_titulo_final.insert(0, color[1])
            self.preview_color_titulo_final.itemconfig('preview', fill=color[1])
            self._update_caratula_final_preview()

    def elegir_color_subtitulo_final(self):
        color = colorchooser.askcolor(title="Color del subtítulo (Final)", initialcolor=self.entry_color_subtitulo_final.get() or '#CCCCCC')
        if color and color[1]:
            self.entry_color_subtitulo_final.delete(0, tk.END)
            self.entry_color_subtitulo_final.insert(0, color[1])
            self.preview_color_subtitulo_final.itemconfig('preview', fill=color[1])
            self._update_caratula_final_preview()

    def elegir_color_textbox_text_color_final(self):
        color = colorchooser.askcolor(title="Color del texto (Final)", initialcolor=self.entry_textbox_text_color_final.get() or '#000000')
        if color and color[1]:
            self.entry_textbox_text_color_final.delete(0, tk.END)
            self.entry_textbox_text_color_final.insert(0, color[1])
            self._update_caratula_final_preview()

    def elegir_color_textbox_bg_final(self):
        color = colorchooser.askcolor(title="Color de fondo (Final)", initialcolor=self.entry_textbox_bg_final.get() or '#FFFFFF')
        if color and color[1]:
            self.entry_textbox_bg_final.delete(0, tk.END)
            self.entry_textbox_bg_final.insert(0, color[1])
            self._update_caratula_final_preview()
    
    def crear_pestana_musica(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎵 Música")
        
        ttk.Label(frame, text="Música del Video", style='Title.TLabel').pack(pady=20, padx=20, anchor=tk.W)
        
        self.frame_info_musica = ttk.Frame(frame)
        self.frame_info_musica.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.label_musica_actual = ttk.Label(self.frame_info_musica, text="No hay música agregada")
        self.label_musica_actual.pack(anchor=tk.W, pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(btn_frame, text="📁 Cargar Archivo",
                  command=self.on_agregar_musica, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🌐 YouTube",
                  command=self.on_descargar_youtube).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Eliminar",
                  command=self.on_eliminar_musica).pack(side=tk.LEFT, padx=5)
    
    def crear_pestana_videos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎬 Videos")
        
        ttk.Label(frame, text="Videos del Proyecto", style='Title.TLabel').pack(pady=20, padx=20, anchor=tk.W)
        
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_videos = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=('Arial', 10))
        self.listbox_videos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_videos.yview)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(btn_frame, text="📁 Agregar",
                  command=self.on_agregar_video, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Eliminar",
                  command=self.on_eliminar_video).pack(side=tk.LEFT, padx=5)
    
    def crear_pestana_configuracion(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚙️ Configuración")
        
        ttk.Label(frame, text="Configuración del Video", style='Title.TLabel').pack(pady=20, padx=20, anchor=tk.W)
        
        config_frame = ttk.Frame(frame)
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(config_frame, text="Resolución:").pack(anchor=tk.W, pady=5)
        self.combo_resolucion = ttk.Combobox(config_frame, values=[
            "1920x1080 (Full HD)",
            "1280x720 (HD)",
            "3840x2160 (4K)"
        ], state='readonly')
        self.combo_resolucion.pack(fill=tk.X, pady=5)
        self.combo_resolucion.set("1920x1080 (Full HD)")
        
        ttk.Label(config_frame, text="FPS:").pack(anchor=tk.W, pady=5)
        self.combo_fps = ttk.Combobox(config_frame, values=["24", "30", "60"], state='readonly')
        self.combo_fps.pack(fill=tk.X, pady=5)
        self.combo_fps.set("30")
    
    def crear_barra_estado(self):
        self.barra_estado = ttk.Label(self.root, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)
    
    def on_nuevo_proyecto(self):
        if self.callback_nuevo_proyecto:
            self.callback_nuevo_proyecto()
    
    def on_abrir_proyecto(self):
        if self.callback_abrir_proyecto:
            self.callback_abrir_proyecto()
    
    def on_guardar_proyecto(self):
        if self.callback_guardar_proyecto:
            self.callback_guardar_proyecto()
    
    def on_agregar_foto(self):
        if self.callback_agregar_foto:
            self.callback_agregar_foto()
    
    def on_eliminar_foto(self):
        if self.callback_eliminar_foto:
            self.callback_eliminar_foto()
    
    def on_editar_foto(self):
        if self.callback_editar_foto:
            self.callback_editar_foto()
    
    def on_mover_foto_arriba(self):
        if self.callback_mover_foto_arriba:
            self.callback_mover_foto_arriba()
    
    def on_mover_foto_abajo(self):
        if self.callback_mover_foto_abajo:
            self.callback_mover_foto_abajo()
    
    def on_agregar_musica(self):
        if self.callback_agregar_musica:
            self.callback_agregar_musica()
    
    def on_eliminar_musica(self):
        if self.callback_eliminar_musica:
            self.callback_eliminar_musica()
    
    def on_agregar_video(self):
        if self.callback_agregar_video:
            self.callback_agregar_video()
    
    def on_eliminar_video(self):
        sel = self.listbox_videos.curselection()
        if sel and self.callback_eliminar_video:
            self.callback_eliminar_video(sel[0])
    
    def on_editar_caratula(self):
        if self.callback_editar_caratula:
            self.callback_editar_caratula()
    
    def on_editar_caratula_final(self):
        if self.callback_editar_caratula_final:
            self.callback_editar_caratula_final()
    
    def on_generar_video(self):
        if self.callback_vista_previa:
            self.callback_vista_previa()
    
    def on_descargar_youtube(self):
        from tkinter.simpledialog import askstring
        url = askstring("Descargar de YouTube", "Ingrese la URL:")
        if url and self.callback_descargar_youtube:
            self.callback_descargar_youtube(url)
    
    def actualizar_lista_fotos(self, fotos):
        self._fotos = fotos or []
        self.listbox_fotos.delete(0, tk.END)
        for i, foto in enumerate(self._fotos):
            nombre = foto.titulo if foto.titulo else os.path.basename(foto.ruta)
            self.listbox_fotos.insert(tk.END, f"{i+1}. {nombre} ({foto.duracion}s)")
    
    def actualizar_lista_videos(self, videos):
        try:
            self.listbox_videos.delete(0, tk.END)
            for i, v in enumerate(videos or []):
                if isinstance(v, str):
                    nombre = os.path.basename(v)
                else:
                    nombre = v.get('nombre', '') or os.path.basename(v.get('ruta', ''))
                self.listbox_videos.insert(tk.END, f"{i+1}. {nombre}")
        except Exception as e:
            print(f"Error: {e}")
    
    def actualizar_info_musica(self, musica):
        if musica:
            texto = f"🎵 {musica.nombre}\n📁 {musica.ruta}"
            self.label_musica_actual.config(text=texto)
        else:
            self.label_musica_actual.config(text="No hay música agregada")
    
    def actualizar_caratula(self, caratula):
        self.entry_titulo_caratula.delete(0, tk.END)
        self.entry_titulo_caratula.insert(0, caratula.titulo)
        
        self.entry_subtitulo_caratula.delete(0, tk.END)
        self.entry_subtitulo_caratula.insert(0, caratula.subtitulo)
        
        self.entry_color_fondo.delete(0, tk.END)
        self.entry_color_fondo.insert(0, caratula.color_fondo)
        self.preview_color_fondo.itemconfig('preview', fill=caratula.color_fondo)
        
        self.entry_color_titulo.delete(0, tk.END)
        self.entry_color_titulo.insert(0, caratula.color_titulo)
        self.preview_color_titulo.itemconfig('preview', fill=caratula.color_titulo)
        
        self.entry_color_subtitulo.delete(0, tk.END)
        self.entry_color_subtitulo.insert(0, caratula.color_subtitulo)
        self.preview_color_subtitulo.itemconfig('preview', fill=caratula.color_subtitulo)
        
        self.combo_titulo_family.set(caratula.fuente_titulo)
        self.spin_titulo_size.set(caratula.tamaño_titulo)
        self.var_titulo_bold.set(1 if caratula.titulo_bold else 0)
        self.var_titulo_italic.set(1 if caratula.titulo_italic else 0)
        
        self.combo_subtitulo_family.set(caratula.fuente_subtitulo)
        self.spin_subtitulo_size.set(caratula.tamaño_subtitulo)
        self.var_subtitulo_bold.set(1 if caratula.subtitulo_bold else 0)
        self.var_subtitulo_italic.set(1 if caratula.subtitulo_italic else 0)
        
        self.spinbox_duracion_caratula.set(caratula.duracion)
        
        self.var_textbox_enabled.set(1 if caratula.textbox_enabled else 0)
        self.textbox_text.delete('1.0', tk.END)
        self.textbox_text.insert('1.0', caratula.textbox_text)
        self.entry_textbox_text_color.delete(0, tk.END)
        self.entry_textbox_text_color.insert(0, caratula.textbox_text_color)
        self.entry_textbox_bg.delete(0, tk.END)
        self.entry_textbox_bg.insert(0, caratula.textbox_bg)
        self.combo_textbox_position.set(caratula.textbox_position)
        
        self._toggle_textbox_controls()
        self._update_caratula_preview()
    
    def actualizar_caratula_final(self, caratula):
        self.entry_titulo_caratula_final.delete(0, tk.END)
        self.entry_titulo_caratula_final.insert(0, caratula.titulo)
        
        self.entry_subtitulo_caratula_final.delete(0, tk.END)
        self.entry_subtitulo_caratula_final.insert(0, caratula.subtitulo)
        
        self.entry_color_fondo_final.delete(0, tk.END)
        self.entry_color_fondo_final.insert(0, caratula.color_fondo)
        self.preview_color_fondo_final.itemconfig('preview', fill=caratula.color_fondo)
        
        self.entry_color_titulo_final.delete(0, tk.END)
        self.entry_color_titulo_final.insert(0, caratula.color_titulo)
        self.preview_color_titulo_final.itemconfig('preview', fill=caratula.color_titulo)
        
        self.entry_color_subtitulo_final.delete(0, tk.END)
        self.entry_color_subtitulo_final.insert(0, caratula.color_subtitulo)
        self.preview_color_subtitulo_final.itemconfig('preview', fill=caratula.color_subtitulo)
        
        self.combo_titulo_family_final.set(caratula.fuente_titulo)
        self.spin_titulo_size_final.set(caratula.tamaño_titulo)
        self.var_titulo_bold_final.set(1 if caratula.titulo_bold else 0)
        self.var_titulo_italic_final.set(1 if caratula.titulo_italic else 0)
        
        self.combo_subtitulo_family_final.set(caratula.fuente_subtitulo)
        self.spin_subtitulo_size_final.set(caratula.tamaño_subtitulo)
        self.var_subtitulo_bold_final.set(1 if caratula.subtitulo_bold else 0)
        self.var_subtitulo_italic_final.set(1 if caratula.subtitulo_italic else 0)
        
        self.spinbox_duracion_caratula_final.set(caratula.duracion)
        
        self.var_textbox_enabled_final.set(1 if caratula.textbox_enabled else 0)
        self.textbox_text_final.delete('1.0', tk.END)
        self.textbox_text_final.insert('1.0', caratula.textbox_text)
        self.entry_textbox_text_color_final.delete(0, tk.END)
        self.entry_textbox_text_color_final.insert(0, caratula.textbox_text_color)
        self.entry_textbox_bg_final.delete(0, tk.END)
        self.entry_textbox_bg_final.insert(0, caratula.textbox_bg)
        self.combo_textbox_position_final.set(caratula.textbox_position)
        
        self._toggle_textbox_controls_final()
        self._update_caratula_final_preview()
    
    def actualizar_imagenes_list(self, imagenes):
        pass
    
    def actualizar_estado(self, mensaje: str):
        self.barra_estado.config(text=mensaje)
        self.root.update_idletasks()
    
    def mostrar_mensaje(self, titulo: str, mensaje: str, tipo: str = "info"):
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
    
    def confirmar(self, titulo: str, mensaje: str) -> bool:
        return messagebox.askyesno(titulo, mensaje)
    
    def mostrar_acerca_de(self):
        mensaje = """Video Maker Pro v1.0

Creador Profesional de Videos

Desarrollado por: José
Gerente Administrativo
Consejo Superior del Colegio de Médicos
Provincia de Buenos Aires

© 2026"""
        messagebox.showinfo("Acerca de", mensaje)