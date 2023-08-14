from datetime import datetime
import json

import pika.spec
from pika import PlainCredentials, BlockingConnection, ConnectionParameters, BasicProperties

credentials = PlainCredentials('guest', 'guest')
connection = BlockingConnection(ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')


if __name__ == '__main__':

    # for i in range(15):
    message = {
        "id": 1,
        "payload": f"Task #{1}",
        "date": datetime.now().isoformat()
    }

    channel.basic_publish(
        exchange='task_mock',
        routing_key='task_queue',
        # body=json.dumps(message).encode(),
        body='Hello my friend!'.encode(),
        properties=BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
    )
    print(" [x] Sent %r" % message)
    connection.close()