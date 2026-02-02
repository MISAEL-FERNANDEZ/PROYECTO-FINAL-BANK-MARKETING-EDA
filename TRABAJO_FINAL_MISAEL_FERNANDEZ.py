import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Bank Marketing EDA", page_icon="🏦", layout="wide")

# 1. MANEJO DE DATOS (POO)

class BankDataManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.load_data()

    @st.cache_data
    def load_data(_self):
        try:
            # Intentamos leer con separador de punto y coma
            data = pd.read_csv(_self.file_path, sep=';')
            return data
        except FileNotFoundError:
            st.error("⚠️ Error: No se encontró el archivo 'BankMarketing.csv'.")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"⚠️ Error inesperado: {e}")
            return pd.DataFrame()

    def get_data(self):
        return self.df

    def get_numeric_columns(self):
        return self.df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    def get_categorical_columns(self):
        return self.df.select_dtypes(include=['object']).columns.tolist()

# Instancia de la clase
data_manager = BankDataManager("BankMarketing.csv")
df = data_manager.get_data()

# 2. SIDEBAR Y NAVEGACIÓN


st.sidebar.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=50)
st.sidebar.title("Menú Principal")

opciones_menu = [
    "Home", 
    "Datos Generales", 
    "Exploración de Variables", 
    "Cruce de Variables",      
    "Conclusiones"
]

opcion = st.sidebar.radio("Ir a:", opciones_menu)

st.sidebar.markdown("---")
st.sidebar.info("Proyecto Final\nPython for Analytics\nMisael Fernandez Castro")


# MÓDULO: HOME

if opcion == "Home":
    st.title("🏦 Análisis de Marketing Bancario")
    st.markdown("""
                
    #### 📋 Información del Autor
    - **Nombre:** Misael Fernandez Castro
    - **Curso:** Python for Analytics
    
                         
    ### Objetivo del Dashboard
    Analizar el comportamiento de los clientes ante campañas de depósitos a plazo.
    Buscamos responder: **¿Qué perfil de cliente es más propenso a contratar el producto?**
    
    #### 🛠️ Herramientas Aplicadas
    * **Python & Streamlit:** Interfaz interactiva.
    * **Pandas:** Manipulación y limpieza de datos.
    * **Seaborn/Matplotlib:** Visualización estadística.
    * **Estadística Descriptiva:** Media, Mediana, Moda y Dispersión.
    """)
    st.image("https://www.investopedia.com/thmb/O2uV4z_C5s5r1V4u5s1v1.jpg", use_container_width=True)
    
    if not df.empty:
        st.success(f"✅ Dataset cargado correctamente con {df.shape[0]:,} filas y {df.shape[1]} columnas.")

# MÓDULO: DATOS GENERALES

elif opcion == "Datos Generales":
    st.title("📂 Visión General del Dataset")
    
    tab1, tab2 = st.tabs(["Tabla de Datos", "Estadísticas Globales"])
    
    with tab1:
        st.write("Muestra de las primeras 100 filas:")
        st.dataframe(df.head(100), use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.write("##### 📊 Variables Numéricas")
            st.dataframe(df.describe())
        with col2:
            st.write("##### 🔠 Variables Categóricas")
            st.dataframe(df.describe(include=['object']))

# MÓDULO: EXPLORACIÓN DE VARIABLES

elif opcion == "Exploración de Variables":
    st.title("📊 Exploración de Variables (Univariado)")
    st.markdown("Análisis detallado de la distribución y medidas de tendencia central.")
    
    tipo_var = st.radio("Selecciona el tipo de variable:", ["Numérica", "Categórica"], horizontal=True)
    
    if tipo_var == "Numérica":
        col_sel = st.selectbox("Variable a analizar:", data_manager.get_numeric_columns())
        
        # --- CÁLCULO DE ESTADÍSTICOS (REQUISITO) ---
        col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4)
        col_metrics1.metric("Media (Promedio)", f"{df[col_sel].mean():.2f}")
        col_metrics2.metric("Mediana", f"{df[col_sel].median():.2f}")
        col_metrics3.metric("Desviación Std", f"{df[col_sel].std():.2f}")
        col_metrics4.metric("Mínimo", f"{df[col_sel].min()}")

        # Gráficos
        fig, ax = plt.subplots(1, 2, figsize=(16, 5))
        
        # Histograma con Curva de Densidad
        sns.histplot(df[col_sel], kde=True, ax=ax[0], color='#3498db')
        ax[0].set_title(f"Distribución de: {col_sel}")
        ax[0].set_xlabel(col_sel)
        
        # Boxplot
        sns.boxplot(x=df[col_sel], ax=ax[1], color='#2ecc71')
        ax[1].set_title(f"Detectando Outliers: {col_sel}")
        
        st.pyplot(fig)
        
    else: # Categórica
        col_sel = st.selectbox("Variable a analizar:", data_manager.get_categorical_columns())
        
        # --- MODA  ---
        moda = df[col_sel].mode()[0]
        st.info(f"📌 La categoría más frecuente (**Moda**) es: **{moda}**")
        
        # Gráfico de Barras
        fig, ax = plt.subplots(figsize=(12, 6))
        conteo = df[col_sel].value_counts()
        sns.barplot(x=conteo.values, y=conteo.index, palette="viridis", ax=ax)
        ax.set_title(f"Frecuencia de categorías: {col_sel}")
        ax.set_xlabel("Cantidad")
        
        # Etiquetas en las barras
        for i, v in enumerate(conteo.values):
            ax.text(v + 3, i, str(v), color='black', va='center')
            
        st.pyplot(fig)


# MÓDULO: CRUCE DE VARIABLES

elif opcion == "Cruce de Variables":
    st.title("🔗 Cruce de Variables (Bivariado)")
    st.markdown("¿Cómo influyen las variables en la decisión del cliente (`y`)?")
    
    tab1, tab2 = st.tabs(["Numérica vs Objetivo", "Categórica vs Objetivo"])
    
    with tab1:
        var_num = st.selectbox("Elige variable numérica:", data_manager.get_numeric_columns(), key="num_bi")
        
        # --- COMPARACIÓN DE GRUPOS ---
        st.write("##### 🆚 Comparación de Medias por Grupo (Sí vs No)")
        # Agrupamos por 'y' y calculamos la media de la variable seleccionada
        grupo = df.groupby('y')[var_num].mean().reset_index()
        st.table(grupo.style.format({var_num: "{:.2f}"}))
        
        # Visualización
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x='y', y=var_num, data=df, palette="Set2", ax=ax)
        ax.set_title(f"Distribución de {var_num} según respuesta del cliente")
        st.pyplot(fig)
        
    with tab2:
        var_cat = st.selectbox("Elige variable categórica:", data_manager.get_categorical_columns(), key="cat_bi")
        
        # Tabla cruzada
        st.write("##### 📋 Tabla de Contingencia")
        crosstab = pd.crosstab(df[var_cat], df['y'], normalize='index') * 100
        st.dataframe(crosstab.style.format("{:.1f}%"))
        
        # Visualización
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(x=var_cat, hue='y', data=df, palette="pastel", ax=ax)
        ax.set_title(f"Relación entre {var_cat} y Suscripción")
        plt.xticks(rotation=45)
        st.pyplot(fig)

# MÓDULO: CONCLUSIONES

elif opcion == "Conclusiones":
    st.title("💡 Conclusiones y Recomendaciones")
    st.markdown("Basado en el análisis de datos realizado, se presentan los siguientes hallazgos estratégicos para la toma de decisiones:")
    
    st.success("""
    ### 1. 🎯 Perfil Demográfico Rentable (Comparación de Grupos)
    Aunque los perfiles administrativos son los más contactados, los **estudiantes y jubilados** muestran las tasas de conversión más altas""")
    
    st.info("""
    ### 2. 📞 La "Regla de los 2 Contactos" (Media y Distribución)
    El análisis de la variable `campaign` revela una relación inversa: el promedio de contactos para un éxito es de **2 llamadas**. A medida que se insiste más (3, 4 o más veces), la probabilidad de éxito cae drásticamente.
    > 
            Acción: Limitar la insistencia a un máximo de 3 contactos para optimizar recursos del Call Center.
    """)
    
    st.warning("""
    ### 3. ⏳ El Engagement mide el Éxito (Media)
    La variable `duration` es el discriminante más fuerte. Las llamadas exitosas duran en promedio "9 minutos (553 seg)", mientras que las fallidas apenas llegan a **3.5 minutos (220 seg)**.
    > 
               Acción: Capacitar a los agentes para mantener la conversación activa. Si la llamada supera los 5 minutos, la probabilidad de cierre aumenta exponencialmente.
    """)
    
    st.success("""
    ### 4. 📅 Estacionalidad: Meses Clave (Moda y Frecuencia)
    A pesar de que mayo es el mes con más volumen de llamadas (Moda), tiene una de las peores tasas de conversión. Meses como **Marzo, Septiembre, Octubre y Diciembre** muestran efectividades cercanas al 50%.
    > 
               Acción: Planificar campañas agresivas en el último y primer trimestre del año, reduciendo la carga en mayo.
    """)
    
    st.info("""
    ### 5. 🔄 El valor de la Fidelización
    La variable `poutcome` muestra que los clientes que aceptaron una campaña previa ("success") tienen una probabilidad del **65** de volver a aceptar.
    > 
            Acción: Crear una campaña VIP exclusiva para clientes con historial exitoso, ya que son la "fruta al alcance de la mano".
    """)

    st.markdown("---")
    st.caption("Reporte generado con Python 🐍 y Streamlit 🎈")