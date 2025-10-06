import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('steam_games.csv')

# Ver las primeras filas del dataset
print("Primeras filas del dataset:")
print(df.head())

# Estadísticas generales de las columnas numéricas
print("\nEstadísticas generales:")
print(df.describe())

# Análisis del total de ventas por género
print("\nVentas totales por género:")
ventas_por_genero = df.groupby('Género')['Ventas (millones)'].sum()
print(ventas_por_genero)

# Juegos con mejor calificación
print("\nJuegos con mejor calificación:")
mejor_calificacion = df[df['Calificación'] == df['Calificación'].max()]
print(mejor_calificacion[['Nombre', 'Calificación']])

# Juegos lanzados en el siglo XXI (desde el año 2000 en adelante)
print("\nJuegos lanzados en el siglo XXI:")
juegos_siglo_XXI = df[df['Año'] >= 2000]
print(juegos_siglo_XXI[['Nombre', 'Año']])

# Juego más vendido
print("\nJuego más vendido:")
juego_mas_vendido = df[df['Ventas (millones)'] == df['Ventas (millones)'].max()]
print(juego_mas_vendido[['Nombre', 'Ventas (millones)']])

# Juegos lanzados por año
print("\nNúmero de juegos lanzados por año:")
juegos_por_anio = df.groupby('Año').size()
print(juegos_por_anio)
