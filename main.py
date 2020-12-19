#!/usr/bin/python
import time
from Server_Service import ServerThread
from datetime import datetime
import configparser
from datetime import date, datetime, timedelta
import sqlite3
import sys
import logging
import logging.handlers
import socket
import os
import time
import threading
from pprint import pprint


"""Load configuration from .ini file."""

print("Run as Python 3")

#from playsound import playsound


#?-------------------- Class Data BAse ------------------------------#

class sqlite_trans():
    def __init__(self, sqlite_db_name):
        self.sqlite_db_name = sqlite_db_name
        print("Set Sqllite as {}".format(sqlite_db_name))

    def insert_trans(self, transGATE, transDate=None):
        try:
            conn = sqlite3.connect(self.sqlite_db_name)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT transID FROM Trans ORDER BY transID DESC LIMIT 1")
            result = cursor.fetchone()
            if(result == None):
                result = 1
            else:
                result = result[0] + 1
            if(transDate == None):
                transDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO Trans(transID, transDate, transGATE) VALUES ({}, '{}', '{}')".format(
                result, transDate, transGATE)
            print("SQL > {}".format(sql))
            cursor.execute(sql)
            res = cursor.lastrowid
            conn.commit()
            cursor.execute("SELECT * FROM Trans ORDER BY transID DESC LIMIT 1")
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as err:
            print("Error insert_trans : {}".format(err))
            return 0

    def select_trans(self, sql):
        try:
            conn = sqlite3.connect(self.sqlite_db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.close()
            return result
        except Exception as err:
            print("Error select_trans : {}".format(err))
            return 0


#?--------------------Global Variable------------------------------#
# Read local file `config.ini`.
config = configparser.ConfigParser()
config.read('./config.ini')

data_base_ip = config.get("CONFIG", "data_base_ip")
data_base_name = config.get("CONFIG", "data_base_name")
data_base_user = config.get("CONFIG", "data_base_user")
data_base_password = config.get("CONFIG", "data_base_password")
sys_share_folder = config.get("CONFIG", "sys_share_folder")
camara_ip_01 = config.get("CONFIG", "camara_ip_01")
device_name = config.get("CONFIG", "device_name")

sys_gate_id = config.get("CONFIG", "sys_gate_id")
sys_user_id = config.get("CONFIG", "sys_user_id")
sys_profile_id = config.get("CONFIG", "sys_profile_id")

tranID = ""
data_base_conn = None

syslog = logging.getLogger('syslog')
syslog.setLevel(logging.DEBUG)
syslog.addHandler(logging.handlers.SysLogHandler(address=(data_base_ip, 514)))

gate_01_count = 0
gate_02_count = 0

transDB = sqlite_trans('data.db')

sqlite_db = sqlite3.connect('data.db').cursor()
# ! Drop Table
#sqlite_db.execute("drop table if exists Trans")
#print("Table 'member_card' Drop successfully")

sqlite_db.execute('''create table if not exists Trans
         (transID               INTEGER PRIMARY KEY,
         transDate              DATE,
         transGATE              varchar(50) NOT NULL
         );''')
print("Table created successfully")


# print("""
# ***************************************************************************
# ************************** Config System   ********************************
# ***************************************************************************
#
#                data_base_ip        :   {}
#                data_base_name      :   {}
#                data_base_user      :   {}
#                data_base_password  :   {}
#                syslog              :   {}
#                device_name         :   {}
#                sys_gate_id         :   {}
#                sys_user_id         :   {}
#                sys_profile_id      :   {}
#                sqlite_db           :   {}
#
# ***************************************************************************
# """.format(data_base_ip, data_base_name, data_base_user, data_base_password, syslog, device_name, sys_gate_id, sys_user_id, sys_profile_id, sqlite_db))

#?--------------------Function------------------------------#


#?--------------------Function Threading------------------------------#

_date_now = datetime.now()
date_start = "2020-12-01T00:00"
date_end = _date_now.strftime("%Y-%m-%dT23:59")
server = None


def gen_x_line():
    global date_start, date_end
    try:
        _time_start = datetime.strptime(date_start, '%Y-%m-%dT%H:%M')
        _time_end = datetime.strptime(date_end, '%Y-%m-%dT%H:%M')
    except Exception as err:
        date_start = "2020-12-01T00:00"
        date_end = _date_now.strftime("%Y-%m-%dT23:59")
        _time_start = datetime.strptime(date_start, '%Y-%m-%dT%H:%M')
        _time_end = datetime.strptime(date_end, '%Y-%m-%dT%H:%M')

    difference = _time_end - _time_start
    _time_div = difference/12

    print(_time_start)
    print(difference)
    print(_time_div)
    print(_time_end)

    sql = "SELECT COUNT(*) FROM Trans WHERE transDate between '{}' AND '{}';".format(
        _time_start, _time_end)
    sql = "SELECT COUNT(*) FROM Trans;"
    res = transDB.select_trans(sql)
    print(" COUNT ALL = {}".format(res[0][0]))

    _t = _time_start
    _ret = []
    _gate_01 = []
    _gate_02 = []
    _gate_all = []
    for i in range(12):
        _ret.append(_t.strftime("%d-%b-%y %H:%M"))
        sql = "SELECT COUNT(*) FROM Trans WHERE transGATE='Gate_01' AND transDate between '{}' and '{}';".format(_t, _t+_time_div)
        res = transDB.select_trans(sql)
        _gate_01.append(res[0][0])

        sql = "SELECT COUNT(*) FROM Trans WHERE transGATE='Gate_02' AND transDate between '{}' and '{}';".format(_t, _t+_time_div)
        res = transDB.select_trans(sql)
        _gate_02.append(res[0][0])

        _gate_all.append(_gate_01[i]+_gate_02[i])
        print(sql)
        print("GET DATA TIME = {} - {}".format(_t, _t+_time_div))
        _t += _time_div
    print(_gate_all)
    return(_ret, _gate_01, _gate_02, _gate_all)


def call_back_server(**kwarg):
    global date_start, date_end, coin_status, gate_01_count, gate_02_count
    if("getdata" in kwarg):
        temp = {}
        temp["status"] = coin_status
        temp["Gate_01"] = gate_01_count
        temp["Gate_02"] = gate_02_count
        chart_data = gen_x_line()
        temp["x_line"] = chart_data[0]
        temp["y_line01"] = chart_data[1]
        temp["y_line02"] = chart_data[2]
        temp["y_line03"] = chart_data[3]
        temp["t_gate_01"] = sum(chart_data[1])
        temp["t_gate_02"] = sum(chart_data[2])
        temp["t_gate"] = sum(chart_data[1]) + sum(chart_data[2])
        temp["date_start"] = date_start
        temp["date_end"] = date_end
        print("------------------------------------------------------------------------------ RET")
        return temp

    if("setdata" in kwarg):
        _config = kwarg["setdata"]
        date_start = _config.get("date_start")
        date_end = _config.get("date_end")
        return 1

    if("gettables" in kwarg):
        sql = "SELECT * FROM Trans ORDER BY transID DESC LIMIT {}".format(
            kwarg["gettables"])
        print(sql)
        rows = transDB.select_trans(sql)
        #rows = rows[::-1]
        # pprint(rows)
        return rows

    if("event" in kwarg):
        _msg = kwarg["event"]["msg"]
        if (_msg == "sw_01"):
            res = transDB.insert_trans(transGATE="Gate_01")
            print(res)
            server.send_message("{},{},{}".format(
                res[0], res[1], res[2]), header="log_table")
            res = transDB.select_trans(
                "SELECT COUNT(transID) FROM Trans WHERE transGATE='Gate_01';")
            server.send_message("gate_01={}".format(res[0][0]))
            gate_01_count = res[0][0]

        if (_msg == "sw_02"):
            res = transDB.insert_trans(transGATE="Gate_02")
            print(res)
            server.send_message("{},{},{}".format(
                res[0], res[1], res[2]), header="log_table")
            res = transDB.select_trans(
                "SELECT COUNT(transID) FROM Trans WHERE transGATE='Gate_02';")
            server.send_message("gate_02={}".format(res[0][0]))
            gate_02_count = res[0][0]

        return 1


def start_server():
    global server
    if(server is None):
        port = int(os.environ.get('PORT', 5000))
        print('PORT USE = {}'.format(port))
        server = ServerThread(device_name, syslog=syslog, call_back=call_back_server, port=port)
        server.start()
    else:
        print("Server Is Running")
    #log.info('server started')


def stop_server():
    global server
    server.shutdown()

    server = None

def restart():
    import sys
    print("argv was", sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")
    import os
    #os.execv(sys.executable, ['python'] + sys.argv)
    python = sys.executable
    os.execl(python, python, * sys.argv)


def ping_ip(ip):
    response = -1
    if(os.name != "nt"):
        response = os.system("ping -c 1 {} > /dev/null 2>&1".format(ip))
    else:
        response = os.system("ping {} -n 1".format(ip))
    if(response == 0):
        return True
    else:
        return False


coin_status = ""


if __name__ == '__main__':

    print("--------------------------------------------------------------")
    #print("GEN DATA TEST")
    #a = datetime(2020, 12, 1)
    #_gate = ["Gate_01",'Gate_02']
    # for i in range(500):
    #    transDB.insert_trans(transGATE=random.choice(_gate),transDate=a)
    #    a = a + timedelta(0,random.randint(60,300))

    #cursor = sqlite3.connect('data.db').cursor()
    #cursor.execute("SELECT * FROM Trans")
    #rows = cursor.fetchall()
    # for row in rows:
    #    print(row)
#
    res = transDB.select_trans(
        "SELECT COUNT(transID) FROM Trans WHERE transGATE='Gate_01';")
    gate_01_count = res[0][0]
    res = transDB.select_trans(
        "SELECT COUNT(transID) FROM Trans WHERE transGATE='Gate_02';")
    gate_02_count = res[0][0]

    print("RUN : MAIN")
    start_server()
    print("\n************************************************** START SYSTEM **************************************************************\n")

    while True:
        time.sleep(1)

    stop_server()

    print("Python CLOSE")
