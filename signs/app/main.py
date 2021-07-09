
import pathlib
from cryptography.fernet import Fernet
import pika
import json
import sys, os
import time



def save_sign(sign, order_num):
    print("save_sign")
    try:
        import base64
        filepath = "" + str(order_num) + ".png"
        with open(filepath, "wb") as fh:
            fh.write(base64.decodebytes(sign.encode()))
        key = open("key.key", "rb").read()
        f = Fernet(key)
        with open(filepath, "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(filepath, "wb") as file:
            file.write(encrypted_data)
        return 
    except Exception as e:
        print(str(e))
        return str(e)

def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit_mq'))
        channel = connection.channel()

        channel.queue_declare(queue='save_sign')

        def callback(ch, method, properties, body):
            print("got_req")
            data_dict = json.loads(body)
            if "sign_file" in data_dict and "order_num" in data_dict:
                save_sign(data_dict["sign_file"], data_dict["order_num"])

        channel.basic_consume(queue='save_sign', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages')
        channel.start_consuming()
    except:
        time.sleep(30)
        main()

if __name__ == '__main__':
    main()