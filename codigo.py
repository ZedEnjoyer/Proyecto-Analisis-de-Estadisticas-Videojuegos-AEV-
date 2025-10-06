import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('steam_games.csv')

# Ver las primeras filas del dataset
print("📄 Primeras filas del dataset:")
print(df.head())

# Estadísticas generales (precio y metacritic)
print("\n📊 Estadísticas generales:")
print(df[['precio', 'metacritic']].describe())

# Juego con mejor puntuación Metacritic
mejor_juego = df[df['metacritic'] == df['metacritic'].max()]
print("\n🏆 Juego con mejor puntuación Metacritic:")
print(mejor_juego[['titulo', 'metacritic']])

# Juego más caro
juego_mas_caro = df[df['precio'] == df['precio'].max()]
print("\n💸 Juego más caro:")
print(juego_mas_caro[['titulo', 'precio']])

# Precio promedio
precio_promedio = df['precio'].mean()
print(f"\n💰 Precio promedio de los juegos: ${precio_promedio:.2f}")

# Juegos publicados después de 2015
juegos_recientes = df[df['año_de_publicacion'] > 2015]
print("\n🕹️ Juegos publicados después de 2015:")
print(juegos_recientes[['titulo', 'año_de_publicacion']])

# Número de juegos por año
juegos_por_anio = df['año_de_publicacion'].value_counts().sort_index()
print("\n📆 Número de juegos publicados por año:")
print(juegos_por_anio)

# Promedio de Metacritic por año
promedio_metacritic_anual = df.groupby('año_de_publicacion')['metacritic'].mean()
print("\n📈 Promedio de Metacritic por año:")
print(promedio_metacritic_anual)

# Top 5 juegos más caros
top_juegos_caros = df.sort_values(by='precio', ascending=False).head(5)
print("\n💸 Top 5 juegos más caros:")
print(top_juegos_caros[['titulo', 'precio']])
