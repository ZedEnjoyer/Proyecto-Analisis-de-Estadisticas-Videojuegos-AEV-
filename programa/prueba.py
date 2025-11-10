import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# --- Ventana principal ---
principal = tk.Tk()
principal.title("Análisis de datos de videojuegos")
principal.geometry("800x500")
principal.configure(background="#1E1E1E")

# --- Cargar CSV ---
def cargar_archivo():
    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=[("Archivos CSV", "*.csv")]
    )
    if not ruta:
        return

    try:
        global df
        df = pd.read_csv(ruta, encoding='utf-8', sep=',', on_bad_lines='skip')
        messagebox.showinfo("Éxito", f"Archivo cargado correctamente: {ruta}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

# --- Análisis de datos ---
def analizar_datos():
    try:
        if df is None or df.empty:
            messagebox.showerror("Error", "Primero debes cargar un archivo CSV.")
            return

        print("\nEstadísticas generales:")
        print(df.describe(include='all'))

        messagebox.showinfo("Análisis completado", "Los datos se analizaron exitosamente. Revisa la consola para detalles.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Gráficas ---
def mostrar_graficas():
    try:
        if df is None or df.empty:
            messagebox.showerror("Error", "Primero debes cargar un archivo CSV.")
            return

        # Verificar columnas
        columnas_necesarias = ['titulo', 'año_de_publicacion', 'genero', 'copias_vendidas']
        for col in columnas_necesarias:
            if col not in df.columns:
                messagebox.showerror("Error", f"Falta la columna '{col}' en el CSV.")
                return

        # Agrupar por año y género
        ventas_genero = df.groupby(['año_de_publicacion', 'genero'])['copias_vendidas'].sum().unstack()
        ventas_genero.plot(kind='bar', figsize=(10, 6))
        plt.title("Comparación de ventas por género y año")
        plt.xlabel("Año de publicación")
        plt.ylabel("Copias vendidas (en millones)")
        plt.legend(title="Género")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Predicción ---
def predecir_exito():
    try:
        if df is None or df.empty:
            messagebox.showerror("Error", "Primero debes cargar un archivo CSV.")
            return

        columnas_requeridas = ['año_de_publicacion', 'precio', 'genero', 'copias_vendidas']
        for col in columnas_requeridas:
            if col not in df.columns:
                messagebox.showerror("Error", f"Falta la columna '{col}' en el CSV.")
                return

        # Preprocesar datos
        data = df.dropna(subset=columnas_requeridas).copy()
        label = LabelEncoder()
        data['genero_cod'] = label.fit_transform(data['genero'])

        X = data[['año_de_publicacion', 'precio', 'genero_cod']]
        y = data['copias_vendidas']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        modelo = RandomForestRegressor(n_estimators=100, random_state=42)
        modelo.fit(X_train, y_train)

        # Solicitar datos al usuario
        ventana_pred = tk.Toplevel(principal)
        ventana_pred.title("Predicción de éxito")
        ventana_pred.geometry("400x400")
        ventana_pred.configure(bg="#1E1E1E")

        tk.Label(ventana_pred, text="Año de publicación:", fg="white", bg="#1E1E1E").pack()
        entry_año = tk.Entry(ventana_pred)
        entry_año.pack()

        tk.Label(ventana_pred, text="Precio ($):", fg="white", bg="#1E1E1E").pack()
        entry_precio = tk.Entry(ventana_pred)
        entry_precio.pack()

        tk.Label(ventana_pred, text="Género:", fg="white", bg="#1E1E1E").pack()
        combo_genero = ttk.Combobox(ventana_pred, values=list(label.classes_))
        combo_genero.pack()

        def realizar_prediccion():
            try:
                año = int(entry_año.get())
                precio = float(entry_precio.get())
                genero = combo_genero.get()

                if genero not in label.classes_:
                    messagebox.showerror("Error", "El género ingresado no es válido.")
                    return

                genero_cod = label.transform([genero])[0]
                prediccion = modelo.predict([[año, precio, genero_cod]])[0]

                messagebox.showinfo("Predicción completada",
                                    f"Predicción de ventas estimadas: {prediccion:.2f} millones de copias")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana_pred, text="Predecir", command=realizar_prediccion, bg="#3A3A3A", fg="white").pack(pady=20)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Botones ---
tk.Button(principal, text="Cargar archivo CSV", command=cargar_archivo, bg="#3A3A3A", fg="white", width=25).pack(pady=10)
tk.Button(principal, text="Análisis de datos", command=analizar_datos, bg="#3A3A3A", fg="white", width=25).pack(pady=10)
tk.Button(principal, text="Mostrar gráficas", command=mostrar_graficas, bg="#3A3A3A", fg="white", width=25).pack(pady=10)
tk.Button(principal, text="Predicción de éxito", command=predecir_exito, bg="#3A3A3A", fg="white", width=25).pack(pady=10)
tk.Button(principal, text="Salir", command=principal.destroy, bg="#7A0000", fg="white", width=25).pack(pady=20)

principal.mainloop()
