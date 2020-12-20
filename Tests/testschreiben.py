#!/usr/bin/python3
import numpy as np
from datetime import datetime
import random, os

date_time = datetime.now().strftime("%y-%m-%d_%H-%M") + ".txt"
#print(date_time)
path = os.path.dirname(__file__) + "/Data/" + date_time
#print(path)

content = [["row tindex", "time", "outputvalue", "force"]]
#print(content)

for row_index in range(10):
    row_time = datetime.now().strftime("%H-%M-%S")
    outputvalue = random.randint(0,100)
    force = outputvalue*3
    row_content = [row_index, row_time, outputvalue, force]
    #print(row_content)
    content.append(row_content)
    row_index+=1
    content_to_safe = np.array(content)
    np.savetxt(path, content_to_safe, delimiter=",",fmt='%s')
    


