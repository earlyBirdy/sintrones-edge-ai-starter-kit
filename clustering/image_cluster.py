# image_cluster.py - Embedding + clustering for image RCA
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np

def cluster_features(features, n_clusters=3):
    pca = PCA(n_components=10)
    reduced = pca.fit_transform(features)
    km = KMeans(n_clusters=n_clusters)
    labels = km.fit_predict(reduced)
    return labels