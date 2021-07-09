#!/home/std/TPIS/env python3

from flask import Flask, request
from flaskext.mysql import MySQL
from flask_jsonrpc import JSONRPC
from jsonrpcclient import request
from typing import Union
import asyncio

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/admin', enable_web_browsable_api=False)
application = app
wsgi_app = app.wsgi_app
mysql = MySQL()
# Параметры подключения к БД
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'zmp24DSSQL'
app.config['MYSQL_DATABASE_DB'] = 'ip_admins_db'
app.config['MYSQL_DATABASE_HOST'] = 'ip_admins_db'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

@jsonrpc.method('App.admin_get_couriers')
def admin_get_couriers(login: str, password: str) -> Union[list, None]:
    if login_admin(login, password) != '-1':
        return request("http://ip_couriers/couriers", "App.get_couriers").data.result 
    return None


@jsonrpc.method('App.admin_login')
def admin_login(login: str, password: str) -> Union[str, None]:
    return login_admin(login, password)


def login_admin(login: str, password: str) -> Union[str, None]:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select full_name from admins where login=%s and password=%s", [login, password])
    data = cursor.fetchall()
    # Если длина ответа больше 0 - запись найдена
    if len(data) > 0:
        return str(data[0][0])
    # Если вход не успешен - возвращаем -1
    else:
        return None


@jsonrpc.method('App.admin_reg')
def admin_login(login: str, password: str, full_name: str) -> Union[str, None]:
    if login_admin(login, password) != '-1':
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO admins (login, password, full_name) VALUES (%s, %s, %s);""", [login, password, full_name])
            conn.commit()
            return "1"
        except Exception as e:
            return str(e)
    # Если вход не успешен - возвращаем -1
    else:
        return None

@jsonrpc.method('App.admin_get_client')
def admin_get_client(login: str, password: str, client_email: str, client_phone: str) -> Union[dict, None]:
    if login_admin(login, password) != '-1':
        return request("http://ip_clients/client", "App.get_client", client_email=client_email, client_phone=client_phone).data.result
    else:
        return None


@jsonrpc.method('App.admin_reg_client')
def admin_reg_client(login: str, password: str, client_email: str, client_phone: str, client_full_name: str) -> Union[str, None]:
    if login_admin(login, password) != '-1':
        return request("http://ip_clients/client", "App.reg_client", email=client_email, password="", full_name=client_full_name, phone_num=client_phone).data.result
    else:
        return None


@jsonrpc.method('App.admin_get_orders')
def admin_get_orders(login: str, password: str) -> Union[list, None]:
    if login_admin(login, password) != '-1':
        orders = request("http://ip_orders/orders", "App.admin_get_orders").data.result
        couriers = request("http://ip_couriers/couriers", "App.get_couriers").data.result 
        for order in orders:
            if order["courier_id"] != None:
                for courier in couriers:
                    if order["courier_id"] == courier["id"]:
                        order["courier_name"] = courier["full_name"]
            else:
                order["courier_name"] = "Поиск курьера"
            if not "courier_name" in order.keys():
                order["courier_name"] = "Ошибка при поиске курьера"
        return orders
    else:
        return None


@jsonrpc.method('App.admin_post_order')
def post_order_admin(login: str, password: str, client_email: str, client_phone: str, 
                    sender_adr: str, sender_comment: str, sender_name: str, sender_coord_1: str, sender_coord_2: str, sender_phone: str,
                    receiver_adr: str, receiver_comment: str, receiver_name: str, receiver_coord_1: str, receiver_coord_2: str, receiver_phone: str,
                    cost: str) -> Union[str, None]:
    if login_admin(login, password) != '-1':
        client = request("http://ip_clients/client", "App.get_client", client_email=client_email, client_phone=client_phone).data.result
        if not client is None:
            client_id = client["personal_info"][0]["id"]
            resp = request("http://ip_orders/orders", "App.post_order", 
                    client_id = client_id, sender_adr = sender_adr, sender_comment = sender_comment, 
                    sender_name = sender_name, sender_coord_1 = sender_coord_1, sender_coord_2 = sender_coord_2, sender_phone = sender_phone,
                    receiver_adr = receiver_adr, receiver_comment = receiver_comment, 
                    receiver_name = receiver_name, receiver_coord_1 = receiver_coord_1, receiver_coord_2 = receiver_coord_2, receiver_phone = receiver_phone,
                    cost = cost).data.result
            # file_log = open("log.txt", "w")
            # file_log.write(resp)
            # file_log.close()
            return resp
        else:
            return None
    return None


# Точка входа
if __name__ == '__main__':
    app.run(host="localhost", port=5101, debug=False) # port 5101
