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
        
        # Duración
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Duración (segundos):").pack(anchor=tk.W)
        self.spinbox_duracion = ttk.Spinbox(frame, from_=0.5, to=60, increment=0.5, width=10)
        self.spinbox_duracion.pack(anchor=tk.W, pady=2)
        self.spinbox_duracion.set(3.0)
        
        # Efecto de transición
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="Efecto de Transición:").pack(anchor=tk.W)
        self.combo_efecto = ttk.Combobox(frame, values=[
            "fade - Fundido",
            "slide_left - Deslizar desde izquierda",
            "slide_right - Deslizar desde derecha",
            "slide_up - Deslizar desde arriba",
            "slide_down - Deslizar desde abajo",
            "zoom - Zoom",
            "zigzag - Zig-zag"
        ], state='readonly')
        self.combo_efecto.pack(fill=tk.X, pady=2)
        self.combo_efecto.set("fade - Fundido")
        
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
        
        self.spinbox_duracion.set(foto.duracion)
        
        # Efecto
        efectos_map = {
            "fade": "fade - Fundido",
            "slide_left": "slide_left - Deslizar desde izquierda",
            "slide_right": "slide_right - Deslizar desde derecha",
            "slide_up": "slide_up - Deslizar desde arriba",
            "slide_down": "slide_down - Deslizar desde abajo",
            "zoom": "zoom - Zoom",
            "zigzag": "zigzag - Zig-zag"
        }
        self.combo_efecto.set(efectos_map.get(foto.efecto, "fade - Fundido"))
        
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
            'duracion': float(self.spinbox_duracion.get()),
            'efecto': self.combo_efecto.get().split(' - ')[0],
            'marco': self.combo_marco.get().split(' - ')[0] if self.combo_marco.get().split(' - ')[0] != 'ninguno' else None,
            'color_marco': self.entry_color_marco.get(),
            'texto': self.entry_texto.get(),
            'color_texto': self.entry_color_texto.get(),
            'posicion_texto': self.combo_posicion_texto.get().split(' - ')[0]
        }
        self.ventana.destroy()
    
    def cancelar(self):
        """Cancela y cierra el diálogo"""
        self.resultado = None
        self.ventana.destroy()
    
    def mostrar(self):
        """Muestra el diálogo y retorna el resultado"""
        self.ventana.wait_window()
        return self.resultado