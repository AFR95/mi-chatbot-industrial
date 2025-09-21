## 📊 Características

- 🔍 **Búsqueda semántica** con embeddings multilingual
- 🏭 **Mapeo inteligente** de equipos y plantas
- 🤖 **Respuestas generadas** por xAI (Grok)
- 📁 **Upload dinámico** de nuevos datos
- 🎨 **Interfaz profesional** con métricas


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


## 🛠️ Arquitectura Técnica
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend        │    │   xAI API       │
│ Streamlit UI    │◄──►│ Flask/Python     │◄──►│   Grok-3        │
│ • Parsing       │    │ • ChromaDB       │    │ • Respuestas    │
│ • Métricas      │    │ • Embeddings     │    │   elaboradas    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │
         ▼
┌──────────────────┐
│   Datos          │
│ • 554 incidencias│
│ • 9 plantas      │
│ • 88 equipos     │
└──────────────────┘

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
```
📝 Conclusión
Proyecto aplicado que resuelve un problema real en mantenimiento industrial con IA. Listo para escalado.
Contacto: afernandez.rubio@outlook.es
