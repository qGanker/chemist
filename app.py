# app.py (Final Stable Version with Self-Correction Drawing)

import streamlit as st
import random
import os
import pandas as pd
from PIL import Image

# --- НОВОЕ: Импортируем надежный компонент для рисования ---
from streamlit_drawable_canvas import st_canvas

# ================== БАЗА ДАННЫХ С ИМЕНАМИ ФАЙЛОВ ==================
chemical_data_full = {
    "Ароматические системы": {
        "Бензол": {"image": "Бензол.png", "факт": "Простейший ароматический углеводород."},
        "Фенол": {"image": "Фенол.png", "факт": "Проявляет слабые кислотные свойства."},
        "Анилин": {"image": "Анилин.png", "факт": "Основание для синтеза многих красителей."},
    },
    "Спирты": {
        "Метанол": {"image": "Метанол.png", "факт": "Сильный яд, вызывает слепоту и смерть."},
        "Этанол": {"image": "Этанол.png", "факт": "Получают спиртовым брожением углеводов."},
    },
    # ... Добавьте сюда остальные соединения по тому же принципу
}
# =====================================================================

# --- Инициализация состояния сессии ---
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

def reset_game(category):
    get_new_question(category)
    st.session_state.show_answer = False

def get_new_question(category):
    st.session_state.show_answer = False
    
    compounds_with_images = []
    for name, data in chemical_data_full[category].items():
        image_path = os.path.join("images", data.get("image", ""))
        # Проверяем реальное существование файла
        if os.path.exists(image_path):
            compounds_with_images.append(name)

    if not compounds_with_images:
        st.session_state.current_question = "no_images"
        return

    compound_name = random.choice(compounds_with_images)
    data = chemical_data_full[category][compound_name]
    
    st.session_state.current_question = {
        "name": compound_name,
        "image_path": os.path.join("images", data["image"]),
        "fact": data.get("fact", "Интересный факт еще не добавлен.")
    }

# --- Интерфейс приложения ---
st.set_page_config(layout="wide")
st.title("✍️ Тренажер по рисованию структур")

with st.sidebar:
    st.title("Настройки")
    categories = list(chemical_data_full.keys())
    selected_category = st.selectbox("Выберите категорию:", categories, index=0)
    
    if st.button("Начать / Следующий вопрос", use_container_width=True):
        reset_game(selected_category)
        st.rerun()

# --- Основная часть экрана ---
if st.session_state.current_question == "no_images":
    st.warning(f"В категории '{selected_category}' не найдено изображений в папке 'images'.")
elif not st.session_state.current_question:
    st.info("Выберите категорию и нажмите 'Начать' в меню слева.")
else:
    q = st.session_state.current_question
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Нарисуйте от руки:")
        st.info(f"## {q['name']}")

        # Настраиваем холст для рисования
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Цвет заливки (не используется)
            stroke_width=3,
            stroke_color="#FFFFFF", # Белый цвет для рисования
            background_color="#0E1117", # Темный фон
            height=400,
            width=500,
            drawing_mode="freedraw",
            key="canvas",
        )

    with col2:
        st.subheader("Правильный ответ:")
        
        if st.button("Показать ответ", use_container_width=True):
            st.session_state.show_answer = True

        if st.session_state.show_answer:
            # Показываем эталонное изображение
            try:
                image = Image.open(q["image_path"])
                st.image(image, caption="Эталонная структура")
                st.markdown(f"**💡 Интересный факт:** {q['fact']}")
            except FileNotFoundError:
                st.error(f"Файл изображения не найден: {q['image_path']}")
