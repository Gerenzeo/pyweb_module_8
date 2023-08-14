from db.connection import connection_to_mongo
from db.models import User

if __name__ == '__main__':
    connection_to_mongo()

    all_users = User.objects.all()

    for user in all_users:
        try:
            user.send_status = True
            user.save()
            print(f"Updated send_status for user: {user.id}")
        except Exception as e:
            print(f"Error updating user: {user.id}, Error: {e}")
