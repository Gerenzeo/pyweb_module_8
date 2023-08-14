from mongoengine import Document, StringField, BooleanField


class User(Document):
    first_name = StringField()
    last_name = StringField()
    email = StringField()
    phone = StringField()
    send_status = BooleanField()

