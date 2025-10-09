import tkinter as tk
import os

principal= tk.Tk()
principal.title("analisis de datos de videojuegos")
principal.geometry("500x300")  
principal.configure(background="#201D1D")

etiqueta = tk.Label(principal, text="bienvenido!, ¿que accion deseas realizar?", font=("Arial", 17),background="#201D1D",foreground="white")
etiqueta.pack(pady=20)

def graficas():
    os.system("codigo_graphs.py")

boton = tk.Button(principal, text="analisis de datos",width=20,height=2, command=graficas)
boton.place(x=70,y=100)

def ingresar_datos():
    campo_entrada = tk.Entry(principal)
    campo_entrada.insert(0, "Escribe tus datos aquí...") 
    campo_entrada.pack(pady=10)
    campo_entrada.place(x=190,y=150)
boton2 =tk.Button(principal, text="ingresar datos",width=20,height=2, command=ingresar_datos)
boton2.place(x=280, y=100)

principal.mainloop()
