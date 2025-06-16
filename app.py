# app.py

import streamlit as st
import random
from rdkit import Chem
from streamlit_ketcher import st_ketcher

# ================== БАЗА ДАННЫХ СО SMILES И ФАКТАМИ ==================
chemical_data_full = {
    "Ароматические системы": {
        "Бензол": {"молекулярная": "C6H6", "структурная": "C6H6", "smiles": "c1ccccc1", "факт": "Простейший ароматический углеводород."},
        "Фенол": {"молекулярная": "C6H6O", "структурная": "C6H5-OH", "smiles": "c1ccc(O)cc1", "факт": "Проявляет слабые кислотные свойства."},
        "Анилин": {"молекулярная": "C6H7N", "структурная": "C6H5-NH2", "smiles": "c1ccc(N)cc1", "факт": "Основание для синтеза многих красителей."},
        "Нафталин": {"молекулярная": "C10H8", "структурная": "C10H8 (два кольца)", "smiles": "c1ccc2ccccc2c1", "факт": "Раньше использовался как средство от моли."},
    },
    "Спирты": {
        "Метанол": {"молекулярная": "CH4O", "структурная": "CH3-OH", "smiles": "CO", "факт": "Сильный яд, вызывает слепоту и смерть."},
        "Этанол": {"молекулярная": "C2H6O", "структурная": "CH3-CH2-OH", "smiles": "CCO", "факт": "Получают спиртовым брожением углеводов."},
        "Глицерин": {"молекулярная": "C3H8O3", "структурная": "C(O)C(O)CO", "smiles": "C(C(CO)O)O", "факт": "Трехатомный спирт, используется в косметике."},
    },
    "Карбоновые кислоты": {
        "Уксусная кислота": {"молекулярная": "C2H4O2", "структурная": "CH3-COOH", "smiles": "CC(=O)O", "факт": "Продукт скисания вина, основной компонент уксуса."},
        "Молочная кислота": {"молекулярная": "C3H6O3", "структурная": "CH3-CH(OH)-COOH", "smiles": "CC(C(=O)O)O", "факт": "Образуется в мышцах при физической нагрузке."},
        "Аспирин": {"молекулярная": "C9H8O4", "структурная": "CH3COO-C6H4-COOH", "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O", "факт": "Ацетилсалициловая кислота, жаропонижающее средство."},
    },
    "Аминокислоты": {
        "Глицин": {"молекулярная": "C2H5NO2", "структурная": "H2N-CH2-COOH", "smiles": "C(C(=O)O)N", "факт": "Простейшая аминокислота."},
        "Аланин": {"молекулярная": "C3H7NO2", "структурная": "CH3-CH(NH2)-COOH", "smiles": "CC(C(=O)O)N", "факт": "Одна из наиболее распространенных аминокислот в белках."},
        "Фенилаланин": {"молекулярная": "C9H11NO2", "структурная": "C6H5-CH2-CH(NH2)-COOH", "smiles": "c1ccc(CC(C(=O)O)N)cc1", "факт": "Ароматическая незаменимая аминокислота."},
    },
    "Азотистые основания": {
        "Аденин": {"молекулярная": "C5H5N5", "структурная": "C5H5N5", "smiles": "c1nc(N)c2nc[nH]c2n1", "факт": "Пуриновое основание в ДНК и РНК."},
        "Урацил": {"молекулярная": "C4H4N2O2", "структурная": "C4H4N2O2", "smiles": "c1cc(O)nc(O)[nH]1", "факт": "Пиримидиновое основание, присутствует только в РНК."}
    }
}
# =====================================================================

# --- Инициализация состояния сессии ---
if 'answered_questions' not in st.session_state:
    st.session_state.answered_questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "Стандартный (Название -> Формула)"

def compare_smiles(smiles1, smiles2):
    """Сравнивает две строки SMILES, приводя их к каноническому виду."""
    if not smiles1 or not smiles2:
        return False
    mol1 = Chem.MolFromSmiles(smiles1)
    mol2 = Chem.MolFromSmiles(smiles2)
    if mol1 is None or mol2 is None:
        return False
    canon_smiles1 = Chem.MolToSmiles(mol1, canonical=True)
    canon_smiles2 = Chem.MolToSmiles(mol2, canonical=True)
    return canon_smiles1 == canon_smiles2

def reset_game(category, mode):
    """Сбрасывает игру для выбранной категории и режима."""
    st.session_state.answered_questions = []
    st.session_state.game_mode = mode
    get_new_question(category)
    st.session_state.show_answer = False

def get_new_question(category):
    """Генерирует новый, еще не заданный вопрос."""
    st.session_state.show_answer = False
    full_list = list(chemical_data_full[category].keys())
    unanswered_list = [q for q in full_list if q not in st.session_state.answered_questions]
    if not unanswered_list:
        st.session_state.current_question = None
        return
    compound_name = random.choice(unanswered_list)
    data = chemical_data_full[category][compound_name]
    formula_type = random.choice(["молекулярная", "структурная"])
    
    st.session_state.current_question = {
        "name": compound_name,
        "formula_type": formula_type,
        "formula": data.get("formula", ""), # Используем .get() для безопасности
        "smiles": data.get("smiles", ""), # Используем .get() для безопасности
        # --- ИСПРАВЛЕНИЕ: Используем data.get() вместо data[] ---
        # Это предотвратит падение, если "факт" отсутствует.
        "fact": data.get("fact", "Интересный факт для этого соединения еще не добавлен.")
    }

# --- Интерфейс приложения ---
st.set_page_config(layout="wide")
st.title("🎨 Химический тренажер с режимом рисования")

with st.sidebar:
    st.title("Настройки игры")
    categories = list(chemical_data_full.keys())
    selected_category = st.selectbox("1. Выберите категорию:", categories, index=0)
    
    selected_mode = st.radio(
        "2. Выберите режим:",
        ["Стандартный (Название -> Формула)", "Обратный (Формула -> Название)", "✍️ Режим рисования (Название -> Структура)"],
        key="game_mode_selector"
    )

    if st.button("Начать / Сбросить игру", use_container_width=True):
        reset_game(selected_category, selected_mode)
        st.rerun()

if not st.session_state.current_question:
    st.info("Выберите категорию и режим в меню слева, затем нажмите 'Начать / Сбросить игру'.")
else:
    q = st.session_state.current_question
    mode = st.session_state.game_mode

    if mode == "✍️ Режим рисования (Название -> Структура)":
        st.subheader("Нарисуйте структурную формулу для:")
        st.info(f"## {q['name']}")
        
        smiles_drawn = st_ketcher(value=None, key="ketcher_canvas")
        
        if st.button("Проверить рисунок", use_container_width=True):
            if compare_smiles(smiles_drawn, q['smiles']):
                st.success("✅ Абсолютно верно! Отличная работа!")
                if q['name'] not in st.session_state.answered_questions:
                    st.session_state.answered_questions.append(q['name'])
            else:
                st.error("❌ Структура неверна. Попробуйте еще раз.")
            
            st.session_state.show_answer = True
            st.rerun()

        if st.session_state.show_answer:
            st.markdown(f"**💡 Интересный факт:** {q['fact']}")
            if st.button("Следующий вопрос", use_container_width=True):
                get_new_question(selected_category)
                st.rerun()
                
    else:
        col1, col2 = st.columns([2, 1.5])
        with col1:
            if mode == "Стандартный (Название -> Формула)":
                st.write(f"Введите **{q['formula_type']}** формулу для соединения:")
                st.info(f"## {q['name']}")
                correct_answer = q['formula']
            else:
                st.write(f"Введите **название** соединения для формулы:")
                st.info(f"## `{q['formula']}`")
                correct_answer = q['name']

            user_answer = st.text_input("Ваш ответ:", key="user_input", disabled=st.session_state.show_answer)

            if st.button("Проверить", disabled=st.session_state.show_answer, use_container_width=True):
                cleaned_user = user_answer.strip().upper().replace("-", "")
                cleaned_correct = correct_answer.strip().upper() if mode == "Обратный (Формула -> Название)" else correct_answer.strip().upper().replace("-", "")
                
                if cleaned_user == cleaned_correct:
                    st.success("✅ Правильно!")
                    if q['name'] not in st.session_state.answered_questions:
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
            st.subheader("Ваш прогресс")
            total_questions = len(chemical_data_full[selected_category])
            answered_count = len(st.session_state.answered_questions)
            score = answered_count
            st.metric(label="Правильных ответов", value=f"{score} из {total_questions}")
            if total_questions > 0:
                progress = answered_count / total_questions
                st.progress(progress, text=f"{progress:.0%} пройдено")
                if answered_count == total_questions:
                    st.balloons()
                    st.success("Поздравляем! Вы изучили всю категорию!")
