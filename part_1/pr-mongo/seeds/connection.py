from mongoengine import connect

def connection_to_mongo():
    connect(db='mongo_db_test', host='localhost', port=27017)