from flask import Flask, jsonify, request, render_template
from jsonrpcclient import request as req
import pika
import json

app = Flask(__name__)
application = app
wsgi_app = app.wsgi_app


def login_courier(password, phone):
    return req("http://host.docker.internal:5004/couriers", "App.login_courier", password=password, phone=phone).data.result


@app.route('/login_courier/<string:phone>/<string:password>')
def login_courier_web(phone, password):
    data_dict = login_courier(password, phone)
    if data_dict == None:
        return "-1"
    else:
        return jsonify(data_dict)


@app.route('/get_courier_free_orders/<string:phone_num>/<string:password>')
def get_courier_free_orders(phone_num, password):
    data_dict = login_courier(password, phone_num)
    if data_dict != None:
        return jsonify(req("http://host.docker.internal:5003/orders", "App.get_courier_free_orders").data.result)
    return "-1"

@app.route('/get_order_details/<string:phone_num>/<string:password>/<int:order_num>')
def get_order_details(phone_num, password, order_num):
    data_dict = login_courier(password, phone_num)
    if data_dict != None:
        return jsonify(req("http://host.docker.internal:5003/orders", "App.get_order_details", order_num=order_num).data.result)
    return "-1"


@app.route('/take_order/<string:phone_num>/<string:password>/<int:order_num>')
def take_order(phone_num, password, order_num):
    data_dict = login_courier(password, phone_num)
    if data_dict != None:
        return req("http://host.docker.internal:5003/orders", "App.take_order", order_num=order_num, courier_id=data_dict["id"]).data.result
    return "-1"



@app.route('/take_parcel/<string:phone_num>/<string:password>/<int:order_num>')
def take_parcel(phone_num, password, order_num):
    data_dict = login_courier(password, phone_num)
    if data_dict != None:
        return req("http://host.docker.internal:5003/orders", "App.take_parcel", order_num=order_num, courier_id=data_dict["id"]).data.result
    return "-1"
    

@app.route('/close_order/<string:phone_num>/<string:password>/<int:order_num>')
def close_order(phone_num, password, order_num):
    data_dict = login_courier(password, phone_num)
    if data_dict != None:
        return req("http://host.docker.internal:5003/orders", "App.close_order", order_num=order_num, courier_id=data_dict["id"]).data.result
    return "-1"

@app.route('/send_location/<string:phone_num>/<string:password>', methods=['POST'])
def send_location(phone_num, password):
    if not request.json:
        print(request.json)
        abort(400)
    d = request.json
    data_dict = login_courier(password, phone_num)
    if data_dict != None and "geo_code_1" in d and "geo_code_2" in d:
        # TODO Переделать на RabbitMQ
        return req("http://host.docker.internal:5004/couriers", "App.send_location", 
        courier_id=data_dict["id"], geo_coord_1=d["geo_code_1"], geo_coord_2=d["geo_code_2"]).data.result
    else:
        return "-1"

@app.route('/save_sign/<string:phone_num>/<string:password>/<int:order_num>', methods=['POST'])
def save_sign(phone_num, password, order_num):
    try:
        # Если пришёл не JSON - возвращаем HTTP ошибку 400
        if not request.json:
            print(request.json)
            abort(400)
        d = request.json
        data_dict = login_courier(password, phone_num)
        if data_dict != None:
            print("auth")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='host.docker.internal'))
            channel = connection.channel()
            channel.queue_declare(queue='save_sign')
            sign_data = {
                "sign_file": d["sign_file"],
                "order_num": order_num
            }
            channel.basic_publish(exchange='', routing_key='save_sign', body=json.dumps(sign_data))
            connection.close()
            return take_parcel(phone_num, password, order_num)
        else:
            return "-1"
        return "-1"
    except Exception as e:
        print(str(e))
        return str(e)

# Точка входа
if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)