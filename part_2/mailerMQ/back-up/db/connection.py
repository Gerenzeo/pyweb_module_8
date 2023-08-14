from mongoengine import connect

def connection_to_mongo():
    connect(db='users', host='localhost', port=27017)