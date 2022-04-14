# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 23:45:25 2022

@author: mdbad
"""

import numpy as np
import pandas as pd
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.manifold import Isomap

import seaborn as sns
sns.set(style='whitegrid')

np.set_printoptions(suppress=True, precision=7, linewidth=150)

import math

def eta(data, unit='natural'): #function to calculate entropy, not used in the study
    base = {
        'shannon' : 2.,
        'natural' : math.exp(1),
        'hartley' : 10.
    }

    if len(data) <= 1:
        return 0
    ent = []
    for i in data:
        r = [(p * math.log(p, base['natural'])) for p in i if p > 0.]
        ent.append(sum(r))

    return ent
 
#Combine all the probabilities extracted prior
file1 = "Cities Link Lengths Probabilities1"

data = pd.read_csv(file1 + '.csv', header=0)
data = data.fillna(0)

data = data.set_index(data.Cities.values)
data = data.drop(['Cities'], axis = 1)
#data1 = data.as_matrix().astype("float32", copy = False)
#data1 = data1.iloc[:,:].div(data1.Max, axis=0)



# Performing PCA analysis
X = data
city = X.index.values

degdis = X.iloc[:,0:16].values
linkdis = X.iloc[:,16:26].values
angdis = X.iloc[:,26:].values

mean_deg = np.true_divide(degdis.sum(1),(degdis!=0).sum(1))
mean_link = np.true_divide(linkdis.sum(1),(linkdis!=0).sum(1))
mean_ang = np.true_divide(angdis.sum(1),(angdis!=0).sum(1))

var_deg=[]
for p,i in enumerate(degdis):
    place = np.nonzero(i)
    var1 = [(mean_deg[p] - i[j]) ** 2 for j in place[0]]
    var_deg.append(sum(var1))

var_link=[]
for p,i in enumerate(linkdis):
    place = np.nonzero(i)
    var1 = [(mean_link[p] - i[j]) ** 2 for j in place[0]]
    var_link.append(sum(var1))
    
var_ang=[]
for p,i in enumerate(angdis):
    place = np.nonzero(i)
    var1 = [(mean_ang[p] - i[j]) ** 2 for j in place[0]]
    var_ang.append(sum(var1))
    
    
ent_deg = np.array(eta(degdis))
ent_link = np.array(eta(linkdis))
ent_ang = np.array(eta(angdis))
    

# Dimentionality reduction ISOmap
iso_ = Isomap(n_neighbors=5, n_components=2)
X_proj = iso_.fit_transform(X)

    
#Cluster analysis
#KMeans - Define number of clusters
clusters = 5

#Define which KMeans algorithm to use and fit it
Y_Kmeans = KMeans(n_clusters = clusters)
Y_Kmeans.fit(X_proj)
Y_Kmeans_labels = Y_Kmeans.labels_
#clus = np.unique(Y_Kmeans_labels)

Y_Kmeans_silhouette = metrics.silhouette_score(X_proj, Y_Kmeans_labels, metric='sqeuclidean')
print("Silhouette for Kmeans: {0}".format(Y_Kmeans_silhouette))
print("Results for Kmeans: {0}".format(Y_Kmeans_labels))

fig,ax = plt.subplots()
colormap = np.array(['black', 'blue', 'red', 'orange', 'green', 'brown', 'yellow', 'magenta', 'cyan']) #Define colors to use in graph - could use c=Y but colors are too similar when only 2-3 clusters
ax.scatter(X_proj[:,0], X_proj[:,1], c=colormap[Y_Kmeans_labels])
#plt.savefig('kmeans_5.png', dpi = 600)
plt.show()
