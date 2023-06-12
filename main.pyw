from scripts.alumnosConSemestreYTurno import format1
from scripts.alumnosConTipoDeInscripcion import format2
from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
from scripts.alumnosDePrimerIngresoConCarreraLugarDeNacimientoProcedenciaYSexo import format3
from scripts.alumnosInscritos import format4
from scripts.alumnosInscritosConEmail import format5
from scripts.alumosPorNivel import format6
import os
import pandas as pd
import time


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #label= label(self,"Hola")
        #etiqueta = tk.Label(text="Hola")
        

        
        self.title("Programa para generar planes")
        self.geometry("400x250")  # Cambiar el tamaño de la ventana

        Label(self, text= "Selecciona un archivo .txt").pack(pady=20, side= TOP, anchor="w")
        Label(self, text= "Dudas").pack(pady=20, side= TOP, anchor="w")

        self.btn_open = tk.Button(self, text="Archivos txt a Analizar",command=self.open_files).pack(side=LEFT,anchor="w")
        #self.btn_open.pack(pady=20)

        self.btn_help_main = tk.Button(self, text="Dudas", command=self.show_main_help).pack(side=LEFT,anchor="w")
        #self.btn_help_main.pack(pady=20)
        
        self.btn_close = tk.Button(self, text="Cerrar Ventana", command=self.close_window)
        self.btn_close.pack(pady=20)

        # Delete files when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Dictionary to store column checkboxes
        self.column_checkboxes = {}

        # Initialize rename_window to None
        self.rename_window = None

    def cargar_archivos(self):
        rutas_archivos = filedialog.askopenfilenames(title="Seleccionar archivos", filetypes=[("Archivos Excel", "*.xlsx")])
        if rutas_archivos:
            for ruta_archivo in rutas_archivos:
                archivo = pd.read_excel(ruta_archivo)
                self.archivos_excel.append(archivo)
            messagebox.showinfo("Archivos cargados", "Los archivos se cargaron exitosamente.")
        else:
            messagebox.showwarning("Archivos no seleccionados", "No se seleccionaron archivos.")

    def close_window(self):
        self.destroy()

    def show_main_help(self):
        messagebox.showinfo("Ayuda", "Esta aplicación permite procesar y seleccionar columnas específicas de archivos .txt.\n\n" \
                       "Primero, use el botón 'Archivos txt a Analizar' para seleccionar los archivos .txt que desea analizar.\n\n" \
                       "A continuación, se abrirá una ventana con todas las columnas de los archivos .xlsx generados, donde podrá seleccionar " \
                       "las columnas que desea conservar.\n\nFinalmente, podrá optar por renombrar las columnas seleccionadas antes de guardarlas " \
                       "en un nuevo archivo .xlsx.")

    def on_closing(self):
        self.clean_up()
        self.destroy()  # Close the window

  

    def open_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[('Text Files', '*.txt')])
        for file_path in file_paths:
            print(f"Archivo seleccionado: {file_path}")
            self.process_file(file_path)

        
        

    def process_file(self, file_path):
        # process file here (your functions)
        format1(file_path)
        format2(file_path)
        format3(file_path)
        format4(file_path)
        format5(file_path)
        format6(file_path)

    def comparar_columnas(self):  ##Funcion para pedirle al usuario que elija al menos 2 archivos para empezar
        if len(os.listdir("processing_files")) < 2:
            messagebox.showwarning("Archivos insuficientes", "Debe cargar al menos 2 archivos para comparar.")
            return
        columnas_archivo_1 = set(self.archivos_excel[0].columns)
        columnas_iguales = True

        for archivo in self.archivos_excel[1:]:
            if set(archivo.columns) != columnas_archivo_1:
                columnas_iguales = False
                break

        if columnas_iguales:
            self.columnas_comunes = list(columnas_archivo_1)
            self.mostrar_seleccion_columnas_comunes()
        else:
            self.columnas_distintas = [set(archivo.columns) for archivo in self.archivos_excel]
            self.mostrar_seleccion_columnas_distintas()

    def mostrar_seleccion_columnas_comunes(self): ##Funcion para mostrar las columnas comunes
        if not self.columnas_comunes:
            return

        ventana_seleccion = tk.Toplevel()
        ventana_seleccion.title("Seleccionar columnas")
        ventana_seleccion.geometry("400x400")

        seleccion = []

        def toggle_columna(columna):
            if columna in seleccion:
                seleccion.remove(columna)
            else:
                seleccion.append(columna)

        for columna in self.columnas_comunes:
            checkbox = tk.Checkbutton(ventana_seleccion, text=columna, command=lambda col=columna: toggle_columna(col))
            checkbox.pack(anchor="w")

        boton_guardar = tk.Button(ventana_seleccion, text="Guardar", command=lambda: self.guardar_columnas(seleccion))
        boton_guardar.pack()

        self.btn_help_columns = tk.Button(self.column_window, text="Ayuda", command=self.show_columns_help)
        self.btn_help_columns.pack()




    def mostrar_seleccion_columnas_distintas(self): ##Funcion para mostrar columnas distintas
            if not self.columnas_distintas:
                return

            ventana_seleccion = tk.Toplevel()
            ventana_seleccion.title("Seleccionar columnas")
            ventana_seleccion.geometry("400x400")

            seleccion_por_archivo = []

            def seleccionar_columnas_distintas():
                for i, archivo in enumerate(self.archivos_excel):
                    columnas_seleccionadas = seleccion_por_archivo[i].get()
                    if columnas_seleccionadas:
                        self.columnas_seleccionadas.append(columnas_seleccionadas)
                    else:
                        self.columnas_seleccionadas.append([])

                self.guardar_columnas_distintas()

            for i, columnas in enumerate(self.columnas_distintas):
                seleccion = []

                etiqueta = tk.Label(ventana_seleccion, text="Archivo {}".format(i+1))
                etiqueta.pack()

                for columna in columnas:
                    checkbox = tk.Checkbutton(ventana_seleccion, text=columna,
                                            variable=tk.BooleanVar(value=False),
                                            command=lambda col=columna, sel=seleccion: sel.append(col))
                    checkbox.pack(anchor="w")

                seleccion_por_archivo.append(seleccion)

            boton_guardar = tk.Button(ventana_seleccion, text="Guardar", command=seleccionar_columnas_distintas)
            boton_guardar.pack()

    def guardar_columnas(self, columnas_seleccionadas):
        if not columnas_seleccionadas:
            messagebox.showwarning("Columnas no seleccionadas", "No se seleccionaron columnas para guardar.")
            return

        archivo_seleccionado = filedialog.asksaveasfilename(title="Guardar archivo", defaultextension=".xlsx")
        if archivo_seleccionado:
            df_nuevo_excel = pd.DataFrame()

            for archivo in self.archivos_excel:
                df_nuevo_excel = pd.concat([df_nuevo_excel, archivo[columnas_seleccionadas]], axis=1)

            df_nuevo_excel.to_excel(archivo_seleccionado, index=False)
            messagebox.showinfo("Guardado", "El archivo se guardó exitosamente.")
            self.reset()

    def guardar_columnas_distintas(self):
        archivo_seleccionado = filedialog.asksaveasfilename(title="Guardar archivo", defaultextension=".xlsx")
        if archivo_seleccionado:
            df_nuevo_excel = pd.DataFrame()

            for i, archivo in enumerate(self.archivos_excel):
                columnas_seleccionadas = self.columnas_seleccionadas[i]
                df_nuevo_excel = pd.concat([df_nuevo_excel, archivo[columnas_seleccionadas]], axis=1)

            df_nuevo_excel.to_excel(archivo_seleccionado, index=False)
            messagebox.showinfo("Guardado", "El archivo se guardó exitosamente.")
            self.reset()

    def show_rename_help(self):
            messagebox.showinfo("Ayuda", "Esta pantalla le permite renombrar las columnas seleccionadas. " \
                        "Ingrese los nuevos nombres de las columnas en los cuadros de entrada y luego haga clic en 'Crear archivo' para " \
                        "guardar las columnas seleccionadas en un nuevo archivo .xlsx con los nombres de las columnas actualizados.Puedes dejar \
                            en blanco las columnas a las que no deseas cambiarles el nombre, el programa tomara el nombre original por defecto")

    def create_file(self):
        for column, entry in self.entries.items():
            new_name = entry.get()
            if new_name:
                self.df_selected = self.df_selected.rename(columns={column: new_name})

        # Save the new DataFrame to a new excel file
        self.save_file(self.df_selected)

    def save_file(self, dataframe):
        # Let the user choose the location and name of the output file
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        # Save the new DataFrame to the chosen file
        dataframe.to_excel(file_path, index=False)
        print(f"Las columnas seleccionadas se han guardado con éxito en '{file_path}'.")

        self.clean_up()

        if self.rename_window:
            self.rename_window.destroy()
            self.rename_window = None

        # Close the columns window
        self.column_window.destroy()

        # Show a message box to inform the user that the process is done
        messagebox.showinfo("Proceso terminado", f"El archivo '{file_path}' ha sido creado con éxito.")
        
    def clean_up(self):
        # Delete all files in the processing_files folder
        for filename in os.listdir("processing_files"):
            processing_file_path = os.path.join("processing_files", filename)
            try:
                if os.path.isfile(processing_file_path):
                    os.unlink(processing_file_path)
            except Exception as e:
                print(f"Error al eliminar el archivo {processing_file_path}: {e}")

        # Delete all references in column_checkboxes
        self.column_checkboxes = {}

if __name__ == "__main__":

    ventana_principal = tk.Tk()
    ventana_principal.title("Comparador de archivos Excel")
    ventana_principal.geometry("600x200")

    Label(ventana_principal,text="Selecciona un archivo .txt").pack(pady=20, side= TOP, anchor="w")
    Label(ventana_principal, text= "Dudas").pack(pady=20, side= TOP, anchor="w")

    app = Application()

    def cargar_archivos():
        app.cargar_archivos()

    def comparar_columnas():
        app.comparar_columnas()

    boton_cargar = tk.Button(ventana_principal, text="Cargar archivos", command=cargar_archivos)
    boton_cargar.pack()

    boton_comparar = tk.Button(ventana_principal, text="Comparar columnas", command=comparar_columnas)
    boton_comparar.pack()

    ventana_principal.mainloop()


"""
self.title("Programa para generar planes")
        self.geometry("400x250")  # Cambiar el tamaño de la ventana

        Label(self, text= "Selecciona un archivo .txt").pack(pady=20, side= TOP, anchor="w")
        Label(self, text= "Dudas").pack(pady=20, side= TOP, anchor="w")

        self.btn_open = tk.Button(self, text="Archivos txt a Analizar",command=self.open_files).pack(side=LEFT,anchor="w")
        #self.btn_open.pack(pady=20)

        self.btn_help_main = tk.Button(self, text="Dudas", command=self.show_main_help).pack(side=LEFT,anchor="w")
        #self.btn_help_main.pack(pady=20)
        
        self.btn_close = tk.Button(self, text="Cerrar Ventana", command=self.close_window)
        self.btn_close.pack(pady=20)

        # Delete files when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Dictionary to store column checkboxes
        self.column_checkboxes = {}

        # Initialize rename_window to None
        self.rename_window = None
"""     