# app.py (DEBUGGING VERSION)

import streamlit as st

# --- НОВОЕ: Импортируем только то, что нужно для отладки ---
from streamlit_ketcher import st_ketcher

# --- Интерфейс приложения ---
st.set_page_config(layout="wide")
st.title("🔬 Отладка компонента Ketcher")

st.info("Цель этой страницы — понять, какие данные возвращает компонент для рисования.")
st.write("Пожалуйста, нарисуйте в холсте ниже молекулу (например, бензол или фенол). Текст в сером блоке под ним должен измениться, показав нам данные, которые компонент передает в Python.")

# Вызов компонента для рисования
user_input_data = st_ketcher(key="ketcher_debug")

st.markdown("---")
st.subheader("Сырые данные от компонента Ketcher:")

# Показываем сырые данные в виде текста. Если компонент ничего не возвращает,
# мы увидим "None" или пустую строку.
st.code(f"{user_input_data}", language="text")
