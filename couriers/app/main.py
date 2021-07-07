#!/home/std/TPIS/env python3

from flask import Flask, jsonify, request, render_template # Использование веб-фреймворка
from flaskext.mysql import MySQL # Использование MySQL коннектора
from flask_jsonrpc import JSONRPC
from typing import Union

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/couriers', enable_web_browsable_api=False)
application = app
wsgi_app = app.wsgi_app
mysql = MySQL()
# Параметры подключения к БД
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'zmp24DSSQL'
app.config['MYSQL_DATABASE_DB'] = 'ip_couriers_db'
app.config['MYSQL_DATABASE_HOST'] = 'ip_couriers_db' # 192.168.20.251:22913
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)


@jsonrpc.method('App.login_courier')
def login_courier(password: str, phone: str) -> Union[dict, None]:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select full_name, email, phone_num, id from couriers where phone_num=%s and password=%s",
                   [phone, password])
    data = cursor.fetchall()
    print(data)
    # Если длина ответа больше 0 - запись найдена
    if len(data) > 0:
        data_dict = {
            'full_name': data[0][0],
            'email': data[0][1],
            'phone_num': data[0][2],
            'id': data[0][3],
            'status': 1
        }
        return data_dict
    else:
        return None


@jsonrpc.method('App.get_courier_by_id')
def get_courier_by_id(courier_id: int) ->Union[dict, None]:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select location_1, location_2 from couriers_locations where id_courier=%s order by time desc "
                   "limit 1", [courier_id])
    data = cursor.fetchall()
    if len(data) > 0:
        data_dict = {"location_1": data[0][0], "location_2": data[0][1]}
        return data_dict
    return None


@jsonrpc.method('App.get_courier_coords')
def get_courier_coords(courier_id: int) -> Union[dict, None]:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select id, phone_num, email, full_name from couriers where id=%s", [courier_id])
    data = cursor.fetchall()
    if len(data) > 0:
        data_dict = {"id": data[0][0],
                     "phone_num": data[0][1],
                     "email": data[0][2],
                     "full_name": data[0][3]}
        return data_dict
    return None

@jsonrpc.method('App.send_location')
def get_courier_coords(courier_id: int, geo_coord_1: float, geo_coord_2: float) -> str:
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO couriers_locations (id_courier, time, location_1, location_2) 
            VALUES (%s, DEFAULT, %s, %s)""", [courier_id, geo_coord_1, geo_code_2])
        conn.commit()
        return "1"
    except:
        return "-3"


@jsonrpc.method('App.get_couriers')
def get_couriers() -> list:
    conn = mysql.connect()
    cursor = conn.cursor()
    data_dict = []
    cursor.execute("""select id, full_name, email, phone_num, updated_in, location_1, location_2 from
                            (select id, full_name, email, phone_num, max(time) as updated_in
                        from couriers left join couriers_locations
                        on couriers.id = couriers_locations.id_courier
                        group by id, full_name, phone_num, email) as groupped left join couriers_locations
                        on updated_in = couriers_locations.time and groupped.id = couriers_locations.id_courier""")
    data = cursor.fetchall()
    for row in data:
        data_dict.append({
            "id": row[0],
            "full_name": row[1],
            "email": row[2],
            "phone_num": row[3],
            'updated_in': row[4],
            'location_1': row[5],
            'location_2': row[6],
        })
    return data_dict 

# Точка входа
if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=False) #5004


