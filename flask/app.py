from flask import Flask, render_template, request, redirect, url_for
import requests
from openpyxl import load_workbook

app = Flask(__name__)


@app.route('/step_one')
def step_one():
    return render_template("step_one.html")


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
    schedule = {}

    if file:
        wb = load_workbook(filename='static/' + file.filename)
        sheets_names = wb.sheetnames

        # цикл по листам excel-файла
        for sh in sheets_names:
            wb.active = sheets_names.index(sh)
            ws = wb.active
            group_name = ""
            lesson = {}

            for row in ws.iter_rows():
                if row[0].value == "Суббота":
                    max_row = row[0].row

            # цикл по всем группам
            for i in range(3, ws.max_column, 4):
                group_name = ws.cell(row=4, column=i).value
                if group_name != "**" and group_name != "*":
                    # цикл по занятиям 1-ой группы
                    for j in range(6, max_row + 1, 6):
                        for k in range(j, j + 6):
                            if ws.cell(row=k, column=3).value is not None:
                                lesson = {
                                    "номер пары": k - 5,
                                    "день недели": (ws.cell(row=j, column=1).value, ""),
                                    "временной отрезок": (ws.cell(row=k, column=2).value, ""),
                                    "название дисциплины": (ws.cell(row=k, column=3).value, ""),
                                    "ФИО преподавателя": (ws.cell(row=k, column=4).value, ""),
                                    "вид деятельности": (ws.cell(row=k, column=5).value, ""),
                                    "номер аудитории": (ws.cell(row=k, column=6).value, ""),
                                }
                                schedule.setdefault(
                                    group_name, []).append(lesson)

        return render_template('schedule.html', data=schedule)

    else:
        error = "Ошибка при загрузке файла"
        return redirect(url_for('main'), error=error)


def get_corpus():
    url = "http://localhost:80/corpus"
    response = requests.get(url)
    return response.text


HOST_PORT = "5000"
if __name__ == '__main__':
    app.debug = True
    app.run(port=HOST_PORT)
