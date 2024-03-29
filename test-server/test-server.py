from flask import Flask, render_template, request, jsonify
import requests


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


groups = {
    "Б-ИВТ-21-1": "09.03.01|7618|ИМИ-Б-ИВТ-21-1|5954",
    "Б-М-21": "01.03.01|7468|ИМИ-Б-М-21|5996",
    "Б-ФИИТ-21": "02.03.02|7471|ИМИ-Б-ФИИТ-21|5998",
    "Б-ИВТ-21-2": "09.03.01|7619|ИМИ-Б-ИВТ-21-2|5999",
    "Б-ИТСС-21": "11.03.02|7467|ИМИ-Б-ИТСС-21|6003",
    "Б-МПО-21": "44.03.01|7469|ИМИ-Б-МПО-21|6004",
    "Б-ПОИМ-21": "44.03.05|7470|ИМИ-Б-ПОИМ-21|6005",
    "Б-ПИГМУ-21": "09.03.03|7856|ИМИ-Б-ПИГМУ-21|6406",
    "Б-ПИЭ-21": "09.03.03|7855|ИМИ-Б-ПИЭ-21|6407",
    "Б-ПМИ-21": "01.03.02|7623|ИМИ-Б-ПМИ-21|6724",
}

lecturers = {
    "895038073": "Акимов Федор Револьевич",
    "714069": "Алексеев Николай Кириллович",
    "90258224": "Неустроева Тамара Константиновна",
    "895038074": "Варламова Анастасия Гаврииловна",
    "895035721": "Васильева Лира Петровна",
    "895035612": "Габышева Анна Михайловна",
    "895038096": "Верховцев Семен Денисович",
    "895038199": "Голоков Вячеслав Валерьевич",
    "717477": "Дедюкина Любовь Лукинична",
    "717689": "Донская Маргарита Ивановна",
    "718121": "Егорова Валентина Никифоровна",
}


@app.route('/load_group', methods=["GET", "POST"])
def loadgroup():
    group_name = request.form.get('groupname')
    group_data = groups.get(group_name)
    return group_data if group_data else f"Не найден ИД группы {group_name}"

@app.route('/get_lecturer', methods=["GET", "POST"])
def loadgroup():
    lecturer_name = request.form.get('lecturername')
    lecturer_data = lecturers.get(lecturer_name)
    return lecturer_data if lecturer_data else f"Не найден ИД преподавателя {lecturer_name}"


@app.route('/')
def index():
    return render_template("index.html")

    return render_template("step1.html")


@app.route('/corpus', methods=["GET", "POST"])
def corpus():
    corpuses = {
        "Moodle": 'Дистанционные курсы Moodle(г. Якутск)',
        "Zoom": 'Zoom(Интернет)',
        "АГИИК": 'Арктический государственный институт культуры и искусств(г. Якутск, Орджоникидзе, 4)',
        "АДФ": 'Корпус автодорожного факультета(г. Якутск, Красильникова,13)',
        "АИЦ": 'Арктический инновационный центр(г. Якутск, Кулаковского, 46)',
        "АК МИ": 'Анатомический корпус Медицинского Института(г. Якутск, Кулаковского, 34)',
        "АО ДСК": 'АО "Домостроительный комбинат"(г.Якутск,Покровский тракт 6 км, 10)',
        "АУ Республиканский дом-интернат для престарелых и инвалидов": 'АУ "Республиканский дом-интернат для престарелых и инвалидов имени В.П. Решетникова"(г. Якутск, ул. Петра Алексеева, д. 6, корп. 1)',
        "Бассейн \"Долгун\"": 'Плавательный бассейн "Долгун"(г. Якутск, Каландаришвили, 15)',
        "БСМЭ": 'Бюро судебной медицинской экспертизы(г. Якутск, Стадухина, 81)',
        "ГАПОУ РС (Я) \"Автодорожный техникум\"": 'Государственное автономное профессиональное образовательное учреждение РС (Я) Якутский автодорожный техникум(г. Якутск, Вилюйский тракт 5 км, 1 корпус 1)',
        "ГБ№4": 'ГАУ РС(Я) "Медицинский центр" г.Якутска(г. Якутск, 202-й микрорайон, 2 )',
        "ГБУ Поликлиника №1": 'ГАУ РС(Я) Поликлиники №1(г. Якутск, ул. Кирова 19)',
        "ГБУ РС(Я) НПЦ \"Фтизиатрия\"": 'ГАУ РС(Я) НПЦ "Фтизиатрия"(г. Якутск, ул.Петра Алексеева, 93)',
        "ГКОУ РС(Я) «РС(К)ШИНО»": 'Государственное Казённое Образовательное Учреждение «Республиканская специальная (коррекционная) школа-интернат для неслышащих обучающихся(г. Якутск, ул. Кузьмина 36)',
        "ГОХРАН": '"Государственное хранилище ценностей Республики Саха (Якутия)"(г. Якутск, ул. Кирова 12)',
        "ГУК": 'Главный учебный корпус(г. Якутск, ул. Кулаковского, 42)',
        "Департамент градостроительства": 'Департамент градостроительства(г. Якутск, ул. Октябрьская, 20/1)',
        "Детская поликлиника": 'Детская поликлиника(г. Якутск, ул. Петровского, 6)',
        "Детская стоматологическая поликлиника": 'Детская стоматологическая поликлиника(г. Якутск, ул.Ярославского, 6/3)',
        "Дзержинского 35": 'Дзержинского 35(г. Якутск, ул. Дзержинского, 35)',
        "ДИКБ": 'Детская инфекционная клиническая больница(г. Якутск, ул. Курашова 91/3)',
        "ДОУ 1": 'Детский сад № 1 "Звёздочка"(г. Якутск, 50 лет Сов Армии 23/4 "А")',
        "Зал СБ": 'Зал борьбы СВФУ(ул.Каландаришвили, 17, 66 корпус, Блок "Г")',
        "ИГАБМ": 'Институт геологии алмаза и благородных металлов СО РАН(г. Якутск, пр. Ленина, 39)',
        "ИГДС": 'Институт горного дела Севера им. Н.В. Черского СО РАН(г. Якутск, Ленина проспект, 43)',
        "ИКФиА": 'Институт космофизических исследований и аэрономии(г. Якутск, Ленина проспект, 31)',
        "Институт мерзлотоведения": 'Институт мерзлотоведения имени П. И. Мельникова СО РАН(г. Якутск, ул. Мерзлотная, 36)',
        "Институт проблем нефти и газа": 'Институт проблем нефти и газа СО РАН(г. Якутск, ул. Октябрьская, 1)',
        "ИФТПС": 'Институт физико-технических проблем Севера СО РАН(г. Якутск, ул. Октябрьская, 1)',
        "Кардиологический диспансер": 'Кардиологический диспансер, Республиканская больница №1-Национальный центр медицины(г. Якутск, ул. Мерзлотная, 42)',
        "КГФ": 'Корпус гуманитарных факультетов(г. Якутск, Ленина проспект, 1)',
        "КИТ": 'Колледж инфраструктурных технологий СВФУ(КИТ)(Колледж инфраструктурных технологий СВФУ(КИТ))',
        "КЛИНИКА ПРОФЕССОРА": 'КЛИНИКА ПРОФЕССОРА (Радужная)(г. Якутск, Радужная (Сергеляхское шоссе 11 км), 69/12)',
        "Клиника СВФУ": 'Клиника СВФУ(г. Якутск, ул. Кулаковского, 36)',
        "КТФ": 'Корпус технических факультетов(г. Якутск, ул. Кулаковского 50)',
        "КФЕН": 'Корпус факультета естественных наук(г. Якутск, ул. Кулаковского 48)',
        "Лаб-рия СиПМ(Ленина 42)": 'Лаборатория скульптурного и пластичного моделирования"(г.Якутск, Пр-т Ленина 42)',
        "Лаборатория Автодорожная 10": 'Лаборатория "Технология и оборудование изготовления корпусной мебели(г.Якутск, ул. Автодорожная 10)',
        "Лаборатория Автодорожная 14/1": 'Лаборатория "Технология и оборудование изготовления столярно-строительных изделий"(г.Якутск, ул. Автодорожная 14/1)',
        "Лыжная база": 'Лыжная база СВФУ(г. Якутск, ул. Павлика Морозова, 2к2)',
        "МАДОУ №18": 'МАДОУ Детский сад №18 «Прометейчик» (г.Якутск, ул.Автодорожная 13/1 Г)',
        "МАЭ": 'Музей археологии и этнографии(г.Якутск, ул. Кулаковского 48)',
        "МДОУ 51": 'Детский сад №51 «Кэскил»(г. Якутск, ул. Ильменская, 23)',
        "МДОУ 70": 'Детский сад №70 «Кэрэчээнэ( г.Якутск, с.Хатассы, ул.Ленина, д.49, к.1)',
        "МДОУ №73": 'МБДОУ Д/с №73 "Светлячок"(г.Якутск, с.Тулагино, ул. Связистов 14)',
        "МДОУ ЦРР 21": 'Детский сад №21 «Кэнчээри»(г. Якутск, ул. Каландарашвили 34/1)',
        "МИ": 'Медицинский институт(г. Якутск, ул. Ойунского, 27)',
        "МОБУ СОШ №31": 'Школа № 31(г. Якутск, ул. Каландарашвили 34)',
        "НБ РС(Я)": 'Национальная библиотека РС(Я)(г. Якутск, пр. Ленина, 40)',
        "НИИ здоровья СВФУ": 'НИИ здоровья СВФУ(г. Якутск, Сергеляхское шоссе, 4 км, к. С-2)',
        "Общ.№6А": '66 квартал Общежитие блок "А"(г. Якутск, ул. Каландарашвили 17, блок А)',
        "Общ.№6Б": '66 квартал Общежитие блок "Б"(г. Якутск, ул. Каландарашвили 17, блок Б)',
        "Общ.№6В": '66 квартал Общежитие блок "В"(г. Якутск, ул. Каландарашвили 17, блок В)',
        "ПИ": 'Педагогический институт(г. Якутск, Ленина проспект, 2)',
        "Пожарная № 1": 'Пожарная часть № 1(г. Якутск, Дзержинского, 35)',
        "Пожарная № 3": 'Пожарная часть No 3(г.Якутск, Маганский тракт, 2 км, 8)',
        "ПЦ ЦОМиД": 'Республиканский центр охраны материнства и детства(г. Якутск, Сергеляхское шоссе,4)',
        "РБ №1-НЦМ": 'Республиканская больница №1, Национальный центр Медицины(г. Якутск, Сергеляхское шоссе,4)',
        "РБ №2-ЦЭМП": 'Республиканская больница №2, Центр экстренной медицинской помощи(г. Якутск, ул. П.Алексеева, 83 «А»)',
        "РБ №3 – МЗ РС (Я)": 'Республиканская больница № 3,Минздрава РС(Я)(г. Якутск, ул. Горького, 94)',
        "Роспотребнадзор": 'Управление Федеральной службы по надзору в сфере защиты прав потребителей и благополучия человека по Республике Саха (Якутия)(г. Якутск, ул. Ойунского, 9)',
        "РЦЭМП": 'Республиканский центр экстренной помощи(г. Якутск, ул. П.Алексеева, 83а)',
        "СЗ УЛК": 'Спортивный зал, УЛК(г. Якутск, ул. Белинского 58в)',
        "Симуляционный центр клиники СВФУ": 'Симуляционный центр клиники СВФУ(г. Якутск, ул. Кулаковского, 36)',
        "СК Модун": 'Спортивный комплекс "Модун"(г. Якутск, ул. Кирова 20/1)',
        "СОШ №31": 'Средняя образовательная школа № 31(г. Якутск, ул. Каландарашвили,31)',
        "СОШ №5": 'Средняя образовательная школа № 5 им. Н.О. Кривошапкина(г. Якутск, ул. Орджоникидзе, 8/2)',
        "СС РС(Я)": 'Служба спасения РС(Я) (Дзержинского, 12/1) (г.Якутск, Дзержинского, 12/1)',
        "Тир": 'Стрелковый тир(г. Якутск, ул.Красильникова)',
        "УЛ ГМ": 'Уч.лаб горных машин(г. Якутск, ул. Кулаковского, 42 к2)',
        "УЛК": 'Учебно-лабораторный корпус(г. Якутск, ул.Белинского 58)',
        "УПЦ Марха": 'Учебно-производственный центр подготовки персонала энергетики Марха(п. Марха, ул. Интернациональная 3)',
        "ФБУЗ": 'ФБУЗ «Центр гигиены и эпидемиологии в Республике Саха (Якутия)»(г. Якутск, ул. Петра-Алексеева, д. 60/2)',
        "Центр реабилитации инвалидов": 'Республиканский Реабилитационный Центр Инвалидов и Ветеранов(г. Якутск, ул.Рихарда Зорге, 2)',
        "Электронная система Moodle": 'Электронная система Moodle()',
        "ЭПЛ1": 'ЭПЛ-1()',
        "Юность": 'Стадион Юность (г. Якутск, ул. Павлика Морозова, 2 к1)',
        "ЯГБ №5": 'Якутская городская больница № 5(г. Якутск, ул. Кальвица, 3)',
        "ЯГКБ": 'Якутская городская клиническая больница(г. Якутск, ул. Стадухина, 81)',
        "ЯГСХА": 'Якутская государственная сельскохозяйственная академия(г. Якутск, ул. Красильникова, 15)',
        "ЯГСХАПокр": 'ЯГСХА, Покровский тракт 5 км(г.Якутск, Покровский тракт 5 км)',
        "ЯНЦ СО РАН": 'Якутский научный центр СО РАН(г. Якутск, ул. Петровского, 2)',
        "ЯПК": 'Якутский Педагогический Колледж(г. Якутск, ул. Ленина, 5)',
        "ЯРКВД": 'Якутский республиканский кожно-венерологический диспансер(г. Якутск, ул. Богдана Чижика, 3)',
        "ЯРОБ": 'Якутская республиканская офтальмологическая больница(г. Якутск, ул. Свердлова, 15)',
        "ЯРОД": 'Якутский республиканский онкологический диспансер(г. Якутск, ул. Свердлова 3/2)',
        "ЯРПНД": 'Якутский республиканский психоневрологический диспансер(г. Якутск, ул. Котенко, 14А)',
        "ЯТЭЦ": 'Якутская ТЭЦ ПАО "Якутскэнерго"(г. Якутск, ул. Федора Попова, 3)',
    }

    # return jsonify(corpuses)
    return corpuses


@app.route('/lecturers', methods=["GET", "POST"])
def get_lecturers():
    return lecturers


HOST_PORT = "8000"
if __name__ == '__main__':
    app.debug = True
    app.run(port=HOST_PORT)
