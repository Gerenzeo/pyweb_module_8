from time import sleep
import json

from pika import  PlainCredentials, BlockingConnection, ConnectionParameters

from db.connection import connection_to_mongo
from models import User


credentials = PlainCredentials('guest', 'guest')
connection = BlockingConnection(ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


def callback(ch, method, properties, body):
    connection_to_mongo()


    message = json.loads(body.decode())
    user = User.objects.get(id=message['user _id'])
    print(f'[x] User with email {user.email} received message: {message["message"]}')
    sleep(0.01)
    user.send_status = True
    user.save()
    print(f'[x] Done: {method.delivery_tag}')


    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()