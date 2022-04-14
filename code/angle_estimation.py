# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:23:26 2022

@author: mdbad
"""

import glob
import csv
import math
import time
import numpy as np
import pandas as pd
import networkx as nx

np.set_printoptions(suppress=True, precision=5, linewidth=150)
 
files_names = glob.glob("*.csv")
cities_name = []
cities = {}

#20 degrees bins to calculate angles 
deg = np.arange(0.0, 380.0, 20.0)

#Extract the intersection angles and save them in a csv file
with open('Cities Graph angle1.csv','w') as ang_data:
    write_data = csv.writer(ang_data,  delimiter = ',',lineterminator = '\n',)
    
    for name in files_names:
        degr = []
        ang_dist = []
        r = name.split("_")
        cities_name.append(str(r[0]))
        
        #created a separate text file to put all the angles at all intersections
        #within in a city for any further analysis
        
        with open(r[0] + '.txt','w') as f:
            data = pd.read_csv(name, header = 0)
            data1 = data.drop_duplicates('START_NODE')
            data2 = data1.drop(['START_NODE','END_NODE','EDGE','LENGTH'], axis = 1)
            data2 = data2.set_index(data1.START_NODE.values)
            #G = nx.from_pandas_edgelist(data, 'START_NODE', 'END_NODE', edge_attr=['EDGE', 'LENGTH'])
            node_all = data.START_NODE.unique()
            print(r[0])
            print('The total number of nodes are %d' %len(node_all))
            
            #these three lines of code is to keep track of progress
            #replace it with tqdm package
            tt = 0
            ty = 1000
            start = time.time()
            
            for d in node_all:
                #GEt all the connected node for node d
                connected_nodes = data[data.START_NODE.values == d].END_NODE
                #print ('\n'+str(time.time() - start))
                #connected_nodes = list(G.neighbors(d))
                if len(connected_nodes) > 1:
                    lat = data2.loc[int(d)][0]
                    long = data2.loc[int(d)][1]
                    ang=[]
                    
                    if tt > ty:
                        print('The node number is %d and time is %.2f' %(tt, time.time() - start))
                        start = time.time()
                        ty = ty + 1000
                    tt = tt + 1
                    
                    #Calculate all angles separated by links at an intersection
                    #The inesection is the node d
                    for i in range(1, len(connected_nodes)):
                        #print(connected_nodes.values[i-1])
                        #print(connected_nodes.values[i])
                        lat1 = data[data.START_NODE == connected_nodes.values[i-1]].XCoord.values[0]
                        long1 = data[data.START_NODE == connected_nodes.values[i-1]].YCoord.values[0]
                        lat2 = data[data.START_NODE == connected_nodes.values[i]].XCoord.values[0]
                        long2 = data[data.START_NODE == connected_nodes.values[i]].YCoord.values[0]
                        #print('The lat is %d and long is %d' %(lat1,long1))
                        #print('The lat is %d and long is %d' %(lat2,long2))
                        
                        #Estimate the variables to use Cosine rule and finally the bearings
                        a = np.sqrt((lat2-lat1)**2+(long2 -long1)**2)
                        b = np.sqrt((lat-lat1)**2+(long -long1)**2)
                        c = np.sqrt((lat-lat2)**2+(long -long2)**2)
                        deg_ = math.degrees(math.acos(round((b**2 + c**2 - a**2)/(2*b*c))))
                        degr.append(deg_) #append all the bearings associated with node d(intersection)
                 
                    #Bearings are not angles, so angles are calculated by imagining
                    #the connected nodes are in any one of the four quadrants
                    La = [data2.loc[int(R)][0] for R in connected_nodes]
                    Lo = [data2.loc[int(R)][1] for R in connected_nodes]
                    
                    X = (La - lat)
                    Y = (Lo - long)
                    #print(d)   
                    #angles are calculated based on which quadrant the connected node is present
                    
                    for i, j in zip(X,Y):
                        if i > 0 and j > 0:
                            ang.append(round(math.degrees(math.atan(i/j)),2))
                        elif i > 0 and j < 0:
                            ang.append(90 + round(math.degrees(math.atan(abs(j/i))),2))
                        elif i < 0 and j < 0:
                            ang.append(180 + round(math.degrees(math.atan(abs(i/j))),2))
                        elif i < 0 and j > 0:
                            ang.append(270 + round(math.degrees(math.atan(abs(j/i))),2))
                            
                    for k in range(1, len(ang)):
                        degr.append(np.sort(ang)[k] - np.sort(ang)[k-1])
            
            #Calculate the probabilities 
            for i in range(1,len(deg)):
                a = [x for x in degr if x >= deg[i-1] and x <= deg[i]]
                ang_dist.append(len(a)/len(degr))
              
            f.write( ','.join( str(v) for v in degr ) )    
        write_data.writerow((r[0],) + tuple(ang_dist))
    
