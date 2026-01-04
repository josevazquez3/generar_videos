"""
Controlador principal de Video Maker
Coordina el modelo y la vista, contiene la lógica de negocio
"""

import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from modelo.modelo import ModeloVideoMaker, Foto, Musica
from vistas.vista_previa_video import VistaPreviewVideo
try:
    from yt_dlp import YoutubeDL
except Exception:
    YoutubeDL = None
from vistas.vista_principal import VistaPrincipal
from vistas.dialogo_editar_foto import DialogoEditarFoto
from validaciones.validaciones import Validaciones
from generador.generador_video import GeneradorVideo

class ControladorVideoMaker:
    """Controlador principal de la aplicación"""
    
    def __init__(self, modelo: ModeloVideoMaker, vista: VistaPrincipal):
        print('DEBUG: ControladorVideoMaker.__init__ - start')
        self.modelo = modelo
        self.vista = vista
        self.generador = GeneradorVideo()
        
        # Conectar callbacks de la vista
        self.conectar_callbacks()
        
        # Crear proyecto por defecto
        self.nuevo_proyecto()
        print('DEBUG: ControladorVideoMaker.__init__ - end')
        
    def conectar_callbacks(self):
        """Conecta los callbacks de la vista con los métodos del controlador"""
        self.vista.callback_nuevo_proyecto = self.nuevo_proyecto
        self.vista.callback_abrir_proyecto = self.abrir_proyecto
        self.vista.callback_guardar_proyecto = self.guardar_proyecto
        self.vista.callback_agregar_foto = self.agregar_foto
        self.vista.callback_eliminar_foto = self.eliminar_foto
        self.vista.callback_editar_foto = self.editar_foto
        self.vista.callback_mover_foto_arriba = self.mover_foto_arriba
        self.vista.callback_mover_foto_abajo = self.mover_foto_abajo
        self.vista.callback_agregar_musica = self.agregar_musica
        self.vista.callback_eliminar_musica = self.eliminar_musica
        # Callbacks para videos
        self.vista.callback_agregar_video = self.agregar_video
        self.vista.callback_eliminar_video = self.eliminar_video
        self.vista.callback_editar_caratula = self.editar_caratula
        self.vista.callback_editar_caratula_final = self.editar_caratula_final
        # callback para aplicar edición directa desde la vista (preview)
        self.vista.callback_aplicar_edicion_foto = self.aplicar_edicion_foto
        self.vista.callback_descargar_youtube = self.descargar_youtube
        # Callbacks para imágenes en la carátula
        self.vista.callback_agregar_imagen_caratula = self.agregar_imagen_caratula
        self.vista.callback_eliminar_imagen_caratula = self.eliminar_imagen_caratula
        self.vista.callback_actualizar_imagen_caratula = self.actualizar_imagen_caratula
        # Callback para vista previa del video
        self.vista.callback_vista_previa = self.mostrar_vista_previa
        
    def nuevo_proyecto(self):
        """Crea un nuevo proyecto"""
        # Confirmar si hay cambios sin guardar
        if self.modelo.proyecto_actual:
            respuesta = self.vista.confirmar(
                "Nuevo Proyecto",
                "¿Desea crear un nuevo proyecto? Los cambios no guardados se perderán."
            )
            if not respuesta:
                return
        
        # Crear nuevo proyecto
        self.modelo.nuevo_proyecto("Mi Video")
        self.actualizar_vista()
        self.vista.actualizar_estado("Nuevo proyecto creado")
        
    def abrir_proyecto(self):
        """Abre un proyecto existente"""
        ruta = filedialog.askopenfilename(
            title="Abrir Proyecto",
            initialdir=self.modelo.directorio_proyectos,
            filetypes=[("Proyectos Video Maker", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if ruta:
            if self.modelo.cargar_proyecto(ruta):
                self.actualizar_vista()
                self.vista.actualizar_estado(f"Proyecto cargado: {os.path.basename(ruta)}")
                self.vista.mostrar_mensaje("Éxito", "Proyecto cargado correctamente")
            else:
                self.vista.mostrar_mensaje("Error", "No se pudo cargar el proyecto", "error")
    
    def guardar_proyecto(self):
        """Guarda el proyecto actual"""
        if not self.modelo.proyecto_actual:
            self.vista.mostrar_mensaje("Error", "No hay proyecto para guardar", "error")
            return
        
        ruta = filedialog.asksaveasfilename(
            title="Guardar Proyecto",
            initialdir=self.modelo.directorio_proyectos,
            defaultextension=".json",
            filetypes=[("Proyectos Video Maker", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if ruta:
            # Antes de guardar, mover audios temporales (descargados) al folder del proyecto
            try:
                project_dir = os.path.dirname(ruta)
                media_dir = os.path.join(project_dir, 'media')
                os.makedirs(media_dir, exist_ok=True)

                musica = getattr(self.modelo.proyecto_actual, 'musica', None)
                if musica and musica.ruta:
                    src = musica.ruta
                    # Mover solo si el archivo existe y no está ya dentro del proyecto
                    if os.path.exists(src) and not os.path.abspath(src).startswith(os.path.abspath(project_dir)):
                        import shutil
                        dest = os.path.join(media_dir, os.path.basename(src))
                        # Si ya existe un archivo con ese nombre, añadir sufijo para evitar sobreescribir
                        base, ext = os.path.splitext(dest)
                        counter = 1
                        final_dest = dest
                        while os.path.exists(final_dest):
                            final_dest = f"{base}_{counter}{ext}"
                            counter += 1
                        shutil.move(src, final_dest)
                        # Actualizar ruta en el modelo
                        self.modelo.proyecto_actual.musica.ruta = final_dest

            except Exception:
                # No bloquear el guardado si el movimiento falla; informar estado
                try:
                    self.vista.actualizar_estado("Advertencia: no se pudo mover archivos multimedia al proyecto")
                except Exception:
                    pass

            if self.modelo.guardar_proyecto(ruta):
                self.vista.actualizar_estado(f"Proyecto guardado: {os.path.basename(ruta)}")
                self.vista.mostrar_mensaje("Éxito", "Proyecto guardado correctamente")
            else:
                self.vista.mostrar_mensaje("Error", "No se pudo guardar el proyecto", "error")
    
    def agregar_foto(self):
        """Agrega una nueva foto al proyecto"""
        rutas = filedialog.askopenfilenames(
            title="Seleccionar Fotos",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if rutas:
            fotos_agregadas = 0
            for ruta in rutas:
                # Validar imagen
                es_valido, mensaje = Validaciones.validar_imagen(ruta)
                if es_valido:
                    foto = Foto(ruta, os.path.basename(ruta))
                    self.modelo.proyecto_actual.agregar_foto(foto)
                    fotos_agregadas += 1
                else:
                    self.vista.mostrar_mensaje("Error", f"Imagen inválida:\n{ruta}\n{mensaje}", "warning")
            
            if fotos_agregadas > 0:
                self.actualizar_lista_fotos()
                self.vista.actualizar_estado(f"{fotos_agregadas} foto(s) agregada(s)")
    
    def eliminar_foto(self):
        """Elimina la foto seleccionada"""
        seleccion = self.vista.listbox_fotos.curselection()
        if not seleccion:
            self.vista.mostrar_mensaje("Advertencia", "Debe seleccionar una foto", "warning")
            return
        
        indice = seleccion[0]
        respuesta = self.vista.confirmar(
            "Eliminar Foto",
            "¿Está seguro de que desea eliminar esta foto?"
        )
        
        if respuesta:
            self.modelo.proyecto_actual.eliminar_foto(indice)
            self.actualizar_lista_fotos()
            self.vista.actualizar_estado("Foto eliminada")
    
    def editar_foto(self):
        """Edita las propiedades de la foto seleccionada"""
        seleccion = self.vista.listbox_fotos.curselection()
        if not seleccion:
            self.vista.mostrar_mensaje("Advertencia", "Debe seleccionar una foto", "warning")
            return
        
        indice = seleccion[0]
        foto = self.modelo.proyecto_actual.fotos[indice]
        
        # Mostrar diálogo de edición
        dialogo = DialogoEditarFoto(self.vista.root, foto)
        resultado = dialogo.mostrar()
        
        if resultado:
            # Aplicar cambios
            foto.titulo = resultado['titulo']
            foto.duracion = resultado['duracion']
            foto.efecto = resultado['efecto']
            foto.marco = resultado['marco']
            foto.color_marco = resultado['color_marco']
            foto.texto = resultado['texto']
            foto.color_texto = resultado['color_texto']
            foto.posicion_texto = resultado['posicion_texto']
            try:
                foto.tamaño_texto = int(resultado.get('tamaño_texto', 36))
            except Exception:
                foto.tamaño_texto = 36
            foto.brillo = resultado['brillo']
            foto.contraste = resultado['contraste']
            foto.rotacion = resultado['rotacion']
            
            # Refrescar lista y mantener selección para que la vista muestre la preview
            self.actualizar_lista_fotos()
            try:
                # re-seleccionar y forzar actualización del panel de propiedades
                self.vista.listbox_fotos.selection_set(indice)
                if hasattr(self.vista, '_on_select_foto'):
                    self.vista._on_select_foto()
            except Exception:
                pass
            self.vista.actualizar_estado("Foto actualizada")

    def aplicar_edicion_foto(self, indice: int, ruta_nueva: str):
        """Actualiza la foto en el modelo con la ruta de la imagen editada"""
        try:
            if not self.modelo.proyecto_actual:
                return
            if indice < 0 or indice >= len(self.modelo.proyecto_actual.fotos):
                return
            foto = self.modelo.proyecto_actual.fotos[indice]
            # Actualizar la ruta al archivo editado
            foto.ruta = ruta_nueva
            # Refrescar vista
            self.actualizar_lista_fotos()
            self.vista.actualizar_estado("Foto editada guardada")
        except Exception:
            pass
    
    def mover_foto_arriba(self):
        """Mueve la foto seleccionada una posición hacia arriba"""
        seleccion = self.vista.listbox_fotos.curselection()
        if not seleccion:
            self.vista.mostrar_mensaje("Advertencia", "Debe seleccionar una foto", "warning")
            return
        
        indice = seleccion[0]
        if indice > 0:
            self.modelo.proyecto_actual.mover_foto(indice, indice - 1)
            self.actualizar_lista_fotos()
            self.vista.listbox_fotos.selection_set(indice - 1)
            self.vista.actualizar_estado("Foto movida")
    
    def mover_foto_abajo(self):
        """Mueve la foto seleccionada una posición hacia abajo"""
        seleccion = self.vista.listbox_fotos.curselection()
        if not seleccion:
            self.vista.mostrar_mensaje("Advertencia", "Debe seleccionar una foto", "warning")
            return
        
        indice = seleccion[0]
        if indice < len(self.modelo.proyecto_actual.fotos) - 1:
            self.modelo.proyecto_actual.mover_foto(indice, indice + 1)
            self.actualizar_lista_fotos()
            self.vista.listbox_fotos.selection_set(indice + 1)
            self.vista.actualizar_estado("Foto movida")
    
    def agregar_musica(self):
        """Agrega música al proyecto"""
        ruta = filedialog.askopenfilename(
            title="Seleccionar Música",
            filetypes=[
                ("Audio", "*.mp3 *.wav *.ogg *.m4a"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if ruta:
            # Validar audio
            es_valido, mensaje = Validaciones.validar_audio(ruta)
            if es_valido:
                musica = Musica(ruta, os.path.basename(ruta), "local")
                self.modelo.proyecto_actual.musica = musica
                self.vista.actualizar_info_musica(musica)
                self.vista.actualizar_estado("Música agregada")
            else:
                self.vista.mostrar_mensaje("Error", f"Archivo de audio inválido:\n{mensaje}", "error")

    def agregar_video(self):
        """Agrega uno o varios videos al proyecto"""
        rutas = filedialog.askopenfilenames(
            title="Seleccionar Videos",
            filetypes=[
                ("Videos", "*.mp4 *.avi *.mov *.mkv *.flv"),
                ("Todos los archivos", "*.*")
            ]
        )

        if rutas:
            agregados = 0
            for ruta in rutas:
                existe, mensaje = Validaciones.validar_archivo_existe(ruta)
                if not existe:
                    self.vista.mostrar_mensaje("Error", f"Archivo inválido:\n{ruta}\n{mensaje}", "warning")
                    continue
                _, ext = os.path.splitext(ruta)
                if ext.lower() not in Validaciones.EXTENSIONES_VIDEO:
                    self.vista.mostrar_mensaje("Error", f"Formato de video no soportado: {ext}", "warning")
                    continue

                # Añadir al modelo
                nombre = os.path.basename(ruta)
                self.modelo.proyecto_actual.videos.append({'ruta': ruta, 'nombre': nombre})
                agregados += 1

            if agregados > 0:
                # Actualizar vista
                try:
                    self.vista.actualizar_lista_videos(self.modelo.proyecto_actual.videos)
                except Exception:
                    pass
                self.vista.actualizar_estado(f"{agregados} video(s) agregados")

    def eliminar_video(self, indice: int):
        """Elimina un video del proyecto por índice"""
        if not self.modelo.proyecto_actual.videos:
            self.vista.mostrar_mensaje("Advertencia", "No hay videos para eliminar", "warning")
            return

        if indice < 0 or indice >= len(self.modelo.proyecto_actual.videos):
            self.vista.mostrar_mensaje("Advertencia", "Índice de video inválido", "warning")
            return

        respuesta = self.vista.confirmar(
            "Eliminar Video",
            "¿Está seguro de que desea eliminar este video?"
        )

        if respuesta:
            try:
                self.modelo.proyecto_actual.videos.pop(indice)
                self.vista.actualizar_lista_videos(self.modelo.proyecto_actual.videos)
                self.vista.actualizar_estado("Video eliminado")
            except Exception:
                self.vista.mostrar_mensaje("Error", "No se pudo eliminar el video", "error")

    def descargar_youtube(self, url: str):
        """Descarga el audio de una URL de YouTube usando yt-dlp y lo añade al proyecto."""
        if not self.modelo.proyecto_actual:
            self.vista.mostrar_mensaje("Error", "No hay proyecto abierto", "error")
            return

        # Validar URL
        es_valido, mensaje = Validaciones.validar_url_youtube(url)
        if not es_valido:
            self.vista.mostrar_mensaje("Error", f"URL inválida: {mensaje}", "error")
            return

        if YoutubeDL is None:
            self.vista.mostrar_mensaje(
                "Error", 
                "La librería yt-dlp no está instalada.\n\n"
                "Instálala con:\npip install yt-dlp",
                "error"
            )
            return

        # Verificar si ffmpeg está disponible
        ffmpeg_path = shutil.which('ffmpeg')
        if not ffmpeg_path:
            self.vista.mostrar_mensaje(
                "Error", 
                "FFmpeg no está instalado o no está en el PATH del sistema.\n\n"
                "Instálalo usando:\n"
                "1. Chocolatey: choco install ffmpeg\n"
                "2. O descarga desde:\n   https://github.com/BtbN/FFmpeg-Builds/releases\n\n"
                "Después de instalar, reinicia la aplicación.",
                "error"
            )
            return

        try:
            self.vista.actualizar_estado("Descargando audio de YouTube...")
            self.vista.root.update_idletasks()
            
            outdir = self.modelo.directorio_temp
            os.makedirs(outdir, exist_ok=True)
            
            # Configuración de yt-dlp con ruta explícita de ffmpeg
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(outdir, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': False,
                'no_warnings': False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': os.path.dirname(ffmpeg_path),  # Especificar ubicación de ffmpeg
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'audio')
                
                # Buscar el archivo MP3 generado
                audio_exts = ['.mp3', '.m4a', '.webm', '.opus']
                candidates = []
                
                for f in os.listdir(outdir):
                    p = os.path.join(outdir, f)
                    if os.path.isfile(p):
                        _, ext = os.path.splitext(p)
                        if ext.lower() in audio_exts:
                            candidates.append(p)
                
                # Ordenar por fecha de modificación (más reciente primero)
                if candidates:
                    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
                    filename = candidates[0]
                else:
                    # Intentar con el nombre esperado
                    filename = os.path.join(outdir, f"{title}.mp3")
            
            if not os.path.exists(filename):
                self.vista.mostrar_mensaje(
                    "Error", 
                    "No se pudo encontrar el archivo descargado.\n"
                    "Verifica que FFmpeg esté correctamente instalado.",
                    "error"
                )
                self.vista.actualizar_estado("Error al descargar audio")
                return
            
            # Crear objeto Musica y agregarlo al proyecto
            musica = Musica(filename, os.path.basename(filename), "youtube")
            musica.url_youtube = url
            self.modelo.proyecto_actual.musica = musica
            
            self.vista.actualizar_info_musica(musica)
            self.vista.actualizar_estado("Música descargada exitosamente")
            self.vista.mostrar_mensaje(
                "Éxito", 
                f"Audio descargado correctamente:\n{os.path.basename(filename)}"
            )
            
        except Exception as e:
            error_msg = str(e)
            if "ffmpeg" in error_msg.lower() or "ffprobe" in error_msg.lower():
                self.vista.mostrar_mensaje(
                    "Error", 
                    "Error con FFmpeg:\n\n"
                    f"{error_msg}\n\n"
                    "Asegúrate de que FFmpeg esté correctamente instalado y en el PATH.\n\n"
                    "Instalación:\n"
                    "1. choco install ffmpeg\n"
                    "2. O descarga desde:\n   https://github.com/BtbN/FFmpeg-Builds/releases",
                    "error"
                )
            else:
                self.vista.mostrar_mensaje("Error", f"Error al descargar audio:\n{error_msg}", "error")
            
            self.vista.actualizar_estado("Error al descargar audio")
            import traceback
            traceback.print_exc()
    
    def eliminar_musica(self):
        """Elimina la música del proyecto"""
        if not self.modelo.proyecto_actual.musica:
            self.vista.mostrar_mensaje("Advertencia", "No hay música para eliminar", "warning")
            return
        
        respuesta = self.vista.confirmar(
            "Eliminar Música",
            "¿Está seguro de que desea eliminar la música?"
        )
        
        if respuesta:
            self.modelo.proyecto_actual.musica = None
            self.vista.actualizar_info_musica(None)
            self.vista.actualizar_estado("Música eliminada")
    
    def editar_caratula(self):
        """Edita las propiedades de la carátula"""
        caratula = self.modelo.proyecto_actual.caratula
        
        # Obtener datos del formulario
        caratula.titulo = self.vista.entry_titulo_caratula.get()
        caratula.subtitulo = self.vista.entry_subtitulo_caratula.get()
        caratula.color_fondo = self.vista.entry_color_fondo.get()
        caratula.color_titulo = self.vista.entry_color_titulo.get()
        
        # color subtitulo (si existe el campo en la vista)
        try:
            caratula.color_subtitulo = self.vista.entry_color_subtitulo.get()
        except Exception:
            pass
        
        # Fuentes y estilos
        try:
            caratula.fuente_titulo = self.vista.combo_titulo_family.get()
            caratula.tamaño_titulo = int(self.vista.spin_titulo_size.get())
            caratula.titulo_bold = bool(self.vista.var_titulo_bold.get())
            caratula.titulo_italic = bool(self.vista.var_titulo_italic.get())
            
            caratula.fuente_subtitulo = self.vista.combo_subtitulo_family.get()
            caratula.tamaño_subtitulo = int(self.vista.spin_subtitulo_size.get())
            caratula.subtitulo_bold = bool(self.vista.var_subtitulo_bold.get())
            caratula.subtitulo_italic = bool(self.vista.var_subtitulo_italic.get())
        except Exception:
            pass
        
        try:
            caratula.duracion = float(self.vista.spinbox_duracion_caratula.get())
        except ValueError:
            self.vista.mostrar_mensaje("Error", "Duración inválida", "error")
            return
        
        # Validar
        es_valido, mensaje = Validaciones.validar_texto(caratula.titulo, min_len=1)
        if not es_valido:
            self.vista.mostrar_mensaje("Error", f"Título inválido: {mensaje}", "error")
            return
        
        es_valido, mensaje = Validaciones.validar_color_hex(caratula.color_fondo)
        if not es_valido:
            self.vista.mostrar_mensaje("Error", f"Color de fondo inválido: {mensaje}", "error")
            return
        
        es_valido, mensaje = Validaciones.validar_color_hex(caratula.color_titulo)
        if not es_valido:
            self.vista.mostrar_mensaje("Error", f"Color de título inválido: {mensaje}", "error")
            return
        
        # validar color subtítulo
        try:
            es_valido, mensaje = Validaciones.validar_color_hex(caratula.color_subtitulo)
            if not es_valido:
                self.vista.mostrar_mensaje("Error", f"Color de subtítulo inválido: {mensaje}", "error")
                return
        except Exception:
            pass

        # Leer opciones del cuadro de texto de la carátula si existen en la vista
        try:
            caratula.textbox_enabled = bool(self.vista.var_textbox_enabled.get())
            caratula.textbox_text = self.vista.textbox_text.get('1.0', 'end').strip()
            caratula.textbox_text_color = self.vista.entry_textbox_text_color.get()
            caratula.textbox_bg = self.vista.entry_textbox_bg.get()
            try:
                caratula.textbox_border = int(self.vista.spin_textbox_border.get())
            except Exception:
                caratula.textbox_border = 1
            caratula.textbox_position = self.vista.combo_textbox_position.get()
            caratula.textbox_font = self.vista.combo_textbox_family.get()
            try:
                caratula.textbox_font_size = int(self.vista.spin_textbox_size.get())
            except Exception:
                caratula.textbox_font_size = 18
            caratula.textbox_font_bold = bool(getattr(self.vista, 'var_textbox_bold', tk.IntVar()).get())
            caratula.textbox_font_italic = bool(getattr(self.vista, 'var_textbox_italic', tk.IntVar()).get())

            # validar colores del textbox
            es_valido, mensaje = Validaciones.validar_color_hex(caratula.textbox_text_color)
            if not es_valido:
                self.vista.mostrar_mensaje("Error", f"Color de texto del cuadro inválido: {mensaje}", "error")
                return
            es_valido, mensaje = Validaciones.validar_color_hex(caratula.textbox_bg)
            if not es_valido:
                self.vista.mostrar_mensaje("Error", f"Color de fondo del cuadro inválido: {mensaje}", "error")
                return
        except Exception:
            # si la vista no tiene esos campos, simplemente ignorar
            pass
        
        self.vista.actualizar_estado("Carátula actualizada")
        self.vista.mostrar_mensaje("Éxito", "Carátula actualizada correctamente")

    def editar_caratula_final(self):
        """Edita las propiedades de la carátula final (desde la vista)"""
        caratula = getattr(self.modelo.proyecto_actual, 'caratula_final', None)
        if caratula is None:
            caratula = self.modelo.proyecto_actual.caratula

        # Obtener datos del formulario final
        caratula.titulo = self.vista.entry_titulo_caratula_final.get()
        caratula.subtitulo = self.vista.entry_subtitulo_caratula_final.get()
        caratula.color_fondo = self.vista.entry_color_fondo_final.get()
        caratula.color_titulo = self.vista.entry_color_titulo_final.get()
        # color subtitulo
        try:
            caratula.color_subtitulo = self.vista.entry_color_subtitulo_final.get()
        except Exception:
            pass

        # Fuentes y estilos
        try:
            caratula.fuente_titulo = self.vista.combo_titulo_family_final.get()
            caratula.tamaño_titulo = int(self.vista.spin_titulo_size_final.get())
            caratula.titulo_bold = bool(self.vista.var_titulo_bold_final.get())
            caratula.titulo_italic = bool(self.vista.var_titulo_italic_final.get())

            caratula.fuente_subtitulo = self.vista.combo_subtitulo_family_final.get()
            caratula.tamaño_subtitulo = int(self.vista.spin_subtitulo_size_final.get())
            caratula.subtitulo_bold = bool(self.vista.var_subtitulo_bold_final.get())
            caratula.subtitulo_italic = bool(self.vista.var_subtitulo_italic_final.get())
        except Exception:
            pass

        try:
            caratula.duracion = float(self.vista.spinbox_duracion_caratula_final.get())
        except Exception:
            caratula.duracion = 3.0

        # Textbox
        try:
            caratula.textbox_enabled = bool(self.vista.var_textbox_enabled_final.get())
            caratula.textbox_text = self.vista.textbox_text_final.get('1.0', 'end').strip()
            caratula.textbox_text_color = self.vista.entry_textbox_text_color_final.get()
            caratula.textbox_bg = self.vista.entry_textbox_bg_final.get()
            try:
                caratula.textbox_border = int(self.vista.spin_textbox_border.get())
            except Exception:
                caratula.textbox_border = 1
            caratula.textbox_position = self.vista.combo_textbox_position_final.get()
            caratula.textbox_font = getattr(self.vista, 'combo_textbox_family_final', caratula.textbox_font)
            try:
                caratula.textbox_font_size = int(getattr(self.vista, 'spin_textbox_size_final', tk.IntVar()).get())
            except Exception:
                caratula.textbox_font_size = caratula.textbox_font_size
            caratula.textbox_font_bold = bool(getattr(self.vista, 'var_textbox_bold_final', tk.IntVar()).get())
            caratula.textbox_font_italic = bool(getattr(self.vista, 'var_textbox_italic_final', tk.IntVar()).get())

            # validar colores del textbox
            # (validaciones sencillas omitidas aquí para simplicidad)
        except Exception:
            pass

        # Guardar en el modelo
        self.modelo.proyecto_actual.caratula_final = caratula

        self.vista.actualizar_estado("Carátula final actualizada")
        self.vista.mostrar_mensaje("Éxito", "Carátula final actualizada correctamente")

    # --- Métodos para manejar imágenes en la carátula desde la vista ---
    def agregar_imagen_caratula(self):
        """Abre diálogo para agregar una imagen a la carátula"""
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen para carátula",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp"), ("Todos", "*.*")]
        )
        if not ruta:
            return
        # agregar con valores por defecto
        item = {'ruta': ruta, 'position': 'center', 'scale': 100}
        self.modelo.proyecto_actual.caratula.imagenes_caratula.append(item)
        self.actualizar_vista()
        self.vista.actualizar_estado("Imagen agregada a la carátula")

    def eliminar_imagen_caratula(self, indice: int):
        try:
            self.modelo.proyecto_actual.caratula.imagenes_caratula.pop(indice)
            self.actualizar_vista()
            self.vista.actualizar_estado("Imagen eliminada de la carátula")
        except Exception:
            pass

    def actualizar_imagen_caratula(self, indice: int, position: str = None, scale: int = None):
        try:
            img = self.modelo.proyecto_actual.caratula.imagenes_caratula[indice]
            if position is not None:
                img['position'] = position
            if scale is not None:
                img['scale'] = int(scale)
            self.actualizar_vista()
            self.vista.actualizar_estado("Propiedades de la imagen actualizadas")
        except Exception:
            pass
    
    def mostrar_vista_previa(self):
        """Muestra la vista previa del video antes de generarlo"""
        if not self.modelo.proyecto_actual:
            self.vista.mostrar_mensaje("Error", "No hay proyecto abierto", "error")
            return
        
        if not self.modelo.proyecto_actual.fotos:
            self.vista.mostrar_mensaje("Error", "El proyecto no tiene fotos", "error")
            return
        
        try:
            # Mostrar ventana de vista previa
            self.vista.actualizar_estado("Generando vista previa...")
            preview = VistaPreviewVideo(self.vista.root, self.modelo.proyecto_actual)
            preview.mostrar()
            
            # Si el usuario confirma, generar el video
            self.generar_video()
            
        except Exception as e:
            self.vista.mostrar_mensaje("Error", f"Error en vista previa: {str(e)}", "error")
            import traceback
            traceback.print_exc()
    
    def generar_video(self):
        """Genera el video final"""
        # Validar proyecto
        es_valido, mensaje = Validaciones.validar_proyecto(self.modelo.proyecto_actual)
        if not es_valido:
            self.vista.mostrar_mensaje("Error", f"Proyecto inválido:\n{mensaje}", "error")
            return
        
        # Solicitar nombre de archivo de salida
        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar Video",
            initialdir=self.modelo.directorio_salida,
            defaultextension=".mp4",
            filetypes=[("Video MP4", "*.mp4"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta_salida:
            return
        
        # Obtener configuración
        resolucion = self.vista.combo_resolucion.get().split(' ')[0]
        fps = int(self.vista.combo_fps.get())
        
        try:
            self.vista.actualizar_estado("Generando video... Por favor espere...")
            self.vista.root.update_idletasks()
            
            # Generar video
            exito = self.generador.generar_video(
                proyecto=self.modelo.proyecto_actual,
                ruta_salida=ruta_salida,
                resolucion=resolucion,
                fps=fps,
                callback_progreso=self.actualizar_progreso
            )
            
            if exito:
                self.vista.actualizar_estado("Video generado exitosamente")
                respuesta = self.vista.confirmar(
                    "Video Generado",
                    f"El video se generó correctamente en:\n{ruta_salida}\n\n¿Desea abrir la carpeta?"
                )
                if respuesta:
                    import subprocess
                    import platform
                    if platform.system() == 'Windows':
                        subprocess.run(['explorer', os.path.dirname(ruta_salida)])
                    elif platform.system() == 'Darwin':  # macOS
                        subprocess.run(['open', os.path.dirname(ruta_salida)])
                    else:  # Linux
                        subprocess.run(['xdg-open', os.path.dirname(ruta_salida)])
            else:
                self.vista.actualizar_estado("Error al generar video")
                self.vista.mostrar_mensaje("Error", "Hubo un error al generar el video", "error")
                
        except Exception as e:
            self.vista.actualizar_estado(f"Error: {str(e)}")
            self.vista.mostrar_mensaje("Error", f"Error al generar video:\n{str(e)}", "error")
    
    def actualizar_progreso(self, mensaje: str, porcentaje: float):
        """Callback para actualizar el progreso de generación"""
        self.vista.actualizar_estado(f"{mensaje} ({porcentaje:.0f}%)")
        self.vista.root.update_idletasks()
    
    def actualizar_vista(self):
        """Actualiza toda la vista con los datos del proyecto actual"""
        if self.modelo.proyecto_actual:
            self.actualizar_lista_fotos()
            self.vista.actualizar_info_musica(self.modelo.proyecto_actual.musica)
            self.vista.actualizar_caratula(self.modelo.proyecto_actual.caratula)
            # actualizar carátula final
            try:
                self.vista.actualizar_caratula_final(getattr(self.modelo.proyecto_actual, 'caratula_final', None) or self.modelo.proyecto_actual.caratula)
            except Exception:
                pass
            # actualizar lista de imagenes en la vista
            try:
                self.vista.actualizar_imagenes_list(self.modelo.proyecto_actual.caratula.imagenes_caratula)
            except Exception:
                pass
    
    def actualizar_lista_fotos(self):
        """Actualiza la lista de fotos en la vista"""
        if not self.modelo.proyecto_actual:
            # No hay proyecto, limpiar lista
            try:
                self.vista.actualizar_lista_fotos([])
            except Exception:
                pass
            return

        fotos = self.modelo.proyecto_actual.fotos
        # Actualizar listbox en la vista
        self.vista.actualizar_lista_fotos(fotos)

        # Mantener selección si es posible
        try:
            if fotos:
                # Seleccionar la primera foto por defecto
                self.vista.listbox_fotos.selection_clear(0, 'end')
                self.vista.listbox_fotos.selection_set(0)
        except Exception:
            pass