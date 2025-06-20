# app.py

import streamlit as st
import random
from rdkit import Chem
from rdkit.Chem import inchi
# Примечание: предполагается, что вы используете компонент, который работает, 
# например, st_jsme, или отлаживаете st_ketcher, как мы обсуждали.
# Замените st_ketcher на st_jsme, если используете его.
from streamlit_ketcher import st_ketcher 

# ================== ПОЛНАЯ БАЗА ДАННЫХ ИЗ PDF ==================
chemical_data_full = {
    "Ароматические и гетероциклические системы": {
        "Бензол": {"молекулярная": "C6H6", "структурная": "C6H6", "smiles": "c1ccccc1", "факт": "Простейший ароматический углеводород."},
        "Фенол": {"молекулярная": "C6H6O", "структурная": "C6H5-OH", "smiles": "c1ccc(O)cc1", "факт": "Проявляет слабые кислотные свойства, ранее использовался как антисептик."},
        "Анилин": {"молекулярная": "C6H7N", "структурная": "C6H5-NH2", "smiles": "c1ccc(N)cc1", "факт": "Основание для синтеза многих красителей."},
        "Нафталин": {"молекулярная": "C10H8", "структурная": "C10H8", "smiles": "c1ccc2ccccc2c1", "факт": "Имеет характерный запах, используется как средство от моли."},
        "Антрацен": {"молекулярная": "C14H10", "структурная": "C14H10", "smiles": "c1ccc2cc3ccccc3cc2c1", "факт": "Используется в производстве красителей, флуоресцирует синим цветом."},
        "Фенантрен": {"молекулярная": "C14H10", "структурная": "C14H10", "smiles": "c1ccc2c(c1)ccc3ccccc32", "факт": "Структурный фрагмент многих стероидов и алкалоидов."},
        "Пиррол": {"молекулярная": "C4H5N", "структурная": "C4H5N", "smiles": "c1cc[nH]c1", "факт": "Входит в состав гема (в гемоглобине) и хлорофилла."},
        "Фуран": {"молекулярная": "C4H4O", "структурная": "C4H4O", "smiles": "c1ccoc1", "факт": "Пятичленный гетероцикл с атомом кислорода."},
        "Тиофен": {"молекулярная": "C4H4S", "структурная": "C4H4S", "smiles": "c1ccsc1", "факт": "Пятичленный гетероцикл с атомом серы."},
        "Имидазол": {"молекулярная": "C3H4N2", "структурная": "C3H4N2", "smiles": "c1c[nH]cn1", "факт": "Важный структурный фрагмент аминокислоты гистидина."},
        "Пиридин": {"молекулярная": "C5H5N", "структурная": "C5H5N", "smiles": "c1ccncc1", "факт": "Шестичленный гетероцикл, аналог бензола с атомом азота."},
        "Пиримидин": {"молекулярная": "C4H4N2", "структурная": "C4H4N2", "smiles": "c1cncnc1", "факт": "Основа для азотистых оснований цитозина, тимина и урацила."},
        "Пурин": {"молекулярная": "C5H4N4", "структурная": "C5H4N4", "smiles": "c1cnc2c(n1)[nH]cn2", "факт": "Основа для аденина и гуанина."},
    },
    "Спирты и фенолы": {
        "Метанол": {"молекулярная": "CH4O", "структурная": "CH3-OH", "smiles": "CO", "факт": "Сильный яд, также известен как древесный спирт."},
        "Этанол": {"молекулярная": "C2H6O", "структурная": "CH3-CH2-OH", "smiles": "CCO", "факт": "Действующее вещество алкогольных напитков."},
        "Этиленгликоль": {"молекулярная": "C2H6O2", "структурная": "HO-CH2-CH2-OH", "smiles": "OCCO", "факт": "Двухатомный спирт, основной компонент антифризов."},
        "Глицерин": {"молекулярная": "C3H8O3", "структурная": "C(O)C(O)CO", "smiles": "C(O)C(O)CO", "факт": "Трехатомный спирт, используется в косметике и пищевой промышленности."},
        "Ксилит": {"молекулярная": "C5H12O5", "структурная": "C(O)C(O)C(O)C(O)CO", "smiles": "C(C(C(C(CO)O)O)O)O", "факт": "Пятиатомный спирт, используется как сахарозаменитель."},
        "Сорбит": {"молекулярная": "C6H14O6", "структурная": "C(O)C(O)C(O)C(O)C(O)CO", "smiles": "C(C(C(C(C(CO)O)O)O)O)O", "факт": "Шестиатомный спирт, используется как подсластитель."},
        "Этаноламин (коламин)": {"молекулярная": "C2H7NO", "структурная": "HO-CH2-CH2-NH2", "smiles": "C(CO)N", "факт": "Входит в состав фосфолипидов клеточных мембран."},
        "Холин": {"молекулярная": "C5H14NO+", "структурная": "[HO-CH2-CH2-N(CH3)3]+", "smiles": "C[N+](C)(C)CCO", "факт": "Витаминоподобное вещество (B4), предшественник ацетилхолина."},
    },
    "Альдегиды и Кетоны": {
        "Метаналь (формальдегид)": {"молекулярная": "CH2O", "структурная": "H-CHO", "smiles": "C=O", "факт": "Используется для консервации биологических материалов (формалин)."},
        "Этаналь (ацетальдегид)": {"молекулярная": "C2H4O", "структурная": "CH3-CHO", "smiles": "CC=O", "факт": "Продукт метаболизма этанола, вызывает симптомы похмелья."},
        "Пропаналь": {"молекулярная": "C3H6O", "структурная": "CH3-CH2-CHO", "smiles": "CCC=O", "факт": "Имеет резкий, удушливый запах."},
        "Бутаналь": {"молекулярная": "C4H8O", "структурная": "CH3-CH2-CH2-CHO", "smiles": "CCCC=O", "факт": "Также известен как масляный альдегид."},
        "Бензальдегид": {"молекулярная": "C7H6O", "структурная": "C6H5-CHO", "smiles": "c1ccc(C=O)cc1", "факт": "Имеет запах горького миндаля."},
        "Ацетон": {"молекулярная": "C3H6O", "структурная": "CH3-CO-CH3", "smiles": "CC(=O)C", "факт": "Простейший кетон, широко используется как растворитель."},
        "Глицериновый альдегид": {"молекулярная": "C3H6O3", "структурная": "HOCH2-CH(OH)-CHO", "smiles": "C(C(C=O)O)O", "факт": "Простейший представитель альдоз."},
    },
    "Карбоновые кислоты": {
        "Муравьиная кислота": {"молекулярная": "CH2O2", "структурная": "HCOOH", "smiles": "C(=O)O", "факт": "Содержится в яде муравьев и жгучих волосках крапивы."},
        "Уксусная кислота": {"молекулярная": "C2H4O2", "структурная": "CH3-COOH", "smiles": "CC(=O)O", "факт": "Основной компонент столового уксуса."},
        "Пропионовая кислота": {"молекулярная": "C3H6O2", "структурная": "CH3-CH2-COOH", "smiles": "CCC(=O)O", "факт": "Используется как консервант (пропионаты)."},
        "Масляная кислота": {"молекулярная": "C4H8O2", "структурная": "CH3-CH2-CH2-COOH", "smiles": "CCCC(=O)O", "факт": "Придает запах прогорклому сливочному маслу."},
        "Пальмитиновая кислота": {"молекулярная": "C16H32O2", "структурная": "C15H31COOH", "smiles": "CCCCCCCCCCCCCCCC(=O)O", "факт": "Одна из наиболее распространенных насыщенных жирных кислот."},
        "Стеариновая кислота": {"молекулярная": "C18H36O2", "структурная": "C17H35COOH", "smiles": "CCCCCCCCCCCCCCCCCC(=O)O", "факт": "Используется в производстве свечей и мыла."},
        "Щавелевая кислота": {"молекулярная": "C2H2O4", "структурная": "HOOC-COOH", "smiles": "C(=O)(C(=O)O)O", "факт": "Двухосновная кислота, ее соли (оксалаты) могут образовывать камни в почках."},
        "Малоновая кислота": {"молекулярная": "C3H4O4", "структурная": "HOOC-CH2-COOH", "smiles": "C(C(=O)O)C(=O)O", "факт": "Используется в синтезе витаминов B1 и B6."},
        "Янтарная кислота": {"молекулярная": "C4H6O4", "структурная": "HOOC-(CH2)2-COOH", "smiles": "C(CC(=O)O)C(=O)O", "факт": "Участник цикла Кребса (цикла трикарбоновых кислот)."},
        "Глутаровая кислота": {"молекулярная": "C5H8O4", "структурная": "HOOC-(CH2)3-COOH", "smiles": "C(CCC(=O)O)C(=O)O", "факт": "Пентандиовая дикарбоновая кислота."},
        "Бензойная кислота": {"молекулярная": "C7H6O2", "структурная": "C6H5-COOH", "smiles": "c1ccc(C(=O)O)cc1", "факт": "Используется как консервант (E210)."},
        "Салициловая кислота": {"молекулярная": "C7H6O3", "структурная": "HO-C6H4-COOH", "smiles": "c1ccc(C(=O)O)c(O)c1", "факт": "Основа для синтеза аспирина, обладает антисептическим действием."},
        "Никотиновая кислота": {"молекулярная": "C6H5NO2", "структурная": "C5H4N-COOH", "smiles": "c1cc(C(=O)O)ccn1", "факт": "Витамин PP или B3."},
        "Олеиновая кислота": {"молекулярная": "C18H34O2", "структурная": "C17H33COOH", "smiles": "CCCCCCCCC=CCCCCCCCC(=O)O", "факт": "Мононенасыщенная жирная кислота, главная в оливковом масле."},
        "Линолевая кислота": {"молекулярная": "C18H32O2", "структурная": "C17H31COOH", "smiles": "CCCCCC=CCC=CCCCCCCCC(=O)O", "факт": "Незаменимая жирная кислота (Омега-6)."},
        "Линоленовая кислота": {"молекулярная": "C18H30O2", "структурная": "C17H29COOH", "smiles": "CCC=CCC=CCC=CCCCCCCCC(=O)O", "факт": "Незаменимая жирная кислота (Омега-3)."},
        "Молочная кислота": {"молекулярная": "C3H6O3", "структурная": "CH3-CH(OH)-COOH", "smiles": "CC(C(=O)O)O", "факт": "Образуется в мышцах при физических нагрузках."},
        "Яблочная кислота": {"молекулярная": "C4H6O5", "структурная": "HOOC-CH(OH)-CH2-COOH", "smiles": "C(C(C(=O)O)O)C(=O)O", "факт": "Содержится во многих фруктах, особенно в яблоках."},
        "Лимонная кислота": {"молекулярная": "C6H8O7", "структурная": "HOOC-CH2-C(OH)(COOH)-CH2-COOH", "smiles": "C(C(=O)O)C(CC(=O)O)(C(=O)O)O", "факт": "Ключевой участник цикла Кребса."},
        "Пировиноградная кислота": {"молекулярная": "C3H4O3", "структурная": "CH3-CO-COOH", "smiles": "CC(=O)C(=O)O", "факт": "Конечный продукт гликолиза (ПВК)."},
        "Ацетоуксусная кислота": {"молекулярная": "C4H6O3", "структурная": "CH3-CO-CH2-COOH", "smiles": "CC(=O)CC(=O)O", "факт": "Одно из кетоновых тел."},
    },
    "Аминокислоты и Иминокислоты": {
        "Глицин (Гли)": {"молекулярная": "C2H5NO2", "структурная": "H2N-CH2-COOH", "smiles": "C(C(=O)O)N", "факт": "Простейшая аминокислота, не имеет оптических изомеров."},
        "Аланин (Ала)": {"молекулярная": "C3H7NO2", "структурная": "CH3-CH(NH2)-COOH", "smiles": "CC(C(=O)O)N", "факт": "Одна из наиболее распространенных аминокислот в белках."},
        "Валин (Вал)": {"молекулярная": "C5H11NO2", "структурная": "(CH3)2CH-CH(NH2)-COOH", "smiles": "CC(C)C(C(=O)O)N", "факт": "Незаменимая аминокислота с разветвленной цепью."},
        "Лейцин (Лей)": {"молекулярная": "C6H13NO2", "структурная": "(CH3)2CH-CH2-CH(NH2)-COOH", "smiles": "CC(C)CC(C(=O)O)N", "факт": "Незаменимая аминокислота, важна для построения мышц."},
        "Изолейцин (Иле)": {"молекулярная": "C6H13NO2", "структурная": "CH3-CH2-CH(CH3)-CH(NH2)-COOH", "smiles": "CCC(C)C(C(=O)O)N", "факт": "Имеет два хиральных центра."},
        "Серин (Сер)": {"молекулярная": "C3H7NO3", "структурная": "HO-CH2-CH(NH2)-COOH", "smiles": "C(C(C(=O)O)N)O", "факт": "Гидроксиаминокислота, важна для активных центров ферментов."},
        "Треонин (Тре)": {"молекулярная": "C4H9NO3", "структурная": "CH3-CH(OH)-CH(NH2)-COOH", "smiles": "CC(C(C(=O)O)N)O", "факт": "Незаменимая гидроксиаминокислота."},
        "Цистеин (Цис)": {"молекулярная": "C3H7NO2S", "структурная": "HS-CH2-CH(NH2)-COOH", "smiles": "C(C(C(=O)O)N)S", "факт": "Способен образовывать дисульфидные мостики в белках."},
        "Метионин (Мет)": {"молекулярная": "C5H11NO2S", "структурная": "CH3-S-(CH2)2-CH(NH2)-COOH", "smiles": "CSCCC(C(=O)O)N", "факт": "Незаменимая серосодержащая аминокислота."},
        "Аспарагиновая кислота (Асп)": {"молекулярная": "C4H7NO4", "структурная": "HOOC-CH2-CH(NH2)-COOH", "smiles": "C(C(C(=O)O)N)C(=O)O", "факт": "Кислая аминокислота, нейромедиатор."},
        "Глутаминовая кислота (Глу)": {"молекулярная": "C5H9NO4", "структурная": "HOOC-(CH2)2-CH(NH2)-COOH", "smiles": "C(CC(=O)O)C(C(=O)O)N", "факт": "Важнейший возбуждающий нейромедиатор в нервной системе."},
        "Лизин (Лиз)": {"молекулярная": "C6H14N2O2", "структурная": "H2N-(CH2)4-CH(NH2)-COOH", "smiles": "C(CCN)C(C(=O)O)N", "факт": "Основная незаменимая аминокислота."},
        "Аргинин (Арг)": {"молекулярная": "C6H14N4O2", "структурная": "H2N-C(NH)-NH-(CH2)3-CH(NH2)-COOH", "smiles": "C(CC(C(=O)O)N)CN=C(N)N", "факт": "Имеет сильноосновную гуанидиновую группу."},
        "Фенилаланин (Фен)": {"молекулярная": "C9H11NO2", "структурная": "C6H5-CH2-CH(NH2)-COOH", "smiles": "c1ccc(CC(C(=O)O)N)cc1", "факт": "Ароматическая незаменимая аминокислота."},
        "Тирозин (Тир)": {"молекулярная": "C9H11NO3", "структурная": "HO-C6H4-CH2-CH(NH2)-COOH", "smiles": "c1cc(O)ccc1CC(C(=O)O)N", "факт": "Предшественник дофамина, адреналина и гормонов щитовидной железы."},
        "Гистидин (Гис)": {"молекулярная": "C6H9N3O2", "структурная": "C3H3N2-CH2-CH(NH2)-COOH", "smiles": "c1c(C[C@H](C(=O)O)N)c[nH]n1", "факт": "Входит в активные центры многих ферментов."},
        "Триптофан (Три)": {"молекулярная": "C11H12N2O2", "структурная": "C8H6N-CH2-CH(NH2)-COOH", "smiles": "c1ccc2c(c1)c(C[C@H](C(=O)O)N)[nH]2", "факт": "Предшественник серотонина и мелатонина."},
        "Пролин (Про)": {"молекулярная": "C5H9NO2", "структурная": "C4H8N-COOH", "smiles": "C1CC(NC1)C(=O)O", "факт": "Иминокислота, создающая жесткие изгибы в цепях белков."},
    },
    "Углеводы": {
        "D-глюкоза": {"молекулярная": "C6H12O6", "структурная": "C6H12O6", "smiles": "C([C@@H]1[C@H]([C@@H]([C@H](C(O1)O)O)O)O)O", "факт": "Основной источник энергии для клеток, «виноградный сахар»."},
        "D-фруктоза": {"молекулярная": "C6H12O6", "структурная": "C6H12O6", "smiles": "C([C@@H]1[C@H]([C@@H](C(O1)CO)O)O)O", "факт": "Кетосахар, самый сладкий из природных сахаров."},
        "D-галактоза": {"молекулярная": "C6H12O6", "структурная": "C6H12O6", "smiles": "C([C@@H]1[C@H]([C@@H]([C@H](C(O1)O)O)O)O)O", "факт": "Входит в состав лактозы (молочного сахара)."},
        "D-рибоза": {"молекулярная": "C5H10O5", "структурная": "C5H10O5", "smiles": "C([C@@H]1[C@H]([C@@H](C(O1)O)O)O)O", "факт": "Входит в состав РНК и АТФ."},
        "D-дезоксирибоза": {"молекулярная": "C5H10O4", "структурная": "C5H10O4", "smiles": "C(C1C(C(C(O1)O)O)O)O", "факт": "Отличается от рибозы отсутствием гидроксила у C2, входит в состав ДНК."},
        "Сахароза": {"молекулярная": "C12H22O11", "структурная": "C12H22O11", "smiles": "C([C@@H]1[C@H]([C@@H]([C@H](C(O1)O[C@]2(C(C(C(O2)CO)O)O)CO)O)O)O)O", "факт": "Тростниковый или свекловичный сахар."},
    },
    "Азотистые основания и их производные": {
        "Аденин": {"молекулярная": "C5H5N5", "структурная": "C5H5N5", "smiles": "c1nc(N)c2nc[nH]c2n1", "факт": "Пуриновое основание, входит в состав ДНК, РНК, АТФ."},
        "Гуанин": {"молекулярная": "C5H5N5O", "структурная": "C5H5N5O", "smiles": "c1nc(N)c2[nH]c(=O)[nH]c2n1", "факт": "Пуриновое основание в ДНК и РНК."},
        "Цитозин": {"молекулярная": "C4H5N3O", "структурная": "C4H5N3O", "smiles": "c1cncc(=O)[nH]1N", "факт": "Пиримидиновое основание в ДНК и РНК."},
        "Тимин": {"молекулярная": "C5H6N2O2", "структурная": "C5H6N2O2", "smiles": "Cc1cn[nH]c(=O)[nH]1c1=O", "факт": "Пиримидиновое основание, содержится только в ДНК."},
        "Урацил": {"молекулярная": "C4H4N2O2", "структурная": "C4H4N2O2", "smiles": "c1cn[nH]c(=O)[nH]1c1=O", "факт": "Пиримидиновое основание, заменяет тимин в РНК."},
        "Кофеин": {"молекулярная": "C8H10N4O2", "структурная": "C8H10N4O2", "smiles": "Cn1cnc2c1c(=O)n(C)c(=O)n2C", "факт": "Алкалоид, психостимулятор."},
        "Теобромин": {"молекулярная": "C7H8N4O2", "структурная": "C7H8N4O2", "smiles": "Cn1c(=O)[nH]c2cnc(C)n2c1=O", "факт": "Содержится в какао-бобах (шоколаде)."},
    }
}
# =====================================================================

# --- Инициализация состояния сессии ---
# (Без изменений)
if 'answered_questions' not in st.session_state:
    st.session_state.answered_questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "Стандартный (Название -> Формула)"
if 'user_drawing' not in st.session_state:
    st.session_state.user_drawing = ""

# --- НОВОЕ: Универсальный парсер для чтения структур ---
def mol_from_input(input_data):
    """
    Создает молекулу RDKit из разных форматов (SMILES или Molblock).
    """
    if not input_data:
        return None
    # Если в строке есть перенос - это, скорее всего, Molblock
    if '\n' in input_data:
        return Chem.MolFromMolBlock(input_data)
    # Иначе, это SMILES
    else:
        return Chem.MolFromSmiles(input_data)

# --- ИЗМЕНЕНО: Функция сравнения теперь использует новый парсер ---
def compare_structures(input_drawn, smiles_correct):
    """
    Сравнивает структуры по InChIKey, используя универсальный парсер.
    """
    # Используем новый парсер для обоих входов для единообразия
    mol_drawn = mol_from_input(input_drawn)
    mol_correct = mol_from_input(smiles_correct)

    if mol_drawn is None or mol_correct is None:
        return False
        
    # Возвращаемся к надежному сравнению по InChIKey, т.к. теперь у нас есть корректные молекулы
    key_drawn = inchi.MolToInchiKey(mol_drawn)
    key_correct = inchi.MolToInchiKey(mol_correct)
    
    return key_drawn == key_correct

# --- Остальные функции (reset_game, get_new_question) остаются без изменений ---
def reset_game(category, mode):
    st.session_state.answered_questions = []
    st.session_state.game_mode = mode
    st.session_state.user_drawing = ""
    get_new_question(category)
    st.session_state.show_answer = False

def get_new_question(category):
    st.session_state.show_answer = False
    st.session_state.user_drawing = ""
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
        "formula": data.get("formula", ""),
        "smiles": data.get("smiles", ""),
        "fact": data.get("fact", "Интересный факт для этого соединения еще не добавлен.")
    }

# --- Интерфейс приложения (без изменений) ---
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
        st.caption("Совет: старайтесь рисовать только одну молекулу для ответа.")
        
        if not st.session_state.show_answer:
            # Важно: Ketcher может возвращать SMILES или Molblock, наша функция теперь это учтет
            user_input_data = st_ketcher(key="ketcher_input")
            if st.button("Проверить рисунок", use_container_width=True):
                st.session_state.user_drawing = user_input_data
                st.session_state.show_answer = True
                st.rerun()

        if st.session_state.show_answer:
            is_correct = compare_structures(st.session_state.user_drawing, q['smiles'])

            if is_correct:
                st.success("✅ Абсолютно верно! Отличная работа!")
                if q['name'] not in st.session_state.answered_questions:
                    st.session_state.answered_questions.append(q['name'])
            else:
                st.error("❌ Структура неверна. Вот правильный ответ:")
                st_ketcher(value=q['smiles'], key="ketcher_solution")

            st.markdown(f"**💡 Интересный факт:** {q['fact']}")
            if st.button("Следующий вопрос", use_container_width=True):
                get_new_question(selected_category)
                st.rerun()
                
    else: # Текстовые режимы
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
