# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:59:40 2022

@author: mdbad
"""
import glob
import numpy as np
import pandas as pd
import csv
import seaborn as sns

np.set_printoptions(suppress=True, precision=5, linewidth=150)

#Make sure you have all your 80 csv files and this .py file in the same folder
files_names = glob.glob("*.csv")
cities_name=[]
#Percentile values (bins)
hea = (10, 20, 30, 40, 50, 60, 70, 80, 90, "Max")

d = np.array([])
city_l = []

s = []
D = []

#Calculate the percentile values for each city
for name in files_names:
    q = []
    r = name.split("_")
    cities_name.append(str(r[0]))
    print(r[0])
    dat = pd.read_csv(name, header = 0)
    #Combine all lengths from all cities into one
    d = np.concatenate((d, (dat.LENGTH.values)), axis=0)
    city_l.append(dat.LENGTH.values)

#Assign percentile values as bins
for i, a in enumerate(hea):
        if isinstance(a, str):
            s.append(max(d))
        else:
            s.append(np.percentile(d, a))
            
x = np.array([s])
#wr = pd.DataFrame(s, columns = hea)
#wr.to_csv('out.csv', index=False)          
        
z = np.insert(x, 0, 0)

with open('Cities Link Lengths Probabilities1.csv','w') as link_data:
    write_data = csv.writer(link_data, delimiter=',',lineterminator='\n',)    
    for name in files_names: 
        q = []
        r = name.split("_")
        cities_name.append(str(r[0]))
        print(r[0])
        da = pd.read_csv(name, header = 0)
        aw = da.LENGTH
        #Calculate probabilities for each bins 
        for i,j in enumerate(s):
            S = ([z[i], s[i]])
            #print(s)
            D.append(len(aw[(aw > S[0]) & (aw <= S[1])]))
            q.append(len(aw[(aw > S[0]) & (aw <= S[1])]) / len(da.LENGTH))       
               
        tr = (r[0],) + tuple(q)        
        write_data.writerow(tr)        
   
