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


class Application(tk.Tk):
    def __init__(self):

        self.archivos_excel = []
        self.columnas_comunes = []
        self.columnas_distintas = []
        self.columnas_seleccionadas = []

        tk.Tk.__init__(self)
        self.title("Archivos txt")
        self.geometry("600x200")
        Label(self,text="Selecciona un archivo .txt").pack(pady=20, side= TOP, anchor="w")

        self.btn_cargar = tk.Button(self, text="Archivos txt a Analizar",command=self.open_files)
        self.btn_cargar.pack(pady=20)

        self.btn_help_main = tk.Button(self, text="Ayuda",command=self.show_main_help)
        self.btn_help_main.pack(pady=20)

        # Delete files when window is closed
        #self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Dictionary to store column checkboxes
        self.column_checkboxes = {}

        # Initialize rename_window to None
        self.rename_window = None


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
        if file_paths:
            for file_path in file_paths:
                print(f"Archivo seleccionado: {file_path}")
                self.process_file(file_path)
            messagebox.showinfo("Archivos cargados", "Los archivos se cargaron exitosamente.")
        else:
            messagebox.showwarning("Archivos no seleccionados", "No se seleccionaron archivos.")
        
        self.comparar_columnas()
        #self.display_columns()

    def comparar_columnas(self):
        if len(os.listdir("processing_files")) < 2:
            messagebox.showwarning("Archivos insuficientes", "Debe cargar al menos 2 archivos para comparar.")
            return
        else:
            print(f'Estos son los archivos creados: {os.listdir("processing_files")}')
        
        dfs = []
        columnas = set()

        for filename in os.listdir("processing_files"):
            try:
                df = pd.read_excel(os.path.join("processing_files", filename))
                dfs.append(df)
                columnas.add(tuple(df.columns))
            except Exception as e:
                print(f"Error al leer el archivo {archivo}: {str(e)}")

        if len(columnas) == 1:
            print("Todos los archivos tienen las mismas columnas:")
            print(columnas.pop())
        else:
            print("Los archivos no tienen las mismas columnas.")
           
        ##A partir de aqui se debera de implementar los demas procesos
            if filename.endswith(".xlsx"):
                df = pd.read_excel(os.path.join("processing_files", filename))

        columnas_archivos_1 = set(pd.read_excelself.archivos_excel().columns)
        columnas_iguales = True

        for archivo in self.archivos_excel[1:]:
            if set(archivo.columns) != list(columnas_archivos_1):
                columnas_iguales = False
                break

        if columnas_iguales:
            self.columnas_comunes = list(columnas_archivos_1)
            self.mostrar_seleccion_columnas_comunes()
        else:
            self.columnas_distintas = [set(archivo.columns) for archivo in self.archivos_excel]
            self.mostrar_seleccion_columnas_distintas()


    def mostrar_seleccion_columnas_comunes(self):
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

    def mostrar_seleccion_columnas_distintas(self):
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

    def reset(self):
            self.archivos_excel = []
            self.columnas_comunes = []
            self.columnas_distintas = []
            self.columnas_seleccionadas = []            

    def process_file(self, file_path):
        df = pd.read_csv(file_path,delimiter='\t')
        # process file here (your functions)
        self.archivos_excel.append(file_path)
        format1(file_path)
        format2(file_path)
        format3(file_path)
        format4(file_path)
        format5(file_path)
        format6(file_path)


if __name__ == "__main__":
    app = Application()
    mainloop()
