import streamlit as st
import numpy as np
import numexpr as ne  # Más seguro que eval
import pandas as pd

# --- Función segura para evaluar expresiones ---
def safe_eval(expr, x):
    try:
        return float(ne.evaluate(expr, local_dict={"x": x}))
    except Exception as e:
        raise ValueError(f"Error al evaluar la expresión: {e}")

# --- Métodos numéricos ---
def bisection_method(f_str, a, b, tol, max_iter=100):
    try:
        if safe_eval(f_str, a) * safe_eval(f_str, b) >= 0:
            return None, "La función no cambia de signo en el intervalo dado.", 0, []

        c = 0
        iterations = 0
        history = []

        while (b - a) / 2 > tol and iterations < max_iter:
            c = (a + b) / 2
            history.append([iterations, a, b, c, safe_eval(f_str, a), safe_eval(f_str, b), safe_eval(f_str, c)])

            if safe_eval(f_str, c) == 0:
                break
            elif safe_eval(f_str, a) * safe_eval(f_str, c) < 0:
                b = c
            else:
                a = c
            iterations += 1

        return c, None, iterations, history
    except Exception as e:
        return None, f"Error en la función o parámetros: {e}", 0, []

def newton_raphson_method(f_str, df_str, x0, tol, max_iter=100):
    try:
        x_n = x0
        iterations = 0
        history = [[iterations, x_n, safe_eval(f_str, x_n)]]

        for i in range(int(max_iter)):
            f_xn = safe_eval(f_str, x_n)
            df_xn = safe_eval(df_str, x_n)

            if df_xn == 0:
                return None, "La derivada es cero en este punto.", 0, history

            x_next = x_n - f_xn / df_xn
            history.append([i+1, x_next, safe_eval(f_str, x_next)])

            if abs(x_next - x_n) < tol:
                return x_next, None, i + 1, history

            x_n = x_next
            iterations += 1

        return None, "No se encontró la raíz dentro del número máximo de iteraciones.", iterations, history
    except Exception as e:
        return None, f"Error en la función, derivada o parámetros: {e}", 0, []

def secant_method(f_str, x0, x1, tol, max_iter=100):
    try:
        x_prev = x0
        x_curr = x1
        iterations = 0
        history = [[iterations, x_prev, safe_eval(f_str, x_prev)], [iterations + 1, x_curr, safe_eval(f_str, x_curr)]]

        for i in range(int(max_iter)):
            f_x_curr = safe_eval(f_str, x_curr)
            f_x_prev = safe_eval(f_str, x_prev)

            if f_x_curr - f_x_prev == 0:
                return None, "División por cero. f(x_n) - f(x_{n-1}) es cero.", 0, history

            x_next = x_curr - f_x_curr * (x_curr - x_prev) / (f_x_curr - f_x_prev)
            history.append([i+2, x_next, safe_eval(f_str, x_next)])

            if abs(x_next - x_curr) < tol:
                return x_next, None, i + 1, history

            x_prev = x_curr
            x_curr = x_next
            iterations += 1

        return None, "No se encontró la raíz dentro del número máximo de iteraciones.", iterations, history
    except Exception as e:
        return None, f"Error en la función o parámetros: {e}", 0, []

# --- Mostrar resultados ---
def mostrar_resultado(root, error, iterations, history, columns, key_checkbox):
    if error:
        st.error(error)
    elif root is not None:
        st.success(f"Raíz aproximada: **{root:.6f}**")
        st.info(f"Iteraciones: {iterations}")
        if st.checkbox("Mostrar historial de iteraciones", key=key_checkbox):
            if history:
                df = pd.DataFrame(history, columns=columns)
                st.dataframe(df)
            else:
                st.warning("No hay historial para mostrar.")
    else:
        st.warning("No se pudo encontrar la raíz.")

# --- Interfaz ---
def roots_module():
    st.subheader("Módulo 1: Cálculo de Raíces")

    method_choice = st.radio(
        "Selecciona un método:",
        ("Bisección", "Newton-Raphson", "Secante")
    )

    st.markdown("---")

    # --- Variables comunes para checkbox keys ---
    key_checkbox = f"{method_choice}_history_checkbox"

    if method_choice == "Bisección":
        st.write("### Método de Bisección")
        st.latex(r"x_{new} = \frac{a+b}{2}")

        func_str = st.text_input("Ingrese la función f(x) (ej. 'x**2 - 2'):", "x**2 - 2", key="bisection_func")
        a = st.number_input("Límite Inferior (a):", value=0.0, key="bisection_a")
        b = st.number_input("Límite Superior (b):", value=2.0, key="bisection_b")
        tol = st.number_input("Tolerancia (ej. 0.001):", value=0.001, format="%.6f", key="bisection_tol")

        if st.button("Calcular Bisección"):
            root, error, iterations, history = bisection_method(func_str, a, b, tol)
            st.session_state["root"] = root
            st.session_state["error"] = error
            st.session_state["iterations"] = iterations
            st.session_state["history"] = history
            st.session_state["columns"] = ["Iteración", "a", "b", "c", "f(a)", "f(b)", "f(c)"]
            st.session_state["key_checkbox"] = key_checkbox

        # Mostrar resultado si ya calculaste
        if "root" in st.session_state:
            mostrar_resultado(
                st.session_state["root"],
                st.session_state["error"],
                st.session_state["iterations"],
                st.session_state["history"],
                st.session_state["columns"],
                st.session_state["key_checkbox"]
            )

    elif method_choice == "Newton-Raphson":
        st.write("### Método de Newton-Raphson")
        st.latex(r"x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}")

        func_str = st.text_input("Ingrese la función f(x) (ej. 'x**2 - 2'):", "x**2 - 2", key="newton_func")
        df_str = st.text_input("Ingrese la derivada f'(x) (ej. '2*x'):", "2*x", key="newton_dfunc")
        x0 = st.number_input("Valor inicial (x0):", value=1.0, key="newton_x0")
        tol = st.number_input("Tolerancia (ej. 0.001):", value=0.001, format="%.6f", key="newton_tol")
        max_iter = st.number_input("Máximo de iteraciones:", value=100, step=1, key="newton_max_iter")

        if st.button("Calcular Newton-Raphson"):
            root, error, iterations, history = newton_raphson_method(func_str, df_str, x0, tol, max_iter)
            st.session_state["root"] = root
            st.session_state["error"] = error
            st.session_state["iterations"] = iterations
            st.session_state["history"] = history
            st.session_state["columns"] = ["Iteración", "x", "f(x)"]
            st.session_state["key_checkbox"] = key_checkbox

        if "root" in st.session_state:
            mostrar_resultado(
                st.session_state["root"],
                st.session_state["error"],
                st.session_state["iterations"],
                st.session_state["history"],
                st.session_state["columns"],
                st.session_state["key_checkbox"]
            )

    elif method_choice == "Secante":
        st.write("### Método de la Secante")
        st.latex(r"x_{n+1} = x_n - f(x_n)\frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}")

        func_str = st.text_input("Ingrese la función f(x) (ej. 'x**2 - 2'):", "x**2 - 2", key="secant_func")
        x0 = st.number_input("Primer valor inicial (x0):", value=0.0, key="secant_x0")
        x1 = st.number_input("Segundo valor inicial (x1):", value=2.0, key="secant_x1")
        tol = st.number_input("Tolerancia (ej. 0.001):", value=0.001, format="%.6f", key="secant_tol")
        max_iter = st.number_input("Máximo de iteraciones:", value=100, step=1, key="secant_max_iter")

        if st.button("Calcular Secante"):
            root, error, iterations, history = secant_method(func_str, x0, x1, tol, max_iter)
            st.session_state["root"] = root
            st.session_state["error"] = error
            st.session_state["iterations"] = iterations
            st.session_state["history"] = history
            st.session_state["columns"] = ["Iteración", "x", "f(x)"]
            st.session_state["key_checkbox"] = key_checkbox

        if "root" in st.session_state:
            mostrar_resultado(
                st.session_state["root"],
                st.session_state["error"],
                st.session_state["iterations"],
                st.session_state["history"],
                st.session_state["columns"],
                st.session_state["key_checkbox"]
            )


# Ejecutar módulo
if __name__ == "__main__":
    roots_module()
