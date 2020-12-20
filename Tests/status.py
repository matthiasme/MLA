
"""
Created on Fri Dec 18 16:52:12 2020

@author: maxbuecker
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib as tikz

# %% import txt

filename = 'CSV.txt'
data = pd.red
v(filename,sep=',',header=0,encoding='utf-8')

time = data.iloc[:,0]
force = data.iloc[:,2]

# %% define limit

limit = np.array([[0, 50],
                  [2, 2]])

# %% plot time vs force

plt.figure(1)
plt.plot(time,force,color='#0083CC')
plt.plot(limit[0,:],limit[1,:],color='#B90F22',linestyle = 'dashed')
plt.xlabel('Zeit in Minuten')
plt.xticks((0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150))
plt.ylabel('Kraft in Newton')
plt.xlim([0, 50])
plt.ylim([np.min(force)-0.4,np.max(force)+0.4])
plt.legend(('Gemessene Kraft','Schwellenwert'))

# %% save figure as .png
plt.savefig('plot.png')

# %% save figure as .tex
tikz.save('plot.tex')