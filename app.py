# app.py

import streamlit as st
import random

# ================== ОБНОВЛЕННАЯ БАЗА ДАННЫХ ==================
chemical_data_full = {
    "Алканы": {
        "Метан": {"молекулярная": "CH4", "структурная": "CH4", "факт": "Основной компонент природного газа."},
        "Этан": {"молекулярная": "C2H6", "структурная": "CH3-CH3", "факт": "Используется для производства этилена."},
        "Пропан": {"молекулярная": "C3H8", "структурная": "CH3-CH2-CH3", "факт": "Используется в баллонах для грилей и портативных плит."},
    },
    "Спирты и Фенолы": {
        "Метанол": {"молекулярная": "CH3OH", "структурная": "CH3-OH", "факт": "Сильный яд, также известен как древесный спирт."},
        "Этанол": {"молекулярная": "C2H5OH", "структурная": "CH3-CH2-OH", "факт": "Действующее вещество алкогольных напитков."},
        "Фенол": {"молекулярная": "C6H5OH", "структурная": "C6H5-OH", "факт": "Использовался как один из первых антисептиков (карболка)."}
    },
    "Карбоновые кислоты": {
        "Муравьиная кислота": {"молекулярная": "HCOOH", "структурная": "H-COOH", "факт": "Содержится в выделениях муравьев и в жгучих волосках крапивы."},
        "Уксусная кислота": {"молекулярная": "CH3COOH", "структурная": "CH3-COOH", "факт": "Главный компонент столового уксуса."},
    }
}
# =====================================================================

# --- Инициализация состояния сессии ---
# Добавили переменные для отслеживания отвеченных вопросов и режима игры
if 'answered_questions' not in st.session_state:
    st.session_state.answered_questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "Стандартный"

def reset_game(category, mode):
    """Сбрасывает игру для выбранной категории и режима."""
    st.session_state.answered_questions = []
    st.session_state.game_mode = mode
    get_new_question(category)
    st.session_state.show_answer = False

def get_new_question(category):
    """Генерирует новый, еще не заданный вопрос."""
    st.session_state.show_answer = False
    if category == "Смешанный режим":
        # Код для смешанного режима...
        pass # Упростим пример, оставив только категории
    else:
        full_list = list(chemical_data_full[category].keys())
        # Выбираем только из тех, на которые еще не отвечали
        unanswered_list = [q for q in full_list if q not in st.session_state.answered_questions]
        
        if not unanswered_list:
            st.session_state.current_question = None # Вопросы кончились
            return
            
        compound_name = random.choice(unanswered_list)

    formulas = chemical_data_full[category][compound_name]
    formula_type = random.choice(["молекулярная", "структурная"])
    
    st.session_state.current_question = {
        "name": compound_name,
        "formula_type": formula_type,
        "formula": formulas[formula_type],
        "fact": formulas["факт"]
    }

# --- Интерфейс приложения ---

st.set_page_config(layout="wide")
st.title("🧪 Продвинутый тренажер химических формул")

# --- Боковая панель ---
with st.sidebar:
    st.title("Настройки игры")
    selected_category = st.selectbox(
        "1. Выберите категорию:",
        list(chemical_data_full.keys())
    )
    
    # --- НОВОЕ: Блок для выбора режима игры ---
    selected_mode = st.radio(
        "2. Выберите режим:",
        ["Стандартный (Название -> Формула)", "Обратный (Формула -> Название)"],
        key="game_mode_selector"
    )

    # --- НОВОЕ: Кнопка для старта/сброса игры ---
    if st.button("Начать / Сбросить игру", use_container_width=True):
        reset_game(selected_category, selected_mode)
        st.rerun()

# --- Основная часть экрана ---
if not st.session_state.current_question:
    st.info("Выберите категорию и режим в меню слева, затем нажмите 'Начать / Сбросить игру'.")
else:
    # --- НОВОЕ: Используем колонки для лучшего вида ---
    col1, col2 = st.columns([2, 1.5])

    with col1:
        q = st.session_state.current_question
        mode = st.session_state.game_mode
        
        # --- НОВОЕ: Логика для разных режимов игры ---
        if mode == "Стандартный (Название -> Формула)":
            st.write(f"Введите **{q['formula_type']}** формулу для соединения:")
            st.info(f"## {q['name']}")
            correct_answer = q['formula']
        else: # Обратный режим
            st.write(f"Введите **название** соединения для формулы:")
            st.info(f"## `{q['formula']}`")
            correct_answer = q['name']

        user_answer = st.text_input("Ваш ответ:", key="user_input", disabled=st.session_state.show_answer)

        # --- ИЗМЕНЕНО: Кнопка проверки ответа ---
        if st.button("Проверить", disabled=st.session_state.show_answer, use_container_width=True):
            cleaned_user = user_answer.strip().upper().replace("-", "")
            cleaned_correct = correct_answer.strip().upper().replace("-", "")
            
            if cleaned_user == cleaned_correct:
                st.success("✅ Правильно!")
                st.session_state.answered_questions.append(q['name'])
            else:
                st.error(f"❌ Неверно. Правильный ответ: **{correct_answer}**")
            
            st.session_state.show_answer = True
            st.rerun()

        if st.session_state.show_answer:
            st.markdown(f"**💡 Интересный факт:** {q['fact']}")
            if st.button("Следующий вопрос", use_container_width=True):
                get_new_question(selected_category)
                st.rerun()

    with col2:
        # --- НОВОЕ: Панель прогресса и счета ---
        st.subheader("Ваш прогресс")
        total_questions = len(chemical_data_full[selected_category])
        answered_count = len(st.session_state.answered_questions)
        
        # Считаем правильные ответы (простой счетчик)
        score = answered_count
        st.metric(label="Правильных ответов", value=f"{score} из {total_questions}")
        
        # Прогресс-бар
        progress = answered_count / total_questions
        st.progress(progress, text=f"{progress:.0%} пройдено")

        if answered_count == total_questions:
            st.balloons()
            st.success("Поздравляем! Вы изучили всю категорию!")
