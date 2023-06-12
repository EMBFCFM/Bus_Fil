import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

def select_columns():
    # Abrir el cuadro de diálogo para seleccionar archivos
    files = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx")])

    if len(files) < 1:
        messagebox.showwarning("Advertencia", "No se seleccionaron archivos.")
        return

    # Leer los archivos Excel y obtener las columnas de cada archivo
    columns = {}
    for file in files:
        df = pd.read_excel(file)
        columns[file] = df.columns.tolist()

    if len(files) == 1:
        # Solo se seleccionó un archivo
        window = Tk()
        window.title("Selección de columnas")
        window.geometry("400x400")

        selected_columns = []

        def save_columns():
            # Guardar las columnas seleccionadas en un nuevo archivo Excel
            selected_columns.extend(listbox.curselection())
            if len(selected_columns) < 1:
                messagebox.showwarning("Advertencia", "No se seleccionaron columnas.")
                return

            save_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

            if save_file:
                # Leer el archivo original nuevamente y guardar solo las columnas seleccionadas en un nuevo archivo
                df = pd.read_excel(files[0])
                df_selected = df.iloc[:, selected_columns]
                df_selected.to_excel(save_file, index=False)

                messagebox.showinfo("Información", "Las columnas seleccionadas se guardaron correctamente.")

            window.destroy()

        scrollbar = Scrollbar(window)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(window, selectmode=MULTIPLE, yscrollcommand=scrollbar.set)
        listbox.pack(side=LEFT, fill=BOTH)

        for column in columns[files[0]]:
            listbox.insert(END, column)

        scrollbar.config(command=listbox.yview)

        save_button = Button(window, text="Guardar", command=save_columns)
        save_button.pack()

        window.mainloop()
    else:
        # Se seleccionaron dos o más archivos
        same_columns = []
        different_columns = []

        for col_list in columns.values():
            if col_list in same_columns:
                continue
            elif col_list in different_columns:
                different_columns.remove(col_list)
                same_columns.append(col_list)
            else:
                different_columns.append(col_list)

        if len(same_columns) > 0:
            # Hay archivos con las mismas columnas
            window = Tk()
            window.title("Selección de columnas")
            window.geometry("400x400")

            selected_columns_same = []

            def save_columns():
                # Guardar las columnas seleccionadas en un nuevo archivo Excel
                selected_columns_same.extend(listbox_same.curselection())

                if len(selected_columns_same) < 1:
                    messagebox.showwarning("Advertencia", "No se seleccionaron columnas.")
                    return

                save_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

                if save_file:
                    # Leer los archivos originales nuevamente y guardar solo las columnas seleccionadas en un nuevo archivo
                    df_concat = pd.DataFrame()
                    for file, cols in columns.items():
                        if cols in same_columns:
                            df = pd.read_excel(file)
                            df_selected = df.iloc[:, selected_columns_same]
                            df_concat = pd.concat([df_concat, df_selected], axis=1)

                    df_concat.to_excel(save_file, index=False)

                    messagebox.showinfo("Información", "Las columnas seleccionadas se guardaron correctamente.")

                window.destroy()

            same_label = Label(window, text="Archivos con las mismas columnas:")
            same_label.pack()

            scrollbar_same = Scrollbar(window)
            scrollbar_same.pack(side=RIGHT, fill=Y)

            listbox_same = Listbox(window, selectmode=MULTIPLE, yscrollcommand=scrollbar_same.set)
            listbox_same.pack(side=LEFT, fill=BOTH)

            for file, cols in columns.items():
                if cols in same_columns:
                    listbox_same.insert(END, file)

            scrollbar_same.config(command=listbox_same.yview)

            save_button = Button(window, text="Guardar", command=save_columns)
            save_button.pack()

            window.mainloop()

        if len(different_columns) > 0:
            # Hay archivos con columnas diferentes
            window = Tk()
            window.title("Selección de columnas")
            window.geometry("400x400")

            selected_columns_different = []

            def save_columns():
                # Guardar las columnas seleccionadas en un nuevo archivo Excel
                selected_columns_different.extend(listbox_different.curselection())

                if len(selected_columns_different) < 1:
                    messagebox.showwarning("Advertencia", "No se seleccionaron columnas.")
                    return

                save_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

                if save_file:
                    # Leer los archivos originales nuevamente y guardar solo las columnas seleccionadas en un nuevo archivo
                    df_concat = pd.DataFrame()
                    for file, cols in columns.items():
                        if cols in different_columns:
                            df = pd.read_excel(file)
                            df_selected = df.iloc[:, selected_columns_different]
                            df_concat = pd.concat([df_concat, df_selected], axis=1)

                    df_concat.to_excel(save_file, index=False)

                    messagebox.showinfo("Información", "Las columnas seleccionadas se guardaron correctamente.")

                window.destroy()

            different_label = Label(window, text="Archivos con columnas diferentes:")
            different_label.pack()

            scrollbar_different = Scrollbar(window)
            scrollbar_different.pack(side=RIGHT, fill=Y)

            listbox_different = Listbox(window, selectmode=MULTIPLE, yscrollcommand=scrollbar_different.set)
            listbox_different.pack(side=LEFT, fill=BOTH)

            for file, cols in columns.items():
                if cols in different_columns:
                    listbox_different.insert(END, file)

            scrollbar_different.config(command=listbox_different.yview)

            save_button = Button(window, text="Guardar", command=save_columns)
            save_button.pack()

            window.mainloop()

        if len(same_columns) < 1 and len(different_columns) < 1:
            # Todos los archivos tienen columnas diferentes
            window = Tk()
            window.title("Selección de columnas")
            window.geometry("400x400")

            selected_columns = []

            def save_columns():
                # Guardar las columnas seleccionadas en un nuevo archivo Excel
                selected_columns.extend(listbox.curselection())

                if len(selected_columns) < 1:
                    messagebox.showwarning("Advertencia", "No se seleccionaron columnas.")
                    return

                save_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

                if save_file:
                    # Leer los archivos originales nuevamente y guardar solo las columnas seleccionadas en un nuevo archivo
                    df_concat = pd.DataFrame()
                    for file in files:
                        df = pd.read_excel(file)
                        df_selected = df.iloc[:, selected_columns]
                        df_concat = pd.concat([df_concat, df_selected], axis=1)

                    df_concat.to_excel(save_file, index=False)

                    messagebox.showinfo("Información", "Las columnas seleccionadas se guardaron correctamente.")

                window.destroy()

            scrollbar = Scrollbar(window)
            scrollbar.pack(side=RIGHT, fill=Y)

            listbox = Listbox(window, selectmode=MULTIPLE, yscrollcommand=scrollbar.set)
            listbox.pack(side=LEFT, fill=BOTH)

            for file in files:
                listbox.insert(END, file)

            scrollbar.config(command=listbox.yview)

            save_button = Button(window, text="Guardar", command=save_columns)
            save_button.pack()

            window.mainloop()

# Ejecutar la función para seleccionar las columnas
select_columns()
