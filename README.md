# 🤖 Chatbot de Incidencias Industriales

Chatbot basado en IA para resolución de incidencias en plantas industriales usando embeddings semánticos y búsqueda vectorial.

## 🚀 Despliegue

1. **Configura la API Key** en GitHub Secrets: `XAI_API_KEY`
2. **Sube tu archivo Excel** como `HISTORICO_INCIDENCIAS.xlsx`
3. **Despliega** en [Streamlit Cloud](https://share.streamlit.io)

## 📊 Características

- 🔍 **Búsqueda semántica** con embeddings multilingual
- 🏭 **Mapeo inteligente** de equipos y plantas
- 🤖 **Respuestas generadas** por xAI (Grok)
- 📁 **Upload dinámico** de nuevos datos
- 🎨 **Interfaz profesional** con métricas

## 🔧 Uso

1. **Consulta incidencias**: "scada cogeneracion no funciona"
2. **Obtén soluciones** automatizadas con pasos detallados
3. **Actualiza datos** subiendo nuevos Excel

## 🛠️ Configuración

### Variables de Entorno
| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `XAI_API_KEY` | Clave API de xAI | `xai-abc123...` |

### Dependencias
Ver `requirements.txt`

## 📁 Estructura del Proyecto

- `app.py` — interfaz principal en Streamlit  
- `preprocesar_datos.py` — limpieza, embeddings y consultas  
- `HISTORICO_INCIDENCIAS.xlsx` — dataset fuente  
- `chroma_db/` — base de datos de embeddings (persistente)  
- `requirements.txt` — dependencias del entorno

# 🤖 Chatbot Industrial de Incidencias

**Estado**: 🟢 **PRODUCCIÓN** | Carga <10s | xAI Grok-3 activo

## 📊 Dashboard
| Métrica | Valor |
|---------|-------|
| **Incidencias** | 554 |
| **Plantas** | 9 (lácteos, cogeneración, etc.) |
| **Equipos** | 88 (scada, robots, calderas, etc.) |
| **Tiempo carga** | <10s (pre-generados) |
| **Tiempo respuesta** | <3s |

## 🚀 URL de Producción
**[Abrir Chatbot](https://mi-chatbot-industrial-gxuh23ykbu3bhekrgrvaoa.streamlit.app)**

## 🔧 Funcionalidades

### **1. Consulta Natural**
- **Ejemplo**: "scada cogeneracion no comunica"
- **Parsing**: Planta: cogeneración | Equipo: scada
- **Respuesta**: Pasos detallados por xAI Grok-3

### **2. Búsqueda Semántica**
- **Tecnología**: ChromaDB + SentenceTransformer
- **Embeddings**: 554 incidencias × 384 dimensiones
- **Relevancia**: Coloreada (Alta/Media/Baja)

### **3. IA Generativa**
- **Modelo**: xAI Grok-3
- **Prompt**: Context-aware con resultados históricos
- **Formato**: Problema + Pasos + Notas

### **4. Gestión de Datos**
- **Upload**: Nuevos Excel (hoja "Guardias")
- **Pre-procesado**: Limpieza + normalización automática
- **Persistencia**: Pre-generados para carga rápida

## 🛠️ Arquitectura Técnica
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend        │    │   xAI API       │
│ Streamlit UI    │◄──►│ Flask/Python     │◄──►│   Grok-3        │
│ • Parsing       │    │ • ChromaDB       │    │ • Respuestas    │
│ • Métricas      │    │ • Embeddings     │    │   elaboradas    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
│
▼
┌─────────────────┐
│   Datos         │
│ • 554 incidencias│
│ • 9 plantas     │
│ • 88 equipos    │
└─────────────────┘


# 🤖 Chatbot Industrial para Resolución de Incidencias

**Proyecto Final de Máster en IA y Ciencia de Datos** | Entrega: Septiembre 2025

## 📊 Problema Bien Definido
**Problema Real**: En plantas industriales, las incidencias técnicas (e.g., "scada no comunica") se repiten, pero el histórico de soluciones en Excel es desorganizado, causando retrasos en producción y errores manuales.

**Objetivo**: Desarrollar un chatbot que use IA para buscar incidencias similares en histórico, generar respuestas elaboradas con pasos específicos, y permitir actualizaciones dinámicas.

**Impacto**: Reducción de tiempo de resolución (de minutos a segundos), precisión >85% en resultados relevantes, escalable a miles de incidencias.

**Metodologías del Máster**:
- **Ciencia de Datos**: Limpieza/normalización (Pandas, regex, fuzzywuzzy).
- **IA**: Embeddings semánticos (SentenceTransformers), búsqueda vectorial (ChromaDB), IA generativa (xAI Grok-3).
- **Automatización**: Upload y reindexación dinámica (Streamlit).
- **Visualización**: UI interactiva con métricas y tablas (Streamlit).

## 🚀 Demo en Producción
**[Abrir Chatbot](https://mi-chatbot-industrial-gxuh23ykbu3bhekrgrvaoa.streamlit.app)** (Streamlit Cloud, 24/7)

**Ejemplo de Uso**:
1. Consulta: "scada cogeneracion no comunica"
2. Parsing: Planta: cogeneración | Equipo: scada
3. Respuesta Grok-3: Pasos detallados (e.g., "Reinicia servidor IP 172.16.6.240")
4. Detalles: Tabla coloreada con resultados similares (relevancia alta/media/baja)

## 🛠️ Arquitectura

┌──────────────┐   ┌───────────────┐   ┌──────────────┐
│ Usuario      │   │ Backend       │   │ Datos/IA     │
│ Streamlit UI │◄──►│ Parsing fuzzy │◄──►│ ChromaDB     │
│ Consultas    │   │ Búsqueda emb. │   │ xAI Grok-3   │
└──────────────┘   └───────────────┘   └──────────────┘



- **Datos**: 554 incidencias (Excel procesado).
- **Embeddings**: Paraphrase-multilingual (384 dims).
- **API**: xAI Grok-3 para respuestas naturales.

## 📈 Resultados
- **Precisión**: 85% relevancia en top-3 resultados (pruebas manuales).
- **Tiempo**: Carga inicial ~30s, respuestas <3s.
- **Métricas**: 554 incidencias, 9 plantas, 88 equipos.
- **Fallback**: Funciona sin xAI.

## 📚 Código y Recursos
- **Repo GitHub**: https://github.com/AFR95/mi-chatbot-industrial
  - `app.py`: Código principal
  - `requirements.txt`: Dependencias
  - `HISTORICO_INCIDENCIAS.xlsx`: Datos
- **Notebook**: [proyecto_final.ipynb](https://github.com/AFR95/mi-chatbot-industrial/blob/main/proyecto_final.ipynb) (explicación código)
- **PDF**: [Informe PDF](https://github.com/AFR95/mi-chatbot-industrial/blob/main/informe_proyecto.pdf) (resumen 5 páginas)

## 🔒 Instalación Local
```bash
git clone https://github.com/AFR95/mi-chatbot-industrial.git
cd mi-chatbot-industrial
pip install -r requirements.txt
export XAI_API_KEY="tu-key"
streamlit run app.py

## 📝 Conclusión
Proyecto aplicado que resuelve un problema real en mantenimiento industrial con IA. Listo para escalado.
Contacto: afr95@email.com
