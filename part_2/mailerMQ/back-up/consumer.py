from time import sleep
import json

from pika import  PlainCredentials, BlockingConnection, ConnectionParameters

credentials = PlainCredentials('guest', 'guest')
connection = BlockingConnection(ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


def callback(ch, method, properties, body):
    # message = json.loads(body.decode())
    message = body.decode()
    print(f'[x] Received {message}')
    sleep(0.01)
    print(f'[x] Done: {method.delivery_tag}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()