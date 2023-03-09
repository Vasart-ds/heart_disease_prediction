import pandas as pd
import streamlit as st
import pickle

# интерфейс
age = st.sidebar.number_input(min_value=18, max_value=100, label='Введите ваш возраст:', key='age')

gender = st.sidebar.radio('Выберете ваш пол:', ('М', 'Ж'))

def gender_column(col):
    if col == 'М':
        return 0
    else:
        return 1

height = st.sidebar.number_input(min_value=100, max_value=255, label='Введите ваш рост:', key='height')
weight = st.sidebar.number_input(min_value=40, max_value=300, label='Введите ваш вес:', key='wieght')

st.sidebar.write("Ваше давление в состоянии покоя")
ap_hi, ap_lo = st.sidebar.columns(2)
ap_hi = ap_hi.number_input(min_value=40, max_value=250, label='Верхнее:', key='ap_hi')
ap_lo = ap_lo.number_input(min_value=20, max_value=200, label='Нижнее:', key='ap_lo')

gluc, chol = st.sidebar.columns(2)
gluc = gluc.selectbox("Уровень сахара", (1, 2, 3))
chol = chol.selectbox("Уровень холестерина", (1, 2, 3))

alco, smoke, active = st.sidebar.columns(3)
smoke = smoke.selectbox('Курение', ('Нет', 'Да'))
alco = alco.selectbox('Алкоголь', ('Нет', 'Да'))
active = active.selectbox('Активность', ('Нет', 'Да'))

def alc_smk_act(value):
    if value == 'Нет':
        return 0
    else:
        return 1

# основной экран

if st.sidebar.button('Рассчитать'):
    data = pd.DataFrame(
        {
            'age': [age],
            'gender': [gender_column(gender)],
            'height': [height],
            'weight': [weight],
            'ap_hi': [ap_hi],
            'ap_lo': [ap_lo],
            'cholesterol': [chol],
            'gluc': [gluc],
            'smoke': [alc_smk_act(smoke)],
            'alco': [alc_smk_act(alco)],
            'active': [alc_smk_act(active)]
        }
    ).astype('int64')
    try:
        model = pickle.load(open(r'D:\workplace\data_science\pycharm\mvp_workshop\xgb_grid_clf.pcl', 'rb'))
    except:
        model = pickle.load(open("./xgb_grid_clf.pcl", "rb"))
    result = model.predict_proba(data)[:, 1]
    result = result[0]

    st.subheader(f'Вероятность возникновения сердечно-сосудистого заболевания: **{result:.0%}**.')

    if result < 0.2:
        st.markdown('Поздравляем! У вас отличное здоровье, однако не забывайте чистить зубы, ложиться спать не позднее '
                    '23 часов и говорить по утрам: **"Доброе утро!"** всем вокруг;)')
        st.image('https://gagz.ru/wp-content/uploads/2017/08/3-41.jpg')
    elif 0.2 < result < 0.5:
        st.write('Ваше здоровье на достаточно хорошем уровне, но помните, что здоровый образ жизни, позитивное мышление '
                 'и отсутствие переработок помогут вам оставаться здоровым как можно дольше!')
        st.image('https://cdn.anywellmag.com/2018/10/hhpy-1-920x600.jpg')
    elif 0.5 < result < 0.75:
        st.write('Кажется, вам пора заняться собой. Для начала постарайтесь выспаться, наладить режим, а уже после '
                 '(если не будет улучшений) - обратиться за помощью к специалистам.')
        st.image('https://demotos.ru/sites/default/files/caricatures/2019-12-20-1576838681.jpg')

    elif result > 0.75:
        st.markdown('Вам нужно **срочно** заняться своим здоровьем - риск слишком велик!')
        st.image('https://bigpicture.ru/wp-content/uploads/2021/04/bigpicture_ru_muzhik-s-peskom-shablon.jpg')
        st.markdown('Если вы вдруг чувствуете, что что-то с вами не так')
else:
    st.header('Расчёт риска возникновения середнчно-сосудистых заболеваний')
    st.subheader('Введите данные о себе в поле слева. После этого нажмите кнопку "Рассчитать" и получите '
                 'персональную информацию о вероятности возникновения у вас заболеваний.')
