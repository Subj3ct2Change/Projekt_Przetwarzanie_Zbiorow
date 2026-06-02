def get_user_data():
    with open(file="DaneLogowania/Data.txt", mode="r") as f:
        user = f.readline().replace("\n", "")
        passwd = f.readline().replace("\n", "")
        host = f.readline().replace("\n", "")
        port = f.readline().replace("\n", "")
        db_name = f.readline().replace("\n", "")
    return user, passwd, host, port, db_name