from flask import Flask, render_template, request
import requests


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/main', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    
    url = 'https://www.s-vfu.ru/?login=yes'

    data = {
        'AUTH_FORM': 'Y',
        'TYPE': 'AUTH',
        'USER_LOGIN': "sp.sobyanin",
        'USER_PASSWORD': "Liverpool123",
        'Login': ''
    }

    session = requests.Session()
    res = session.post(url, data=data)
    res.raise_for_status()
    right_index = res.text.find("<h1>") + 4
    left_index = res.text.find("</h1>")
    if left_index != -1:
        title = "Login success"
        name = "Здравствуйте, " + res.text[right_index:left_index] + "!"
    else:
        title = "Login failed"
        right_index = res.text.find("<strong>Ошибка!</strong>")
        left_index = res.text.find("авторизация,") + 11
        name = res.text[right_index:left_index].replace("<strong>", "").replace("</strong> <br>", "") + "!"

    return render_template('main.html', res=res, session=session, name=name, title=title)

if __name__ == '__main__':
    app.debug = True
    app.run()