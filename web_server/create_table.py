from models import *
import db
import os


if __name__ == '__main__':
    path = SQLITE3_NAME
    if not os.path.isfile(path):
        Base.metadata.create_all(db.engine)

    test = Server(ip_addr='192.168.10.110', status=0, ram=0.1, cpu=0.1)
    db.session.add(test)
    db.session.commit()

    db.session.close()
