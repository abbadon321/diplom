from flask import Flask, render_template, request
import requests


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lecturers')
def lect():
    return render_template('auth.html')


@app.route('/corpus')
def corp():
    return render_template('corpus.html')


if __name__ == '__main__':
    app.debug = True
    app.run()