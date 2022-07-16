import flask
from flask import Flask, render_template
from flask_restful import Api
from psycopg2 import Error
import psycopg2
import os


app = Flask(__name__, template_folder="templates")
api = Api()
app.config.update(DEBUG=True, SERVER_NAME='127.0.0.1:5430')
app.config['JSON_AS_ASCII'] = False


def conn_db():
    connect = psycopg2.connect(
        database="postgres",
        host="127.0.0.1",
        port="5432",
        user="postgres",
        password="admin"
    )
    return connect


def create_table():
    connect = conn_db()
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE test_1
                    (
                        number INT PRIMARY KEY,
                        order_number INT NOT NULL,
                        price_usd INT NOT NULL,
                        delivery_date VARCHAR(10) NOT NULL,
                        price_rub VARCHAR(20) NOT NULL);''')
    connect.commit()
    cursor.close()
    connect.close()
    return "<h1><center>Table created.</center></p>", 200


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html'), 200


@app.route('/conn_and_create/', methods=['GET'])
def conn_and_create():
    connect = psycopg2.connect(
        database="postgres",
        host="127.0.0.1",
        port="5432",
        user="postgres",
        password="admin"
    )
    cursor = connect.cursor()
    try:
        cursor.execute('''CREATE TABLE test_1 (number TEXT NOT NULL,
                                                order_number TEXT NOT NULL,
                                                price_usd TEXT NOT NULL,
                                                delivery_date TEXT NOT NULL,
                                                price_rub TEXT NOT NULL);''')
        connect.commit()
        cursor.close()
        connect.close()
        return flask.redirect('http://127.0.0.1:5430/'), 200

    except (Exception, Error):
        return render_template('index.html'), 200


@app.route('/update_the_data/', methods=['GET'])
def update_the_data():
    os.system('python service.py')
    return flask.redirect('http://127.0.0.1:5430/'), 200


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, port=5430, host="127.0.0.1")
    os.system('python telegram_mess.py')
