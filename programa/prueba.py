import tkinter as tk
import os
import pandas as pd
import subprocess
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# --- Ventana principal ---
principal = tk.Tk()
principal.title("Análisis de datos de videojuegos")
principal.geometry("900x600")
principal.configure(background="#1E1E1E")

color_fondo = "#1E1E1E"
color_boton = "#3A3A3A"
color_acento = "#00FF7F"
fuente_titulo = ("Segoe UI", 18, "bold")
fuente_normal = ("Segoe UI", 11)

style = ttk.Style()

etiqueta = tk.Label(
    principal,
    text="¡Bienvenido! ¿Qué acción deseas realizar?",
    font=fuente_titulo,
    background=color_fondo,
    foreground=color_acento
)
etiqueta.pack(pady=20)

frame_botones = tk.Frame(principal, background=color_fondo)
frame_botones.pack(pady=10)

# --- Funciones principales ---

def mostrar_datos():
    frame_texto.pack(fill="both", expand=True, padx=20, pady=10)
    texto_area.delete("1.0", tk.END)
    df = pd.read_csv("steam_games.csv")
    texto_area.insert(tk.END, df.head(50).to_string(index=False))

def graficas():
    try:
        df = pd.read_csv("steam_games.csv")

        if 'genero' not in df.columns or 'ventas_millones' not in df.columns:
            messagebox.showerror("Error", "El CSV debe tener columnas: 'genero' y 'ventas_millones'")
            return

        plt.figure(figsize=(10,6))
        sns.barplot(data=df, x='genero', y='ventas_millones', estimator='mean')
        plt.title('Promedio de ventas por género')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10,6))
        sns.lineplot(data=df, x='año_de_publicacion', y='ventas_millones', hue='genero', marker='o')
        plt.title('Comparación de ventas por año y género')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        texto_area.insert(tk.END, f"Error al ejecutar gráficas: {e}\n")

def limpiar_texto():
    texto_area.delete("1.0", tk.END)


# --- NUEVA FUNCIÓN: Predicción de éxito del juego ---
def predecir_exito():
    try:
        df = pd.read_csv("steam_games.csv")

        if 'genero' not in df.columns or 'precio' not in df.columns or 'año_de_publicacion' not in df.columns or 'ventas_millones' not in df.columns:
            messagebox.showerror("Error", "El CSV debe tener columnas: 'genero', 'precio', 'año_de_publicacion', 'ventas_millones'")
            return

        # Codificar el género
        le = LabelEncoder()
        df['genero_cod'] = le.fit_transform(df['genero'])

        # Variables independientes y dependiente
        X = df[['genero_cod', 'precio', 'año_de_publicacion']]
        y = df['ventas_millones']

        modelo = LinearRegression()
        modelo.fit(X, y)

        # Ventana para ingresar los datos
        ventana_pred = tk.Toplevel(principal)
        ventana_pred.title("Predicción de éxito")
        ventana_pred.geometry("400x400")
        ventana_pred.configure(background=color_fondo)

        tk.Label(ventana_pred, text="Selecciona el género:", bg=color_fondo, fg=color_acento).pack(pady=5)
        genero_var = tk.StringVar()
        genero_cb = ttk.Combobox(ventana_pred, textvariable=genero_var, values=list(le.classes_))
        genero_cb.pack(pady=5)

        tk.Label(ventana_pred, text="Precio del juego ($):", bg=color_fondo, fg=color_acento).pack(pady=5)
        precio_var = tk.DoubleVar()
        tk.Entry(ventana_pred, textvariable=precio_var).pack(pady=5)

        tk.Label(ventana_pred, text="Año de publicación:", bg=color_fondo, fg=color_acento).pack(pady=5)
        anio_var = tk.IntVar()
        tk.Entry(ventana_pred, textvariable=anio_var).pack(pady=5)

        def calcular_prediccion():
            try:
                genero_cod = le.transform([genero_var.get()])[0]
                nuevo_dato = pd.DataFrame([[genero_cod, precio_var.get(), anio_var.get()]],
                                          columns=['genero_cod', 'precio', 'año_de_publicacion'])
                prediccion = modelo.predict(nuevo_dato)[0]
                texto = f"Tu juego podría vender aproximadamente {prediccion:.2f} millones de copias."
                if prediccion > df['ventas_millones'].mean():
                    texto += "\n💡 ¡Es probable que sea un éxito!"
                else:
                    texto += "\n⚠️ Podría tener un rendimiento moderado."
                messagebox.showinfo("Resultado de predicción", texto)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo calcular: {e}")

        tk.Button(ventana_pred, text="Predecir éxito", bg=color_boton, fg=color_acento,
                  command=calcular_prediccion).pack(pady=20)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# --- BOTONES ---
boton = tk.Button(
    frame_botones,
    text="Visualizar datos en el CSV",
    width=30,
    height=2,
    bg=color_boton,
    fg=color_acento,
    font=fuente_normal,
    relief="raised",
    activebackground="#00A86B",
    activeforeground="white",
    command=mostrar_datos,
    cursor="hand2"
)
boton.grid(row=0, column=0, padx=20, pady=10)

boton2 = tk.Button(
    frame_botones,
    text="Análisis de datos (gráficas)",
    width=30,
    height=2,
    bg=color_boton,
    fg=color_acento,
    font=fuente_normal,
    relief="raised",
    activebackground="#00A86B",
    activeforeground="white",
    command=graficas,
    cursor="hand2"
)
boton2.grid(row=0, column=1, padx=20, pady=10)

boton_pred = tk.Button(
    principal,
    text="Predecir éxito de tu juego",
    width=30,
    height=2,
    bg=color_boton,
    fg=color_acento,
    font=fuente_normal,
    relief="raised",
    activebackground="#00A86B",
    activeforeground="white",
    command=predecir_exito,
    cursor="hand2"
)
boton_pred.pack(pady=10)

frame_texto = tk.Frame(principal, background=color_fondo, bd=2, relief="groove")

scroll = tk.Scrollbar(frame_texto)
scroll.pack(side="right", fill="y")

texto_area = tk.Text(
    frame_texto,
    wrap="none",
    yscrollcommand=scroll.set,
    bg="#111111",
    fg="#7CFC00",
    font=("Consolas", 10),
    insertbackground=color_acento
)
texto_area.pack(fill="both", expand=True)
scroll.config(command=texto_area.yview)
frame_texto.pack_forget()

boton_limpiar = tk.Button(
    principal,
    text="Limpiar pantalla",
    width=25,
    height=2,
    bg=color_boton,
    fg=color_acento,
    font=fuente_normal,
    relief="raised",
    activebackground="#00A86B",
    activeforeground="white",
    command=limpiar_texto,
    cursor="hand2"
)
boton_limpiar.pack(pady=10)

pie = tk.Label(
    principal,
    text="Desarrollado por: Tu nombre aquí",
    bg=color_fondo,
    fg="#888888",
    font=("Segoe UI", 9)
)
pie.pack(side="bottom", pady=10)

principal.mainloop()
