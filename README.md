This repository contains the data extraction and clustering analysis codes for the study titled "A Geometric Classification of World Urban Road Networks" published in Urban Science Journal at https://doi.org/10.3390/urbansci6010011.

# Data
The data used in this study is downloaded from the [CSUN](http://csun.uic.edu/datasets.html) website under Urban Road Network Data. The data contains all the necessary information to recreate the road networks of 80 cities worldwide. You need to unzip the data individually and store the .csv files in one folder. I also share the final data I used in the data folder. If you are using the data in the data folder then you can only use the kmeans_clustering.py file. The other three python files, angle_estimation.py, Link_length_distribution.py, and degree_distribution.py are used to extract the probabilities, which is the file shared in data folder.

Make sure when you run the three .py files, the folder should only contains the (80) unziped csv files of the cities. Because each time you generate a extra csv file when you run those three .py files. 

# Code
*degree_distribution.py* - to extract the degree distribution of all 80 cities.<br>
*angle_estimation.py* - to extract the intersection anlge distribution of all 80 cities.<br>
*Link_length_distribution.py* - to extract the distribution of link lengths (road segments, i.e. distance between two intersections) of all 80 cities.

#Packages
NetworkX<br>
Seaborn<br>
pandas<br>
numpy<br>
scikit-learn<br>
math<br>
glob<br>

