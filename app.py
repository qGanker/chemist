# app.py

import streamlit as st
import random

# ================== БАЗА ДАННЫХ ХИМИЧЕСКИХ ФОРМУЛ ==================
# Та же самая база данных, что и раньше
chemical_data_full = {
    "Алканы": {
        "Метан": {"молекулярная": "CH4", "структурная": "CH4"},
        "Этан": {"молекулярная": "C2H6", "структурная": "CH3-CH3"},
        "Пропан": {"молекулярная": "C3H8", "структурная": "CH3-CH2-CH3"},
    },
    "Спирты и Фенолы": {
        "Метанол": {"молекулярная": "CH3OH", "структурная": "CH3-OH"},
        "Этанол": {"молекулярная": "C2H5OH", "структурная": "CH3-CH2-OH"},
        "Фенол": {"молекулярная": "C6H5OH", "структурная": "C6H5-OH"}
    },
    "Карбоновые кислоты": {
        "Муравьиная кислота": {"молекулярная": "HCOOH", "структурная": "H-COOH"},
        "Уксусная кислота": {"молекулярная": "CH3COOH", "структурная": "CH3-COOH"},
    },
    "Альдегиды и Кетоны": {
        "Ацетальдегид": {"молекулярная": "C2H4O", "структурная": "CH3-CHO"},
        "Ацетон": {"молекулярная": "C3H6O", "структурная": "CH3-CO-CH3"}
    },
}
# =====================================================================

# Инициализация состояния сессии (чтобы переменные не сбрасывались)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'category' not in st.session_state:
    st.session_state.category = None


def get_new_question(category):
    """Генерирует новый вопрос и сохраняет его в session_state."""
    if category == "Смешанный режим":
        all_formulas = {}
        for topic_dict in chemical_data_full.values():
            all_formulas.update(topic_dict)
        formulas_to_learn = all_formulas
    else:
        formulas_to_learn = chemical_data_full[category]
    
    compound_name = random.choice(list(formulas_to_learn.keys()))
    formulas = formulas_to_learn[compound_name]
    formula_type = random.choice(["молекулярная", "структурная"])
    correct_answer = formulas[formula_type]
    
    st.session_state.current_question = {
        "compound": compound_name,
        "type": formula_type,
        "answer": correct_answer,
        "all_formulas": formulas
    }

# --- Интерфейс приложения ---

st.title("🧪 Тренажер химических формул")

# Боковая панель для выбора категории
st.sidebar.title("Настройки")
selected_category = st.sidebar.selectbox(
    "Выберите категорию:",
    ["--"] + list(chemical_data_full.keys()) + ["Смешанный режим"]
)

if selected_category != "--":
    # Если пользователь выбрал новую категорию
    if st.session_state.category != selected_category:
        st.session_state.category = selected_category
        st.session_state.score = 0  # Сбрасываем счет при смене категории
        get_new_question(selected_category)
        st.rerun() # Перезапускаем скрипт, чтобы обновить интерфейс

    # Отображение счета
    st.header(f"Тема: {st.session_state.category}")
    st.subheader(f"Ваш счет: {st.session_state.score}")

    # Если вопрос сгенерирован
    if st.session_state.current_question:
        q = st.session_state.current_question
        st.write(f"Введите **{q['type']}** формулу для соединения:")
        st.info(f"## **{q['compound']}**")

        # Форма для ввода ответа
        with st.form(key="answer_form"):
            user_answer = st.text_input("Ваш ответ:", key="user_input")
            submit_button = st.form_submit_button("Проверить")

        if submit_button and user_answer:
            # Логика проверки ответа
            cleaned_user = user_answer.strip().upper().replace("-", "")
            cleaned_correct = q['answer'].strip().upper().replace("-", "")

            if cleaned_user == cleaned_correct:
                st.session_state.score += 1
                st.success("✅ Правильно!")
            else:
                st.error(f"❌ Неверно. Правильный ответ: {q['answer']}")
                st.write(f"**Все формулы для '{q['compound']}':**")
                st.write(f"- Молекулярная: `{q['all_formulas']['молекулярная']}`")
                st.write(f"- Структурная: `{q['all_formulas']['структурная']}`")

            # Генерируем следующий вопрос и очищаем поле ввода
            get_new_question(st.session_state.category)
            st.rerun()

else:
    st.info("Пожалуйста, выберите категорию в меню слева, чтобы начать игру.")
