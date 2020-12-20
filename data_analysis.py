#!/usr/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import random, os

def data_analysis(path_txt, path_png, limit_value):
    #read in data:
    data = pd.read_csv(path_txt,sep=',',header=0,encoding='utf-8')
    
    #plot:
    time = data.iloc[:,0]
    force = data.iloc[:,2]
    limit = np.array([[0, 50],
                    [limit_value, limit_value]])
    plt.figure(1)
    plt.plot(time,force,color='#0083CC')
    plt.plot(limit[0,:],limit[1,:],color='#B90F22',linestyle = 'dashed')
    plt.xlabel('Zeit in Minuten')
    plt.xticks((0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150))
    plt.ylabel('Kraft in Newton')
    plt.xlim([0, 50])
    plt.ylim([np.min(force)-0.4,np.max(force)+0.4])
    plt.legend(('Gemessene Kraft','Schwellenwert'))

    #safe png:
    plt.savefig(path_png)