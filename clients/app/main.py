#!/home/std/TPIS/env python3

from flask import Flask, jsonify, request, render_template # Использование веб-фреймворка
from flaskext.mysql import MySQL # Использование MySQL коннектора
from flask_jsonrpc import JSONRPC
from jsonrpcclient import request
from typing import Union


app = Flask(__name__)
jsonrpc = JSONRPC(app, '/client', enable_web_browsable_api=False)
application = app
wsgi_app = app.wsgi_app
mysql = MySQL()
# Параметры подключения к БД
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'zmp24DSSQL'
app.config['MYSQL_DATABASE_DB'] = 'ip_clients_db'
app.config['MYSQL_DATABASE_HOST'] = 'ip_clients_db' # 192.168.20.251:22913
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)


@jsonrpc.method('App.get_client')
def get_client(client_email: str, client_phone: str) -> Union[dict, None]:
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("select full_name, email, phone_num, id from clients where email=%s or phone_num=%s",
                   [client_email, client_phone])
    data = cursor.fetchall()
    data_dict = {}
    if len(data) > 0:
        try:
            orders = request("http://host.docker.internal:5003/orders", "App.get_client_orders",id_client=data[0][3]).data.result
        except Exception as e:
            # Возвращаем пустой массив?
            orders = []
        data_dict = { 
            "personal_info":
                [{
                    "full_name": data[0][0],
                    "email": data[0][1],
                    "phone_num": data[0][2],
                    "id": data[0][3]
                }],
            "orders": orders
            }
        return data_dict
    else:
        return None


@jsonrpc.method('App.reg_client')
def client_reg(email: str, password: str, full_name: str, phone_num: str) -> Union[str, None]:
    conn = mysql.connect()
    cursor = conn.cursor()
    # Ищем пользователя
    cursor.execute(
        "select email from clients where phone_num = %s or email = %s",
        [phone_num, email])
    data = cursor.fetchall()
    # Если таких email и username нет
    if len(data) == 0:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (`full_name`, `email`, `phone_num`, `password`) "
            "values (%s, %s, %s, %s)",
            [full_name, email, phone_num, password])
        conn.commit()
        return "1"
    # Если пользователь с таким email или username существует
    else:
        return None

if __name__ == '__main__':
    app.run()