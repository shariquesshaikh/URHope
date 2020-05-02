import pymysql
import csv
import os


from zipfile import ZipFile 

db = pymysql.connect(host='localhost', user='root', passwd='CoronaPassword.1#',
                         db='covid', charset='utf8mb4')
c = db.cursor()
keys = ['pin', 'officename', 'divisionname', 'regionname', 'circlename', 'taluk', 'districtname', 'statename', 'relsuboffice']
key_map = {}
with ZipFile("india_po_data.csv.zip", "r") as z:
    z.extractall()

with open("india_po_data.csv") as f:
    for i, j in enumerate(f.readlines()):
        headers = []
        if not i:
            headers = j.split(",")
            for k in keys:
                key_map[k]=headers.index(k)
        else:
            j = j.split(",")
            query = "insert into podata ("
            vals = " values ("
            for k,v in key_map.items():
                query += k+", "
                vals += "'"+j[v]+"', "
            q = query[:-2]+") "+vals[:-2]+");"
            print("Processing :%s" % j[key_map['pin']])
            try:
                c.execute(q)
                db.commit()
            except:
                pass

        # if i ==11:
        #     break
os.remove("india_po_data.csv")
db.close()
