from flask import Flask, render_template, request
import requests
from openpyxl import load_workbook
import pandas as pd


app = Flask(__name__)


@app.route('/')
@app.route('/auth')
def index():
    return render_template("index.html")


def get_corpus():
    url = "http://localhost:80/corpus"
    response = requests.get(url)
    return response.text


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


@app.route("/schedule")
def schedule():
    wb = load_workbook(filename="static/schedule.xlsx")
    # sheets = []
    sheets_names = wb.sheetnames
    # for sh in sheets_names:
    #     wb.active = sheets_names.index(sh)
    #     sheet = wb.active
    #     if sheet['B6'].value is not None:
    #         print(sheet['B6'].value)
    data = pd.read_excel(
        "static/schedule.xlsx", sheet_name=[sheets_names[1]], header=None)
    return render_template("schedule.html", data=data.keys())


HOST_PORT = "5000"
if __name__ == '__main__':
    app.debug = True
    app.run(port=HOST_PORT)
