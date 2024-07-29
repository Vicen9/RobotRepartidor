import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import conexion2 as cn
import time
import pedidos as pd
import mensajeInterfaz as mi

# Clase que crea una ventana secundaria con la matriz de botones
class MatrixWindow:

    # Constructor de la clase MatrixWindow
    def __init__(self, master, matriz, queue_callback):
        """master: Ventana principal del Tkinter, Toplevel: crea una nueva ventana"""
        self.master = tk.Toplevel(master)
        self.master.title("Creación de pedido")
        """matriz: matriz de valores para los botones"""
        self.matriz = matriz
        """queue_call: manejar eventos de click en los botones"""
        self.queue_callback = queue_callback
        """click_positions: almacena las posiciones de los botones que han sido clicados"""
        self.click_positions = []
        """Cargar imagenes"""
        self.load_images()
        """Muestra botones dentro de la ventana emergente"""
        self.display_buttons()
        """Bloquea la ventana principal y solo funciona la ventana emergente"""
        self.master.grab_set()

    # Carga imagenes desde el directorio imagenes y las ajusta al tamaño deseado. 
    # Si una imagen no se encuentra, muestra un mensaje de error y coloca una casilla gris
    def load_images(self):
        """self.imagenes: diccionario vacio donde se alamacenarán las imagenes"""
        self.images = {}
        desired_size = (50, 50)
        for i in range(12):
            image_number = f"{i:02}"
            try:
                """Abre la imagen desde el directorio usando el nombre formateado"""
                image = Image.open(f"images/{image_number}.png")
                """Redimensiona la imagen al tamaño deseado usando el método LANCZOS, 
                que es adecuado para iamgenes que se reducen de tamaño"""
                image = image.resize(desired_size, Image.Resampling.LANCZOS)
                """Convierte la imagen redimensionada a un objeto PhotoImage que es el formato requerido
                por TKinter para mostrar imágenes y se guarda en el diccionario,
                usando como clave el numero de imagen"""
                self.images[image_number] = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                print(f"Error: No se encontró la imagen para {image_number}")
        self.images['default'] = ImageTk.PhotoImage(Image.new('RGB', desired_size, color='grey'))

    # Crea botones en la ventana secuandaria usando las imagenes cargadas. 
    #Los botones tienen asignados comandos que llaman a 'record_click()'
    def display_buttons(self):
        for i in range(7):
            for j in range(5):
                image_value = self.matriz[i][j]
                """Busca en el diccionario de imágenes una imagen que corresponda si no la encuientra carga la imagen por defecto"""
                image = self.images.get(image_value, self.images['default'])
                """Creacion de Botones o etiquetas"""
                if(image_value == '01'):
                    if(j-1 < 0 or j+1 >4):
                        """Se asignan comandos mediante el uso de lambda que capturan las coordenadas i y j y
                          llaman a record_click cuando se ahce click en el boton"""
                        btn = tk.Button(self.master, image=image, compound=tk.CENTER, command=lambda i=i, j=j: self.record_click(i, j), bg='#515e5d')
                    else:
                        if((self.matriz[i][j-1] != '05' and self.matriz[i][j-1] != '06' and self.matriz[i][j-1] != '10' and self.matriz[i][j-1] != '00') and (self.matriz[i][j+1] != '03' and self.matriz[i][j+1] != '04' and self.matriz[i][j+1] != '08' and self.matriz[i][j+1] != '00') ):
                            btn = tk.Label(self.master, image=image, compound=tk.CENTER)
                        else:
                            btn = tk.Button(self.master, image=image, compound=tk.CENTER, command=lambda i=i, j=j: self.record_click(i, j), bg='#515e5d')        
                elif(image_value == '02'):
                    if(i-1 < 0 or i+1 >6):
                        btn = tk.Button(self.master, image=image, compound=tk.CENTER, command=lambda i=i, j=j: self.record_click(i, j), bg='#515e5d')
                    else:
                        if((self.matriz[i-1][j] != '03' and self.matriz[i-1][j] != '06' and self.matriz[i-1][j] != '07' and self.matriz[i-1][j] != '00') and (self.matriz[i+1][j] != '04' and self.matriz[i+1][j] != '05' and self.matriz[i+1][j] != '09' and self.matriz[i+1][j] != '00') ):
                            btn = tk.Label(self.master, image=image, compound=tk.CENTER)
                        else:
                            btn = tk.Button(self.master, image=image, compound=tk.CENTER, command=lambda i=i, j=j: self.record_click(i, j), bg='#515e5d')      
                else:
                    btn = tk.Label(self.master, image=image, compound=tk.CENTER)
                """Evita que la referencia a la iamgen sea recolectada por el recolector de basura de Python"""
                btn.image = image
                """Colocar en las posicion correspondiente a sus indices, el boton o etiqueta en la ventana emergente"""
                btn.grid(row=i, column=j)

    # Registra clicks en los botones y, al seleccionar dos botones diferentes, 
    # llama al callback para actualizar la cola visual y cierra la ventana secuandaria
    def record_click(self, i, j):
        """crea una tupla con las coordenadas"""
        position = (i, j)
        if position not in self.click_positions:
            self.click_positions.append(position)
            if len(self.click_positions) == 2:
                if self.click_positions[0] != self.click_positions[1]:
                    """Inserta un nuevo par origen-destino en la Listbox"""
                    self.queue_callback(self.click_positions[0], self.click_positions[1])
                    """Cierra la ventana emergente"""
                    self.master.destroy()
                else:
                    """Elimina la ultima posicion añadida si es igual a la primera, ignorando el segundo click"""
                    self.click_positions.pop() 

# Clase principal que gestiona la ventana principal de la aplicación
class MainApp:

    #Constructor
    def __init__(self, master):
        """Funcion que maneja los mensajes MQTT que recibe la aplicacion"""
        def on_message(client, userdata, message):
            print(f'Topic:{message.topic} Mensage:{str(message.payload.decode("utf-8"))}')
            if(message.topic == "map"):
                self.cadena = str(message.payload.decode("utf-8"))

        """Inicialización de Atributos"""
        self.robot_position = None
        self.borrar = False
        
        """Configuracion de la ventana principal"""
        self.master = master
        master.title("Ventana Principal")

        """Configuración de la interfaz"""
        self.setup_interface()

        """Iniciar actualización periódica de la posición del robot"""
        self.schedule_robot_updates()

    #Configuracion de la interfaz
    def setup_interface(self):
        """Estructura la disposion de la interfaz"""
        self.left_panel = ttk.Frame(self.master)
        """Posiciona el panel izquierdo en el lado izquierdo, permitiendo que se expanda"""
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_panel = ttk.Frame(self.master)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        """Crea un boton en el panel derecho"""
        ttk.Button(self.right_panel, text="Añadir Peticiones", command=self.open_matrix_window).pack(pady=20)
        """Crea una lista de elementos, donde se van a ver las peticiones"""
        self.queue_listbox = tk.Listbox(self.right_panel, width=40, height=10)
        self.queue_listbox.pack(padx=20, pady=20)

        self.cadena = ""
        self.mensaje = mi.MensajeInterfaz()  
        """Almacena el mapa"""
        self.cadena = self.mensaje.getMapa()

        """Inicialización de la matriz"""
        self.matriz = self.create_initial_matrix() 

        """Cargar imágenes y mostrar matriz estática"""
        self.load_images()
        self.labels = {}
        """Llama al metodo para crear la matriz de imagenes estatica"""
        self.display_static_matrix()      
    
    # Crea una matriz basada en una cadena codificada que representa valores
    def create_initial_matrix(self):
        segmentos = [self.cadena[i:i+2] for i in range(0, len(self.cadena), 2)]
        matriz = []
        for i in range(7):
            fila = segmentos[i*5:(i+1)*5]
            matriz.append(fila)
        return matriz
    
    # Carga imagenes desde un directorio y las ajusta al tamaño deseado. Si una imagen no se encuentra, 
    # muestra un mensaje de error y coloca una casilla gris
    def load_images(self):
        self.images = {}
        desired_size = (50, 50)
        for i in range(12):
            image_number = f"{i:02}"
            try:
                image = Image.open(f"images/{image_number}.png")
                image = image.resize(desired_size, Image.Resampling.LANCZOS)
                self.images[image_number] = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                print(f"Error: No se encontró la imagen para {image_number}")
        self.images['default'] = ImageTk.PhotoImage(Image.new('RGB', desired_size, color='grey'))

    # Muestra una version estática de la matriz en la ventana principal sin funcionalidad
    def display_static_matrix(self):
        for i in range(7):
            for j in range(5):
                image_value = self.matriz[i][j]
                image = self.images.get(image_value, self.images['default'])
                lbl = tk.Label(self.left_panel, image=image, relief='flat')
                lbl.image = image
                lbl.grid(row=i, column=j)
                self.labels[(i, j)] = lbl

    # Inicia la ventana secundaria MatrixWindow
    def open_matrix_window(self):
        MatrixWindow(self.master, self.matriz, self.update_queue_display)

    # Inserta un nuevo par origen-destino en la Listbox
    def update_queue_display(self, origen, destino):
        self.queue_listbox.insert(tk.END, (origen, destino))
        self.highlight_path()

    #Ejecuta de manera periodica, actualizacion del robot y maneja los pedidos
    def schedule_robot_updates(self):
        self.update_robot_position(self.mensaje.getPosicion())
        """Se llama de forma recursiva cada 1 segundo"""
        self.master.after(1000, self.schedule_robot_updates)


        # Revisa si hay pedidos pendientes y si se ha solicitado un pedido
        if self.mensaje.pedidoSolicitado and self.queue_listbox.size() > 0:
        # Si self.borrar es True, borra el pedido anterior y prepara para enviar el siguiente
            if self.borrar:
                self.queue_listbox.delete(0)
                self.borrar = False  # Resetear self.borrar después de borrar el pedido

            # Si aún hay pedidos después de borrar, enviar el siguiente pedido
            if self.queue_listbox.size() > 0:
                print("Breakpoint Enviar Pedido: ", self.queue_listbox.get(0))
                self.mensaje.sendPedido(self.queue_listbox.get(0))
                self.borrar = True      

    #Actualiza la posición del robot y actualiza el resaltado correspondiente.
    def update_robot_position(self, new_position):
        self.robot_position = self.mensaje.getPosicion()
        self.highlight_path()

    # Resalta los botones correspondientes al primer elemento de la Listbox
    # Resalta donde se encuentra el robot
    def highlight_path(self):
        """Resetea todo los labels"""
        for label in self.labels.values():
            label.config(relief='flat', bg='SystemButtonFace')

        if self.queue_listbox.size() > 0:
            origen, destino = self.queue_listbox.get(0)
            """Resalta origen y destino, con un borde elevador y el color correspondiente"""
            self.labels[origen].config(relief='raised', borderwidth=2, bg='green')
            self.labels[destino].config(relief='raised', borderwidth=2, bg='red')

        """Resalta la posición del robot si está disponible"""
        if self.robot_position is not None:
            self.labels[self.robot_position].config(relief='raised', borderwidth=2, bg='blue')   
            
#Inicializa la aplicación
def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
