from faker import Faker
from connection import connection_to_mongo
from models import User

fake = Faker()

def create_user(count):
    for _ in range(count):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.numerify('+##-###-###-##-##'),
            send_status=False
        ).save()

if __name__ == '__main__':
    connection_to_mongo()
    create_user(20)
