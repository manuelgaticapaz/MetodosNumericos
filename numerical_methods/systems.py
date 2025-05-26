import streamlit as st
import numpy as np
import pandas as pd

# ------------------- Método de Gauss-Seidel -------------------
def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    n = len(b)
    x = np.zeros_like(b, dtype=np.double) if x0 is None else x0.copy()
    history = []

    for k in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            s1 = sum(A[i][j] * x[j] for j in range(i))
            s2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
            x[i] = (b[i] - s1 - s2) / A[i][i]

        history.append(x.copy())
        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            return x, history, None

    return x, history, "No se alcanzó la convergencia dentro del número máximo de iteraciones."

# ------------------- Factorización LU -------------------
def lu_decomposition(A):
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
        for j in range(i, n):
            if i == j:
                L[i][i] = 1
            else:
                L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]
    return L, U

def lu_solve(L, U, b):
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
    x = np.zeros(n)
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x

# ------------------- Módulo principal para Streamlit -------------------
def systems_module():
    st.subheader("Módulo 3: Sistemas de Ecuaciones Lineales")

    method = st.radio("Selecciona un método:", ("Gauss-Seidel", "Factorización LU"))
    st.markdown("---")

    A_input = st.text_area("Matriz A (usa comas y punto y coma para separar filas):", "4,1,2;3,5,1;1,1,3")
    b_input = st.text_input("Vector b (separado por comas):", "4,7,3")

    try:
        A = np.array([[float(num) for num in row.split(",")] for row in A_input.split(";")])
        b = np.array([float(num) for num in b_input.split(",")])

        if A.shape[0] != b.shape[0]:
            st.error("La dimensión de A y b no coinciden.")
            return

        if method == "Gauss-Seidel":
            tol = st.number_input("Tolerancia:", value=1e-6, format="%.8f")
            max_iter = st.number_input("Máximo de iteraciones:", value=100, step=1)
            if st.button("Resolver con Gauss-Seidel"):
                x, history, error = gauss_seidel(A, b, tol=tol, max_iter=max_iter)
                if error:
                    st.error(error)
                else:
                    st.success("Solución encontrada:")
                    st.write(x)
                    st.write("### Historial de iteraciones")
                    df = pd.DataFrame(history, columns=[f"x{i+1}" for i in range(len(x))])
                    st.dataframe(df)

        elif method == "Factorización LU":
            if st.button("Resolver con LU"):
                L, U = lu_decomposition(A)
                x = lu_solve(L, U, b)

                st.success("Solución encontrada:")
                st.write(x)
                st.write("### Matriz L")
                st.dataframe(pd.DataFrame(L))
                st.write("### Matriz U")
                st.dataframe(pd.DataFrame(U))

    except Exception as e:
        st.error(f"Error en la entrada: {e}")

# Ejecutar módulo
if __name__ == "__main__":
    systems_module()
