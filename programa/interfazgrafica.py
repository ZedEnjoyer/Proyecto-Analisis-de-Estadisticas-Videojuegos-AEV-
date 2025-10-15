import tkinter as tk
import os
import pandas as pd

# --- Ventana principal ---
principal = tk.Tk()
principal.title("Análisis de datos de videojuegos")
principal.geometry("700x400")
principal.configure(background="#201D1D")

# --- Etiqueta de bienvenida ---
etiqueta = tk.Label(
    principal,
    text="¡Bienvenido! ¿Qué acción deseas realizar?",
    font=("Arial", 17),
    background="#201D1D",
    foreground="white"
)
etiqueta.pack(pady=20)

def graficas():
    os.system("python codigo_graphs.py")

boton = tk.Button(
    principal,
    text="Análisis de datos (gráficas)",
    width=25,
    height=2,
    command=graficas
)
boton.place(x=60, y=100)

frame_texto = tk.Frame(principal, background="#201D1D")

scroll = tk.Scrollbar(frame_texto)
scroll.pack(side="right", fill="y")

texto_area = tk.Text(
    frame_texto,
    wrap="none",
    yscrollcommand=scroll.set,
    bg="#1E1E1E",
    fg="lightgreen",
    font=("Consolas", 9)
)
texto_area.pack(fill="both", expand=True)
scroll.config(command=texto_area.yview)

frame_texto.pack_forget()

def cargar_datos():
    try:
        df = pd.read_csv("steam_games.csv")

        frame_texto.pack(fill="both", expand=True, padx=20, pady=10)

        texto_area.delete("1.0", tk.END)
        texto_area.insert(tk.END, df.to_string(index=False))
    except Exception as e:
        frame_texto.pack(fill="both", expand=True, padx=20, pady=10)
        texto_area.delete("1.0", tk.END)
        texto_area.insert(tk.END, f"Error al cargar datos: {e}")

boton2 = tk.Button(
    principal,
    text="Cargar datos del CSV",
    width=25,
    height=2,
    command=cargar_datos
)
boton2.place(x=380, y=100)

principal.mainloop()
