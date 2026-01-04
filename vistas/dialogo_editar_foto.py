"""
Vista de diálogo para editar propiedades de fotos
"""

import tkinter as tk
from tkinter import ttk, colorchooser
from typing import Optional

class DialogoEditarFoto:
    """Diálogo para editar una foto"""
    
    def __init__(self, parent, foto=None):
        self.resultado = None
        self.foto = foto
        
        # Crear ventana de diálogo
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Editar Foto")
        self.ventana.geometry("500x600")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.crear_interfaz()
        
        if foto:
            self.cargar_datos(foto)
        
        # Centrar ventana
        self.centrar_ventana()
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        width = self.ventana.winfo_width()
        height = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (height // 2)
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')
        
    def crear_interfaz(self):
        """Crea la interfaz del diálogo"""
        # Frame principal con scroll
        canvas = tk.Canvas(self.ventana)
        scrollbar = ttk.Scrollbar(self.ventana, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Título de la Foto:").pack(anchor=tk.W)
        self.entry_titulo = ttk.Entry(frame, font=('Arial', 10))
        self.entry_titulo.pack(fill=tk.X, pady=2)
        
        # Duración (en minutos)
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Duración (minutos):").pack(anchor=tk.W)
        # Rango en minutos: 0.1 (6s) hasta 60 minutos, incremento 0.1
        self.spinbox_duracion = ttk.Spinbox(frame, from_=0.1, to=60, increment=0.1, width=10)
        self.spinbox_duracion.pack(anchor=tk.W, pady=2)
        # Valor por defecto 0.5 minutos (30 segundos)
        self.spinbox_duracion.set(0.5)
        
        # Efecto de transición
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Efecto de Transición:").pack(anchor=tk.W)
        self.combo_efecto = ttk.Combobox(frame, values=[
            "ninguno - Sin efecto",
            "fade - Fundido",
            "slide_left - Deslizar desde izquierda",
            "slide_right - Deslizar desde derecha",
            "slide_up - Deslizar desde arriba",
            "slide_down - Deslizar desde abajo",
            "zoom - Zoom",
            "zigzag - Zig-zag"
        ], state='readonly')
        self.combo_efecto.pack(fill=tk.X, pady=2)
        self.combo_efecto.set("ninguno - Sin efecto")
        
        # Tipo de marco
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Tipo de Marco:").pack(anchor=tk.W)
        self.combo_marco = ttk.Combobox(frame, values=[
            "ninguno - Sin marco",
            "simple - Marco simple",
            "doble - Marco doble",
            "sombra - Con sombra",
            "relieve - Con relieve"
        ], state='readonly')
        self.combo_marco.pack(fill=tk.X, pady=2)
        self.combo_marco.set("ninguno - Sin marco")
        
        # Color del marco
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color del Marco:").pack(anchor=tk.W)
        frame_color = ttk.Frame(frame)
        frame_color.pack(fill=tk.X)
        self.entry_color_marco = ttk.Entry(frame_color, width=10)
        self.entry_color_marco.pack(side=tk.LEFT, pady=2)
        self.entry_color_marco.insert(0, "#FFFFFF")
        self.btn_color_marco = tk.Button(frame_color, text="🎨", width=3,
                                         command=self.elegir_color_marco)
        self.btn_color_marco.pack(side=tk.LEFT, padx=5)
        
        # Texto sobre la foto
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Texto sobre la Foto:").pack(anchor=tk.W)
        self.entry_texto = ttk.Entry(frame, font=('Arial', 10))
        self.entry_texto.pack(fill=tk.X, pady=2)

        # Opciones de estilo: negrita y subrayado
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=2)
        self.var_texto_bold = tk.IntVar()
        self.var_texto_underline = tk.IntVar()
        chk_bold = ttk.Checkbutton(frame, text="Negrita", variable=self.var_texto_bold)
        chk_bold.pack(side=tk.LEFT, padx=(0, 8))
        chk_underline = ttk.Checkbutton(frame, text="Subrayado", variable=self.var_texto_underline)
        chk_underline.pack(side=tk.LEFT)
        
        # Color del texto
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Color del Texto:").pack(anchor=tk.W)
        frame_color = ttk.Frame(frame)
        frame_color.pack(fill=tk.X)
        self.entry_color_texto = ttk.Entry(frame_color, width=10)
        self.entry_color_texto.pack(side=tk.LEFT, pady=2)
        self.entry_color_texto.insert(0, "#000000")
        self.btn_color_texto = tk.Button(frame_color, text="🎨", width=3,
                                        command=self.elegir_color_texto)
        self.btn_color_texto.pack(side=tk.LEFT, padx=5)
        
        # Posición del texto
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Posición del Texto:").pack(anchor=tk.W)
        self.combo_posicion_texto = ttk.Combobox(frame, values=[
            "top - Arriba",
            "center - Centro",
            "bottom - Abajo"
        ], state='readonly')
        self.combo_posicion_texto.pack(fill=tk.X, pady=2)
        self.combo_posicion_texto.set("bottom - Abajo")

        # Tamaño del texto
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Tamaño del Texto:").pack(anchor=tk.W)
        self.spin_texto_size = ttk.Spinbox(frame, from_=8, to=200, increment=1, width=10)
        self.spin_texto_size.pack(anchor=tk.W, pady=2)
        self.spin_texto_size.set(36)

        # Brillo
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Brillo (0.0 - 2.0):").pack(anchor=tk.W)
        self.spin_brillo = ttk.Spinbox(frame, from_=0.0, to=2.0, increment=0.1, width=10)
        self.spin_brillo.pack(anchor=tk.W, pady=2)
        self.spin_brillo.set(1.0)

        # Contraste
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Contraste (0.0 - 2.0):").pack(anchor=tk.W)
        self.spin_contraste = ttk.Spinbox(frame, from_=0.0, to=2.0, increment=0.1, width=10)
        self.spin_contraste.pack(anchor=tk.W, pady=2)
        self.spin_contraste.set(1.0)

        # Rotación
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Rotación (grados):").pack(anchor=tk.W)
        self.combo_rotacion = ttk.Combobox(frame, values=["0 - Ninguna", "90", "180", "270"], state='readonly')
        self.combo_rotacion.pack(fill=tk.X, pady=2)
        self.combo_rotacion.set("0 - Ninguna")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones
        frame_botones = ttk.Frame(self.ventana)
        frame_botones.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        ttk.Button(frame_botones, text="✓ Aceptar", command=self.aceptar).pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame_botones, text="✗ Cancelar", command=self.cancelar).pack(side=tk.RIGHT, padx=5)
        
    def cargar_datos(self, foto):
        """Carga los datos de una foto en el formulario"""
        self.entry_titulo.delete(0, tk.END)
        self.entry_titulo.insert(0, foto.titulo)
        
        # El modelo guarda la duración en segundos; para mostrarla aquí convertimos a minutos
        try:
            minutos = float(foto.duracion) / 60.0
        except Exception:
            minutos = 0.5
        self.spinbox_duracion.set(minutos)
        
        # Efecto
        efectos_map = {
            None: "ninguno - Sin efecto",
            "fade": "fade - Fundido",
            "slide_left": "slide_left - Deslizar desde izquierda",
            "slide_right": "slide_right - Deslizar desde derecha",
            "slide_up": "slide_up - Deslizar desde arriba",
            "slide_down": "slide_down - Deslizar desde abajo",
            "zoom": "zoom - Zoom",
            "zigzag": "zigzag - Zig-zag"
        }
        self.combo_efecto.set(efectos_map.get(foto.efecto, "ninguno - Sin efecto"))
        
        # Marco
        marcos_map = {
            None: "ninguno - Sin marco",
            "simple": "simple - Marco simple",
            "doble": "doble - Marco doble",
            "sombra": "sombra - Con sombra",
            "relieve": "relieve - Con relieve"
        }
        self.combo_marco.set(marcos_map.get(foto.marco, "ninguno - Sin marco"))
        
        self.entry_color_marco.delete(0, tk.END)
        self.entry_color_marco.insert(0, foto.color_marco)
        
        self.entry_texto.delete(0, tk.END)
        self.entry_texto.insert(0, foto.texto)
        
        self.entry_color_texto.delete(0, tk.END)
        self.entry_color_texto.insert(0, foto.color_texto)
        
        posiciones_map = {
            "top": "top - Arriba",
            "center": "center - Centro",
            "bottom": "bottom - Abajo"
        }
        self.combo_posicion_texto.set(posiciones_map.get(foto.posicion_texto, "bottom - Abajo"))

        try:
            self.spin_texto_size.set(foto.tamaño_texto)
        except Exception:
            self.spin_texto_size.set(36)
        
        # Valores de edición: brillo, contraste, rotación
        try:
            self.spin_brillo.set(foto.brillo)
        except Exception:
            self.spin_brillo.set(1.0)

        try:
            self.spin_contraste.set(foto.contraste)
        except Exception:
            self.spin_contraste.set(1.0)

        try:
            if foto.rotacion == 0:
                self.combo_rotacion.set("0 - Ninguna")
            else:
                self.combo_rotacion.set(str(foto.rotacion))
        except Exception:
            self.combo_rotacion.set("0 - Ninguna")
        
    def elegir_color_marco(self):
        """Abre el selector de color para el marco"""
        color = colorchooser.askcolor(title="Elegir Color del Marco")
        if color[1]:
            self.entry_color_marco.delete(0, tk.END)
            self.entry_color_marco.insert(0, color[1])
    
    def elegir_color_texto(self):
        """Abre el selector de color para el texto"""
        color = colorchooser.askcolor(title="Elegir Color del Texto")
        if color[1]:
            self.entry_color_texto.delete(0, tk.END)
            self.entry_color_texto.insert(0, color[1])
    
    def aceptar(self):
        """Guarda los cambios y cierra el diálogo"""
        # Crear diccionario con los datos
        self.resultado = {
            'titulo': self.entry_titulo.get(),
            # Convertir minutos a segundos para almacenar en el modelo
            'duracion': float(self.spinbox_duracion.get()) * 60.0,
            # Guardar efecto como `None` si se selecciona 'ninguno'
            'efecto': (None if self.combo_efecto.get().split(' - ')[0] == 'ninguno' else self.combo_efecto.get().split(' - ')[0]),
            'marco': self.combo_marco.get().split(' - ')[0] if self.combo_marco.get().split(' - ')[0] != 'ninguno' else None,
            'color_marco': self.entry_color_marco.get(),
            'texto': self.entry_texto.get(),
            'color_texto': self.entry_color_texto.get(),
            'posicion_texto': self.combo_posicion_texto.get().split(' - ')[0]
        }
        try:
            self.resultado['tamaño_texto'] = int(self.spin_texto_size.get())
        except Exception:
            self.resultado['tamaño_texto'] = 36
        # Añadir parámetros de edición: brillo, contraste, rotación
        try:
            self.resultado['brillo'] = float(self.spin_brillo.get())
        except Exception:
            self.resultado['brillo'] = 1.0

        try:
            self.resultado['contraste'] = float(self.spin_contraste.get())
        except Exception:
            self.resultado['contraste'] = 1.0

        try:
            rot_text = self.combo_rotacion.get()
            if ' - ' in rot_text:
                rot_val = int(rot_text.split(' - ')[0])
            else:
                rot_val = int(rot_text)
            self.resultado['rotacion'] = rot_val
        except Exception:
            self.resultado['rotacion'] = 0
        self.ventana.destroy()
    
    def cancelar(self):
        """Cancela y cierra el diálogo"""
        self.resultado = None
        self.ventana.destroy()
    
    def mostrar(self):
        """Muestra el diálogo y retorna el resultado"""
        self.ventana.wait_window()
        return self.resultado