import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------- Función para diferencias divididas de Newton -------------------
def newton_divided_diff(x, y):
    n = len(x)
    coef = np.array(y, float)
    for j in range(1, n):
        coef[j:n] = (coef[j:n] - coef[j - 1]) / (x[j:n] - x[j - 1])
    return coef

# ------------------- Evaluación del polinomio de Newton -------------------
def newton_interpolate(x_data, coef, x):
    n = len(coef)
    result = coef[-1]
    for i in range(n - 2, -1, -1):
        result = result * (x - x_data[i]) + coef[i]
    return result

# ------------------- Construcción de la ecuación de Newton -------------------
def newton_polynomial_string(x_data, coef):
    terms = [f"{coef[0]:.4f}"]
    for i in range(1, len(coef)):
        term = f"{coef[i]:+.4f}"
        for j in range(i):
            term += f"*(x - {x_data[j]})"
        terms.append(term)
    return " + ".join(terms)

# ------------------- Interpolación de Lagrange -------------------
def lagrange_interpolation(x_data, y_data, x):
    total = 0
    n = len(x_data)
    for i in range(n):
        term = y_data[i]
        for j in range(n):
            if i != j:
                term *= (x - x_data[j]) / (x_data[i] - x_data[j])
        total += term
    return total

# ------------------- Construcción de la ecuación de Lagrange -------------------
def lagrange_polynomial_string(x_data, y_data):
    n = len(x_data)
    terms = []
    for i in range(n):
        num_terms = []
        denom = 1
        for j in range(n):
            if i != j:
                num_terms.append(f"(x - {x_data[j]})")
                denom *= (x_data[i] - x_data[j])
        term = f"({y_data[i]:.4f}/({denom:.4f})) * " + " * ".join(num_terms)
        terms.append(term)
    return " + ".join(terms)

# ------------------- Visualización de resultados -------------------
def plot_interpolation(x_data, y_data, x_eval, y_interp, method):
    x_plot = np.linspace(min(x_data) - 1, max(x_data) + 1, 400)
    if method == "Lagrange":
        y_plot = [lagrange_interpolation(x_data, y_data, xi) for xi in x_plot]
    else:
        coef = newton_divided_diff(x_data, y_data)
        y_plot = [newton_interpolate(x_data, coef, xi) for xi in x_plot]

    plt.figure(figsize=(8, 5))
    plt.plot(x_plot, y_plot, label=f"Interpolación ({method})", color="blue")
    plt.scatter(x_data, y_data, color="red", label="Puntos dados")
    plt.scatter([x_eval], [y_interp], color="green", zorder=5, label=f"f({x_eval}) ≈ {y_interp:.3f}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Interpolación de puntos")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# ------------------- Módulo principal para Streamlit -------------------
def interpolation_module():
    st.subheader("Módulo 2: Interpolación")

    method = st.radio("Selecciona un método de interpolación:", ("Lagrange", "Newton"))
    st.markdown("---")

    x_values = st.text_input("Valores de x (separados por comas):", "1,2,3,4")
    y_values = st.text_input("Valores de y (separados por comas):", "1,4,9,16")
    x_eval = st.number_input("Valor de x a interpolar:", value=2.5)

    if st.button("Interpolar"):
        try:
            x_data = np.array([float(i) for i in x_values.split(",")])
            y_data = np.array([float(i) for i in y_values.split(",")])

            if len(x_data) != len(y_data):
                st.error("Las listas de x e y deben tener la misma longitud.")
                return

            if method == "Lagrange":
                y_interp = lagrange_interpolation(x_data, y_data, x_eval)
                equation = lagrange_polynomial_string(x_data, y_data)
                st.success(f"Resultado usando Lagrange: f({x_eval}) ≈ {y_interp:.6f}")

            elif method == "Newton":
                coef = newton_divided_diff(x_data, y_data)
                y_interp = newton_interpolate(x_data, coef, x_eval)
                equation = newton_polynomial_string(x_data, coef)
                st.success(f"Resultado usando Newton: f({x_eval}) ≈ {y_interp:.6f}")

            # Mostrar tabla de datos
            data = pd.DataFrame({"x": x_data, "y": y_data})
            st.write("### Datos de entrada")
            st.dataframe(data)

            # Mostrar ecuación del polinomio
            st.write("### Ecuación del polinomio de interpolación")
            st.code(equation, language="python")

            # Mostrar gráfica de interpolación
            st.write("### Visualización de la interpolación")
            plot_interpolation(x_data, y_data, x_eval, y_interp, method)

        except Exception as e:
            st.error(f"Error en la entrada o cálculo: {e}")

# Ejecutar módulo
if __name__ == "__main__":
    interpolation_module()