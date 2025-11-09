import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

CSV_PATH = 'steam_games.csv'

# Intentar leer el CSV
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

col_aliases = {
    'precio': ['precio', 'price', 'price_final', 'final_price'],
    'metacritic': ['metacritic', 'metacritic_score', 'score'],
    'año_de_publicacion': ['año_de_publicacion', 'anio_de_publicacion', 'year', 'release_year', 'release_date'],
    'ventas': ['ventas', 'sales', 'copies_sold', 'sold'],
    'genero': ['genero', 'genre', 'category']
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
else:
    df = df.rename(columns={found[k]: k for k in found})

# --- Limpieza ---
if 'precio' in df.columns:
    df['precio'] = df['precio'].astype(str).str.replace(r'[^\d\.,-]', '', regex=True)
    df['precio'] = df['precio'].str.replace(',', '.', regex=False)
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')

for col in ['metacritic', 'ventas', 'año_de_publicacion']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Estilo ---
sns.set(style="darkgrid")

# --- 1️⃣ Promedio de ventas por género ---
if 'genero' in df.columns and 'ventas' in df.columns:
    plt.figure(figsize=(10,6))
    promedio_ventas = df.groupby('genero')['ventas'].mean().sort_values(ascending=False)
    sns.barplot(x=promedio_ventas.index, y=promedio_ventas.values, palette="viridis")
    plt.title("Promedio de Ventas por Género")
    plt.xlabel("Género")
    plt.ylabel("Promedio de Ventas (millones)")
    plt.xticks(rotation=45)
    plt.show()

# --- 2️⃣ Evolución de ventas por año y género ---
if {'año_de_publicacion', 'ventas', 'genero'}.issubset(df.columns):
    plt.figure(figsize=(12,7))
    promedio_anual_genero = df.dropna(subset=['año_de_publicacion', 'ventas', 'genero']).groupby(['año_de_publicacion', 'genero'])['ventas'].mean().reset_index()
    sns.lineplot(data=promedio_anual_genero, x='año_de_publicacion', y='ventas', hue='genero', marker='o')
    plt.title('Evolución de Ventas Promedio por Año y Género')
    plt.xlabel('Año de Publicación')
    plt.ylabel('Ventas Promedio (millones)')
    plt.legend(title='Género', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# --- 3️⃣ Precio vs Ventas ---
if {'precio', 'ventas', 'genero'}.issubset(df.columns):
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=df, x='precio', y='ventas', hue='genero', alpha=0.8)
    plt.title('Relación entre Precio y Ventas por Género')
    plt.xlabel('Precio')
    plt.ylabel('Ventas (millones)')
    plt.legend(title='Género', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# --- 4️⃣ Metacritic por género ---
if {'metacritic', 'genero'}.issubset(df.columns):
    plt.figure(figsize=(10,6))
    sns.boxplot(data=df, x='genero', y='metacritic', palette='Set3')
    plt.title('Distribución de Puntuaciones Metacritic por Género')
    plt.xlabel('Género')
    plt.ylabel('Puntuación Metacritic')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
