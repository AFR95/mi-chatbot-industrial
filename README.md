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
