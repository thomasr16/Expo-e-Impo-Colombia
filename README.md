#  Análisis de Comercio Exterior (Importaciones & Exportaciones)

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Polars](https://img.shields.io/badge/Polars-Performance-orange?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)

##  Descripción
Este proyecto analiza un conjunto de datos masivo de **más de 23 millones de registros** correspondientes a movimientos comerciales internacionales. El enfoque principal es la optimización del procesamiento de datos (ETL) y la extracción de métricas clave sobre la balanza comercial.



##  Stack Tecnológico
- **Procesamiento:** `Polars` (optimización multihilo) y `Pandas`.
- **Almacenamiento:** Formato `Parquet` para alta compresión y velocidad de lectura.
- **Visualización:** `Plotly` y `Seaborn`.
- **Entorno:** Jupyter Notebooks y VS Code.

## 📂 Estructura del Proyecto
```text
├── data/
│   ├── raw/          # Datos originales (.zip)
│   └── processed/    # Datos optimizados en Parquet
├── notebooks/
│   ├── Ejecucion_etl.ipynb  # Análisis exploratorio
│   └── analisis_negocio.ipynb  # Visualizaciones finales
├── src/
│   ├── etl.py        # Limpieza y transformación
│   └── utils.py      # Funciones de apoyo
└── requirements.txt 
```
## Analisis de negocio 
En este proyecto encontramos informacion interesante al rededor del comportamiento de la economia Colombia. \
Entre algunas conclusiones importantes vemos la siguiente grafica:
### 📊 Análisis de Importaciones
![Ver Gráfico Interactivo](/Reportes/Imagenes/balanza_comercial.png)
Como notamos, Colombia en general tiene deficit con respecto a lo que compra y lo que vende. 
