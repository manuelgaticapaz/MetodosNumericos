import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------- Derivadas por Diferencias Finitas -------------------
def aproximacion_derivada(fx, x, h, metodo="progresiva"):
    if metodo == "progresiva":
        return (fx(x + h) - fx(x)) / h
    elif metodo == "regresiva":
        return (fx(x) - fx(x - h)) / h
    elif metodo == "centrada":
        return (fx(x + h) - fx(x - h)) / (2 * h)
    else:
        raise ValueError("Método no reconocido. Elige entre progresiva, regresiva o centrada.")

# ------------------- Método del Trapecio -------------------
def integracion_trapecio(fx, a, b, n):
    h = (b - a) / n
    suma = fx(a) + fx(b)
    for i in range(1, n):
        suma += 2 * fx(a + i * h)
    return (h / 2) * suma

# ------------------- Módulo principal para Streamlit -------------------
def calculus_module():
    st.subheader("Módulo 4: Cálculo Numérico")

    option = st.radio("Selecciona una operación:", ["Aproximación de Derivadas", "Integración Numérica (Trapecio)"])
    st.markdown("---")

    if option == "Aproximación de Derivadas":
        st.write("### Derivadas por Diferencias Finitas")
        funcion_str = st.text_input("Función f(x):", value="np.sin(x)")
        a = st.number_input("Límite inferior a:", value=0.0)
        b = st.number_input("Límite superior b:", value=2 * np.pi)
        n = st.number_input("Número de subintervalos n:", min_value=1, value=10, step=1)
        metodo = st.selectbox("Método:", ["progresiva", "regresiva", "centrada"])

        if st.button("Calcular Derivadas"):
            try:
                fx = lambda x_val: eval(funcion_str, {"np": np, "x": x_val})
                x_vals = np.linspace(a, b, n + 1)
                h = (b - a) / n
                derivadas = [aproximacion_derivada(fx, x, h, metodo) for x in x_vals]

                df = pd.DataFrame({
                    "x": x_vals,
                    f"f'({metodo})": derivadas
                })
                st.dataframe(df)

                # Gráfico
                y_vals = [fx(x) for x in x_vals]
                fig, ax = plt.subplots()
                ax.plot(x_vals, y_vals, label="f(x)", color="blue")
                ax.plot(x_vals, derivadas, label=f"f'(x) - {metodo}", color="red")
                ax.set_title("Función y su Derivada Aproximada")
                ax.legend()
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Error evaluando la función: {e}")

    elif option == "Integración Numérica (Trapecio)":
        st.write("### Integración usando el Método del Trapecio")
        funcion_str = st.text_input("Función f(x):", value="np.exp(-x**2)")
        a = st.number_input("Límite inferior a:", value=0.0)
        b = st.number_input("Límite superior b:", value=1.0)
        n = st.number_input("Número de subintervalos n:", min_value=1, value=10, step=1)

        if st.button("Calcular Integral"):
            try:
                fx = lambda x_val: eval(funcion_str, {"np": np, "x": x_val})
                resultado = integracion_trapecio(fx, a, b, int(n))
                st.success(f"Aproximación de la integral en [{a}, {b}] con n={n}: {resultado:.6f}")

                # Visualización de la función y los trapecios
                x_vals = np.linspace(a, b, 1000)
                y_vals = [fx(x) for x in x_vals]
                st.pyplot(plot_integral(fx, a, b, int(n), x_vals, y_vals))

            except Exception as e:
                st.error(f"Error evaluando la función: {e}")

# ------------------- Función para graficar integración -------------------
def plot_integral(fx, a, b, n, x_vals, y_vals):
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label="f(x)", color='blue')

    h = (b - a) / n
    for i in range(n):
        x0 = a + i * h
        x1 = a + (i + 1) * h
        y0 = fx(x0)
        y1 = fx(x1)
        ax.fill([x0, x0, x1, x1], [0, y0, y1, 0], color='orange', alpha=0.3)

    ax.set_title("Visualización del Método del Trapecio")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    return fig

# Ejecutar módulo
if __name__ == "__main__":
    calculus_module()