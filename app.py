import streamlit as st
import numerical_methods.roots as roots
import numerical_methods.interpolation as interpolation
import numerical_methods.systems as systems
import numerical_methods.calculus as calculus

st.set_page_config(layout="centered") # O "wide" si prefieres un layout más amplio

# --- Título y descripción general de la aplicación ---
st.title("Calculadora de Métodos Numéricos")
st.write("Explora diferentes métodos numéricos para resolver problemas matemáticos.")

st.markdown("---")

# --- Barra lateral para el menú de módulos ---
st.sidebar.title("Menú Principal")

# Opción de menú con radio buttons
module_choice = st.sidebar.radio(
    "Selecciona un Módulo:",
    (
        "Módulo 1: Cálculo de Raíces",
        "Módulo 2: Interpolación y Ajuste de Curvas",
        "Módulo 3: Sistemas de Ecuaciones",
        "Módulo 4: Derivación e Integración Numérica"
    )
)

st.sidebar.markdown("---")
st.sidebar.info("Desarrollado por el grupo 'Los lisiados'")


# --- Contenido principal basado en la selección del módulo ---
if module_choice == "Módulo 1: Cálculo de Raíces":
    roots.roots_module() # Llama a la función del módulo de raíces

elif module_choice == "Módulo 2: Interpolación y Ajuste de Curvas":
    interpolation.interpolation_module() 

elif module_choice == "Módulo 3: Sistemas de Ecuaciones":
    systems.systems_module() # Descomenta cuando crees este módulo

elif module_choice == "Módulo 4: Derivación e Integración Numérica":
    calculus.calculus_module() # Descomenta cuando crees este módulo

# Puedes añadir una sección de información general o bienvenida
else:
    st.write("Selecciona un módulo del menú lateral para comenzar.")

st.markdown("---")