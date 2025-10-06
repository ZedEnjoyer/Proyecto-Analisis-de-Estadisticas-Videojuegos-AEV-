import pandas as pd

df = pd.read_csv('steam_games.csv')

print("📄 Primeras filas del dataset:")
print(df.head())

print("\nEstadísticas generales:")
print(df[['precio', 'metacritic']].describe())

mejor_juego = df[df['metacritic'] == df['metacritic'].max()]
print("\nJuego con mejor puntuación Metacritic:")
print(mejor_juego[['titulo', 'metacritic']])

juego_mas_caro = df[df['precio'] == df['precio'].max()]
print("\nJuego más caro:")
print(juego_mas_caro[['titulo', 'precio']])

precio_promedio = df['precio'].mean()
print(f"\nPrecio promedio de los juegos: ${precio_promedio:.2f}")

juegos_recientes = df[df['año_de_publicacion'] > 2015]
print("\nJuegos publicados después de 2015:")
print(juegos_recientes[['titulo', 'año_de_publicacion']])

juegos_por_anio = df['año_de_publicacion'].value_counts().sort_index()
print("\n📆 Número de juegos publicados por año:")
print(juegos_por_año)


promedio_metacritic_anual = df.groupby('año_de_publicacion')['metacritic'].mean()
print("\n📈 Promedio de Metacritic por año:")
print(promedio_metacritic_anual)

top_juegos_caros = df.sort_values(by='precio', ascending=False).head(5)
print("\n💸 Top 5 juegos más caros:")
print(top_juegos_caros[['titulo', 'precio']])

