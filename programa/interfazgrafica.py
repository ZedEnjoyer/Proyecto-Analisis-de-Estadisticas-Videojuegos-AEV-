import tkinter as tk
import os
import pandas as pd
import subprocess

principal = tk.Tk()
principal.title("Análisis de datos de videojuegos")
principal.geometry("800x500")
principal.configure(background="#1E1E1E")

color_fondo = "#1E1E1E"
color_boton = "#3A3A3A"
color_texto = "white"
color_acento = "#00FF7F"
fuente_titulo = ("Segoe UI", 18, "bold")
fuente_normal = ("Segoe UI", 11)

etiqueta = tk.Label(
    principal,
    text="¡Bienvenido! ¿Qué acción deseas realizar?",
    font=fuente_titulo,
    background=color_fondo,
    foreground=color_acento
)
etiqueta.pack(pady=20)

# --- Marco para botones principales ---
frame_botones = tk.Frame(principal, background=color_fondo)
frame_botones.pack(pady=10)

def graficas():
    try:
        subprocess.Popen(["python", "codigo_graphs.py"])
    except Exception as e:
        texto_area.insert(tk.END, f"Error al ejecutar gráficas: {e}\n")

boton = tk.Button(
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
    command=graficas
)
boton.grid(row=0, column=0, padx=20, pady=10)

def cargar_datos():
    frame_texto.pack(fill="both", expand=True, padx=20, pady=10)
    texto_area.delete("1.0", tk.END)
    try:
        if not os.path.exists("steam_games.csv"):
            texto_area.insert(tk.END, "No se encontró el archivo 'steam_games.csv'.\n")
            return
        df = pd.read_csv("steam_games.csv")
        texto_area.insert(tk.END, df.head(50).to_string(index=False))
        texto_area.insert(tk.END, f"\n\nMostrando 50 primeras filas de {len(df)} totales.")
    except Exception as e:
        texto_area.insert(tk.END, f"Error al cargar datos: {e}\n")

boton2 = tk.Button(
    frame_botones,
    text="Cargar datos del CSV",
    width=30,
    height=2,
    bg=color_boton,
    fg=color_acento,
    font=fuente_normal,
    relief="raised",
    activebackground="#00A86B",
    activeforeground="white",
    command=cargar_datos
)
boton2.grid(row=0, column=1, padx=20, pady=10)

frame_texto = tk.Frame(principal, background=color_fondo, bd=2, relief="groove")

# --- Scrollbar ---
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

def limpiar_texto():
    texto_area.delete("1.0", tk.END)

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
    command=limpiar_texto
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


