from flask import Flask, render_template, request, redirect, url_for, session
import requests
import re
from openpyxl import load_workbook
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'mysecretkey'
# buid = None

# rm.kylatchanov@empl.s-vfu.ru
# 25041955


@app.route('/test')
def test():
    return render_template("test.html")


@app.route('/')
@app.route('/auth')
def index():
    return render_template('index.html')


@app.route('/main', methods=['post', 'get'])
def authorize():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

    url = 'https://www.s-vfu.ru/?login=yes'

    data = {
        'AUTH_FORM': 'Y',
        'TYPE': 'AUTH',
        'USER_LOGIN': username,
        'USER_PASSWORD': password,
        'Login': ''
    }

    cookies = {
        "entersite": "www.s-vfu.ru",
    }

    my_session = requests.Session()
    res = my_session.post(url, data=data, cookies=cookies, verify=False)
    res.raise_for_status()
    right_index = res.text.find("<h1>") + 4
    left_index = res.text.find("</h1>")
    if left_index != -1:
        title = "Главная"
        name = "Здравствуйте, " + \
            res.text[right_index:left_index] + "!"
    else:
        title = "Login failed"
        right_index = res.text.find("<strong>Ошибка!</strong>")
        left_index = res.text.find("авторизация,") + 11
        name = "Ошибка авторизации! Неверные логин и/или пароль"
        return redirect(url_for('index'))
    res = my_session.get("https://www.s-vfu.ru/user/rasp/new/")
    index = res.text.find("buid")
    buid = res.text[index + 13:index + 17]
    session['buid'] = buid
    # session.cookies.set('buid', buid)
    return render_template('main.html', buid=buid, res=res, session=session, name=name, title=title)
    # return redirect(url_for('schedule_parse'))


@app.route("/schedule", methods=['GET', 'POST'])
def schedule_parse():
    file = request.files['file']
    file.save('static/' + file.filename)
    form = request.form.get('form')
    fac = request.form.get('fac')
    schedule = {}

    if file and fac and form:
        # lecturers = requests.get(url="http://localhost:8000/lecturers").json()
        buid = session.get('buid', 'ошибка')
        wb = load_workbook(filename='static/' + file.filename)
        sheets_names = wb.sheetnames

        # цикл по листам excel-файла
        for sh in sheets_names:
            if sh.find("курс") == -1:
                continue
            wb.active = sheets_names.index(sh)
            ws = wb.active

            course = str(ws.cell(row=2, column=1).value).strip()[0]
            year_and_semestr = str(ws.cell(row=1, column=1).value)
            if course == "None" and year_and_semestr == "None":
                continue
           

            # цикл по всем группам
            for i in range(3, ws.max_column, 4):
                # получение названия группы
                group_name = str(ws.cell(row=4, column=i).value).strip()
                year, semestr = get_year_and_semestr(year_and_semestr)

                # получения кода для формы обучения
                code = get_code(group_name)
                # получение списка подходящих групп
                response = query(id=buid, action="loadgroup", fac=fac, code=code,
                                 course=course, form=form, semestr=semestr, year=year)
                # получение нужной группы из списка
                group = parse_loadgroup(response, group_name)
                # получение id группы
                group_id = group[group.find("|") + 1:]

                # получение РУПа
                # ПОЧЕМУ PLAN И FILENAME В КОНЕЧНОМ ИТОГЕ РАЗНЫЕ
                filename = query(id=buid, action="choicerup",
                                 fac=fac, course=course, form=form, semestr=semestr, year=year, groupname=group)

                if group_name != "**" and group_name != "*" and group_name != "None":
                    # цикл по занятиям одной группы
                    for j in range(6, 42):
                        lesson = {}
                        # получение дня недели
                        weekday = ws.cell(
                            row=j, column=1).value.strip().upper()

                        # проверка, что дисциплина есть (наличие пары)
                        if ws.cell(row=j, column=i).value is not None:
                            time = ws.cell(row=j, column=2).value.replace(
                                ".", ":").replace(" -- ", "-")
                            lesson_name = ws.cell(
                                row=j, column=i).value.strip()
                            
                            # if len(lesson_name.split("\n")) > 1:
                            
                            chet = get_parity(lesson_name)

                            lecturer_name = str(
                                ws.cell(row=j, column=i + 1).value).split('\n')
                            
                            # if len(lecturer_name) > 1:
                            #     for i in range(len(lecturer_name)):
                            #         lecturer = get_lecturers(lecturer_name)
                            
                            # добавление строки в таблицу
                            response = query(action="addrow", fac=fac, filename=filename, groupname=group, code=code, course=course, year=year)
                            
                            # получение данных проподователя с сервера
                            lecturer = parse_addrow(response, lecturer_name)
                            
                            activity = ws.cell(row=j, column=i + 2).value
                            activity = get_activity(activity)

                            classroom = (
                                str(ws.cell(row=j, column=i + 3).value).strip())
                            
                            corpus = extract_corpus(classroom) if (corpus := extract_corpus(corpus)) is not None else "КФЕН"
                            
                            lesson = {
                                "ИД группы": group_id,
                                "номер пары": j - 5,
                                "день недели": weekday,
                                "временной отрезок": time,
                                "название дисциплины": lesson_name,
                                "ФИО преподавателя": lecturer,
                                "вид деятельности": activity,
                                "номер аудитории": classroom,
                            }
                            schedule.setdefault(
                                group_name, []).append(lesson)
                            result = query(id_group=group_id, filename=filename, semestr=semestr, course=course, fac=fac, form=form[0], action="insertrow", lesson=lesson_name, lecturer=lecturer, weekday=weekday, time=time, chet=chet, activity=activity, corpus=corpus, classroom=classroom)
                            

        return render_template('schedule.html', buid=buid, data=schedule, res = result.text, asd=(year, semestr))

    else:
        error = "Ошибка при загрузке файла"
        return redirect(url_for('main'), error=error)


def get_year_and_semestr(string):
    string1 = re.findall(r"\b\d+\b(?=\s*полугодие)", string)
    if string1:
        semestr = string1[0]
    else:
        semestr = "Семестр не определен. Проверьте формат файла!"

    string2 = re.findall(r"полугодие\s+(\d+)\s*-\s*", string)
    if string2:
        year = string2[0][-4:]
    else:
        year = "Год не определен. Проверьте формат файла!"
    return (year, semestr)


def get_parity(lesson):
    if lesson.endswith("**"):
        return 2
    elif lesson.endswith("*"):
        return 1
    else:
        return 0


def get_code(group_name):
    string = group_name.strip()[0].upper()
    if string == "Б":
        return 3
    elif string == "М":
        return 4
    elif string == "А":
        return 6
    return 5


def get_activity(act):
    act = act.replace(" ", "").replace('\\', "\n").replace('/', "\n")
    if act == "лек":
        return "лекция"
    elif act == "пр":
        return "практика"
    elif act == "лек\nпр":
        return "лекция, практика"
    elif act == "лаб":
        return "Лабораторная работа"
    elif act == "СРС":
        return "самостоятельная работа"
    else: return ""

def extract_corpus(string):
    # Паттерн для поиска числа и слова
    pattern = r'\b(\d+)\b\s+([a-zA-Zа-яА-Я]{2,})\b'
    # Ищем совпадения в строке
    match = re.search(pattern, string)
    if match is not None:
        # Возвращаем слово из совпадения
        return match.group(2)
    else:
        return None
    

# # Add a new row
# def add_new_row(lesson):
#     pass


# # make schedule public
# def deploy_schedule():
#     pass


# # returns set of tuples
# def get_current_schedule():
#     pass


# def get_new_schdeule(excel_schedule):
#     current = get_current_schedule()
#     all_schedule = set(excel_schedule)
#     return list(current - all_schedule)


# def add_schedule(excel_schedule):
#     to_be_added = get_new_schdeule(excel_schedule)
#     for lesson in to_be_added:
#         add_new_row(lesson)
#     deploy_schedule()


def query(id=None, action=None, fac=None,
          code=None, course=None, form=None,
          semestr=None, year=None, filename=None,
          id_group=None, groupname=None, full=None,
          chet=None, weekday=None, activity=None,
          corpus=None, classroom=None, lesson=None,
          lecturer=None, time=None):
    last_index = str(groupname).rfind("|")
    # добавление строки
    if action == 'addrow':
        type = "POST"
        url = "ajax.php"
        id = 1
        # groupname: 02.03.02|7471|ИМИ-Б-ФИИТ-21|5998
        # ИМИ|02030201_22_2ФИИТ.plx|7471|ИМИ-Б-ФИИТ-21|3|2|2022|1|5998|03|5998|1
        data = {"id": id,
                "full": fac + "|" + filename + "|" + \
            groupname[:last_index] + "|" + str((course-1) * 2 + semestr) + "|" + course + \
            "|" + year + "|" + semestr + "|" + \
            groupname[last_index:len(groupname)] + "|" + groupname[3:5] + "|" + \
            groupname[last_index:len(groupname)] + "|" + form
        }

    # вставка строки
    if action == 'insertrow':        
        type = "POST"
        url = "ajax.php"
        data = {
            "data": fac + "|" + filename + "|" + \
            groupname[:last_index] + "|" + str((course-1) * 2 + semestr) + "|" + course + \
            "|" + year + "|" + semestr + "|" + \
            groupname[last_index:len(groupname)] + "|" + groupname[3:5] + "|" + \
            groupname[last_index:len(groupname)] + "|" + form,
            'courseequalsemestr': 0,
            'id_group': id_group,
            "filename": filename,
            "global_semestr": semestr,
            "semestr": (course-1) * 2 + semestr,
            "course": course,
            "fac": fac,
            "year": year,
            "form": groupname[3:5],
            "formshort": 1,
            'id': 1,
            'action': action,
            'I': lesson,
            # "Акинин Михаил Александрович|895035670"
            "J": lecturer,
            "hours": lecturer[lecturer.find("|") + 1:],
            'poggruppa': 0,
            "B": weekday,
            "F": time,
            "chet": chet,
            "c": "09.01.2023",
            "d": "30.06.2023",
            "H": activity,
            "L": corpus,
            "K": classroom
        }

    # удаление строки
    elif action == 'delete':
        type = "POST"
        url = "ajax.php"
        data = {
            'id': id,
            'action': action,
            'full': full,
            "fac": fac,
            "data": id
        }

    # удаление расписания
    elif action == 'remove':
        type = "POST"
        url = "ajax.php"
        data = {
            'id': id,
            'action': action,
            'full': full,
            "fac": fac
        }

    # публикация расписания
    elif action == 'public1':
        type = "POST"
        url = "ajax.php"
        data = {
            'id': id,
            'action': action,
            'full': full,
            "fac": fac
        }
    elif action == 'public2':
        type = "POST"
        url = "ajax.php"
        data = {
            'data': fac + "|" + filename + "|" + id_group + "|" + groupname[:last_index] + "|" + str((course-1) * 2 + semestr) + "|" + course + "|" + year + "|" + semestr + "|" + groupname[last_index:len(groupname)] + "|" + groupname[3:5] + "|" + groupname[last_index:len(groupname)] + "|" + form,
            'id_group': id_group,
            'filename': filename,
            'global_semestr': semestr,
            'semestr': (course-1) * 2 + semestr,
            'course': course,
            'fac': fac,
            'year': year,
            'form': groupname[3:5],
            'formshort': form[0],
            'action': action,
        }

    # сохранение расписания
    elif action == 'apply':
        type = "POST"
        url = "ajax.php"
        data = {
            'id': id,
            'action': action,
            'filename': filename,
            "course": course,
            "id_group": id_group,
            "semestr": semestr,
            "year": year,
            "fac": fac
        }

    # выбрать группу
    elif action == 'loadgroup':
        type = "POST"
        url = "ajax.php"
        data = {
            'id': id,
            'action': action,
            "fac": fac,
            "code": code,
            "course": course,
            "form": form,
            "semestr": semestr,
            "year": year
        }

    # выбрать руп
    elif action == 'choicerup':
        type = "POST"
        url = "ajax.php"
        data = {
            'id': id,
            'action': action,
            "fac": fac,
            "course": course,
            "form": form,
            "semestr": semestr,
            "year": year,
            "groupname": groupname,
        }

    response = requests.post(url="https://www.s-vfu.ru/user/rasp/new/ajax.php", data=data)
    return response.text


def parse_loadgroup(html, groupname):
    soup = BeautifulSoup(html, 'html.parser')
    select = soup.find('select')
    if select:
        options = select.find_all('option')
        for option in options:
            value = option.get('value')
            if value and groupname in value:
                return value
    return None


def parse_choicerup(html):
    soup = BeautifulSoup(html, 'html.parser')
    radiobuttons = soup.find_all('input', {'type': 'radio'})

    selected_value = None
    for radiobutton in radiobuttons:
        if radiobutton.has_attr('checked'):
            selected_value = radiobutton['value']
            break

    return selected_value


def parse_addrow(html, lecturer):
    soup = BeautifulSoup(html, 'html.parser')
    options = soup.find_all('option')

    surname, initials = lecturer.split()
    initials = initials.replace(".", "")

    for option in options:
        text = option.text
        if text.startswith(surname):
            string = text.split()
            lecturer_initials = string[1][0] + string[2][0]
            if initials == lecturer_initials:
                return text + "|" + option['value']

    else:
        # есть проблема совпадений по фамилии и инициалам а также полных тесок
        response = requests.get(
            url=f"https://www.s-vfu.ru/stud/searchadddata.php?tablename=svfudbnew.forexcel&term={surname} {initials[0]}")
        data = response.json()
        for d in data:
            string = d.split()
            if string[2].startswith(initials[1]):
                return d
            else: 
                "Преподаватель не найден!"
                


HOST_PORT = "5000"
if __name__ == '__main__':
    app.debug = True
    app.run(port=HOST_PORT)
