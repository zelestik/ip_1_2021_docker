from flask import Flask, jsonify, request, render_template
from flaskext.mysql import MySQL
from flask_jsonrpc import JSONRPC
import cryptography
from typing import Union


app = Flask(__name__)
jsonrpc = JSONRPC(app, '/orders', enable_web_browsable_api=False)
application = app
wsgi_app = app.wsgi_app
mysql = MySQL()
# Параметры подключения к БД
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'zmp24DSSQL'
app.config['MYSQL_DATABASE_DB'] = 'ip_orders_db'
app.config['MYSQL_DATABASE_HOST'] = 'ip_orders_db'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)


@jsonrpc.method('App.get_courier_free_orders')
def get_courier_free_orders() -> list:
    data_dict = []
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select order_num_from, adr_from, geo_code_1_from, geo_code_2_from from order_details where courier_id is null")
    data = cursor.fetchall()
    for row in data:
        data_dict.append({
            'order_num': row[0],
            'adr': row[1],
            'geo_code_1': row[2],
            'geo_code_2': row[3]
        })
    return data_dict


@jsonrpc.method('App.take_order')
def take_order(order_num: int, courier_id: int) -> str:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from orders where order_num=%s and courier_id is null", [order_num])
    data = cursor.fetchall()
    if len(data) > 0:
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""UPDATE orders SET courier_id = %s WHERE order_num = %s;""", [courier_id, order_num])
            cursor.execute("""INSERT INTO order_statuses (order_status, status_date, status_reason, order_num)
                                    VALUES ('Курьер найден', DEFAULT, null, %s);""", [order_num])
            conn.commit()
            return "1"
        except:
            return "-3"
    else:
        return "-2"
@jsonrpc.method('App.take_parcel')
def take_parcel(order_num: int, courier_id: int) -> str:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from orders where order_num=%s and courier_id = %s", [order_num, courier_id])
    data = cursor.fetchall()
    data_dict = []
    if len(data) > 0:
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO order_statuses (order_status, status_date, status_reason, order_num)
                                    VALUES ('Посылка принята курьером', DEFAULT, null, %s);""", [int(order_num)])
            conn.commit()
            return "1"
        except:
            return "-3"
    else:
        return "-2"
    

@jsonrpc.method('App.close_order')
def close_order(order_num: int, courier_id: int) -> str:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from orders where order_num=%s and courier_id = %s", [order_num, courier_id])
    data = cursor.fetchall()
    if len(data) > 0:
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO order_statuses (order_status, status_date, status_reason, order_num)
                                    VALUES ('Заказ выполнен', DEFAULT, null, %s);""", [order_num])
            conn.commit()
            return "1"
        except:
            return "-3"
    else:
        return "-2"

@jsonrpc.method('App.get_order_details')
def get_order_details(order_num: int) -> list:
        data_dict = []
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select order_num_from, adr_from, geo_code_1_from, geo_code_2_from, adr_to, geo_code_1_to, geo_code_2_to, full_name_from, full_name_to from order_details where order_num_from=%s", [int(order_num)])
        data = cursor.fetchall()
        for row in data:
            data_dict.append({
                'order_num': row[0],
                'adr_from': row[1],
                'geo_code_1_from': row[2],
                'geo_code_2_from': row[3],
                'adr_to': row[4],
                'geo_code_1_to': row[5],
                'geo_code_2_to': row[6],
                'full_name_from': row[7],
                'full_name_to': row[8]
            })
        return data_dict


@jsonrpc.method('App.admin_get_orders')
def get_orders_admin() -> list:
    data_dict = []
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select order_num_from as order_num, order_date, full_name_from, adr_from,
       courier_id, order_status, status_date, cost, client_id from order_details
           left join (select num, order_status, status_date
                                from (
                                    select order_statuses.order_num as num, max(status_date) latestDate
                                    from order_statuses
                                    inner join orders on order_statuses.order_num = orders.order_num
                                    group by order_statuses.order_num
                                    ) a
                                inner join order_statuses on order_statuses.order_num = a.num
                                where order_statuses.status_date = a.latestDate) as status on num = order_num_from;""")
    data = cursor.fetchall()
    for row in data:
        data_dict.append({
            'order_num': row[0],
            'order_date': row[1],
            'receiver': row[2],
            'address': row[3],
            'courier_id': row[4],
            'last_status': row[5],
            'status_date': row[6],
            'cost': str(row[7]),
            'client_id': row[8]
        })
    return data_dict

@jsonrpc.method('App.get_client_orders')
def get_orders_admin(id_client: int) -> list:
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select order_num_from, adr_from, geo_code_1_from, geo_code_2_from,
    adr_to, geo_code_1_to, geo_code_2_to, full_name_from, full_name_to, phone_from, phone_to, cost,
    ifnull(courier_id, 0) as courier_id, order_date, client_id, order_status, status_date from order_details
           left join (select num, order_status, status_date
                                from (
                                    select order_statuses.order_num as num, max(status_date) latestDate
                                    from order_statuses
                                    inner join orders on order_statuses.order_num = orders.order_num
                                    group by order_statuses.order_num
                                    ) a
                                inner join order_statuses on order_statuses.order_num = a.num
                                where order_statuses.status_date = a.latestDate) as status on num = order_num_from where client_id=%s""", [id_client])
    orders_data = cursor.fetchall()
    orders = []
    for row in orders_data:
        orders.append({
            'order_num': row[0],
            'adr_from': row[1],
            'geo_code_1_from': row[2],
            'geo_code_2_from': row[3],
            'adr_to': row[4],
            'geo_code_1_to': row[5],
            'geo_code_2_to': row[6],
            'full_name_from': row[7],
            'full_name_to': row[8],
            'phone_from': row[9],
            'phone_to': row[10],
            'cost': str(row[11]),
            'courier_id': row[12],
            'order_date': row[13],
            'order_status': row[15],
            'status_date': row[16]
        })
    return orders


@jsonrpc.method('App.post_order')
def post_order_admin(client_id: int, sender_adr: str, sender_comment: str, sender_name: str, sender_coord_1: str, sender_coord_2: str, sender_phone: str,
                    receiver_adr: str, receiver_comment: str, receiver_name: str, receiver_coord_1: str, receiver_coord_2: str, receiver_phone: str,
                    cost: str) -> Union[str, None]:
    data_dict = []
    try:
        sender_coord_1 = float(sender_coord_1)
        sender_coord_2 = float(sender_coord_2)
        receiver_coord_1 = float(receiver_coord_1)
        receiver_coord_2 = float(receiver_coord_2)
        cost = float(cost)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO addresses (id_client, str_adr, comment, full_name, geo_code_1, geo_code_2, phone)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);""", [client_id, sender_adr, sender_comment, sender_name, sender_coord_1, sender_coord_2, sender_phone])
        conn.commit()
        cursor.execute("""SELECT max(id) from addresses""")
        id_from = cursor.fetchall()[0][0]
        cursor.execute("""INSERT INTO addresses (id_client, str_adr, comment, full_name, geo_code_1, geo_code_2, phone)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);""", [client_id, receiver_adr, receiver_comment, receiver_name, receiver_coord_1, receiver_coord_2, receiver_phone])
        conn.commit()
        cursor.execute("""SELECT max(id) from addresses""")
        id_to = cursor.fetchall()[0][0]
        cursor.execute("""INSERT INTO orders (client_id, courier_id, sent_from_id, sent_to_id, order_date, cost)
                            VALUES (%s, null, %s, %s, DEFAULT, %s);""", [client_id, id_from, id_to, cost])
        conn.commit()
        cursor.execute("""SELECT max(order_num) from orders""")
        data = cursor.fetchall()
        if len(data) > 0:
            cursor.execute("""INSERT INTO order_statuses (order_status, status_date, status_reason, order_num)
                                VALUES ('Заказ создан', DEFAULT, null, %s);""", [data[0][0]])
            conn.commit()
            print(str(data[0][0]))                    
            return str(data[0][0])
        else:
            print(1)
            return None
    except Exception as e:
        print(str(e))
        return None



# Точка входа
if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=False)