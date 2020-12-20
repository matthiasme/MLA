#!/usr/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import random, os

date_time = datetime.now().strftime("%y-%m-%d_%H-%M")
#print(date_time)
path_txt = os.path.dirname(__file__) + "/Data/" + date_time + ".txt"
path_png = os.path.dirname(__file__) + "/Data/" + date_time + ".png"
#print(path)

content = [["row tindex", "time", "outputvalue", "force"]]
#print(content)

for row_index in range(10):
    row_time = datetime.now().strftime("%H-%M-%S")
    outputvalue = random.uniform(0,1)
    force = outputvalue*3
    row_content = [row_index, row_time, outputvalue, force]
    #print(row_content)
    content.append(row_content)
    row_index+=1
    content_to_safe = np.array(content)
    np.savetxt(path_txt, content_to_safe, delimiter=",",fmt='%s')
    
data = pd.read_csv(path_txt,sep=',',header=0,encoding='utf-8')
print(data)

time = data.iloc[:,0]
force = data.iloc[:,2]

limit = np.array([[0, 50],
                  [0.5, 0.5]])
plt.figure(1)
plt.plot(time,force,color='#0083CC')
plt.plot(limit[0,:],limit[1,:],color='#B90F22',linestyle = 'dashed')
plt.xlabel('Zeit in Minuten')
plt.xticks((0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150))
plt.ylabel('Kraft in Newton')
plt.xlim([0, 50])
plt.ylim([np.min(force)-0.4,np.max(force)+0.4])
plt.legend(('Gemessene Kraft','Schwellenwert'))
plt.savefig(path_png)
