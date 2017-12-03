# title manipulation
* our work is to analyse the three models to get features:
    1) popular word dictionary by tf
    2) k-means to get k features (k clusters)
    3) LDA to get N features (N topics)



## popular word dictionary with tf to predict score
* related file : linear model 2.ipynb
* use the words with term frequency over 500 to form a dictionary where there are 157 terms.
* use the 158 features to predict score. With R^2 equals 0.06, model is bad.
## k-means Process
* from csv file, read relavant data including 'title', 'number_of_upvotes', 'number_of_downvotes', 'score'
* compute [tfidf](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) vector for each title (the dimension is roughly 4600 for each vector)
* take as input the tfidf matrix, use [k-means](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html) clustering algorithm to divide data into 10 clusters
* conduct dimensionality reduction using [truncated SVD (aka LSA)](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html) to reduce the dimension of tfidf vectors from 4600 to 100
* compute [TSNE](http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html) so as to transform high-dimensional vectors into 2-dimensional vectors for the purpose of displaying the clustering results
* plot k_means clustering results using 2-dimensional vectors and the results of k-means
![alt text](https://github.com/IvanQin/cse258_project/blob/master/title/k-means-10-cluster(figure%201).png)
* train a [Neural Network](http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html#sklearn.neural_network.MLPRegressor) to predict socre (take as input the supressed tfidf vectors)

## LDA
* related files : topics_....txt F_...json
* base on the belief network and em algorith to get the latent topic distribution over N topics of a particular document.
* topics_... shows the topics learned from data under different N and different method to clean data.
* F_... is the features get from the specific model which uses 10/20/50 topics and all under stem + tfidf data cleaning method.

## Future work & ideas
* 可以试试看用k-means得到的类别信息作为feature，或者，拼接tfidf和k-means得到的类别信息，组成刻画title的feature，训练模型。
