"""
Vista Principal de Video Maker
Interfaz gráfica principal con Tkinter y vistas previas en tiempo real
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, font as tkfont, filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFont
import os

class VistaPrincipal:
    """Vista principal de la aplicación"""
    
    def __init__(self, root: tk.Tk):
        print('DEBUG: VistaPrincipal.__init__ - start')
        self.root = root
        self.root.title("Video Maker - Creador de Videos con Fotos")
        self.root.geometry("1400x900")
        
        # Configurar estilo
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
        self.callback_generar_video = None
        self.callback_aplicar_edicion_foto = None
        self.callback_agregar_imagen_caratula = None
        self.callback_eliminar_imagen_caratula = None
        self.callback_actualizar_imagen_caratula = None
        self.callback_vista_previa = None
        
        # Variables internas
        self._fotos = []
        self._imagenes_items = []
        self._original_image = None
        self._current_image = None
        self._preview_image_tk = None
        self._caratula_preview_tk = None
        self._imagen_preview_tk = None
        
        # Crear interfaz
        self.crear_menu()
        self.crear_toolbar()
        self.crear_panel_principal()
        self.crear_barra_estado()
        print('DEBUG: VistaPrincipal.__init__ - end')
        
    def configurar_estilos(self):
        """Configura los estilos de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
        
    def crear_menu(self):
        """Crea el menú principal"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nuevo Proyecto", accelerator="Ctrl+N", 
                                command=self.on_nuevo_proyecto)
        menu_archivo.add_command(label="Abrir Proyecto", accelerator="Ctrl+O", 
                                command=self.on_abrir_proyecto)
        menu_archivo.add_command(label="Guardar Proyecto", accelerator="Ctrl+S", 
                                command=self.on_guardar_proyecto)
        menu_archivo.add_command(label="Guardar Como...", accelerator="Ctrl+Shift+S")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", accelerator="Alt+F4", command=self.root.quit)
        
        # Menú Editar
        menu_editar = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=menu_editar)
        menu_editar.add_command(label="Agregar Foto", command=self.on_agregar_foto)
        menu_editar.add_command(label="Eliminar Foto", command=self.on_eliminar_foto)
        menu_editar.add_command(label="Editar Foto", command=self.on_editar_foto)
        menu_editar.add_separator()
        menu_editar.add_command(label="Agregar Música", command=self.on_agregar_musica)
        menu_editar.add_command(label="Editar Carátula", command=self.on_editar_caratula)
        
        # Menú Video
        menu_video = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Video", menu=menu_video)
        menu_video.add_command(label="Generar Video", accelerator="F5", 
                              command=self.on_generar_video)
        menu_video.add_command(label="Vista Previa")
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Manual de Usuario")
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        
        # Atajos de teclado
        self.root.bind('<Control-n>', lambda e: self.on_nuevo_proyecto())
        self.root.bind('<Control-o>', lambda e: self.on_abrir_proyecto())
        self.root.bind('<Control-s>', lambda e: self.on_guardar_proyecto())
        self.root.bind('<F5>', lambda e: self.on_generar_video())
        
    def crear_toolbar(self):
        """Crea la barra de herramientas"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="📁 Nuevo", command=self.on_nuevo_proyecto).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📂 Abrir", command=self.on_abrir_proyecto).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💾 Guardar", command=self.on_guardar_proyecto).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(toolbar, text="🖼️ Agregar Foto", command=self.on_agregar_foto).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🎵 Agregar Música", command=self.on_agregar_musica).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📋 Editar Carátula", command=self.on_editar_caratula).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(toolbar, text="▶️ Generar Video", style='Accent.TButton',
                  command=self.on_generar_video).pack(side=tk.LEFT, padx=2)
        
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
        """Crea la pestaña de gestión de fotos con vista previa mejorada"""
        frame_fotos = ttk.Frame(self.notebook)
        self.notebook.add(frame_fotos, text="📷 Fotos")
        
        # Panel izquierdo - Lista de fotos
        panel_izq = ttk.Frame(frame_fotos, width=350)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        panel_izq.pack_propagate(False)
        
        ttk.Label(panel_izq, text="Lista de Fotos", style='Title.TLabel').pack(anchor=tk.W, pady=5)
        
        # Listbox con scrollbar
        frame_lista = ttk.Frame(panel_izq)
        frame_lista.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_fotos = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, 
                                        font=('Arial', 10), selectmode=tk.SINGLE)
        self.listbox_fotos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_fotos.yview)
        self.listbox_fotos.bind('<<ListboxSelect>>', lambda e: self._on_select_foto())
        
        # Botones de control
        frame_botones = ttk.Frame(panel_izq)
        frame_botones.pack(fill=tk.X, pady=5)
        
        ttk.Button(frame_botones, text="➕", width=3, command=self.on_agregar_foto).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="✏️", width=3, command=self.on_editar_foto).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🗑️", width=3, command=self.on_eliminar_foto).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="⬆️", width=3, command=self.on_mover_foto_arriba).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="⬇️", width=3, command=self.on_mover_foto_abajo).pack(side=tk.LEFT, padx=2)
        
        # Panel derecho - Vista previa y propiedades
        panel_der = ttk.Frame(frame_fotos)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(panel_der, text="Vista Previa y Propiedades", style='Title.TLabel').pack(anchor=tk.W, pady=5)
        
        # Canvas de vista previa grande
        self.canvas_foto_preview = tk.Canvas(panel_der, width=600, height=450, bd=2, 
                                            relief=tk.SUNKEN, bg='#ffffff')
        self.canvas_foto_preview.pack(pady=10)
        
        # Panel de propiedades rápidas
        props_frame = ttk.LabelFrame(panel_der, text="Propiedades Rápidas", padding=10)
        props_frame.pack(fill=tk.X, pady=5)
        
        # Info de la foto
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
        
        # Botón de edición completa
        ttk.Button(props_frame, text="✏️ Editar Foto Completa", 
                  command=self.on_editar_foto).pack(pady=10)
        
    def _on_select_foto(self):
        """Manejador cuando se selecciona una foto en la lista"""
        sel = self.listbox_fotos.curselection()
        if not sel:
            return
        
        idx = sel[0]
        try:
            foto = self._fotos[idx]
            self._mostrar_preview_foto(foto)
            
            # Actualizar labels de info
            self.label_foto_titulo.config(text=foto.titulo or "Sin título")
            self.label_foto_duracion.config(text=f"{foto.duracion}s")
            self.label_foto_efecto.config(text=foto.efecto)
            
        except Exception as e:
            print(f"Error al mostrar preview: {e}")
    
    def _mostrar_preview_foto(self, foto):
        """Muestra la vista previa de una foto con todos sus efectos"""
        try:
            if not foto.ruta or not os.path.exists(foto.ruta):
                self.canvas_foto_preview.delete('all')
                self.canvas_foto_preview.create_text(10, 10, anchor='nw', 
                                                     text="Archivo no encontrado", 
                                                     fill='red', font=('Arial', 12))
                return
            
            # Cargar imagen
            img = Image.open(foto.ruta)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Aplicar rotación
            if foto.rotacion != 0:
                img = img.rotate(-foto.rotacion, expand=True)
            
            # Aplicar brillo
            if foto.brillo != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(foto.brillo)
            
            # Aplicar contraste
            if foto.contraste != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(foto.contraste)
            
            # Aplicar marco
            if foto.marco:
                img = self._aplicar_marco_preview(img, foto.marco, foto.color_marco)
            
            # Aplicar texto
            if foto.texto:
                img = self._aplicar_texto_preview(img, foto.texto, foto.color_texto, 
                                                 foto.posicion_texto)
            
            # Redimensionar para canvas
            img.thumbnail((580, 430), Image.Resampling.LANCZOS)
            
            # Convertir a PhotoImage
            self._preview_image_tk = ImageTk.PhotoImage(img)
            
            # Mostrar en canvas
            self.canvas_foto_preview.delete('all')
            self.canvas_foto_preview.create_image(300, 225, image=self._preview_image_tk)
            
        except Exception as e:
            print(f"Error al generar preview: {e}")
            self.canvas_foto_preview.delete('all')
            self.canvas_foto_preview.create_text(10, 10, anchor='nw', 
                                                text=f"Error: {str(e)}", 
                                                fill='red', font=('Arial', 10))
    
    def _aplicar_marco_preview(self, img, tipo_marco, color):
        """Aplica marco a la imagen de preview"""
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
                draw.rectangle([offset+i, offset+i, width-offset-1-i, height-offset-1-i], 
                             outline=color_rgb)
                             
        elif tipo_marco == "sombra":
            grosor = max(5, width // 100)
            sombra = tuple(max(0, c - 80) for c in color_rgb)
            draw.rectangle([grosor, grosor, width-1, height-1], outline=sombra, width=grosor)
            for i in range(grosor):
                draw.rectangle([i, i, width-grosor-i, height-grosor-i], outline=color_rgb)
                
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
        """Aplica texto a la imagen de preview"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        try:
            font = ImageFont.truetype("arial.ttf", max(20, width // 25))
        except:
            font = ImageFont.load_default()
        
        # Calcular posición
        bbox = draw.textbbox((0, 0), texto, font=font)
        texto_width = bbox[2] - bbox[0]
        texto_height = bbox[3] - bbox[1]
        
        x = (width - texto_width) // 2
        
        if posicion == "top":
            y = 20
        elif posicion == "center":
            y = (height - texto_height) // 2
        else:  # bottom
            y = height - texto_height - 20
        
        # Sombra
        draw.text((x+2, y+2), texto, fill='#000000', font=font)
        # Texto
        draw.text((x, y), texto, fill=color, font=font)
        
        return img
        
    def crear_pestana_caratula(self):
        """Crea la pestaña de configuración de carátula con vista previa en tiempo real"""
        frame_caratula = ttk.Frame(self.notebook)
        self.notebook.add(frame_caratula, text="📋 Carátula")

        # Contenedor principal
        container = ttk.Frame(frame_caratula)
        container.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo - Controles con scroll
        left = ttk.Frame(container, width=500)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Panel derecho - Vista previa
        right = ttk.Frame(container, width=600)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        right.pack_propagate(False)

        # Scroll en panel izquierdo
        canvas = tk.Canvas(left)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Campos de carátula
        self.crear_campos_caratula(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Vista previa en panel derecho
        ttk.Label(right, text="Vista Previa en Tiempo Real", 
                 style='Title.TLabel').pack(pady=5)
        
        self.canvas_caratula_preview = tk.Canvas(right, width=560, height=420, 
                                                bd=2, relief=tk.SUNKEN, bg='#ffffff')
        self.canvas_caratula_preview.pack(pady=10)
        
        # Botón para vista previa en ventana grande
        ttk.Button(right, text="🔍 Vista Previa Grande", 
                  command=self._show_caratula_preview_window).pack(pady=5)
        
    def crear_campos_caratula(self, parent):
        """Crea los campos de edición de carátula"""
        # Título
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Título:").pack(anchor=tk.W)
        self.entry_titulo_caratula = ttk.Entry(frame, font=('Arial', 12))
        self.entry_titulo_caratula.pack(fill=tk.X, pady=2)
        self.entry_titulo_caratula.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        # Controles de fuente para título
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
        self.spin_titulo_size.bind('<FocusOut>', lambda e: self._update_caratula_preview())
        
        self.var_titulo_bold = tk.IntVar()
        self.var_titulo_italic = tk.IntVar()
        
        ttk.Checkbutton(sub, text='Negrita', variable=self.var_titulo_bold, 
                       command=self._update_caratula_preview).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(sub, text='Cursiva', variable=self.var_titulo_italic, 
                       command=self._update_caratula_preview).pack(side=tk.LEFT, padx=6)
        
        # Subtítulo
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Subtítulo:").pack(anchor=tk.W)
        self.entry_subtitulo_caratula = ttk.Entry(frame, font=('Arial', 10))
        self.entry_subtitulo_caratula.pack(fill=tk.X, pady=2)
        self.entry_subtitulo_caratula.bind('<KeyRelease>', lambda e: self._update_caratula_preview())
        
        # Controles de fuente para subtítulo
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
        self.spin_subtitulo_size.bind('<FocusOut>', lambda e: self._update_caratula_preview())
        
        self.var_subtitulo_bold = tk.IntVar()
        self.var_subtitulo_italic = tk.IntVar()
        
        ttk.Checkbutton(sub2, text='Negrita', variable=self.var_subtitulo_bold, 
                       command=self._update_caratula_preview).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(sub2, text='Cursiva', variable=self.var_subtitulo_italic, 
                       command=self._update_caratula_preview).pack(side=tk.LEFT, padx=6)
        
        # Color de fondo
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color de Fondo:").pack(anchor=tk.W)
        frame_color = ttk.Frame(frame)
        frame_color.pack(fill=tk.X)
        
        self.entry_color_fondo = ttk.Entry(frame_color, width=10)
        self.entry_color_fondo.pack(side=tk.LEFT, pady=2)
        self.entry_color_fondo.bind('<FocusOut>', lambda e: self._update_caratula_preview())
        
        self.btn_color_fondo = tk.Button(frame_color, text="🎨", width=3, 
                                         command=self.elegir_color_fondo)
        self.btn_color_fondo.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_fondo = tk.Canvas(frame_color, width=34, height=20, 
                                            bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_fondo.create_rectangle(1, 1, 33, 19, fill="#000080", 
                                                  outline="#888888", tags=('preview',))
        self.preview_color_fondo.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Color de título
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color del Título:").pack(anchor=tk.W)
        frame_color = ttk.Frame(frame)
        frame_color.pack(fill=tk.X)
        
        self.entry_color_titulo = ttk.Entry(frame_color, width=10)
        self.entry_color_titulo.pack(side=tk.LEFT, pady=2)
        self.entry_color_titulo.bind('<FocusOut>', lambda e: self._update_caratula_preview())
        
        self.btn_color_titulo = tk.Button(frame_color, text="🎨", width=3, 
                                          command=self.elegir_color_titulo)
        self.btn_color_titulo.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_titulo = tk.Canvas(frame_color, width=34, height=20, 
                                             bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_titulo.create_rectangle(1, 1, 33, 19, fill="#FFFFFF", 
                                                   outline="#888888", tags=('preview',))
        self.preview_color_titulo.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Color del subtítulo
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color del Subtítulo:").pack(anchor=tk.W)
        frame_color_sub = ttk.Frame(frame)
        frame_color_sub.pack(fill=tk.X)
        
        self.entry_color_subtitulo = ttk.Entry(frame_color_sub, width=10)
        self.entry_color_subtitulo.pack(side=tk.LEFT, pady=2)
        self.entry_color_subtitulo.bind('<FocusOut>', lambda e: self._update_caratula_preview())
        
        self.btn_color_subtitulo = tk.Button(frame_color_sub, text="🎨", width=3, 
                                            command=self.elegir_color_subtitulo)
        self.btn_color_subtitulo.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_subtitulo = tk.Canvas(frame_color_sub, width=34, height=20, 
                                                bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_subtitulo.create_rectangle(1, 1, 33, 19, fill="#cccccc", 
                                                      outline="#888888", tags=('preview',))
        self.preview_color_subtitulo.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Duración
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Duración (segundos):").pack(anchor=tk.W)
        self.spinbox_duracion_caratula = ttk.Spinbox(frame, from_=1, to=10, increment=0.5, width=10)
        self.spinbox_duracion_caratula.pack(anchor=tk.W, pady=2)
        self.spinbox_duracion_caratula.set(3.0)
        
        # Cuadro de texto opcional
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
        
        # Posición del textbox
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
        
        # Colores del textbox
        frame_tb_colors = ttk.Frame(self.frame_textbox_controls)
        frame_tb_colors.pack(fill=tk.X, pady=4)
        
        ttk.Label(frame_tb_colors, text='Color Texto:').pack(anchor=tk.W)
        row = ttk.Frame(frame_tb_colors)
        row.pack(fill=tk.X)
        
        self.entry_textbox_text_color = ttk.Entry(row, width=10)
        self.entry_textbox_text_color.pack(side=tk.LEFT)
        self.entry_textbox_text_color.insert(0, "#000000")
        self.entry_textbox_text_color.bind('<FocusOut>', lambda e: self._update_caratula_preview())
        
        tk.Button(row, text='🎨', width=3, 
                 command=self.elegir_color_textbox_text_color).pack(side=tk.LEFT, padx=6)
        
        ttk.Label(frame_tb_colors, text='Color Fondo:').pack(anchor=tk.W, pady=(5,0))
        row2 = ttk.Frame(frame_tb_colors)
        row2.pack(fill=tk.X)
        
        self.entry_textbox_bg = ttk.Entry(row2, width=10)
        self.entry_textbox_bg.pack(side=tk.LEFT)
        self.entry_textbox_bg.insert(0, "#FFFFFF")
        self.entry_textbox_bg.bind('<FocusOut>', lambda e: self._update_caratula_preview())
        
        tk.Button(row2, text='🎨', width=3, 
                 command=self.elegir_color_textbox_bg).pack(side=tk.LEFT, padx=6)
        
        self._toggle_textbox_controls()
        
        # Botón guardar
        frame_bot_guardar = ttk.Frame(parent)
        frame_bot_guardar.pack(pady=20, fill=tk.X, padx=10)
        
        ttk.Button(frame_bot_guardar, text="💾 Guardar Cambios de Carátula",
                  command=self.on_editar_caratula).pack(side=tk.RIGHT, padx=6)
        
    def _update_caratula_preview(self):
        """Actualiza la vista previa de la carátula en tiempo real"""
        try:
            # Obtener dimensiones del canvas
            self.canvas_caratula_preview.update_idletasks()
            w = self.canvas_caratula_preview.winfo_width() or 560
            h = self.canvas_caratula_preview.winfo_height() or 420
            
            # Crear imagen base
            color_fondo = self.entry_color_fondo.get() or '#000080'
            if not color_fondo.startswith('#'):
                color_fondo = f'#{color_fondo}'
            
            img = Image.new('RGB', (w, h), color_fondo)
            draw = ImageDraw.Draw(img)
            
            # Dibujar título
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
            
            # Dibujar subtítulo
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
            
            # Dibujar cuadro de texto si está habilitado
            if self.var_textbox_enabled.get():
                tb_text = self.textbox_text.get('1.0', 'end').strip()
                if tb_text:
                    bg = self.entry_textbox_bg.get() or '#FFFFFF'
                    color = self.entry_textbox_text_color.get() or '#000000'
                    position = self.combo_textbox_position.get()
                    
                    # Dibujar rectángulo de fondo
                    rect_h = 100
                    margin = 20
                    
                    if position == 'top':
                        rect_y = margin
                    elif position == 'center':
                        rect_y = (h - rect_h)//2
                    else:  # bottom
                        rect_y = h - rect_h - margin
                    
                    draw.rectangle([margin, rect_y, w-margin, rect_y+rect_h], 
                                 fill=bg, outline='#888888', width=2)
                    
                    # Dibujar texto
                    try:
                        font_tb = ImageFont.truetype('arial.ttf', 16)
                    except:
                        font_tb = ImageFont.load_default()
                    
                    draw.text((margin+10, rect_y+10), tb_text, fill=color, font=font_tb)
            
            # Convertir y mostrar
            self._caratula_preview_tk = ImageTk.PhotoImage(img)
            self.canvas_caratula_preview.delete('all')
            self.canvas_caratula_preview.create_image(w//2, h//2, image=self._caratula_preview_tk)
            
        except Exception as e:
            print(f"Error al actualizar preview de carátula: {e}")
    
    def _toggle_textbox_controls(self):
        """Muestra u oculta los controles del cuadro de texto"""
        if self.var_textbox_enabled.get():
            self.frame_textbox_controls.pack(fill=tk.X, padx=10, pady=2)
        else:
            self.frame_textbox_controls.pack_forget()
    
    def _show_caratula_preview_window(self):
        """Muestra ventana con vista previa grande de la carátula"""
        try:
            W, H = 1280, 720
            
            color_fondo = self.entry_color_fondo.get() or '#000080'
            if not color_fondo.startswith('#'):
                color_fondo = f'#{color_fondo}'
            
            img = Image.new('RGB', (W, H), color_fondo)
            draw = ImageDraw.Draw(img)
            
            # Título
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
            
            # Subtítulo
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
            
            # Cuadro de texto
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
            
            # Crear ventana
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
            print(f"Error en vista previa grande: {e}")
    
    def crear_pestana_musica(self):
        """Crea la pestaña de gestión de música"""
        frame_musica = ttk.Frame(self.notebook)
        self.notebook.add(frame_musica, text="🎵 Música")
        
        ttk.Label(frame_musica, text="Música del Video", style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=10)
        
        self.frame_info_musica = ttk.Frame(frame_musica)
        self.frame_info_musica.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.label_musica_actual = ttk.Label(self.frame_info_musica, text="No hay música agregada")
        self.label_musica_actual.pack(anchor=tk.W, pady=5)
        
        # Botones
        frame_botones = ttk.Frame(frame_musica)
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(frame_botones, text="📁 Cargar desde Archivo", 
                  command=self.on_agregar_musica).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="🌐 Descargar de YouTube", 
                  command=self.on_descargar_youtube).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="🗑️ Eliminar Música", 
                  command=self.on_eliminar_musica).pack(side=tk.LEFT, padx=5)

    def crear_pestana_videos(self):
        """Crea la pestaña de gestión de videos"""
        frame_videos = ttk.Frame(self.notebook)
        self.notebook.add(frame_videos, text="🎬 Videos")

        ttk.Label(frame_videos, text="Videos del Proyecto", style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=10)

        # Lista de videos
        self.frame_lista_videos = ttk.Frame(frame_videos)
        self.frame_lista_videos.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        frame_lb = ttk.Frame(self.frame_lista_videos)
        frame_lb.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_lb)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_videos = tk.Listbox(frame_lb, yscrollcommand=scrollbar.set,
                                         font=('Arial', 10), selectmode=tk.SINGLE)
        self.listbox_videos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_videos.yview)

        # Botones
        frame_botones_v = ttk.Frame(frame_videos)
        frame_botones_v.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(frame_botones_v, text="📁 Cargar desde Archivo",
                  command=self.on_agregar_video).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_v, text="🗑️ Eliminar Video",
                  command=self.on_eliminar_video).pack(side=tk.LEFT, padx=5)
        
    def crear_pestana_configuracion(self):
        """Crea la pestaña de configuración del video"""
        frame_config = ttk.Frame(self.notebook)
        self.notebook.add(frame_config, text="⚙️ Configuración")
        
        # Resolución
        frame = ttk.Frame(frame_config)
        frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(frame, text="Resolución:").pack(anchor=tk.W)
        self.combo_resolucion = ttk.Combobox(frame, values=[
            "1920x1080 (Full HD)",
            "1280x720 (HD)",
            "3840x2160 (4K)",
            "640x480 (SD)"
        ], state='readonly')
        self.combo_resolucion.pack(fill=tk.X, pady=2)
        self.combo_resolucion.set("1920x1080 (Full HD)")
        
        # FPS
        frame = ttk.Frame(frame_config)
        frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(frame, text="Frames por Segundo (FPS):").pack(anchor=tk.W)
        self.combo_fps = ttk.Combobox(frame, values=["24", "25", "30", "50", "60"], state='readonly')
        self.combo_fps.pack(fill=tk.X, pady=2)
        self.combo_fps.set("30")
        
        # Directorio de salida
        frame = ttk.Frame(frame_config)
        frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(frame, text="Directorio de Salida:").pack(anchor=tk.W)
        frame_dir = ttk.Frame(frame)
        frame_dir.pack(fill=tk.X)
        self.entry_dir_salida = ttk.Entry(frame_dir)
        self.entry_dir_salida.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=2)
        ttk.Button(frame_dir, text="📂", width=3).pack(side=tk.LEFT, padx=5)
        
    def crear_barra_estado(self):
        """Crea la barra de estado"""
        self.barra_estado = ttk.Label(self.root, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)
        
    # Métodos callback
    
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

    def on_agregar_video(self):
        if self.callback_agregar_video:
            self.callback_agregar_video()

    def on_eliminar_video(self):
        sel = self.listbox_videos.curselection()
        if sel and self.callback_eliminar_video:
            self.callback_eliminar_video(sel[0])
    
    def on_eliminar_musica(self):
        if self.callback_eliminar_musica:
            self.callback_eliminar_musica()
    
    def on_editar_caratula(self):
        if self.callback_editar_caratula:
            self.callback_editar_caratula()
    
    def on_generar_video(self):
       if self.callback_vista_previa:
           self.callback_vista_previa()
    
    def on_descargar_youtube(self):
        from tkinter.simpledialog import askstring
        url = askstring("Descargar de YouTube", "Ingrese la URL del video de YouTube:")
        if url:
            if hasattr(self, 'callback_descargar_youtube') and self.callback_descargar_youtube:
                self.callback_descargar_youtube(url)
            else:
                self.mostrar_mensaje("Información", "Funcionalidad en desarrollo")
    
    # Métodos de utilidad
    
    def actualizar_lista_fotos(self, fotos):
        """Actualiza la lista de fotos en la interfaz"""
        self._fotos = fotos or []
        self.listbox_fotos.delete(0, tk.END)
        for i, foto in enumerate(self._fotos):
            nombre = foto.titulo if foto.titulo else os.path.basename(foto.ruta)
            self.listbox_fotos.insert(tk.END, f"{i+1}. {nombre} ({foto.duracion}s)")

    def actualizar_lista_videos(self, videos):
        """Actualiza la lista de videos en la interfaz"""
        try:
            self.listbox_videos.delete(0, tk.END)
            for i, v in enumerate(videos or []):
                if isinstance(v, str):
                    nombre = os.path.basename(v)
                else:
                    nombre = v.get('nombre', '') or os.path.basename(v.get('ruta', ''))
                self.listbox_videos.insert(tk.END, f"{i+1}. {nombre}")
        except Exception as e:
            print(f"Error actualizando lista de videos: {e}")
    
    def actualizar_info_musica(self, musica):
        """Actualiza la información de música"""
        if musica:
            texto = f"🎵 {musica.nombre}\n📁 {musica.ruta}"
            self.label_musica_actual.config(text=texto)
        else:
            self.label_musica_actual.config(text="No hay música agregada")
    
    def actualizar_caratula(self, caratula):
        """Actualiza los campos de la carátula"""
        self.entry_titulo_caratula.delete(0, tk.END)
        self.entry_titulo_caratula.insert(0, caratula.titulo)
        
        self.entry_subtitulo_caratula.delete(0, tk.END)
        self.entry_subtitulo_caratula.insert(0, caratula.subtitulo)
        
        self.entry_color_fondo.delete(0, tk.END)
        self.entry_color_fondo.insert(0, caratula.color_fondo)
        self._update_preview_color(caratula.color_fondo, self.preview_color_fondo)
        
        self.entry_color_titulo.delete(0, tk.END)
        self.entry_color_titulo.insert(0, caratula.color_titulo)
        self._update_preview_color(caratula.color_titulo, self.preview_color_titulo)
        
        self.entry_color_subtitulo.delete(0, tk.END)
        self.entry_color_subtitulo.insert(0, caratula.color_subtitulo)
        self._update_preview_color(caratula.color_subtitulo, self.preview_color_subtitulo)
        
        self.combo_titulo_family.set(caratula.fuente_titulo)
        self.spin_titulo_size.set(caratula.tamaño_titulo)
        self.var_titulo_bold.set(1 if caratula.titulo_bold else 0)
        self.var_titulo_italic.set(1 if caratula.titulo_italic else 0)
        
        self.combo_subtitulo_family.set(caratula.fuente_subtitulo)
        self.spin_subtitulo_size.set(caratula.tamaño_subtitulo)
        self.var_subtitulo_bold.set(1 if caratula.subtitulo_bold else 0)
        self.var_subtitulo_italic.set(1 if caratula.subtitulo_italic else 0)
        
        self.spinbox_duracion_caratula.set(caratula.duracion)
        
        # Textbox
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
    
    def _update_preview_color(self, color, canvas):
        """Actualiza el canvas de preview de color"""
        try:
            if not color.startswith('#'):
                color = f'#{color}'
            canvas.itemconfig('preview', fill=color)
        except:
            pass
    
    def elegir_color_fondo(self):
        """Selector de color para fondo"""
        color = colorchooser.askcolor(title="Elegir color de fondo", 
                                     initialcolor=self.entry_color_fondo.get() or '#000080')
        if color and color[1]:
            self.entry_color_fondo.delete(0, tk.END)
            self.entry_color_fondo.insert(0, color[1])
            self._update_preview_color(color[1], self.preview_color_fondo)
            self._update_caratula_preview()

    def elegir_color_titulo(self):
        """Selector de color para título"""
        color = colorchooser.askcolor(title="Elegir color del título", 
                                     initialcolor=self.entry_color_titulo.get() or '#FFFFFF')
        if color and color[1]:
            self.entry_color_titulo.delete(0, tk.END)
            self.entry_color_titulo.insert(0, color[1])
            self._update_preview_color(color[1], self.preview_color_titulo)
            self._update_caratula_preview()

    def elegir_color_subtitulo(self):
        """Selector de color para subtítulo"""
        color = colorchooser.askcolor(title="Elegir color del subtítulo", 
                                     initialcolor=self.entry_color_subtitulo.get() or '#CCCCCC')
        if color and color[1]:
            self.entry_color_subtitulo.delete(0, tk.END)
            self.entry_color_subtitulo.insert(0, color[1])
            self._update_preview_color(color[1], self.preview_color_subtitulo)
            self._update_caratula_preview()
    
    def elegir_color_textbox_text_color(self):
        """Selector de color para texto del textbox"""
        color = colorchooser.askcolor(title="Elegir color del texto", 
                                     initialcolor=self.entry_textbox_text_color.get() or '#000000')
        if color and color[1]:
            self.entry_textbox_text_color.delete(0, tk.END)
            self.entry_textbox_text_color.insert(0, color[1])
            self._update_caratula_preview()

    def elegir_color_textbox_bg(self):
        """Selector de color para fondo del textbox"""
        color = colorchooser.askcolor(title="Elegir color de fondo del cuadro", 
                                     initialcolor=self.entry_textbox_bg.get() or '#FFFFFF')
        if color and color[1]:
            self.entry_textbox_bg.delete(0, tk.END)
            self.entry_textbox_bg.insert(0, color[1])
            self._update_caratula_preview()
    
    def actualizar_estado(self, mensaje: str):
        """Actualiza el mensaje de la barra de estado"""
        self.barra_estado.config(text=mensaje)
        self.root.update_idletasks()
    
    def mostrar_mensaje(self, titulo: str, mensaje: str, tipo: str = "info"):
        """Muestra un mensaje al usuario"""
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
    
    def confirmar(self, titulo: str, mensaje: str) -> bool:
        """Muestra un diálogo de confirmación"""
        return messagebox.askyesno(titulo, mensaje)
    
    def mostrar_acerca_de(self):
        """Muestra el diálogo Acerca de"""
        mensaje = """Video Maker v1.0
        
Creador de Videos con Fotos y Música

Desarrollado por: José
Gerente Administrativo
Consejo Superior del Colegio de Médicos
Provincia de Buenos Aires

© 2026 - Todos los derechos reservados"""
        messagebox.showinfo("Acerca de Video Maker", mensaje)

    # --- Carátula Final: duplicado de carátula principal pero con sufijo _final ---
    def crear_pestana_caratula_final(self):
        """Crea la pestaña de configuración de la carátula final"""
        frame_caratula = ttk.Frame(self.notebook)
        self.notebook.add(frame_caratula, text="📋 Carátula Final")

        # Contenedor principal
        container = ttk.Frame(frame_caratula)
        container.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo - Controles con scroll
        left = ttk.Frame(container, width=500)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Panel derecho - Vista previa
        right = ttk.Frame(container, width=600)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        right.pack_propagate(False)

        # Scroll en panel izquierdo
        canvas = tk.Canvas(left)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Campos de carátula final (se reutilizan nombres con sufijo _final)
        self.crear_campos_caratula_final(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Vista previa en panel derecho
        ttk.Label(right, text="Vista Previa Carátula Final", 
                 style='Title.TLabel').pack(pady=5)
        
        self.canvas_caratula_final_preview = tk.Canvas(right, width=560, height=420, 
                                                bd=2, relief=tk.SUNKEN, bg='#ffffff')
        self.canvas_caratula_final_preview.pack(pady=10)
        
        # Botón para vista previa en ventana grande
        ttk.Button(right, text="🔍 Vista Previa Grande", 
                  command=self._show_caratula_final_preview_window).pack(pady=5)

    def crear_campos_caratula_final(self, parent):
        """Crea los campos de edición de la carátula final"""
        # Similar a crear_campos_caratula pero con sufijos _final
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Título (Final):").pack(anchor=tk.W)
        self.entry_titulo_caratula_final = ttk.Entry(frame, font=('Arial', 12))
        self.entry_titulo_caratula_final.pack(fill=tk.X, pady=2)
        self.entry_titulo_caratula_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())

        # Controles de fuente para título
        frame_font = ttk.Frame(parent)
        frame_font.pack(fill=tk.X, padx=10, pady=2)
        ttk.Label(frame_font, text="Estilo Título (Final):").pack(anchor=tk.W)
        
        sub = ttk.Frame(frame_font)
        sub.pack(fill=tk.X)
        
        self.combo_titulo_family_final = ttk.Combobox(sub, values=['Arial','Helvetica','Times New Roman',
                                                              'Courier New','Verdana'], 
                                               width=16, state='readonly')
        self.combo_titulo_family_final.pack(side=tk.LEFT)
        self.combo_titulo_family_final.set('Arial')
        self.combo_titulo_family_final.bind('<<ComboboxSelected>>', lambda e: self._update_caratula_final_preview())
        
        self.spin_titulo_size_final = ttk.Spinbox(sub, from_=8, to=72, width=5)
        self.spin_titulo_size_final.pack(side=tk.LEFT, padx=6)
        self.spin_titulo_size_final.set(48)
        self.spin_titulo_size_final.bind('<FocusOut>', lambda e: self._update_caratula_final_preview())
        
        self.var_titulo_bold_final = tk.IntVar()
        self.var_titulo_italic_final = tk.IntVar()
        
        ttk.Checkbutton(sub, text='Negrita', variable=self.var_titulo_bold_final, 
                       command=self._update_caratula_final_preview).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(sub, text='Cursiva', variable=self.var_titulo_italic_final, 
                       command=self._update_caratula_final_preview).pack(side=tk.LEFT, padx=6)

        # Subtítulo
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Subtítulo (Final):").pack(anchor=tk.W)
        self.entry_subtitulo_caratula_final = ttk.Entry(frame, font=('Arial', 10))
        self.entry_subtitulo_caratula_final.pack(fill=tk.X, pady=2)
        self.entry_subtitulo_caratula_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())

        # Controles de fuente para subtítulo
        frame_font_sub = ttk.Frame(parent)
        frame_font_sub.pack(fill=tk.X, padx=10, pady=2)
        ttk.Label(frame_font_sub, text="Estilo Subtítulo (Final):").pack(anchor=tk.W)
        
        sub2 = ttk.Frame(frame_font_sub)
        sub2.pack(fill=tk.X)
        
        self.combo_subtitulo_family_final = ttk.Combobox(sub2, values=['Arial','Helvetica','Times New Roman',
                                                                  'Courier New','Verdana'], 
                                                  width=16, state='readonly')
        self.combo_subtitulo_family_final.pack(side=tk.LEFT)
        self.combo_subtitulo_family_final.set('Arial')
        self.combo_subtitulo_family_final.bind('<<ComboboxSelected>>', lambda e: self._update_caratula_final_preview())
        
        self.spin_subtitulo_size_final = ttk.Spinbox(sub2, from_=8, to=72, width=5)
        self.spin_subtitulo_size_final.pack(side=tk.LEFT, padx=6)
        self.spin_subtitulo_size_final.set(24)
        self.spin_subtitulo_size_final.bind('<FocusOut>', lambda e: self._update_caratula_final_preview())
        
        self.var_subtitulo_bold_final = tk.IntVar()
        self.var_subtitulo_italic_final = tk.IntVar()
        
        ttk.Checkbutton(sub2, text='Negrita', variable=self.var_subtitulo_bold_final, 
                       command=self._update_caratula_final_preview).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(sub2, text='Cursiva', variable=self.var_subtitulo_italic_final, 
                       command=self._update_caratula_final_preview).pack(side=tk.LEFT, padx=6)

        # Color de fondo
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color de Fondo (Final):").pack(anchor=tk.W)
        frame_color = ttk.Frame(frame)
        frame_color.pack(fill=tk.X)
        
        self.entry_color_fondo_final = ttk.Entry(frame_color, width=10)
        self.entry_color_fondo_final.pack(side=tk.LEFT, pady=2)
        self.entry_color_fondo_final.bind('<FocusOut>', lambda e: self._update_caratula_final_preview())
        
        self.btn_color_fondo_final = tk.Button(frame_color, text="🎨", width=3, 
                                         command=self.elegir_color_fondo_final)
        self.btn_color_fondo_final.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_fondo_final = tk.Canvas(frame_color, width=34, height=20, 
                                            bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_fondo_final.create_rectangle(1, 1, 33, 19, fill="#000080", 
                                                  outline="#888888", tags=('preview',))
        self.preview_color_fondo_final.pack(side=tk.LEFT, padx=5, pady=2)

        # Color de título
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color del Título (Final):").pack(anchor=tk.W)
        frame_color = ttk.Frame(frame)
        frame_color.pack(fill=tk.X)
        
        self.entry_color_titulo_final = ttk.Entry(frame_color, width=10)
        self.entry_color_titulo_final.pack(side=tk.LEFT, pady=2)
        self.entry_color_titulo_final.bind('<FocusOut>', lambda e: self._update_caratula_final_preview())
        
        self.btn_color_titulo_final = tk.Button(frame_color, text="🎨", width=3, 
                                          command=self.elegir_color_titulo_final)
        self.btn_color_titulo_final.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_titulo_final = tk.Canvas(frame_color, width=34, height=20, 
                                             bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_titulo_final.create_rectangle(1, 1, 33, 19, fill="#FFFFFF", 
                                                   outline="#888888", tags=('preview',))
        self.preview_color_titulo_final.pack(side=tk.LEFT, padx=5, pady=2)

        # Color del subtítulo
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color del Subtítulo (Final):").pack(anchor=tk.W)
        frame_color_sub = ttk.Frame(frame)
        frame_color_sub.pack(fill=tk.X)
        
        self.entry_color_subtitulo_final = ttk.Entry(frame_color_sub, width=10)
        self.entry_color_subtitulo_final.pack(side=tk.LEFT, pady=2)
        self.entry_color_subtitulo_final.bind('<FocusOut>', lambda e: self._update_caratula_final_preview())
        
        self.btn_color_subtitulo_final = tk.Button(frame_color_sub, text="🎨", width=3, 
                                            command=self.elegir_color_subtitulo_final)
        self.btn_color_subtitulo_final.pack(side=tk.LEFT, padx=5)
        
        self.preview_color_subtitulo_final = tk.Canvas(frame_color_sub, width=34, height=20, 
                                                bd=0, highlightthickness=1, relief=tk.SUNKEN)
        self.preview_color_subtitulo_final.create_rectangle(1, 1, 33, 19, fill="#cccccc", 
                                                      outline="#888888", tags=('preview',))
        self.preview_color_subtitulo_final.pack(side=tk.LEFT, padx=5, pady=2)

        # Duración
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Duración (segundos) (Final):").pack(anchor=tk.W)
        self.spinbox_duracion_caratula_final = ttk.Spinbox(frame, from_=1, to=10, increment=0.5, width=10)
        self.spinbox_duracion_caratula_final.pack(anchor=tk.W, pady=2)
        self.spinbox_duracion_caratula_final.set(3.0)

        # Cuadro de texto opcional
        frame_tb_enable = ttk.Frame(parent)
        frame_tb_enable.pack(fill=tk.X, padx=10, pady=2)
        
        self.var_textbox_enabled_final = tk.IntVar()
        ttk.Checkbutton(frame_tb_enable, text='Habilitar cuadro de texto', 
                       variable=self.var_textbox_enabled_final, 
                       command=lambda: [self._toggle_textbox_controls_final(), 
                                      self._update_caratula_final_preview()]).pack(anchor=tk.W)
        
        self.frame_textbox_controls_final = ttk.Frame(parent)
        self.frame_textbox_controls_final.pack(fill=tk.X, padx=10, pady=2)
        
        ttk.Label(self.frame_textbox_controls_final, text='Texto:').pack(anchor=tk.W)
        self.textbox_text_final = tk.Text(self.frame_textbox_controls_final, height=3)
        self.textbox_text_final.pack(fill=tk.X, pady=2)
        self.textbox_text_final.bind('<KeyRelease>', lambda e: self._update_caratula_final_preview())
        
        # Posición del textbox
        frame_tb_pos = ttk.Frame(self.frame_textbox_controls_final)
        frame_tb_pos.pack(fill=tk.X, pady=2)
        
        ttk.Label(frame_tb_pos, text='Posición:').pack(side=tk.LEFT)
        self.combo_textbox_position_final = ttk.Combobox(frame_tb_pos, 
                                                   values=['top','center','bottom'], 
                                                   width=10, state='readonly')
        self.combo_textbox_position_final.pack(side=tk.LEFT, padx=6)
        self.combo_textbox_position_final.set('bottom')
        self.combo_textbox_position_final.bind('<<ComboboxSelected>>', 
                                         lambda e: self._update_caratula_final_preview())
        
        # Colores del textbox
        frame_tb_colors = ttk.Frame(self.frame_textbox_controls_final)
        frame_tb_colors.pack(fill=tk.X, pady=4)
        
        ttk.Label(frame_tb_colors, text='Color Texto:').pack(anchor=tk.W)
        row = ttk.Frame(frame_tb_colors)
        row.pack(fill=tk.X)
        
        self.entry_textbox_text_color_final = ttk.Entry(row, width=10)
        self.entry_textbox_text_color_final.pack(side=tk.LEFT)
        self.entry_textbox_text_color_final.insert(0, "#000000")
        self.entry_textbox_text_color_final.bind('<FocusOut>', lambda e: self._update_caratula_final_preview())
        
        tk.Button(row, text='🎨', width=3, 
                 command=self.elegir_color_textbox_text_color_final).pack(side=tk.LEFT, padx=6)
        
        ttk.Label(frame_tb_colors, text='Color Fondo:').pack(anchor=tk.W, pady=(5,0))
        row2 = ttk.Frame(frame_tb_colors)
        row2.pack(fill=tk.X)
        
        self.entry_textbox_bg_final = ttk.Entry(row2, width=10)
        self.entry_textbox_bg_final.pack(side=tk.LEFT)
        self.entry_textbox_bg_final.insert(0, "#FFFFFF")
        self.entry_textbox_bg_final.bind('<FocusOut>', lambda e: self._update_caratula_final_preview())
        
        tk.Button(row2, text='🎨', width=3, 
                 command=self.elegir_color_textbox_bg_final).pack(side=tk.LEFT, padx=6)
        
        self._toggle_textbox_controls_final()
        
        # Botón guardar
        frame_bot_guardar = ttk.Frame(parent)
        frame_bot_guardar.pack(pady=20, fill=tk.X, padx=10)
        
        ttk.Button(frame_bot_guardar, text="💾 Guardar Cambios de Carátula Final",
                  command=self.on_editar_caratula_final).pack(side=tk.RIGHT, padx=6)

    def _toggle_textbox_controls_final(self):
        if self.var_textbox_enabled_final.get():
            self.frame_textbox_controls_final.pack(fill=tk.X, padx=10, pady=2)
        else:
            self.frame_textbox_controls_final.pack_forget()

    def _update_caratula_final_preview(self):
        """Actualiza la vista previa de la carátula final en tiempo real"""
        try:
            self.canvas_caratula_final_preview.update_idletasks()
            w = self.canvas_caratula_final_preview.winfo_width() or 560
            h = self.canvas_caratula_final_preview.winfo_height() or 420
            
            color_fondo = self.entry_color_fondo_final.get() or '#000080'
            if not color_fondo.startswith('#'):
                color_fondo = f'#{color_fondo}'
            
            img = Image.new('RGB', (w, h), color_fondo)
            draw = ImageDraw.Draw(img)
            
            titulo = self.entry_titulo_caratula_final.get() or 'Mi Video'
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
            
            # Subtítulo
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
                draw.text(((w - w_s)//2, h//3 + h_t + 20), subtitulo, 
                         fill=color_subtitulo, font=font_s)
            
            # Textbox
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
                    draw.rectangle([margin, rect_y, w-margin, rect_y+rect_h], 
                                 fill=bg, outline='#888888', width=2)
                    try:
                        font_tb = ImageFont.truetype('arial.ttf', 16)
                    except:
                        font_tb = ImageFont.load_default()
                    draw.text((margin+10, rect_y+10), tb_text, fill=color, font=font_tb)
            
            self._caratula_final_preview_tk = ImageTk.PhotoImage(img)
            self.canvas_caratula_final_preview.delete('all')
            self.canvas_caratula_final_preview.create_image(w//2, h//2, image=self._caratula_final_preview_tk)
        except Exception as e:
            print(f"Error al actualizar preview de carátula final: {e}")

    def _show_caratula_final_preview_window(self):
        try:
            W, H = 1280, 720
            color_fondo = self.entry_color_fondo_final.get() or '#000080'
            if not color_fondo.startswith('#'):
                color_fondo = f'#{color_fondo}'
            img = Image.new('RGB', (W, H), color_fondo)
            draw = ImageDraw.Draw(img)
            
            titulo = self.entry_titulo_caratula_final.get() or 'Mi Video'
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
                draw.text(((W - w_s)//2, H//3 + h_t + 40), subtitulo, 
                         fill=color_subtitulo, font=font_s)

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
                    draw.rectangle([margin, rect_y, W-margin, rect_y+rect_h], 
                                 fill=bg, outline='#888888', width=3)
                    try:
                        font_tb = ImageFont.truetype('arial.ttf', 24)
                    except:
                        font_tb = ImageFont.load_default()
                    draw.text((margin+20, rect_y+20), tb_text, fill=color, font=font_tb)

            # Crear ventana
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
            print(f"Error en vista previa grande final: {e}")

    def elegir_color_fondo_final(self):
        color = colorchooser.askcolor(title="Elegir color de fondo (Final)", 
                                     initialcolor=self.entry_color_fondo_final.get() or '#000080')
        if color and color[1]:
            self.entry_color_fondo_final.delete(0, tk.END)
            self.entry_color_fondo_final.insert(0, color[1])
            try:
                if not color[1].startswith('#'):
                    c = f"#{color[1]}"
                else:
                    c = color[1]
                self.preview_color_fondo_final.itemconfig('preview', fill=c)
            except Exception:
                pass
            self._update_caratula_final_preview()

    def elegir_color_titulo_final(self):
        color = colorchooser.askcolor(title="Elegir color del título (Final)", 
                                     initialcolor=self.entry_color_titulo_final.get() or '#FFFFFF')
        if color and color[1]:
            self.entry_color_titulo_final.delete(0, tk.END)
            self.entry_color_titulo_final.insert(0, color[1])
            try:
                self.preview_color_titulo_final.itemconfig('preview', fill=color[1])
            except Exception:
                pass
            self._update_caratula_final_preview()

    def elegir_color_subtitulo_final(self):
        color = colorchooser.askcolor(title="Elegir color del subtítulo (Final)", 
                                     initialcolor=self.entry_color_subtitulo_final.get() or '#CCCCCC')
        if color and color[1]:
            self.entry_color_subtitulo_final.delete(0, tk.END)
            self.entry_color_subtitulo_final.insert(0, color[1])
            try:
                self.preview_color_subtitulo_final.itemconfig('preview', fill=color[1])
            except Exception:
                pass
            self._update_caratula_final_preview()

    def elegir_color_textbox_text_color_final(self):
        color = colorchooser.askcolor(title="Elegir color del texto (Final)", 
                                     initialcolor=self.entry_textbox_text_color_final.get() or '#000000')
        if color and color[1]:
            self.entry_textbox_text_color_final.delete(0, tk.END)
            self.entry_textbox_text_color_final.insert(0, color[1])
            self._update_caratula_final_preview()

    def elegir_color_textbox_bg_final(self):
        color = colorchooser.askcolor(title="Elegir color de fondo del cuadro (Final)", 
                                     initialcolor=self.entry_textbox_bg_final.get() or '#FFFFFF')
        if color and color[1]:
            self.entry_textbox_bg_final.delete(0, tk.END)
            self.entry_textbox_bg_final.insert(0, color[1])
            self._update_caratula_final_preview()

    def actualizar_caratula_final(self, caratula):
        """Actualiza los campos de la carátula final"""
        self.entry_titulo_caratula_final.delete(0, tk.END)
        self.entry_titulo_caratula_final.insert(0, caratula.titulo)
        
        self.entry_subtitulo_caratula_final.delete(0, tk.END)
        self.entry_subtitulo_caratula_final.insert(0, caratula.subtitulo)
        
        self.entry_color_fondo_final.delete(0, tk.END)
        self.entry_color_fondo_final.insert(0, caratula.color_fondo)
        try:
            self.preview_color_fondo_final.itemconfig('preview', fill=caratula.color_fondo)
        except Exception:
            pass
        
        self.entry_color_titulo_final.delete(0, tk.END)
        self.entry_color_titulo_final.insert(0, caratula.color_titulo)
        try:
            self.preview_color_titulo_final.itemconfig('preview', fill=caratula.color_titulo)
        except Exception:
            pass
        
        self.entry_color_subtitulo_final.delete(0, tk.END)
        self.entry_color_subtitulo_final.insert(0, caratula.color_subtitulo)
        try:
            self.preview_color_subtitulo_final.itemconfig('preview', fill=caratula.color_subtitulo)
        except Exception:
            pass
        
        self.combo_titulo_family_final.set(caratula.fuente_titulo)
        self.spin_titulo_size_final.set(caratula.tamaño_titulo)
        self.var_titulo_bold_final.set(1 if caratula.titulo_bold else 0)
        self.var_titulo_italic_final.set(1 if caratula.titulo_italic else 0)
        
        self.combo_subtitulo_family_final.set(caratula.fuente_subtitulo)
        self.spin_subtitulo_size_final.set(caratula.tamaño_subtitulo)
        self.var_subtitulo_bold_final.set(1 if caratula.subtitulo_bold else 0)
        self.var_subtitulo_italic_final.set(1 if caratula.subtitulo_italic else 0)
        
        self.spinbox_duracion_caratula_final.set(caratula.duracion)
        
        # Textbox
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

    def on_editar_caratula_final(self):
        if hasattr(self, 'callback_editar_caratula_final') and self.callback_editar_caratula_final:
            self.callback_editar_caratula_final()