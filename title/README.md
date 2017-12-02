# title manipulation

## Process
* from csv file, read relavant data including 'title', 'number_of_upvotes', 'number_of_downvotes', 'score'
* compute [tfidf](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) vector for each title (the dimension is roughly 4600 for each vector)
* take as input the tfidf matrix, use [k-means](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html) clustering algorithm to divide data into 10 clusters
* conduct dimensionality reduction using [truncated SVD (aka LSA)](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html) to reduce the dimension of tfidf vectors from 4600 to 100
* compute [TSNE](http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html) so as to transform high-dimensional vectors into 2-dimensional vectors for the purpose of displaying the clustering results
* plot k_means clustering results using 2-dimensional vectors and the results of k-means
* train a [Neural Network](http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html#sklearn.neural_network.MLPRegressor) to predict socre (take as input the supressed tfidf vectors)

## Future work & ideas
* 可以试试看用k-means得到的类别信息作为feature，或者，拼接tfidf和k-means得到的类别信息，组成刻画title的feature，训练模型。
