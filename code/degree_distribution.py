# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:21:58 2022

@author: mdbad
"""


import glob
import csv
import numpy as np
import pandas as pd
import networkx as nx

np.set_printoptions(suppress=True, precision=5, linewidth=150)

#Make sure you have all your 80 csv files and this .py file in the same folder
files_names = glob.glob("*.csv")
cities_name = []
cities = {}
#to store the network objects
networks = []
nodes = []
edges = []

avg_link_length = []


            
#Calucalte degree distribution for each city and store it in a csv file
#in the same folder as the city csv files

with open('Cities Graph Degree.csv','w') as deg_data: 
    write_data = csv.writer(deg_data, delimiter=',',lineterminator='\n',)
    
    for name in files_names:
        r = name.split("_")
        cities_name.append(str(r[0]))
        
        print(r[0])
        
        data = pd.read_csv(name, header = 0)
        
        #Construct the network to extract degree distribution
        G = nx.from_pandas_edgelist(data, 'START_NODE', 'END_NODE', edge_attr=['EDGE', 'LENGTH'])
        
        #store the network object in a list
        networks.append([str(r[0]), G])
        
        nodes.append(G.number_of_nodes())
        edges.append(G.number_of_edges())
        
        avg_link_length.append(data['LENGTH'].mean())
        degrees = [val for (node, val) in G.degree()]
        
        #Calculate the probability
        freq = [(degrees.count(i)/G.number_of_nodes()) for i in set(degrees)]
        tr = (r[0],) + tuple(freq)
        
        #copy the degree distribution to the csv file
        write_data.writerow(tr)
    
