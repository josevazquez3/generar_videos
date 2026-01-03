"""Video Maker Application
Aplicación para crear videos con fotos y música
Autor: José - Gerente Administrativo
"""

import tkinter as tk
from vistas.vista_principal import VistaPrincipal
from modelo.modelo import ModeloVideoMaker
from controlador.controlador import ControladorVideoMaker


def main():
    """Función principal que inicia la aplicación"""
    print('DEBUG: Iniciando aplicación - creando root')
    root = tk.Tk()

    # Crear modelo
    modelo = ModeloVideoMaker()

    # Crear vista
    vista = VistaPrincipal(root)

    # Crear controlador
    controlador = ControladorVideoMaker(modelo, vista)

    # Iniciar aplicación
    print('DEBUG: Iniciando mainloop')
    root.mainloop()


if __name__ == "__main__":
    main()