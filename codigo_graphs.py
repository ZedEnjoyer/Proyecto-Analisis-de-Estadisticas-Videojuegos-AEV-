import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv('steam_games.csv')

# Mostrar primeras filas
print("Primeras filas del dataset:")
print(df.head())

# Estadísticas básicas
print("\nEstadísticas básicas:")
print(df[['precio', 'metacritic']].describe())

# Gráfico 1: Histograma de precios
plt.figure(figsize=(10,6))
sns.histplot(df['precio'], bins=30, kde=True)
plt.title('Distribución de Precios de Videojuegos')
plt.xlabel('Precio')
plt.ylabel('Cantidad de Juegos')
plt.grid(True)
plt.show()

# Gráfico 2: Distribución de Metacritic
plt.figure(figsize=(10,6))
sns.histplot(df['metacritic'], bins=30, color='orange', kde=True)
plt.title('Distribución de Puntuaciones Metacritic')
plt.xlabel('Puntuación Metacritic')
plt.ylabel('Cantidad de Juegos')
plt.grid(True)
plt.show()

# Gráfico 3: Juegos por año de publicación (barras)
plt.figure(figsize=(12,7))
juegos_por_anio = df['año_de_publicacion'].value_counts().sort_index()
sns.barplot(x=juegos_por_anio.index, y=juegos_por_anio.values, palette="viridis")
plt.title('Número de Juegos Publicados por Año')
plt.xlabel('Año de Publicación')
plt.ylabel('Cantidad de Juegos')
plt.xticks(rotation=45)
plt.show()

# Gráfico 4: Promedio de Metacritic por año (línea)
plt.figure(figsize=(12,7))
promedio_metacritic_anual = df.groupby('año_de_publicacion')['metacritic'].mean()
sns.lineplot(x=promedio_metacritic_anual.index, y=promedio_metacritic_anual.values, marker='o')
plt.title('Promedio de Puntuación Metacritic por Año')
plt.xlabel('Año de Publicación')
plt.ylabel('Puntuación Metacritic Promedio')
plt.grid(True)
plt.show()

# Gráfico 5: Precio vs Metacritic (scatter plot)
plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='precio', y='metacritic')
plt.title('Relación entre Precio y Puntuación Metacritic')
plt.xlabel('Precio')
plt.ylabel('Puntuación Metacritic')
plt.grid(True)
plt.show()
