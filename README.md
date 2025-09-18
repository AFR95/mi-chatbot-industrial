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

