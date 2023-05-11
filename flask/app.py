from flask import Flask, render_template, request, redirect, url_for
import requests
import re
from openpyxl import load_workbook

app = Flask(__name__)


@app.route('/step_one')
def step_one():
    return render_template("step_one.html")


@app.route('/test')
def test():
    return render_template("test.html")


@app.route('/step_two')
def step_two():
    return render_template("step_two.html")


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

    session = requests.Session()
    res = session.post(url, data=data, verify=False)
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
    return render_template('main.html', res=res, session=session, name=name, title=title)


@app.route("/schedule", methods=['POST'])
def schedule_parse():
    file = request.files['file']
    file.save('static/' + file.filename)
    fac = "ИМИ"
    schedule = {}

    if file:
        wb = load_workbook(filename='static/' + file.filename)
        sheets_names = wb.sheetnames

        # цикл по листам excel-файла
        for sh in sheets_names:
            wb.active = sheets_names.index(sh)
            ws = wb.active

            course = str(ws.cell(row=2, column=1).value)
            year_and_semestr = str(ws.cell(row=1, column=1).value)
            if course == "None" and year_and_semestr == "None":
                continue

            for row in ws.iter_rows():
                if row[0].value == "Суббота":
                    max_row = row[0].row

            # цикл по всем группам
            for i in range(3, ws.max_column, 4):
                group_name = (ws.cell(row=4, column=i).value, ws.title)

                if group_name[0] != "**" and group_name[0] != "*":
                    # цикл по занятиям одной группы
                    for j in range(6, 42):
                        lesson = {}
                        if ws.cell(row=j, column=1).value is not None:
                            weekday = ws.cell(row=j, column=1).value

                        # проверка, что дисциплина есть (наличие пары)
                        if ws.cell(row=j, column=i).value is not None:
                            course_id, code = get_course_and_code(course)
                            year, semestr = get_year_and_semestr(
                                year_and_semestr, group_name[0])
                            group = query(action="loadgroup", groupname=group_name[0])
                            lesson = {
                                "номер пары": j - 5,
                                "день недели": (weekday, ""),
                                "временной отрезок": (ws.cell(row=j, column=2).value, ""),
                                "название дисциплины": (ws.cell(row=j, column=i).value, ""),
                                "ФИО преподавателя": (ws.cell(row=j, column=i + 1).value, ""),
                                "вид деятельности": (ws.cell(row=j, column=i + 2).value, ""),
                                "номер аудитории": (ws.cell(row=j, column=i + 3).value, ""),
                                # "код курса и уровня обучения": (course_id, code),
                                # "год, семестр": (year, semestr),
                                "данные группы": group
                            }
                            schedule.setdefault(
                                group_name[0], []).append(lesson)
                            

            # course_id, code = get_course_and_code(course)
            # year, semestr = get_year_and_semestr(year_and_semestr, group_name[0])
        # query(2902, "loadgroup", fac, )
        return render_template('schedule.html', data=schedule, zxc=(course_id, code), asd=(year, semestr))

    else:
        error = "Ошибка при загрузке файла"
        return redirect(url_for('main'), error=error)


def get_year_and_semestr(string, group_name):
    string1 = re.findall(r"\b\d+\b(?=\s*полугодие)", string)
    if string1:
        semestr = string1[0]
    else:
        semestr = "Семестр не определен. Проверьте формат файла!"

    string2 = re.findall(r"полугодие\s+(\d+)\s*-\s*", string)
    if string2:
        year = string2[0][-4:]
        # group_year = int(group_name[-2:])
        # year = current_year - group_year
    else:
        year = "Год не определен. Проверьте формат файла!"
    return (year, semestr)


def get_course_and_code(course):
    course_id = 0
    code = 0
    string = course.replace(" ", "").upper()
    if string == "1КУРС":
        course_id = 1
        code = 3
    elif string == "2КУРС":
        course_id = 2
        code = 3
    elif string == "3КУРС":
        course_id = 3
        code = 3
    elif string == "4КУРС":
        course_id = 4
        code = 3
    elif string == "1КУРСМАГИСТРАТУРЫ":
        course_id = 1
        code = 4
    elif string == "2КУРСМАГИСТРАТУРЫ":
        course_id = 2
        code = 4
    return (course_id, code)


def get_corpus():
    url = "http://localhost:80/corpus"
    response = requests.get(url)
    return response.text


def query(id=None, action=None, fac=None,  code=None, course=None, form=None,
          semestr=None, year=None, filename=None, id_group=None, groupname=None, full=None):
    # добавление строки
    if action == 'addrow':
        type = "POST"
        url = "ajax.php"
        data = {
            'id': id,
            'action': action,
            'full': full,
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
    elif action == 'public':
        type = "POST"
        url = "ajax.php"
        data = {
            'id': id,
            'action': action,
            'full': full,
            "fac": fac
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
        # type = "POST"
        # url = "ajax.php"
        # data = {
        #     'id': id,
        #     'action': action,
        #     "fac": fac,
        #     "code": code,
        #     "course": course,
        #     "form": form,
        #     "semestr": semestr,
        #     "year": year
        # }
        data = {
            "groupname": groupname
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

    response = requests.post(url="http://localhost:8000/loadgroup", data=data)
    return response


# Add a new row
def add_new_row(lesson):
    pass


# make schedule public
def deploy_schedule():
    pass


# returns set of tuples
def get_current_schedule():
    pass


def get_new_schdeule(excel_schedule):
    current = get_current_schedule()
    all_schedule = set(excel_schedule)
    return list(current - all_schedule)


def add_schedule(excel_schedule):
    to_be_added = get_new_schdeule(excel_schedule)
    for lesson in to_be_added:
        add_new_row(lesson)
    deploy_schedule()


HOST_PORT = "5000"
if __name__ == '__main__':
    app.debug = True
    app.run(port=HOST_PORT)
