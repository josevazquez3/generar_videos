import traceback
import tkinter as tk
import time

print('TEST: inicio')
try:
    from modelo.modelo import ModeloVideoMaker
    from vistas.vista_principal import VistaPrincipal
    from controlador.controlador import ControladorVideoMaker

    print('TEST: instanciando ModeloVideoMaker')
    modelo = ModeloVideoMaker()
    print('TEST: modelo creado')

    print('TEST: creando root')
    root = tk.Tk()
    print('TEST: root creado')

    print('TEST: instanciando VistaPrincipal')
    vista = VistaPrincipal(root)
    print('TEST: vista creada')

    print('TEST: instanciando ControladorVideoMaker')
    controlador = ControladorVideoMaker(modelo, vista)
    print('TEST: controlador creado')

    # Cerrar la ventana automáticamente después de 3 segundos
    root.after(3000, root.destroy)
    print('TEST: entrando en mainloop (3s)')
    root.mainloop()
    print('TEST: mainloop finalizado')

except Exception as e:
    print('TEST: Excepción detectada:', e)
    traceback.print_exc()

print('TEST: fin')
