# ...existing code...
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

CSV_PATH = 'steam_games.csv'

# Intentar leer el CSV con manejo de errores
if not os.path.exists(CSV_PATH):
    print(f"Error: no se encontró el archivo '{CSV_PATH}' en {os.getcwd()}")
    sys.exit(1)

try:
    df = pd.read_csv(CSV_PATH, encoding='utf-8')
except Exception as e:
    print("Error leyendo el CSV:", e)
    try:
        df = pd.read_csv(CSV_PATH, encoding='latin-1')
        print("Leído con encoding latin-1")
    except Exception as e2:
        print("Fallo lectura con latin-1:", e2)
        raise

print("Columnas detectadas:", list(df.columns))

# Mapear nombres de columnas comunes a los usados en el script
col_aliases = {
    'precio': ['precio', 'price', 'price_final', 'final_price'],
    'metacritic': ['metacritic', 'metacritic_score', 'score'],
    'año_de_publicacion': ['año_de_publicacion', 'anio_de_publicacion', 'year', 'release_year', 'release_date']
}

found = {}
for target, variants in col_aliases.items():
    for v in variants:
        if v in df.columns:
            found[target] = v
            break

missing = [k for k in col_aliases.keys() if k not in found]
if missing:
    print("Columnas faltantes (no encontradas):", missing)
    print("Ajusta el CSV o los aliases y vuelve a intentar.")
    # No salir inmediatamente: permitirá mostrar algunas gráficas parciales si hay datos
else:
    # Renombrar a los nombres esperados para el resto del script
    df = df.rename(columns={found['precio']: 'precio', found['metacritic']: 'metacritic', found['año_de_publicacion']: 'año_de_publicacion'})

# Limpiar y convertir tipos si existen
if 'precio' in df.columns:
    # eliminar símbolos de moneda y comas, convertir a float
    df['precio'] = df['precio'].astype(str).str.replace(r'[^\d\.,-]', '', regex=True)
    df['precio'] = df['precio'].str.replace(',', '.', regex=False)  # si usaron coma decimal
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')

if 'metacritic' in df.columns:
    df['metacritic'] = pd.to_numeric(df['metacritic'], errors='coerce')

if 'año_de_publicacion' in df.columns:
    # intentar extraer año si es fecha completa
    try:
        # si la columna contiene fechas, convertir y extraer año
        if df['año_de_publicacion'].dtype == object:
            possible_dates = pd.to_datetime(df['año_de_publicacion'], errors='coerce', dayfirst=True)
            if possible_dates.notna().any():
                df['año_de_publicacion'] = possible_dates.dt.year
            else:
                df['año_de_publicacion'] = pd.to_numeric(df['año_de_publicacion'], errors='coerce')
        else:
            df['año_de_publicacion'] = pd.to_numeric(df['año_de_publicacion'], errors='coerce')
    except Exception:
        df['año_de_publicacion'] = pd.to_numeric(df['año_de_publicacion'], errors='coerce')

# Mostrar estadísticas básicas sólo si existen las columnas
print("\nEstadísticas básicas:")
cols_for_desc = [c for c in ['precio', 'metacritic'] if c in df.columns]
if cols_for_desc:
    print(df[cols_for_desc].describe())
else:
    print("No hay columnas numéricas 'precio' ni 'metacritic' para describir.")

sns.set(style="darkgrid")

# Gráficas con comprobaciones
if 'precio' in df.columns and df['precio'].notna().any():
    plt.figure(figsize=(10,6))
    sns.histplot(df['precio'].dropna(), bins=30, kde=True)
    plt.title('Distribución de Precios de Videojuegos')
    plt.xlabel('Precio')
    plt.ylabel('Cantidad de Juegos')
    plt.grid(True)
    plt.show()
else:
    print("Omitido histograma de precio: columna ausente o sin valores válidos.")

if 'metacritic' in df.columns and df['metacritic'].notna().any():
    plt.figure(figsize=(10,6))
    sns.histplot(df['metacritic'].dropna(), bins=30, color='orange', kde=True)
    plt.title('Distribución de Puntuaciones Metacritic')
    plt.xlabel('Puntuación Metacritic')
    plt.ylabel('Cantidad de Juegos')
    plt.grid(True)
    plt.show()
else:
    print("Omitido histograma de metacritic: columna ausente o sin valores válidos.")

if 'año_de_publicacion' in df.columns and df['año_de_publicacion'].notna().any():
    plt.figure(figsize=(12,7))
    juegos_por_anio = df['año_de_publicacion'].dropna().astype(int).value_counts().sort_index()
    sns.barplot(x=juegos_por_anio.index.astype(str), y=juegos_por_anio.values, palette="viridis")
    plt.title('Número de Juegos Publicados por Año')
    plt.xlabel('Año de Publicación')
    plt.ylabel('Cantidad de Juegos')
    plt.xticks(rotation=45)
    plt.show()

    plt.figure(figsize=(12,7))
    promedio_metacritic_anual = None
    if 'metacritic' in df.columns:
        promedio_metacritic_anual = df.dropna(subset=['año_de_publicacion','metacritic']).groupby('año_de_publicacion')['metacritic'].mean()
    if promedio_metacritic_anual is not None and not promedio_metacritic_anual.empty:
        sns.lineplot(x=promedio_metacritic_anual.index, y=promedio_metacritic_anual.values, marker='o')
        plt.title('Promedio de Puntuación Metacritic por Año')
        plt.xlabel('Año de Publicación')
        plt.ylabel('Puntuación Metacritic Promedio')
        plt.grid(True)
        plt.show()
    else:
        print("Omitido gráfico de promedio metacritic por año: datos insuficientes.")
else:
    print("Omitidos gráficos por año: columna 'año_de_publicacion' ausente o sin valores válidos.")

if 'precio' in df.columns and 'metacritic' in df.columns and df[['precio','metacritic']].dropna().shape[0] > 5:
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=df.dropna(subset=['precio','metacritic']), x='precio', y='metacritic')
    plt.title('Relación entre Precio y Puntuación Metacritic')
    plt.xlabel('Precio')
    plt.ylabel('Puntuación Metacritic')
    plt.grid(True)
    plt.show()
else:
    print("Omitido scatter precio vs metacritic: columnas ausentes o insuficientes datos.")
# ...existing code...