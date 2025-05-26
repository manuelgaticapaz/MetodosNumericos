# 🧮 Proyecto de Métodos Numéricos con Streamlit

Este repositorio contiene una aplicación web interactiva desarrollada con **Streamlit** que implementa diversos **métodos numéricos** usados en matemáticas aplicadas, física e ingeniería. 
La herramienta está dividida en módulos organizados por temas fundamentales.

---

## 📚 Módulos Disponibles

### 1️⃣ Módulo 1: Cálculo de Raíces de Ecuaciones
- Método de **Bisección**
- Método de **Newton-Raphson**
- Método de **la Secante**

### 2️⃣ Módulo 2: Interpolación y Ajuste de Curvas
- Interpolación con el **Polinomio de Lagrange**
- Interpolación con el **Polinomio de Newton**
- Visualización interactiva de los resultados

### 3️⃣ Módulo 3: Resolución de Sistemas de Ecuaciones
- Método iterativo de **Gauss-Seidel**
- **Factorización LU**

### 4️⃣ Módulo 4: Derivación e Integración Numérica
- **Diferencias finitas** para derivación numérica
- Método del **Trapecio** para integración numérica

---

## 💻 Tecnologías Usadas

- [Streamlit](https://streamlit.io/) para la interfaz de usuario
- [NumPy](https://numpy.org/) y [Pandas](https://pandas.pydata.org/) para cálculos y manejo de datos
- [Matplotlib](https://matplotlib.org/) y [Altair](https://altair-viz.github.io/) para visualización
- Otras dependencias incluidas en [`requirements.txt`](./requirements.txt)

---

## 🛠️ Instalación

(Opcional) Crea y activa un entorno virtual:

python -m venv venv
 # En Windows: 
 venv\Scripts\activate

Instala las dependencias:

pip install -r requirements.txt


▶️ Cómo Ejecutar la Aplicación
Ejecuta el siguiente comando para iniciar la aplicación:

streamlit run app.py
Asegúrate de reemplazar app.py 
