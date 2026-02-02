# 🏦 Dashboard de Análisis de Marketing Bancario

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Status](https://img.shields.io/badge/Status-Finalizado-success)

## 📄 Descripción
Este proyecto es una aplicación web interactiva desarrollada en **Python** utilizando **Streamlit**. Su objetivo es realizar un **Análisis Exploratorio de Datos (EDA)** profundo sobre el dataset *Bank Marketing*, transformando datos crudos en decisiones de negocio estratégicas.

A diferencia de un análisis estático, esta herramienta permite calcular métricas en tiempo real y visualizar qué factores influyen realmente en que un cliente acepte un depósito a plazo.

## 🚀 Características del Proyecto

### 1. Arquitectura Robusta
* **POO (Programación Orientada a Objetos):** Clase `BankDataManager` para una gestión eficiente y modular de la carga de datos.
* **Optimización:** Uso de decoradores `@st.cache_data` para un rendimiento fluido.

### 2. Módulos de Análisis
* **📊 Exploración de Variables:**
    * Cálculo automático de **Media, Mediana y Desviación Estándar** para variables numéricas.
    * Detección de **Moda** y frecuencias para variables categóricas.
    * Visualización de distribuciones (Histogramas y Boxplots).
* **🔗 Cruce de Variables:**
    * **Comparación de Grupos:** Tablas dinámicas que contrastan el promedio de métricas entre clientes que aceptaron (Sí) vs los que no (No).
    * Mapas de calor y gráficos de barras segmentados.

### 3. Toma de Decisiones
* **💡 Conclusiones Estratégicas:** Una sección dedicada a "Insights de Negocio", donde se traducen los números en 4 recomendaciones claras para el equipo de marketing (ej. duración de llamadas, perfiles demográficos rentables, etc.).

## 🛠️ Requisitos Previos

Para ejecutar este proyecto localmente, necesitas las siguientes librerías de Python:

* `streamlit` (Interface web)
* `pandas` (Manipulación de datos)
* `seaborn` (Gráficos estadísticos)
* `matplotlib` (Gráficos base)

## ⚙️ Instalación y Ejecución

1.  **Descarga los archivos:**
    Asegúrate de tener `app.py` y `BankMarketing.csv` en la misma carpeta.

2.  **Instala las dependencias:**
    Abre tu terminal en la carpeta del proyecto y ejecuta:
    ```bash
    pip install streamlit pandas seaborn matplotlib
    ```

3.  **Ejecuta la aplicación:**
    Corre el siguiente comando en la terminal:
    ```bash
    streamlit run app.py
    ```

4.  **¡Listo!**
  

## 📂 Estructura del Repositorio

```text
├── app.py                # Código fuente principal (Lógica + UI)
├── BankMarketing.csv     # Dataset (separador ';')
└── README.md             # Documentación del proyecto