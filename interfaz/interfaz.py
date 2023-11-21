from tkinter import Button, Tk, Frame, Entry, END, Label, ttk, Menu, Scrollbar
import os
import shutil
from datetime import datetime
import subprocess


class Interfaz():
    
    def __init__(self):
        self.ruta = "semana_9/talleres/files_manager/c"
        ventana = Tk()
        ventana.geometry('774x428')
        ventana.config(bg="white")
        ventana.iconbitmap('semana_9\\talleres\\files_manager\\interfaz\\icons\\administrador.ico')
        ventana.resizable(0,0)
        ventana.title("Administrador de archivos")
        
        # Crear dos ventanas
        frameFolder = Frame(ventana, bg="#937687")
        frameFiles = Frame(ventana, bg="#B7A0AD")
        
        # Dividir la ventana en dos columnas
        frameFolder.grid(row=0, column=0, sticky="nsew")
        frameFiles.grid(row=0, column=1, sticky="nsew")

        # Peso de las columnas
        ventana.grid_rowconfigure(0, weight=1)
        ventana.grid_columnconfigure(0, weight=1)
        ventana.grid_columnconfigure(1, weight=4)

        # Etiquetas folders y files
        labelFolder = Label(frameFolder, text="Folders", bg="#B1B5B5", fg="#442034", font=("Arial", 13, "bold"))
        labelFolder.grid(row=0, column=0, columnspan=3, sticky="nsew")

        labelFiles = Label(frameFiles, text="Files", bg="#B1B5B5", fg="#442034", font=("Arial", 13, "bold"))
        labelFiles.grid(row=0, column=0, columnspan=3, sticky="nsew")
        
        # Configurar expansión horizontal de los frames
        frameFolder.grid_columnconfigure(0, weight=1)
        frameFolder.grid_columnconfigure(1, weight=1)
        frameFolder.grid_columnconfigure(2, weight=0)
        frameFolder.grid_rowconfigure(0, weight=0)
        frameFolder.grid_rowconfigure(1, weight=1)
        
        frameFiles.grid_columnconfigure(0, weight=1)
        frameFiles.grid_columnconfigure(1, weight=1)
        frameFiles.grid_columnconfigure(2, weight=0)
        frameFiles.grid_rowconfigure(0, weight=0)
        frameFiles.grid_rowconfigure(1, weight=1)
        
        # treeviewFolder
        # Creación de la vista de árbol.
        treeviewFolder = ttk.Treeview(frameFolder)
        treeviewFolder.heading("#0", text="Carpetas y archivos")
        
        treeviewFolder.grid(row=1, rowspan=2, column=0, columnspan=3, sticky="nsew")
        treeviewFolder.bind("<Button-3>", lambda event: self.mostrar_menu(event, treeviewFolder, treeviewFiles, ventana))
        
        # Agregar barras de desplazamiento
        scroll_y = ttk.Scrollbar(frameFolder, orient="vertical", command=treeviewFolder.yview)
        scroll_y.grid(row=1, column=2, sticky="ns")
        treeviewFolder.configure(yscrollcommand=scroll_y.set)

        scroll_x = ttk.Scrollbar(frameFolder, orient="horizontal", command=treeviewFolder.xview)
        scroll_x.grid(row=2, column=0, columnspan=3, sticky="ew")
        treeviewFolder.configure(xscrollcommand=scroll_x.set)
        
        
        # treeviewFiles
        treeviewFiles = ttk.Treeview(frameFiles, columns=("size", "lastmod"))
        treeviewFiles.heading("#0", text="Archivo")
        treeviewFiles.heading("#1", text="Tipo")
        treeviewFiles.heading("lastmod", text="Última modificación")
     
        treeviewFiles.grid(row=1, rowspan=2, column=0, columnspan=3, sticky="nsew")
        treeviewFiles.bind("<Double-1>", lambda event: self.abrir_archivo(event, treeviewFolder, treeviewFiles, ventana))
        
        # Agregar barras de desplazamiento
        scroll_y = ttk.Scrollbar(frameFiles, orient="vertical", command=treeviewFiles.yview)
        scroll_y.grid(row=1, column=2, sticky="ns")
        treeviewFiles.configure(yscrollcommand=scroll_y.set)

        scroll_x = ttk.Scrollbar(frameFiles, orient="horizontal", command=treeviewFiles.xview)
        scroll_x.grid(row=2, column=0, columnspan=3, sticky="ew")
        treeviewFiles.configure(xscrollcommand=scroll_x.set)
        
        self.llenar_treeview(treeviewFolder, self.ruta, "")
        
        ventana.mainloop()
        
    def mostrar_menu(self, event, treeviewFolder, treeviewFiles, root):
        item_seleccionado = treeviewFolder.focus()  # Obtener el ítem seleccionado
        valores = treeviewFolder.item(item_seleccionado, "values")

        # Crear un menú contextual
        menu = Menu(root, tearoff=0)
        # menu.add_command(label="Insertar", command=lambda: self.insertar_item(item_seleccionado, treeviewFolder))
        menu.add_command(label="Insertar", command=lambda: self.mostrar_submenu_insertar(event, item_seleccionado, treeviewFolder))
        menu.add_command(label="Eliminar", command=lambda: self.eliminar_item(item_seleccionado, treeviewFolder))
        menu.add_command(label="Actualizar", command=lambda: self.actualizar_item(item_seleccionado, valores, treeviewFolder))
        menu.add_command(label="Mostrar", command=lambda: self.mostrar_item(item_seleccionado, treeviewFolder, treeviewFiles))

        # Mostrar el menú en la posición del doble clic
        menu.post(event.x_root, event.y_root)
    
    def mostrar_submenu_insertar(self, event, item_seleccionado, treeviewFolder):
        # Crear un submenú para la opción "Insertar"
        submenu_insertar = Menu(treeviewFolder, tearoff=0)
        submenu_insertar.add_command(label="Carpeta", command=lambda: self.insertar_carpeta(item_seleccionado, treeviewFolder))
        submenu_insertar.add_command(label="Archivo", command=lambda: self.insertar_archivo(item_seleccionado, treeviewFolder))

        # Mostrar el submenú en la posición del clic derecho
        submenu_insertar.post(event.x_root, event.y_root)
    
    def insertar_carpeta(self, item_padre, treeviewFolder):
        ruta = self.construir_ruta(treeviewFolder, item_padre)
        nombre_carpeta = input("Nombre de la carpeta: ")
        ruta_completa = os.path.join(ruta, nombre_carpeta)
        hora_local = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Intenta crear la carpeta en la ruta deseada
            os.makedirs(ruta_completa)
            print(f"Carpeta '{nombre_carpeta}' creada en {ruta}.")
        except FileExistsError:
            print(f"La carpeta '{nombre_carpeta}' ya existe en {ruta}.")
        except Exception as e:
            print(f"Error al crear la carpeta: {e}")
        
        treeviewFolder.insert(item_padre, "end", values=("Carpeta", hora_local), text=nombre_carpeta)
        
    def mostrar_item(self, item_seleccionado, treeviewFolder, treeviewFiles):
        # Insertar un nuevo elemento después del elemento seleccionado
        self.obtener_elementos_principales(item_seleccionado, treeviewFolder, treeviewFiles)
        # treeview.insert(item_seleccionado, "end", values=("850 bytes", "18:30"), text="Nuevo Valor 1")

    def eliminar_item(self, item_seleccionado, treeview):
        # Eliminar el elemento seleccionado
        path = self.construir_ruta(treeview, item_seleccionado)
        
        if "." in treeview.item(item_seleccionado, "text"):
            self.eliminar_archivo(path)
        else:
            self.eliminar_carpeta(path)
        treeview.delete(item_seleccionado)
        
    def actualizar_item(self, item_seleccionado, valores, treeview):
        # Actualizar el item
        path = self.construir_ruta(treeview, item_seleccionado)
        if "." in treeview.item(item_seleccionado, "text"):
            nuevo_nombre = self.nuevo_nombre_archivo()
            self.cambiar_nombre_archivo(path, nuevo_nombre)
        else:
            nuevo_nombre = self.nuevo_nombre_carpeta()
            self.cambiar_nombre_carpeta(path, nuevo_nombre)
        treeview.item(item_seleccionado, text=nuevo_nombre)
        
    def nuevo_nombre_carpeta(self):
        nuevo_texto = input("Ingrese el nuevo nombre de la carpeta: ")
        return nuevo_texto
    
    def nuevo_nombre_archivo(self):
        nuevo_texto = input("Ingrese el nuevo nombre del archivo: ")
        return nuevo_texto
             
    def on_scroll_y(self, *args, tree):
        tree.yview(*args)
        
    def on_scroll_x(self, *args, tree):
        tree.yview(*args)
        
    def obtener_elementos_principales(self, item_seleccionado, treeviewFolder, treeviewFiles):
        elementos_principales = treeviewFolder.get_children(item_seleccionado)  # Obtener los elementos principales
        self.borrar_elementos(treeviewFiles)
        for elemento in elementos_principales:
            self.mostrar_elementos_en_treeviewFiles(treeviewFolder, treeviewFiles, elemento)
        
    def mostrar_elementos_en_treeviewFiles(self, treeviewOrigen, treeviewDestino, elemento):
        treeviewDestino.insert("", END, text=treeviewOrigen.item(elemento, "text"), values=treeviewOrigen.item(elemento, "values"))
    
    def borrar_elementos(self, treeview):
        treeview.delete(*treeview.get_children())  # Borra todos los elementos
        
    def construir_ruta(self, treeview, item_padre):
        # Construye la ruta recorriendo los padres del elemento seleccionado
        parent = treeview.parent(item_padre)
        path = ""
            
        while parent:
            path = treeview.item(parent, 'text') + '/' +  path 
            parent = treeview.parent(parent)
            
        item = treeview.item(item_padre, 'text')
        if item != '':
            path = path + item
        
        path = self.ruta + "/" + path
        
        return path
    
    def llenar_treeview(self, treeview, ruta_carpeta, item_padre = ""):    
        for elemento in os.listdir(ruta_carpeta):
            ruta_completa = os.path.join(ruta_carpeta, elemento)
            ruta_completa = ruta_completa.replace('\\', '/')
            
            try:
                if os.path.exists(ruta_completa):
                    if os.path.isdir(ruta_completa):
                        # Es una carpeta
                        n_item_padre = treeview.insert(item_padre, "end", text=elemento, values=("Carpeta", self.obtener_fecha_ultima_modificacion(ruta_completa)))
                        self.llenar_treeview(treeview, ruta_completa, n_item_padre)
                    elif os.path.isfile(ruta_completa):
                        print("Hola muindo")
                        # Es un archivo
                        n_item_padre = treeview.insert(item_padre, "end", text=elemento, values=("Archivo", self.obtener_fecha_ultima_modificacion(ruta_completa), ruta_completa))
                        self.llenar_treeview(treeview, ruta_completa, n_item_padre)
                else:
                    print(f"La ruta {ruta_completa} no existe.")
            except NotADirectoryError:
                print(f"{ruta_completa} no es un directorio válido.")
            except Exception as e:
                print(f"Error al procesar {ruta_completa}: {e}")
                
    def eliminar_carpeta(self, ruta_carpeta):
        try:
            shutil.rmtree(ruta_carpeta)
            print(f"Carpeta '{ruta_carpeta}' eliminada exitosamente.")
        except FileNotFoundError:
            print(f"La carpeta en {ruta_carpeta} no existe.")
        except Exception as e:
            print(f"Error al eliminar la carpeta: {e}")

    def cambiar_nombre_carpeta(self, ruta_carpeta, nuevo_nombre):
        try:
            nueva_ruta = os.path.join(os.path.dirname(ruta_carpeta), nuevo_nombre)
            os.rename(ruta_carpeta, nueva_ruta)
            print(f"El nombre de la carpeta se cambió a '{nuevo_nombre}'")
        except Exception as e:
            print(f"Error al cambiar el nombre de la carpeta: {e}")
            
    def cambiar_nombre_archivo(self, ruta_archivo, nuevo_nombre):
        try:
            nueva_ruta = os.path.join(os.path.dirname(ruta_archivo), nuevo_nombre)
            os.rename(ruta_archivo, nueva_ruta)
            print(f"El nombre del archivo se cambió a '{nuevo_nombre}'")
        except Exception as e:
            print(f"Error al cambiar el nombre del archivo: {e}")
            
    def obtener_fecha_ultima_modificacion(self, ruta):
        try:
            timestamp_ultima_modificacion = os.path.getmtime(ruta)
            fecha_ultima_modificacion = datetime.fromtimestamp(timestamp_ultima_modificacion)
            fecha_hora_formateada = fecha_ultima_modificacion.strftime("%Y-%m-%d %H:%M:%S")
            return fecha_hora_formateada
        except Exception as e:
            print(f"Error al obtener la fecha de última modificación: {e}")
            return None

    def insertar_archivo(self, item_padre, treeviewFolder):
        ruta = self.construir_ruta(treeviewFolder, item_padre)
        nombre_archivo = input("Nombre del archivo: ")
        ruta_completa = os.path.join(ruta, nombre_archivo)
        hora_local = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
        try:
            # Intenta crear la carpeta en la ruta deseada
            # os.makedirs(ruta_completa)
            with open(ruta_completa, 'w') as archivo:
                archivo.write("")
                
            print(f"Archivo '{nombre_archivo}' creado en {ruta}.")
        except FileExistsError:
            print(f"El archivo '{nombre_archivo}' ya existe en {ruta}.")
        except Exception as e:
            print(f"Error al crear el archivo: {e}")
        
        treeviewFolder.insert(item_padre, "end", values=("Archivo", hora_local), text=nombre_archivo)
        
    def eliminar_archivo(self, ruta_archivo):
        try:
            os.remove(ruta_archivo)
            print(f"Archivo en {ruta_archivo} eliminado exitosamente.")
        except FileNotFoundError:
            print(f"El archivo en {ruta_archivo} no existe.")
        except Exception as e:
            print(f"Error al eliminar el archivo: {e}")
            
    def abrir_archivo(self, event, treeviewFolder, treeviewFiles, root):
        item_seleccionado = treeviewFiles.focus()
        valores = treeviewFiles.item(item_seleccionado, "values")
        self.abrir_archivo_en_pantalla(valores[2])
              
    def abrir_archivo_en_pantalla(self, ruta_archivo):
        try:
            # Utiliza el comando xdg-open para abrir el archivo con la aplicación predeterminada
            subprocess.Popen('start "" "' + ruta_archivo + '"', shell=True)
        except Exception as e:
            print(f"Error al abrir el archivo: {e}")

    