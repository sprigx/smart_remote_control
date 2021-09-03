import socket
import pickle
import time
import json
import csv
import re
import hashlib
import sqlite3
from pprint import pprint as pp
from logging import getLogger, StreamHandler, FileHandler, config, DEBUG


# id追加、UNIX時間の小数点丸め、statusのINT化
def preprocess_proc_info(proc_info):
    if proc_info['status'] == 'running':
        proc_info['status'] = 0
    elif proc_info['status'] == 'sleeping':
        proc_info['status'] = 1
    else:
        proc_info['status'] = 3
    addr = mask_ip_addr(proc_info['ip_addr'])
    proc_info['create_time'] = round(proc_info['create_time'])
    utime = str(proc_info['create_time'])
    pid = str(proc_info['pid'])
    proc_info['id'] = int(utime+pid+addr)
    return proc_info

def select_procs(proc_list, ids):
    return [proc_info for proc_info in proc_list if proc_info['id'] in ids]

def mask_ip_addr(ip_addr):
    return re.findall('[0-9]+$', ip_addr)[0]

def insert_procs(proc_list, cur):
    if proc_list == []:
        return 0
    for proc_info in proc_list:
        cur.execute(f"insert into procs values(\
                      {proc_info['id']}, '{proc_info['ip_addr']}', '{proc_info['username']}',\
                      {proc_info['memory_percent']}, {proc_info['cpu_percent']},\
                      {proc_info['status']}, {proc_info['pid']},\
                      {proc_info['create_time']})")

def update_procs(proc_list, cur):
    if proc_list == []:
        return 0
    for proc_info in proc_list:
        cur.execute(f"update procs set \
                      memory_percent = {proc_info['memory_percent']},\
                      cpu_percent = {proc_info['cpu_percent']},\
                      status = {proc_info['status']}\
                      where id = {proc_info['id']}")

def finish_procs(id_set, cur):
    if id_set == {}:
        return 0
    for id in id_set:
        cur.execute(f"update procs set \
                      status = 2 \
                      where id = {id}")

PORT = 50000
BUFFER_SIZE = 1024
TIMEOUT_TIME = 3

dbname = 'server_state.db'
con = sqlite3.connect(dbname)
con.row_factory = sqlite3.Row
c = con.cursor()
c.execute('drop table servers')
c.execute('drop table procs')
c.execute('create table if not exists servers(ip_addr text primary key, status int, ram real, cpu real)')
c.execute('create table if not exists procs(id int primary key, \
           ip_addr text, username text, memory_percent real, cpu_percent real, \
           status int, pid int, create_time int)')

c.execute('insert into procs values(1000000, "127.0.0.1", "username", 0.0, 1.2, 1, 2045, 10000000)')
c.execute('insert into procs values(2000000, "192.168.10.108", "username", 0.0, 1.2, 1, 1045, 20000000)')
c.execute('insert into servers values("192.168.10.108", 0, 0.0, 1.2)')
with open('log_config.json', 'r') as f:
    log_conf = json.load(f)
    config.dictConfig(log_conf)
logger = getLogger(__name__)
logger.info('Started crawling!')

try:
    while True:
        time.sleep(2)
        with open('server_list.csv', 'r') as f:
            reader = csv.reader(f)
            ip_addr_set = {e[0] for e in reader}
        logger.info('IP address list loaded.')

        c.execute('SELECT * FROM servers')
        old_ip_addr_set = {server_info['ip_addr'] for server_info in c}
        disabled_server_addr_set = old_ip_addr_set - ip_addr_set
        # CSVから削除されたサーバーを停止扱いに
        for server_addr in disabled_server_addr_set:
            c.execute(f"update servers set status = 2 where ip_addr = '{server_addr}'")
        # CSVに新しく追加されたサーバーのレコード作成
        new_server_addr_set = ip_addr_set - old_ip_addr_set
        for server_addr in new_server_addr_set:
            c.execute(f"insert into servers values('{server_addr}', 1, 0, 0)")

        for ip_addr in ip_addr_set:
            time.sleep(0.1)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.settimeout(TIMEOUT_TIME)
                    s.connect((ip_addr, PORT))
                    data = s.recv(BUFFER_SIZE)
                    server_info = pickle.loads(data)
                    logger.info('client '+ip_addr+' successfully connected!')
                    for i in range(len(server_info['process_info'])):
                        server_info['process_info'][i]['ip_addr'] = ip_addr

                    new_proc_list = list(map(preprocess_proc_info, server_info['process_info']))
                    c.execute(f"SELECT * FROM procs WHERE status != 2 and ip_addr = '{ip_addr}'")

                    old_proc_id_set = {proc_info['id'] for proc_info in c}
                    new_proc_id_set = {proc_info['id'] for proc_info in new_proc_list}
                    # すでにレコードが存在するプロセスの情報をアップデート
                    update_proc_id_set = new_proc_id_set & old_proc_id_set
                    update_proc_list = select_procs(new_proc_list, update_proc_id_set)
                    update_procs(update_proc_list, c)
                    # レコードが存在するが、更新されたデータにないプロセスを終了ステータスに
                    finished_proc_id_set = old_proc_id_set - new_proc_id_set
                    finish_procs(finished_proc_id_set, c)
                    # 新規プロセスは新しくレコード作成
                    insert_proc_id_set = new_proc_id_set - old_proc_id_set
                    insert_proc_list = select_procs(new_proc_list, insert_proc_id_set)
                    insert_procs(insert_proc_list, c)

                    status = 0

                except socket.timeout:
                    logger.error('client '+ip_addr+' connection timed out.')
                    status = 1
                except ConnectionError:
                    logger.error('client '+ip_addr+' connection failed.')
                    status = 1
                except Exception:
                    logger.error('client '+ip_addr+' something wrong.')
                    status = 1
                finally:
                    c.execute(f"update servers set \
                                status = {status}, \
                                ram = {server_info['total_memory_percent']}, \
                                cpu = {server_info['total_cpu_percent']} \
                                where ip_addr = '{ip_addr}'")
                    con.commit()

except KeyboardInterrupt:
    con.commit()
    con.close()
