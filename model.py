import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from copy import deepcopy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
"""
file used to perform clustering
"""


class model:
    def __init__(self, K):
        self.filename = os.getcwd()+"\\Data\\merged.csv"
        self.db = pd.read_csv(self.filename)
        self.le = LabelEncoder()
        self.vectorizer = TfidfVectorizer(stop_words ="english")
        names =  self.le.fit_transform(self.db["Names"])

        genres = self.le.fit_transform(self.db["Genre"])
        studios =   self.le.fit_transform(self.db["Studios"])
        self.X = np.array(list(zip( names, genres,studios,self.db["rate"],
                          self.db["Episodes"])))
        self.numCent = K
        
    def scatter_data(self,x,y):
        C = self.create_cent()
        Cx,Cy = zip(*C)
        plt.scatter(self.db[x],self.db[y], c ='b', s = 18)
        plt.scatter(Cx,Cy ,marker ="+", c ='r', s =160)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()


    def predict(self,toPredict):
        kMeans = KMeans(n_clusters = self.numCent)
        kMeans = kMeans.fit(self.X)
        toPredict = self.le.fit_transform(toPredict)
        prediction = kMeans.predict([toPredict])
        val = self.db[kMeans.labels_ == prediction][:5]
        return val

    def eculid_dist(self, a, b, ax=1):
        return np.linalg.norm(a-b,axis = ax)

    def do_Scki(self):
        kMeans = KMeans(n_clusters = self.numCent)
        kMeans = kMeans.fit(self.X)
        cent = kMeans.cluster_centers_
        c = ['b','y','r','g','c','m']
        labels = kMeans.predict(self.X)
        color = [c[i] for i in labels]
        plt.scatter(self.db["Episodes"],self.db["rate"], c = color, s= 18)
        plt.scatter(cent[:,0], cent[:,1], marker = "+", s =100, c = 'black')
        plt.show()

    def do_KMeans_Clusetring(self):
        C = self.create_cent()
        C_prev = np.zeros(C.shape)
        clust = np.zeros(len(self.X))
        dist = self.eculid_dist(C,C_prev)
        while dist.any() != 0:
            for i in range(len(self.X)):
                dist = self.eculid_dist(self.X[i],C)
                cluster = np.argmin(dist)
                clust[i]= cluster
            C_prev = deepcopy(C)

            for i in range(self.numCent):
                points = [self.X[j] for j in range(len(self.X)) if clust[j]==i]
                if len(points) != 0:
                    C[i] = np.mean(points, axis = 0)
            dist = self.eculid_dist(C,C_prev)
        colors = ['b','y','r','g','c','m']

        for i in range(self.numCent):
            points = np.array([self.X[j] for j in range(len(self.X)) if clust[j] == i])
            if len(points) >0:
                plt.scatter(points[:,0], points[:,1], s = 10, c = colors[i])
            else:
                print("Please regen centroids again")
            plt.scatter(points[:, 0], points[:, 1],s = 10, c = colors[i])
            plt.scatter(C[:,0], C[:,1], marker="+", c='r', s=160)
        plt.show()

    def create_cent(self):
        Cx = np.random.randint(np.min(self.X[:,0]),np.max(self.X[:,0]), size = self.numCent)
        Cy = np.random.randint(np.min(self.X[:,1]),np.max(self.X[:,1]), size = self.numCent)
        C = np.array(list(zip(Cx,Cy)), dtype =np.float64)
        return C
