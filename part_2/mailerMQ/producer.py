from datetime import datetime
import json

import pika.spec
from pika import PlainCredentials, BlockingConnection, ConnectionParameters, BasicProperties

from db.connection import connection_to_mongo
from db.create_users import create_user
from models import User

credentials = PlainCredentials('guest', 'guest')
connection = BlockingConnection(ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')




if __name__ == '__main__':
    connection_to_mongo()
    create_user(10)

    all_users = User.objects.all()

    for user in all_users:
        message = {
            "user _id": str(user.id),
            "payload": f"Send mail to {user.email}",
            "date": datetime.now().isoformat(),
            'message': 'Hello everyone! Please contact to your manager!'
        }

        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=json.dumps(message).encode(),
            properties=BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
        )
        print(" [x] Sent %r" % message)
    connection.close()