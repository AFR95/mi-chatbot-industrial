import pandas as pd
import numpy as np
import sys
import os

# Importar funciones desde app.py
sys.path.append('.')
from app import limpiar_datos, normalizar_datos  # Importa tus funciones

print("📊 Cargando datos...")
df = pd.read_excel('HISTORICO_INCIDENCIAS.xlsx', sheet_name='Guardias')
print(f"📄 Datos cargados: {len(df)} filas")

print("🧹 Limpiando datos...")
df = limpiar_datos(df)
print(f"✅ Datos limpios: {len(df)} filas")

print("🔤 Normalizando...")
df = normalizar_datos(df)
print("✅ Normalización completada")

# Guardar datos procesados
df.to_pickle('datos_procesados.pkl')
print(f"💾 Datos guardados: datos_procesados.pkl")

print("🤖 Cargando modelo SentenceTransformer...")
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
print("✅ Modelo cargado")

print("🧮 Generando embeddings...")
embeddings = model.encode(df['error'].tolist(), show_progress_bar=True)
print(f"✅ Embeddings generados: {embeddings.shape}")

np.save('embeddings.npy', embeddings)
print(f"💾 Embeddings guardados: embeddings.npy ({embeddings.shape[0]} docs x {embeddings.shape[1]} dims)")

print("🎉 ¡PRE-GENERADOS COMPLETOS!")
print("Archivos creados:")
print("- datos_procesados.pkl (~100KB)")
print("- embeddings.npy (~1MB)")
print("Sube ambos a GitHub y la carga será <10s")
