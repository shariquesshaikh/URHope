import pymysql
import csv
import os


from zipfile import ZipFile 

db = pymysql.connect(host='localhost', user='root', passwd='',
                         db='covid', charset='utf8mb4')

def string(s):
    return "'"+s+"'" if s else "''"

files = ["Goa.csv", "UT.csv", "Initiatives-05-05-2020.csv"]
for file in files:
    with open("./Initiatives/"+file) as f:
        for c,i in enumerate(f.readlines()):
            if not c:
                continue
            q = "insert into govtdata values (DEFAULT,"
            data = i.split(",")
            for i in range(15):
                qry_rem = "'', "*(15-len(data))
                if type(i) != tuple and len(data) >= i+1:
                    q += string(data[i]) + ", "
                elif type(i) == tuple:
                    if len(data) == i[1]:
                        q += string(data[i[0]] + ", " + data[i[1]]) + ", "
                    elif len(data)>= i[0]:
                        q += string(data[i[0]]) + ", "
            fin_q = q + qry_rem[:-2]+", DEFAULT);" if qry_rem else  q[:-2]+", DEFAULT);"
            print(fin_q)
            cur = db.cursor()
            cur.execute(fin_q)
            cur.close()
            db.commit()
db.close()


# keys = ['pin', 'officename', 'divisionname', 'regionname', 'circlename', 'taluk', 'districtname', 'statename', 'relsuboffice']
# key_map = {}
# with ZipFile("./india_po_data.csv.zip", "r") as z:
#     z.extractall()

# with open("./india_po_data.csv") as f:
#     for i, j in enumerate(f.readlines()):
#         headers = []
#         if not i:
#             headers = j.split(",")
#             for k in keys:
#                 key_map[k]=headers.index(k)
#         else:
#             j = j.split(",")
#             try:
#                 int(j[key_map['pin']])
#             except:
#                 print(j[key_map['pin']])
#             query = "insert into podata ("
#             vals = " values ("
#             for k,v in key_map.items():
#                 query += k+", "
#                 vals += "'"+j[v]+"', "
#             q = query[:-2]+") "+vals[:-2]+");"
#             print("Processing :%s" % j[key_map['pin']])
#             try:
#                 c.execute(q)
#                 db.commit()
#             except:
#                 pass

#         if i ==11:
#             break
# os.remove("./india_po_data.csv")
# db.close()