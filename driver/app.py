from flask import Flask, render_template, request
import requests


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lecturers')
def auth():
    return render_template('auth.html')


@app.route('/classrooms')
def login():
    return render_template()


@app.route('/classrooms')
def login():
    return render_template()


@app.route('/subjects')
def login():
    return render_template()


if __name__ == '__main__':
    app.debug = True
    app.run()