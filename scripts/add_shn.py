import pymysql
import csv
import os


# from zipfile import ZipFile 

db = pymysql.connect(host='localhost', user='root', passwd='',
                         db='covid', charset='utf8mb4')
cur = db.cursor()

for file in ["UT_helplinesC.csv", "All_except_UT_helplinesC.csv"]:
    with open("./Helplines/"+file) as f:
        for c,i in enumerate(f.readlines()):
            if not c:
                continue
            q = "insert into statewisehelplinenos values (DEFAULT, "
            data = i.split(",")
            if len(data) == 3:
                data.append("''")
            for i in range(4):
                q += "'"+ data[i] + "', "
            print(q[:-2]+", DEFAULT);")
            cur.execute(q[:-2]+", DEFAULT);")
            db.commit()
db.close()

