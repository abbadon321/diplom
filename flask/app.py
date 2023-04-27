from flask import Flask, render_template, request, redirect, url_for
import requests
from openpyxl import load_workbook

app = Flask(__name__)


@app.route('/')
@app.route('/auth')
def index():
    return render_template("index.html")


@app.route('/main', methods=['post', 'get'])
def login():
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
        name = res.text[right_index:left_index].replace(
            "<strong>", "").replace("</strong> <br>", "") + "!"
    print(username, password)
    return render_template('main.html', res=res, session=session, name=name, title=title)


@app.route("/schedule", methods=['POST'])
def schedule():
    file = request.files['file']
    file.save('static/' + file.filename)
    if file:
        data_dict = {}
        wb = load_workbook(filename='static/' + file.filename)
        sheets_names = wb.sheetnames
        sheet_data = {}
        for sh in sheets_names:
            values = []
            wb.active = sheets_names.index(sh)
            sheet = wb.active
            for cell in sheet[3]:
                if cell.value == "Наименование группы":
                    next_cell = sheet.cell(
                        row=cell.row + 1, column=cell.column)
                    values.append(next_cell.value)
            sheet_data[sh] = values
        data_dict.update(sheet_data)
        return render_template('schedule.html', data=data_dict)
    else:
        return redirect(url_for('main'))


def get_corpus():
    url = "http://localhost:80/corpus"
    response = requests.get(url)
    return response.text


HOST_PORT = "5000"
if __name__ == '__main__':
    app.debug = True
    app.run(port=HOST_PORT)
