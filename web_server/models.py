from db import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.types import Float
from sqlalchemy.types import Integer
from sqlalchemy.types import String


SQLITE3_NAME = "./db.sqlite3"


class Server(Base):
    __tablename__ = 'servers'
    ip_addr = Column('ip_addr', String(256), primary_key=True)
    status = Column('status', Integer)
    ram = Column('ram', Float)
    cpu = Column('cpu', Float)

    def __init__(self, ip_addr, status, ram, cpu):
        self.ip_addr = ip_addr
        self.status = status
        self.ram = ram
        self.cpu = cpu

    def __str__(self):
        return self.ip_addr + ':' + self.status

class Proc(Base):
    __tablename__ = 'procs'
    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )
    ip_addr = Column('ip_addr', ForeignKey('servers.ip_addr'))
    username = Column('username', String(256))
    memory_percent = Column('memory_percent', Float)
    cpu_percent = Column('cpu_percent', Float)
    status = Column('status', Integer)
    pid = Column('pid', Integer)
    create_time = Column('create_time', Integer)

    def __init__(self, ip_addr, username, memory_percent,
                 cpu_percent, status, pid, create_time):
        self.ip_addr = ip_addr
        self.username = username
        self.memory_percent = memory_percent
        self.cpu_percent = cpu_percent
        self.status = status
        self.pid = pid
        self.create_time = create_time

