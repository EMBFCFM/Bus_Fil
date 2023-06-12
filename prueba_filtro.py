import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd


class ExcelComparator:
    def __init__(self):
        self.archivos_excel = []
        self.columnas_comunes = []
        self.columnas_distintas = []
        self.columnas_seleccionadas = []

    def cargar_archivos(self):
        rutas_archivos = filedialog.askopenfilenames(title="Seleccionar archivos", filetypes=[("Archivos Excel", "*.xlsx")])
        if rutas_archivos:
            for ruta_archivo in rutas_archivos:
                archivo = pd.read_excel(ruta_archivo)
                self.archivos_excel.append(archivo)
            messagebox.showinfo("Archivos cargados", "Los archivos se cargaron exitosamente.")
        else:
            messagebox.showwarning("Archivos no seleccionados", "No se seleccionaron archivos.")

    def comparar_columnas(self):
        if len(self.archivos_excel) < 2:
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


# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Comparador de archivos Excel")
ventana_principal.geometry("200x200")

comparador = ExcelComparator()


def cargar_archivos():
    comparador.cargar_archivos()


def comparar_columnas():
    comparador.comparar_columnas()


boton_cargar = tk.Button(ventana_principal, text="Cargar archivos", command=cargar_archivos)
boton_cargar.pack()

boton_comparar = tk.Button(ventana_principal, text="Comparar columnas", command=comparar_columnas)
boton_comparar.pack()

ventana_principal.mainloop()
