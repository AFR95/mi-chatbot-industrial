ƒimport streamlit as st
import pandas as pd
try:
    import pysqlite3
    import sys
    sys.modules["sqlite3"] = pysqlite3
except ImportError:
    pass

import chromadb
from sentence_transformers import SentenceTransformer
import logging
import re
from fuzzywuzzy import process
import openai  # Import completo para v0.28.1
import os
import tempfile
from datetime import datetime
import httpx

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# === Carga API KEY con st.secrets ===
api_key = st.secrets.get("XAI_API_KEY")

if not api_key:
    st.error("❌ **Error de configuración**: No se encontró la clave `XAI_API_KEY` en secrets.")
    st.warning("⚠️ La app funcionará en modo **fallback** (sin IA generativa).")
    st.info("**Solución**: Ve a Streamlit Cloud → Manage app → Settings → Secrets → Add: `XAI_API_KEY`")
    # No usar st.stop() - permitir que la app continúe
    HAS_XAI = False
else:
    HAS_XAI = True
    st.success("✅ API de xAI configurada correctamente.")
    openai.api_key = api_key

# === FUNCIÓN: Llamada directa a Grok API con httpx ===
def llamar_grok(prompt):
    """Llama directamente a la API de xAI (Grok) usando httpx"""
    if not HAS_XAI:
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "grok-3",   # Modelo estable de xAI
        "messages": [
            {
                "role": "system", 
                "content": "Eres un asistente técnico especializado en mantenimiento industrial. Responde de forma clara y profesional."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 250,
        "temperature": 0.7
    }
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()  # Error si no es 200
        
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    
    except httpx.TimeoutException:
        logging.error("⏱️ Timeout al llamar a xAI API")
        st.error("❌ Timeout: la API de xAI no respondió a tiempo.")
        return None
    except httpx.HTTPStatusError as e:
        logging.error(f"⚠️ Error HTTP {e.response.status_code}: {e.response.text}")
        st.error(f"❌ Error HTTP {e.response.status_code} en la API de xAI")
        st.code(e.response.text, language="json")
        return None
    except Exception as e:
        logging.error(f"🔥 Error inesperado en xAI API: {e}")
        st.error(f"❌ Error inesperado al conectar con la API de xAI: {e}")
        return None
        
# === Diccionarios globales ===
diccionario_equipos = {
    'aljibe': 'aljibe',
    'aguasineras': 'aguasineras',
    'almacen frio': 'almacén frío',
    'r05': 'robot 5', 'r5': 'robot 5', 'ro5': 'robot 5',
    'robot paletizado': 'robot 5', 'robot de paletizado': 'robot 5',
    'paletizador': 'robot 5', 'paletizadora': 'robot 5', 'paletizador 1': 'robot 5',
    'dosificador 3': 'dosificador 03', 'dosif 3': 'dosificador 03',
    'aplicacion circutor': 'circutor',
    'aplicacion etiquetado sacos': 'etiquetadora sacos',
    'armario central': 'armario central',
    'basculas': 'básculas',
    'botella': 'envasadora botella',
    'caldera': 'caldera', 'caldera 2 y 3': 'caldera', 'caldera 3': 'caldera',
    'camara congelados polivalentes matadero': 'cámara congelados',
    'camara vision artificial meurer encajadora b': 'visión artificial',
    'cañon simon': 'cañón simón',
    'cap30 de la j': 'cap30',
    'carro expediciones': 'carro expediciones',
    'cip': 'cip', 'cip de limpieza': 'cip', 'cip llenadora b': 'cip',
    'cip mantequera': 'cip', 'cip mantequilla': 'cip', 'cip procesos': 'cip',
    'cip recepcion': 'cip', 'cip recepcion sistein': 'cip',
    'cliente 172166241': 'scada cliente',
    'cliente scada friobuco': 'scada friobuco',
    'colector vapor aporte a ctc pretanque': 'colector vapor',
    'comunicacion envio sosa y acido': 'sistema sosa ácido',
    'conductimetro': 'conductimetro', 'conductimetro leche interna': 'conductimetro',
    'covap': 'covap',
    'datos informes': 'sistema informes',
    'dematic': 'dematic', 'dematic isla': 'dematic', 'isla dematic': 'dematic',
    'depuradora': 'depuradora', 'depuradora matadero': 'depuradora',
    'depurardora armario central': 'depuradora',
    'electrovia': 'electrovía',
    'encajadora': 'encajadora', 'encajadora j': 'encajadora',
    'enfardadora': 'enfardadora', 'enfardadora 1': 'enfardadora',
    'enfardadoras': 'enfardadora',
    'ensacadora': 'ensacadora', 'ensacado': 'ensacadora',
    'envasadora': 'envasadora', 'envasadora a': 'envasadora',
    'envasadoras': 'envasadora',
    'entrada ip50': 'ip50', 'entrada ip50 mt54': 'ip50',
    'equipos uht': 'uht',
    'etiqueta covap entera 1l': 'etiquetadora',
    'etiquetadora': 'etiquetadora', 'etiquetadora 2': 'etiquetadora',
    'etiquetadoras': 'etiquetadora',
    'etiquetadora ensacadora linea 2': 'etiquetadora',
    'etiquetadora linea 2': 'etiquetadora',
    'etiquetadora sacos linea 2': 'etiquetadora',
    'expediciones x2': 'expediciones',
    'fallo aplicacion etiquetado': 'etiquetadora',
    'fermentos': 'fermentos',
    'granuladora': 'granuladora',
    'granuladoras': 'granuladora',
    'hmi pretanque': 'hmi pretanque',
    'horno m': 'horno',
    'indago': 'visión indago',
    'ip50': 'ip50',
    'isla': 'isla', 'isla enfardado': 'isla',
    'lecturas': 'sistema lecturas',
    'linea a': 'línea a',
    'linea profibus pa leche interna': 'profibus',
    'linea sacrificio vacuno': 'línea sacrificio',
    'liquidos': 'líquidos',
    'mantequilla': 'mantequilla', 'mantequilla light': 'mantequilla',
    'meira control': 'meira control', 'programa meira control': 'meira control',
    'mes': 'mes', 'sistema mes': 'mes',
    'mesa mt125': 'mesa mt125', 'mesa mt135': 'mesa mt135',
    'mezcladora': 'mezcladora', 'mezcladora 1': 'mezcladora',
    'molinos': 'molinos',
    'mt124': 'mt124', 'mt37': 'mt37',
    'pajitera': 'pajitera',
    'pc scada envasadoras': 'scada', 'pc scadas izquierda': 'scada',
    'scada principal frio': 'scada',
    'scada proleit': 'proleit',
    'periferia analogicas lcp001': 'periferia lcp001',
    'planta estatica': 'planta estática',
    'planta estatica control': 'planta estática',
    'planta estatica equipos': 'planta estática',
    'plc depuradora matadero': 'plc depuradora', 'plc2 cip mantequera': 'plc cip',
    'plcs': 'plc',
    'premix': 'premix', 'silo 216 premix': 'premix', 'transporte premix': 'premix',
    'pretanque': 'pretanque',
    'procesos': 'procesos',
    'proleit': 'proleit', 'proleitcip tanque mezclas 369': 'proleit',
    'r6': 'robot 6', 'robot 01': 'robot 1', 'robot 02': 'robot 2',
    'robot 03': 'robot 3', 'robot 05': 'robot 5', 'robot 06': 'robot 6',
    'robot 1': 'robot 1', 'robot 2': 'robot 2', 'robot 3': 'robot 3',
    'robot 4': 'robot 4', 'robot 5': 'robot 5', 'robot 6': 'robot 6',
    'robot colaborativo tarrinas': 'robot tarrinas',
    'robots': 'robots',
    'rompedora': 'rompedora', 'rompedora hsm': 'rompedora',
    'sad cogeneracion': 'cogeneración',
    'sala control expedicionestrasloscarros': 'sala control',
    'sala rv': 'sala rv',
    'scada': 'scada', 'scada ctc': 'scada', 'scada frio buco': 'scada',
    'scada mantequilla': 'scada', 'scada principal': 'scada',
    'servidor': 'servidor', 'servidor cogeneracion': 'servidor',
    'servidor sad': 'servidor',
    'silo': 'silo', 'silo 8': 'silo',
    'silos de sosa y acido': 'sistema sosa ácido',
    'sistema etiquetado': 'etiquetadora',
    'software etiquetado': 'etiquetadora',
    'sonda de temperatura': 'sonda temperatura',
    'tanque aseptico': 'tanque aséptico', 'tanque aseptico 6': 'tanque aséptico',
    'tanque 2 de fermentos': 'tanque fermentos',
    'transportes piensosmezclas de premix': 'premix',
    'turbidimetros': 'turbidímetros', 'turbidimetros leche interna': 'turbidímetros',
    'uht': 'uht',
    'v artificial batido': 'visión artificial',
    'variadores': 'variadores',
    'varios equipos': 'varios equipos',
    'vision artificial': 'visión artificial',
    'vision artificial bcnvision': 'visión artificial',
    'vision artificial combi': 'visión artificial',
    'vision artificial linea l': 'visión artificial',
    'vision artificial m': 'visión artificial',
    'vision artificial rafavision': 'visión artificial',
    'vision artificial rafavision batido': 'visión artificial',
    'vision artificial rafavision pastillas': 'visión artificial',
    'vision artificial sig': 'visión artificial',
    'vision artificial tarrinas': 'visión artificial',
    'rafavision': 'visión artificial', 'rafavision b': 'visión artificial',
    'rafavision batido': 'visión artificial',
    'rafavision pastillas': 'visión artificial',
    'rafavision tarrinas': 'visión artificial',
    'visión indago': 'visión indago',
    'vision indago': 'visión indago',
    'vision m': 'visión artificial',
    'vtis100': 'vtis100',
    'zona encartonado': 'zona encartonado',
    'zona encartonado 1 l': 'zona encartonado',
    'zona encartonado batido': 'zona encartonado',
    'zona frio': 'zona frío',
    'zona mezclas': 'zona mezclas',
    'zona mezclas linea elaboracion 2': 'zona mezclas'
}

diccionario_plantas = {
    'lacteos': 'lácteos', 'piensos': 'piensos', 'iot': 'iot', 'naturleite': 'naturleite',
    'ibericos': 'ibéricos', 'cogeneracion': 'cogeneración', 'ctc': 'ctc',
    'mezclas': 'mezclas', 'zona mantequilla': 'zona mantequilla',
    'zona frio buco': 'zona frío buco', 'scada mantequilla': 'zona mantequilla',
    'scada frio buco': 'zona frío buco', 'frio buco': 'zona frío buco',
    'mantequera': 'zona mantequilla'
}

# === Utilidades ===
def normalizar_texto(texto):
    if pd.isna(texto):
        return 'no especificado'
    texto = str(texto).strip().lower()
    texto = re.sub(r'[áàäâ]', 'a', texto)
    texto = re.sub(r'[éèëê]', 'e', texto)
    texto = re.sub(r'[íìïî]', 'i', texto)
    texto = re.sub(r'[óòöô]', 'o', texto)
    texto = re.sub(r'[úùüû]', 'u', texto)
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

# === Cargar datos ===
def cargar_datos(archivo, sheet_name='Guardias'):
    try:
        df = pd.read_excel(archivo, sheet_name=sheet_name)
        logging.info(f"Cargada sheet '{sheet_name}' con {len(df)} filas")
        return df
    except Exception as e:
        logging.error(f"Error al cargar {archivo}: {e}")
        raise

# === Limpiar datos ===
def limpiar_datos(df):
    df.columns = df.columns.str.strip().str.lower()
    columnas_map = {
        'planta': ['planta', 'site', 'ubicación', 'location'],
        'equipo': ['equipo', 'maquina', 'máquina', 'equipment', 'machine'],
        'error': ['error', 'problema', 'fallo', 'issue', 'problem'],
        'solución': ['solución', 'solucion', 'resolución', 'resolution', 'solution'],
        '¿es necesario?': ['¿es necesario?', 'es necesario', 'necesario', 'required', 'is required']
    }
    for col_esperada, col_posibles in columnas_map.items():
        for col_posible in col_posibles:
            if col_posible in df.columns:
                df = df.rename(columns={col_posible: col_esperada})
                break
    columnas_utiles = ['planta', 'equipo', 'error', 'solución', '¿es necesario?']
    missing_cols = [col for col in columnas_utiles if col not in df.columns]
    if missing_cols:
        logging.error(f"Faltan columnas: {missing_cols}")
        raise KeyError(f"Faltan columnas: {missing_cols}")
    df = df[columnas_utiles].copy()
    df = df.dropna(how='all').dropna(subset=['equipo', 'error'])
    df['solución'] = df['solución'].fillna('no especificada')
    df['¿es necesario?'] = df['¿es necesario?'].str.strip().str.upper().eq('SÍ')
    df = df[df['¿es necesario?']]
    df = df.drop_duplicates(subset=['error', 'solución'])
    logging.info(f"Datos limpios: {len(df)} filas")
    return df

# === Normalizar datos ===
def normalizar_datos(df):
    def aplicar_diccionario(valor, diccionario):
        valor = normalizar_texto(valor)
        if valor not in diccionario:
            logging.warning(f"Valor no mapeado: {valor}")
        return diccionario.get(valor, valor)

    for col in ['planta', 'equipo', 'error', 'solución']:
        df[col] = df[col].apply(normalizar_texto)
    df['equipo'] = df['equipo'].apply(lambda x: aplicar_diccionario(x, diccionario_equipos))
    df['planta'] = df['planta'].apply(lambda x: aplicar_diccionario(x, diccionario_plantas))
    logging.info("Normalización completada")
    return df

# === Indexar en Chroma ===
def indexar_chroma(df, model_name='paraphrase-multilingual-MiniLM-L12-v2', db_path='./chroma_db'):
    model = SentenceTransformer(model_name)
    df_unique = df.drop_duplicates(subset=['error', 'solución', 'planta', 'equipo'])
    logging.info(f"Datos deduplicados: {len(df_unique)} filas")
    embeddings = model.encode(df_unique['error'].tolist(), show_progress_bar=True)
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name='incidencias', metadata={'hnsw:space': 'cosine'})
    if collection.count() > 0:
        all_ids = collection.get()['ids']
        collection.delete(ids=all_ids)
    ids = [f'doc_{i}' for i in range(len(df_unique))]
    metadatos = [{
        'planta': row['planta'],
        'equipo': row['equipo'],
        'solución': row['solución'],
        'requiere_ingenieria': str(row['¿es necesario?'])
    } for _, row in df_unique.iterrows()]
    collection.add(
        embeddings=embeddings.tolist(),
        documents=df_unique['error'].tolist(),
        metadatas=metadatos,
        ids=ids
    )
    logging.info(f"Indexados {collection.count()} documentos en Chroma")
    return collection

# === Parsear consulta ===
def parse_query(query):
    query = normalizar_texto(query)
    planta = None
    equipo = None
    plantas = ['lacteos', 'piensos', 'iot', 'naturleite', 'cogeneracion', 'ctc', 'mezclas', 'ibericos', 'zona mantequilla', 'zona frio buco']
    equipos = ['aljibe', 'dematic', 'robots', 'robot 1', 'robot 2', 'robot 3', 'robot 4', 'robot 5', 'robot 6', 'visión artificial', 'etiquetadora', 'envasadora', 'scada', 'cip', 'caldera', 'conductimetro', 'ensacadora', 'tanque aseptico', 'uht', 'proleit', 'pretanque', 'servidor', 'plc', 'plc cip', 'plc depuradora']
    equipos_extendidos = {
        'aljibe': ['aljibe', 'bomba del aljibe', 'bombas del aljibe'],
        'robot': ['robot', 'robots', 'robot paletizado', 'robot de paletizado'],
        'robot 1': ['robot 1', 'robot 01'],
        'robot 2': ['robot 2', 'robot 02'],
        'robot 3': ['robot 3', 'robot 03'],
        'robot 4': ['robot 4', 'robot 04'],
        'robot 5': ['robot 5', 'robot 05', 'r05', 'r5', 'ro5', 'paletizador', 'paletizador 1', 'paletizadora'],
        'robot 6': ['robot 6', 'robot 06', 'r6'],
        'etiquetadora': ['etiquetadora', 'etiquetadoras', 'sistema etiquetado'],
        'envasadora': ['envasadora', 'envasadoras', 'envasadora botella'],
        'scada': ['scada', 'scada principal', 'scada ctc', 'scada wincc', 'scada proleit'],
        'cip': ['cip', 'cip de limpieza', 'cip recepcion'],
        'caldera': ['caldera', 'caldera 2 y 3', 'caldera 3'],
        'plc': ['plc', 'plcs', 'plc de comunicaciones', 'plc calderas']
    }
    # Fuzzy matching para planta
    planta_match = process.extractOne(query, plantas, score_cutoff=80)
    if planta_match:
        planta = planta_match[0]
        for p in plantas:
            if p in diccionario_plantas and diccionario_plantas[p] == diccionario_plantas.get(planta, planta):
                query = re.sub(r'\b' + re.escape(p) + r'\b', '', query)
        query = re.sub(r'\b' + re.escape(planta_match[0]) + r'\b', '', query).strip()
    # Fuzzy matching para equipo
    for key, aliases in equipos_extendidos.items():
        alias_match = process.extractOne(query, aliases + [key], score_cutoff=80)
        if alias_match:
            equipo = key
            query = re.sub(r'\b' + re.escape(alias_match[0]) + r'\b', '', query).strip()
            break
    if not equipo:
        equipo_match = process.extractOne(query, equipos, score_cutoff=80)
        if equipo_match:
            equipo = equipo_match[0]
            query = re.sub(r'\b' + re.escape(equipo_match[0]) + r'\b', '', query).strip()
    
    stop_words = [' en ', ' de ', ' para ', ' con ', ' a ', ' el ', ' la ', ' los ', ' las ']
    clean_query = query
    for word in stop_words:
        clean_query = re.sub(r'\b' + re.escape(word.strip()) + r'\b', '', clean_query)
    clean_query = re.sub(r'\b[0-6]\b', '', clean_query)
    clean_query = re.sub(r'\s+', ' ', clean_query).strip()
    if not clean_query:
        clean_query = 'fallo'
    if not planta:
        planta = 'lácteos'
    planta = diccionario_plantas.get(planta, planta)
    equipo = diccionario_equipos.get(equipo, equipo)
    return planta, equipo, clean_query

# === Generar respuesta elaborada con xAI API (httpx) ===
def generar_respuesta_elaborada(query, planta, equipo, results):
    resultados_str = "\n".join([
        f"- Error: {doc}, Solución: {meta['solución']}, Planta: {meta['planta']}, "
        f"Equipo: {meta['equipo']}, Distancia: {dist:.3f}, Requiere Ingeniería: {meta['requiere_ingenieria']}"
        for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0])
    ])
    if not resultados_str:
        resultados_str = "No se encontraron incidencias relevantes."

    prompt = f"""Eres un asistente técnico especializado en mantenimiento industrial. He ejecutado una consulta sobre incidencias en una planta industrial, y obtuve los siguientes resultados de una base de datos de incidencias:

**Consulta**: '{query}'
**Planta**: '{planta}'
**Equipo**: '{equipo}'
**Resultados**:
{resultados_str}

**Instrucciones**:
1. Resume las incidencias más relevantes (prioriza las de menor distancia, e.g., distancia < 0.75).
2. Genera una respuesta en lenguaje natural en español que:
   - Explique el problema identificado en la consulta.
   - Proporcione una lista numerada de 2-3 pasos para resolver el problema, basada en las soluciones de las incidencias, consolidando soluciones similares.
   - Incluya detalles específicos como IPs, componentes (e.g., HMI, PLC, variador), o verificaciones adicionales (e.g., cables, logs, fusibles).
   - Indique si se requiere intervención de ingeniería (basado en `requiere_ingenieria='True'`).
   - Si no hay resultados relevantes, sugiere pasos genéricos de diagnóstico (e.g., verificar conexiones, reiniciar equipo).
3. Usa un tono profesional pero claro, como si estuvieras guiando a un técnico en planta.
4. Si hay incidencias con distancia alta (> 0.75), ignóralas a menos que sean las únicas disponibles.
5. Limita la respuesta a 250 palabras para que sea concisa.

**Formato de Salida**:
**Problema**: [Descripción clara del problema basado en la consulta y los errores]
**Pasos para Resolver**:
1. [Paso 1 consolidado con detalles específicos]
2. [Paso 2, si aplica]
3. [Paso 3, si aplica]
**Notas**:
- [Mencionar si requiere ingeniería o precauciones adicionales]
- [Si no hay resultados, indicar que no se encontraron incidencias y sugerir pasos genéricos]
"""

    # Intentar con xAI
    if HAS_XAI:
        respuesta_xai = llamar_grok(prompt)
        if respuesta_xai:
            st.info("🤖 Respuesta generada por xAI (Grok)")
            return respuesta_xai

    # Fallback si xAI falla o no está disponible
    logging.warning("Usando fallback - xAI no disponible")
    st.warning("⚠️ Modo fallback: Respuesta basada en histórico (sin IA generativa)")
    
    if not results['documents'][0]:
        return f"""
**Problema**: No se encontraron incidencias relevantes para el equipo '{equipo}' en la planta '{planta}' con el problema descrito ('{query}').

**Pasos para Resolver**:
1. Verifica las conexiones físicas del equipo (cables de red, alimentación, fusibles).
2. Reinicia el equipo o su controlador (PLC, servidor, variador) si es seguro.
3. Consulta los logs del sistema y verifica la configuración de red.
4. Contacta al equipo de ingeniería para diagnóstico avanzado.

**Notas**:
- Se recomienda intervención de ingeniería.
- Verifica si el equipo está configurado correctamente en SCADA.
- xAI no disponible - respuesta automática.
"""
    else:
        relevant_results = [
            (doc, meta['solución'], dist)
            for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0])
            if dist < 0.75
        ]
        if not relevant_results:
            relevant_results = [
                (doc, meta['solución'], dist)
                for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0])
            ][:3]
        
        # Agrupar por tipo de solución
        pasos = []
        tipos = {'reinicio': False, 'configuracion': False, 'hardware': False}
        
        for doc, solucion, dist in relevant_results:
            if 'reinicia' in solucion.lower() and not tipos['reinicio']:
                pasos.append("1. Reinicia el servidor SCADA (IP: 172.16.6.240 o 172.16.1.240) y conéctate por web. Si no responde, reinicia el servidor físico o la máquina virtual WinCC2k16 en el host ESXi.")
                tipos['reinicio'] = True
            elif 'configuracion' in solucion.lower() or 'red' in solucion.lower() and not tipos['configuracion']:
                pasos.append("2. Verifica la configuración de red y variadores. Revisa cables, switches, y logs del sistema para identificar fallos de comunicación.")
                tipos['configuracion'] = True
            elif 'motor' in solucion.lower() or 'hardware' in solucion.lower() and not tipos['hardware']:
                pasos.append("3. Inspecciona componentes de hardware (motores, fusibles, PLC). Sustituye elementos defectuosos si es necesario.")
                tipos['hardware'] = True
            elif len(pasos) < 3:
                pasos.append(f"3. {solucion}")
        
        pasos_str = "\n".join(pasos[:3]) if pasos else "No hay soluciones específicas disponibles."
        problema = f"El equipo '{equipo}' en la planta '{planta}' presenta un problema de {query.lower()}."
        respuesta = f"""
**Problema**: {problema}

**Pasos para Resolver**:
{pasos_str}

**Notas**:
- Todas las soluciones requieren intervención de ingeniería.
- Verifica la conectividad de red, switches, y logs del sistema si el problema persiste.
- xAI no disponible - respuesta basada en histórico.
"""
        return respuesta

# === NUEVA FUNCIÓN PARA ACTUALIZAR BASE DE DATOS ===
def actualizar_base_datos(uploaded_file):
    """Actualiza la base de datos con un nuevo archivo Excel"""
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Cargar y procesar datos
        df = cargar_datos(tmp_file_path, sheet_name='Guardias')
        df = limpiar_datos(df)
        df = normalizar_datos(df)
        
        # Guardar dataset limpio
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_salida = f"dataset_limpio_actualizado_{timestamp}.xlsx"
        df.to_excel(archivo_salida, index=False)
        
        # Reindexar Chroma
        collection = indexar_chroma(df)
        
        # Limpiar archivo temporal
        os.unlink(tmp_file_path)
        
        logging.info(f"Base de datos actualizada con {len(df)} incidencias")
        return collection, df, archivo_salida
        
    except Exception as e:
        logging.error(f"Error al actualizar base de datos: {e}")
        st.error(f"❌ Error al procesar el archivo: {e}")
        return None, None, None

# === INTERFAZ STREAMLIT ===
st.title("🤖 Chatbot de Incidencias Industriales")
st.markdown("---")

# Sidebar para configuración y actualizaciones
with st.sidebar:
    # === TEST de conexión con xAI ===
    st.header("🔑 Testear conexión con xAI")
    if HAS_XAI and st.button("Probar conexión con Grok"):
        st.info("⏳ Probando conexión con xAI...")
        test_prompt = "Dime en una frase qué hace un PLC en una planta industrial."
        respuesta_test = llamar_grok(test_prompt)
        if respuesta_test:
            st.success("✅ Conexión correcta con xAI")
            st.write("**Respuesta de prueba:**")
            st.markdown(f"> {respuesta_test}")
        else:
            st.error("❌ No se pudo conectar con xAI. Revisa tu API Key o logs.")
    st.header("⚙️ Configuración")
    
    # Estado de xAI
    if HAS_XAI:
        st.success("🤖 xAI (Grok) **ACTIVA**")
    else:
        st.warning("⚠️ xAI **DESACTIVADA** - Modo fallback")
        st.info("Configura `XAI_API_KEY` en Secrets para activar IA generativa")
    
    # Upload de nuevos archivos
    st.header("📁 Actualizar Base de Datos")
    uploaded_file = st.file_uploader(
        "Subir nuevo histórico de incidencias",
        type=['xlsx'],
        help="Selecciona un archivo Excel con la hoja 'Guardias'"
    )
    
    if uploaded_file is not None:
        # Mostrar info del archivo
        file_details = {
            "Nombre": uploaded_file.name,
            "Tamaño": f"{uploaded_file.size / 1024:.1f} KB",
            "Tipo": uploaded_file.type
        }
        st.json(file_details)
        
        if st.button("🔄 Actualizar Base de Datos", type="primary"):
            with st.spinner("Procesando nuevo archivo..."):
                new_collection, new_df, archivo_generado = actualizar_base_datos(uploaded_file)
                
                if new_collection:
                    # Actualizar session_state
                    st.session_state.collection = new_collection
                    st.session_state.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                    st.session_state.df_actual = new_df
                    st.session_state.ultima_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    st.success(f"✅ **Base de datos actualizada exitosamente!**")
                    st.info(f"📊 Nuevas incidencias: {len(new_df)}")
                    st.info(f"💾 Dataset guardado: `{archivo_generado}`")
                    st.info(f"🕒 Última actualización: {st.session_state.ultima_actualizacion}")
                else:
                    st.error("❌ Falló la actualización. Revisa los logs.")

# === ESTADO DE LA APLICACIÓN ===
if 'collection' not in st.session_state:
    st.info("🚀 **Cargando sistema**...")
    with st.spinner("Inicializando..."):
        try:
            # PRIORIDAD 1: INTENTAR PRE-GENERADOS (RÁPIDO)
            if os.path.exists('datos_procesados.pkl') and os.path.exists('embeddings.npy'):
                st.info("⚡ Cargando pre-generados...")
                
                # Cargar datos procesados
                import pickle
                import numpy as np
                df = pd.read_pickle('datos_procesados.pkl')
                embeddings = np.load('embeddings.npy')
                
                st.session_state.df_actual = df
                st.session_state.ultima_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Cargar modelo
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                st.session_state.model = model
                
                # Reconstruir ChromaDB (rápido, en memoria)
                import chromadb
                client = chromadb.Client()  # En memoria para velocidad
                collection = client.create_collection('incidencias')
                
                # Agregar documentos únicos
                df_unique = df.drop_duplicates(subset=['error']).reset_index(drop=True)
                ids = [f'doc_{i}' for i in range(len(df_unique))]
                metadatos = [{
                    'planta': row['planta'],
                    'equipo': row['equipo'],
                    'solución': row['solución'],
                    'requiere_ingenieria': str(row['¿es necesario?'])
                } for _, row in df_unique.iterrows()]
                
                # Usar embeddings pre-generados
                collection.add(
                    embeddings=embeddings[:len(df_unique)].tolist(),
                    documents=df_unique['error'].tolist(),
                    metadatas=metadatos,
                    ids=ids
                )
                
                st.session_state.collection = collection
                st.success(f"⚡ Pre-generados cargados! ({len(df)} incidencias, {len(ids)} únicos)")
                
            else:
                # FALLBACK: INDEXACIÓN ORIGINAL (lenta)
                st.info("🔄 Indexación inicial...")
                archivo_entrada = "HISTORICO_INCIDENCIAS.xlsx"
                if not os.path.exists(archivo_entrada):
                    st.error(f"❌ Archivo `{archivo_entrada}` no encontrado.")
                    st.stop()
                    
                df = cargar_datos(archivo_entrada)
                df = limpiar_datos(df)
                df = normalizar_datos(df)
                st.session_state.collection = indexar_chroma(df)
                st.session_state.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                st.session_state.df_actual = df
                st.session_state.ultima_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.success("✅ Indexación completada.")
                
        except Exception as e:
            st.error(f"❌ Error carga: {e}")
            st.stop()
else:
    # Mostrar métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Incidencias", len(st.session_state.df_actual))
    with col2:
        st.metric("🏭 Plantas", len(st.session_state.df_actual['planta'].unique()))
    with col3:
        st.metric("⚙️ Equipos", len(st.session_state.df_actual['equipo'].unique()))
    
    st.caption(f"🕒 Última actualización: {st.session_state.ultima_actualizacion}")
st.markdown("---")

# Input de consulta
st.header("💬 Consulta de Incidencias")
query = st.text_input(
    "Ingrese su consulta (ej: 'scada cogeneracion no funciona'):",
    placeholder="Escribe aquí tu problema..."
)

if st.button("🔍 Consultar", type="primary") and query.strip():
    with st.spinner("Analizando incidencia..."):
        try:
            planta, equipo, clean_query = parse_query(query)
            
            # Mostrar parsing
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"🏭 **Planta**: {planta}")
            with col2:
                st.info(f"⚙️ **Equipo**: {equipo}")
            with col3:
                st.info(f"🔍 **Consulta**: {clean_query}")
            
            query_emb = st.session_state.model.encode([clean_query]).tolist()
            where_clause = {}
            
            if equipo or planta:
                where_conditions = [{"requiere_ingenieria": 'True'}]
                if equipo:
                    where_conditions.append({"equipo": equipo})
                if planta:
                    where_conditions.append({"planta": planta})
                where_clause = {"$and": where_conditions}
            
            results = st.session_state.collection.query(
                query_embeddings=query_emb,
                n_results=10,
                where=where_clause if where_clause else None
            )
            
            respuesta = generar_respuesta_elaborada(query, planta, equipo, results)
            
        except Exception as e:
            st.error(f"❌ Error al procesar consulta: {e}")
            respuesta = f"Lo siento, ocurrió un error técnico: {e}"
    
    # Mostrar respuesta
    st.markdown("### 📋 Respuesta del Sistema:")
    st.markdown(respuesta)
    
    # ✅ CORREGIDO: Mover este bloque DENTRO del if
    with st.expander("🔍 Ver detalles técnicos (resultados de búsqueda)", expanded=False):
        if 'results' in locals() and results['documents'][0]:
            results_df = pd.DataFrame({
                'Error': results['documents'][0],
                'Solución': [m['solución'] for m in results['metadatas'][0]],
                'Planta': [m['planta'] for m in results['metadatas'][0]],
                'Equipo': [m['equipo'] for m in results['metadatas'][0]],
                'Distancia': results['distances'][0],
                'Relevancia': ['Alta' if d < 0.5 else 'Media' if d < 0.75 else 'Baja' for d in results['distances'][0]]
            })
            
            def highlight_relevant(row):
                try:
                    distancia = float(row['Distancia'])
                    if distancia < 0.5:
                        return ['background-color: #d4edda'] * len(row)
                    elif distancia < 0.75:
                        return ['background-color: #fff3cd'] * len(row)
                    else:
                        return ['background-color: #f8d7da'] * len(row)
                except (ValueError, TypeError):
                    return [''] * len(row)
            
            styled_df = results_df.style.apply(highlight_relevant, axis=1)
            st.dataframe(styled_df)
            
            # Estadísticas
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total resultados", len(results_df))
            with col2:
                st.metric("✅ Alta relevancia", len(results_df[results_df['Distancia'] < 0.5]))
            with col3:
                st.metric("🔄 Media relevancia", len(results_df[(results_df['Distancia'] >= 0.5) & (results_df['Distancia'] < 0.75)]))
        else:
            st.warning("⚠️ No se encontraron incidencias relevantes para esta consulta.")
            st.info("💡 **Sugerencias**:\n- Prueba términos más específicos\n- Incluye el equipo\n- Especifica la planta")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🤖 Chatbot Industrial v1.0 | Desarrollado con ❤️ para mantenimiento industrial</p>
    </div>
    """, 
    unsafe_allow_html=True
)
