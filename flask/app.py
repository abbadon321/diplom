from flask import Flask, render_template, request, redirect, url_for, session
import requests
import re
from openpyxl import load_workbook
from bs4 import BeautifulSoup

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


app = Flask(__name__)
app.secret_key = 'mysecretkey'

my_session = requests.Session()

system_url = "https://www.s-vfu.ru/user/rasp/new/"
server_url = "https://www.s-vfu.ru/user/rasp/new/ajax.php"


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

    res = my_session.post(url, data=data, cookies=cookies, verify=False)
    res.raise_for_status()
    cookies = res.cookies
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

    res = my_session.get(system_url)
    index = res.text.find("buid")
    buid = res.text[index + 13:index + 17]
    session['buid'] = buid
    # session.cookies.set('buid', buid)
    return render_template('main.html', buid=buid, res=res, session=session, name=name, title=title)
    # return redirect(url_for('schedule_parse'))


@app.route("/schedule", methods=['GET', 'POST'])
def schedule_parse():
    path = 'C:/Users/Серега/Documents/GitHub/diplom/flask/static/'
    file = request.files['file']
    file.save(path + file.filename)
    form = request.form.get('form')
    fac = request.form.get('fac')
    schedule = {}

    if file and fac and form:
        # lecturers = requests.get(url="http://localhost:8000/lecturers").json()
        buid = session.get('buid', 'ошибка')
        wb = load_workbook(filename=path + file.filename)
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
                if group_name != "**" and group_name != "*" and group_name != "None":
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
                    response = query(id=buid, action="choicerup",
                                     fac=fac, course=course, form=form, semestr=semestr, year=year, groupname=group)

                    filename = parse_choicerup(response)

                    result = query(action="show", semestr=semestr, course=course, fac=fac,
                                   year=year, form=form, code=code, id_group=group_id, filename=filename)

                    # цикл по занятиям одной группы
                    for j in range(6, 42):
                        lesson = {}
                        # получение дня недели
                        if (j - 6) % 6 == 0:
                            weekday = str(
                                ws.cell(row=j, column=1).value).strip().upper()

                        # проверка, что дисциплина есть (наличие пары)
                        if ws.cell(row=j, column=i).value is not None:
                            time = ws.cell(row=j, column=2).value.replace(
                                ".", ":").replace(" -- ", "-")
                            lesson_name = ws.cell(
                                row=j, column=i).value.strip()

                            # if len(lesson_name.split("\n")) > 1:

                            lesson_name, chet = get_parity(lesson_name)

                            lecturer_name = str(
                                ws.cell(row=j, column=i + 1).value)

                            # if len(lecturer_name) > 1:
                            #     for i in range(len(lecturer_name)):
                            #         lecturer = get_lecturers(lecturer_name)

                            # добавление строки в таблицу

                            response = query(action="addrow", fac=fac, filename=filename,
                                             groupname=group, code=code, course=course, year=year, semestr=semestr, form=form[0])

                            # получение данных проподователя с сервера
                            lecturer = parse_addrow(response, lecturer_name)

                            activity = ws.cell(row=j, column=i + 2).value
                            activity = get_activity(activity)

                            classroom = (
                                str(ws.cell(row=j, column=i + 3).value).strip())

                            corpus = extract_corpus(classroom)

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
                            # print(group_id, filename, semestr, course,
                            #       fac, form[0], lesson_name,
                            #       lecturer, weekday, time, chet,
                            #       activity, corpus, classroom, year, sep="\n")

                            query(action="choicecorpus",
                                  id=99999, corpus=corpus, fac=0)

                            result = query(code=code, id_group=group_id, filename=filename, semestr=semestr, course=course,
                                           fac=fac, form=form[0], action="insertrow", lesson=lesson_name,
                                           lecturer=lecturer, weekday=weekday, time=time, chet=chet,
                                           activity=activity, corpus=corpus, classroom=classroom, year=year, groupname=group)

                            # print(result)

        return render_template('schedule.html', buid=buid, data=schedule, res=result)

    else:
        error = "Ошибка при загрузке файла"
        return redirect(url_for('main'))


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
        return ((lesson[:len(lesson) - 2]).strip(), "2")
    elif lesson.endswith("*"):
        return ((lesson[:len(lesson) - 1]).strip(), "1")
    else:
        return (lesson, "0")


def get_code(group_name):
    string = group_name.strip()[0].upper()
    if string == "Б":
        return "3"
    elif string == "М":
        return "4"
    elif string == "А":
        return "6"
    return "5"


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
    else:
        return ""


def extract_corpus(string):
    # Паттерн для поиска числа и слова
    pattern = r'\b(\d+)\b\s+([a-zA-Zа-яА-Я]{2,})\b'
    # Ищем совпадения в строке
    match = re.search(pattern, string)
    if match is not None:
        # Возвращаем слово из совпадения
        return match.group(2)
    else:
        return "КФЕН"


def query(id=None, action=None, fac=None,
          code=None, course=None, form=None,
          semestr=None, year=None, filename=None,
          id_group=None, groupname=None, full=None,
          chet=None, weekday=None, activity=None,
          corpus=None, classroom=None, lesson=None,
          lecturer=None, time=None, startdate="", enddate=""):

    url = "https://www.s-vfu.ru/user/rasp/new/ajax.php"

    # добавление строки
    if action == 'addrow':

        last_index = str(groupname).rfind("|") + 1
        full_semestr = str((int(course) - 1) * 2 + int(semestr))
        full = fac + "|" + filename + "|" + \
            groupname[:last_index] + full_semestr + "|" + course + \
            "|" + year + "|" + semestr + "|" + \
            groupname[last_index:len(groupname)] + "|0" + code + "|" + \
            groupname[last_index:len(groupname)] + "|" + form
        id = 1
        data = {
            "action": action,
            "id": id,
            "full": full
        }

    elif action == "choicecorpus":
        data = {
            "id": id,
            "action": action,
            "corpus": corpus,
            "fac": fac
        }

    # вставка строки
    if action == 'insertrow':

        url = "https://www.s-vfu.ru/user/rasp/new/"

        last_index = str(groupname).rfind("|") + 1 + 1
        full_semestr = str((int(course) - 1) * 2 + int(semestr))
        full = fac + "|" + filename + "|" + \
            groupname[:last_index] + full_semestr + "|" + course + \
            "|" + year + "|" + semestr + "|" + \
            groupname[last_index:len(groupname)] + "|0" + code + "|" + \
            groupname[last_index:len(groupname)] + "|" + form

        data = {
            "data": full,
            'id_group': id_group,
            "filename": filename,
            "global_semestr": semestr,
            "semestr": full_semestr,
            "course": course,
            "fac": fac,
            "year": year,
            "form": "0" + code,
            "formshort": form,
            'id': 1,
            'action': action,
            'I': lesson,
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

    # удаление расписания
    elif action == 'remove':

        last_index = str(groupname).rfind("|") + 1
        full_semestr = str((int(course) - 1) * 2 + int(semestr))
        full = fac + "|" + filename + "|" + \
            groupname[:last_index] + full_semestr + "|" + course + \
            "|" + year + "|" + semestr + "|" + \
            groupname[last_index:len(groupname)] + "|0" + code + "|" + \
            groupname[last_index:len(groupname)] + "|" + form

        data = {
            'id': id,
            'action': action,
            'full': full,
            "fac": fac
        }

    # публикация расписания
    elif action == 'public1':

        last_index = str(groupname).rfind("|") + 1
        full_semestr = str((int(course) - 1) * 2 + int(semestr))
        full = fac + "|" + filename + "|" + \
            groupname[:last_index] + full_semestr + "|" + course + \
            "|" + year + "|" + semestr + "|" + \
            groupname[last_index:len(groupname)] + "|0" + code + "|" + \
            groupname[last_index:len(groupname)] + "|" + form

        data = {
            'id': id,
            'action': action,
            'full': full,
            "fac": fac
        }
    elif action == 'public2':

        data = {
            'data': fac + "|" + filename + "|" + id_group + "|" + groupname[:last_index] + str(full_semestr) + "|" + course + "|" + year + "|" + semestr + "|" + groupname[last_index:len(groupname)] + "|" + groupname[3:5] + "|" + groupname[last_index:len(groupname)] + "|" + form,
            'id_group': id_group,
            'filename': filename,
            'global_semestr': semestr,
            'semestr': full_semestr,
            'course': course,
            'fac': fac,
            'year': year,
            'form': groupname[3:5],
            'formshort': form[0],
            'action': action,
        }

    # сохранение расписания
    elif action == 'apply':

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

    # выбор группы и РУПа
    elif action == 'show':
        full_semestr = str((int(course) - 1) * 2 + int(semestr))
        url = "https://www.s-vfu.ru/user/rasp/new/"
        data = {
            "global_semestr": semestr,
            "semestr": full_semestr,
            "course": course,
            "fac": fac,
            "year": year,
            "formshort": form[0],
            "formname": form[2:],
            "action": action,
            "allplany": "on",
            "code": "0" + code,
            "id_group": id_group,
            "plan": filename,
            "startdate": startdate,
            "enddate": enddate
        }
    print(url)
    print()
    print(data)
    print()
    print()

    response = my_session.post(
        url=url, data=data)
    print(response.text)
    print("\n============================================================================================================================\n\n")
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
    plan_element = soup.find('input', {'name': 'plan'})
    if plan_element:
        plan_value = plan_element.get('value')
        return plan_value
    else:
        return "РУП не найден!"


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
