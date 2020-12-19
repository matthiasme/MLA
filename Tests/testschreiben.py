import csv
from datetime import datetime
import os
import random

date_time = datetime.now().strftime("%y-%m-%d_%H-%M")
path=os.path.dirname(__file__)+"/Data/" + date_time + ".csv"
print(path)
f = open(path, mode='w',encoding="utf-8", newline="")
f_csv_writer = csv.writer(f,delimiter=",")
row_index = 0

outputvalue = random.randint(0,100)
row_time = datetime.now().strftime("%H/%M/%S")
row_content = [row_index, row_time, outputvalue]
row_index +=1
f_csv_writer.writerow(row_content)

f.close()