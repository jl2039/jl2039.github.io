import pymysql
from datetime import datetime
from KasaSmartPowerStrip import SmartPowerStrip
import subprocess
import os
import time as t
power_strip = SmartPowerStrip('192.168.50.70')

print(datetime.now())
#try:
db = pymysql.connect(host='127.0.0.1',
                     user='USER name in step 2',
                     passwd='Password in step 2',
                     db='Database name in step 2',
                     port=3306,
                     charset='utf8')

cursor = db.cursor()
#cursor.execute('DROP TABLE IF EXISTS PLUG')
for ii in range(6):
    cursor.execute("SELECT * FROM PLUG{}".format(ii))
    row = cursor.fetchone()
    if row is None:
        # cursor.execute('DROP TABLE IF EXISTS PLUG{}'.format(ii))
        sql = """CREATE TABLE `PLUG{}` (
              `Time` char(26) NOT NULL,
              `Voltage_mv` int(10) NOT NULL,
              `Current_ma` int(10) NOT NULL,
              `Power_mw` int(10) NOT NULL,
              `Total_wh` int(20) NOT NULL
              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;""".format(ii)
        cursor.execute(sql)
# Write data in the database
try: 
    while True:
        # Prepare data
        for ii in range(6):
            #print(ii)
            time = datetime.now()
            flag, M = power_strip.get_realtime_energy_info(plug_num=ii+1)
            if flag is not 1:
                print("Time out by pass node, sleep 1s")
                sleep_time = 1
                break
            i = 0;
            item  = [0, 0, 0, 0, 0]
            for v in M.values() :
                item[i] = v
                i = i + 1
            sleep_time = 0.1
            print(time, ii, M)
            V = item[0]
            I = item[1]
            P = item[2]
            E = item[3]
            # Write to the database
            sql =  "INSERT INTO PLUG%d(Time, Voltage_mv, Current_ma, Power_mw, Total_wh) \
                VALUES('%s', '%d', '%d', '%d', '%d') " % \
                (ii,time, item[0], item[1], item[2], item[3])
            #print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
        t.sleep(sleep_time)
except KeyboardInterrupt:
    print("Press Ctrl-C to terminate while statement")
    pass

# Read from database
for ii in range(6):
    print("Plug{}".format(ii))
    cursor.execute("SELECT * FROM PLUG{}".format(ii))
    row = cursor.fetchone()
    while row is not None:
        print(row)
        row = cursor.fetchone()
# print('create table')
db.close()



