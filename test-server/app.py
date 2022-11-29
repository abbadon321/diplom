from flask import Flask, render_template, request, jsonify
import requests


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/index')
def index():
    return 'Hello!'



@app.route('/corpus', methods=["GET","POST"])
def corpus():
    corpuses = {
        "corpuses": [
            {
                "KFEN":'КФЕН',
                "GUK":'ГУК',
                "ULK":'УЛК'
            }
        ]
    }

    return jsonify(corpuses)
    return corpuses


HOST_PORT="80"
if __name__ == '__main__':
    app.debug = True
    app.run(port=HOST_PORT)