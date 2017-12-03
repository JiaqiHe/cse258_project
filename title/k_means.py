import csv
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation,TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.preprocessing import MaxAbsScaler
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
import pandas as pd
import random
import numpy as np
import operator

def get_titles(path):
    label = ['image_id','unixtime','rawtime','title','total_votes','reddit_id','number_of_upvotes',\
    'subreddit','number_of_downvotes','localtime','score','number_of_comments','username',\
    'undefined1','undefined2', 'undefined3']
    data = []
    with open('submissions.csv', newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile)
        for row in csvReader:
            if row[0] == '#image_id':
                continue
            d = {}
            for i,elem in enumerate(row):
                if i == 0 or i == 3 or i == 6 or i == 8 or i == 7 or i == 10: #title, number_of_upvotes, number_of_downvotes, score
                    d[label[i]] = elem
            data.append(d)
    return data

def tokenize(text):
    tokens = tokenizer.tokenize(text)
    return [stemmer.stem(t) for t in tokens]

def get_tf(data, use_idf, max_df=1.0, min_df=1, ngram_range=(1,2)):
    if use_idf:
        m = TfidfVectorizer(max_df=max_df, min_df=min_df, stop_words='english', ngram_range=ngram_range, tokenizer=tokenize)
    else:
        m = CountVectorizer(max_df=max_df, min_df=min_df, stop_words='english', ngram_range=ngram_range, tokenizer=tokenize)
    d = m.fit_transform(data)
    return m, d

def get_kmeans(data, k, scale=True):
    if scale:
        s = MaxAbsScaler()
        data = s.fit_transform(data)
    m = KMeans(n_clusters=k).fit(data)
    d = m.predict(data)
    return m, d

def get_svd(data, components):
    svd = TruncatedSVD(n_components=components).fit(data)
    data_processed = svd.transform(data)
    return svd, data_processed

def supress_data(size):
    supressed_data = []
    counter = {}
    for x in range(n_topics_):
        counter[x] = 0
    while len(supressed_data) < size:
        a = int(random.random() * len(data))
        if counter[kmean_d[a]] < size/n_topics_:
            supressed_data.append(a)
            counter[kmean_d[a]] += 1
    random_data = np.array(svd_m)[supressed_data,:]
    supressed_results = np.array(kmean_d)[supressed_data]
    return random_data,supressed_results

def get_tsne(data, components, perplexity):
    tsne = TSNE(n_components=components, perplexity=perplexity, n_iter=1000)
    low_data = tsne.fit_transform(data)
    return tsne, low_data

def plot_scatter_2d(x, y, c, title):
    df = pd.DataFrame({'x': x, 'y': y, 'c': c})
    l = len(np.unique(c))
    ax = plt.subplot(111)
    colors = cm.rainbow(np.linspace(0, 1, l))
    for c in range(0,l):
        qq = df[df['c']==c]
        ax.scatter(qq['x'], qq['y'],c=colors[c], label=c)
    plt.legend(loc='upper left', numpoints=1, ncol=3, fontsize=8, title='Topic/Cluster')
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_title(title)
    plt.show()

def get_top_10_subreddits(kmean_d):
    subreddits = [x['subreddit'] for x in data]
    pool = set([]) # all subreddits
    for elem in subreddits:
        pool.add(elem)
    pool = list(pool)
    sub_dict = {} # indexing all subreddits
    for i,elem in enumerate(pool):
        sub_dict[elem] = i
    sum_dict = {}
    for i,elem in enumerate(pool):
        sum_dict[elem] = 0
    for elem in subreddits:
        sum_dict[elem] += 1
    sorted_dict = sorted(sum_dict.items(), key=operator.itemgetter(1), reverse=True)[:10]
    top_10 = [x for (x,y) in sorted_dict]
    cluster_count = [0] * n_topics_
    for elem in kmean_d:
        cluster_count[elem] += 1
    matrix = [[0]* len(pool) for _ in range(n_topics_)]
    for i,elem in enumerate(kmean_d):
        row = elem
        col = sub_dict[subreddits[i]]
        matrix[row][col] += 1
    top_10_index = [sub_dict[x] for x in top_10]
    top_10_matrix = np.array(matrix)[:, top_10_index]
    denominator = []
    for s in top_10:
        denominator.append(1/sum_dict[s])
    denominator = np.array(denominator)
    d = np.diag(denominator)
    top_10_ratio = np.dot(top_10_matrix, d)
    return top_10,top_10_ratio

def plot_bar_distribution(top_10, top_10_ratio):
    y_pos = np.array(top_10)
    performance = top_10_ratio.tolist()
    colors = cm.rainbow(np.linspace(0, 1, 10))
    base = []
    for i in range(10):
        if i == 0:
            plt.bar(y_pos, performance[0], align='center', alpha=0.8, color=colors[i])
            base = performance[0]
        else:
            plt.bar(y_pos, performance[i], bottom=base, align='center', alpha=0.8, color=colors[i])
            for j,b in enumerate(base):
                base[j] = base[j] + performance[i][j]
    plt.xticks(y_pos, top_10, rotation=45)
    plt.ylabel('Ratio')
    plt.title('Subreddit Distribution in 10 Clusters')
    plt.show()

# read data related to title
data = get_titles('submissions.csv')
titles = [x['title'] for x in data]
scores = [int(x['score']) for x in data]
images = [x['image_id'] for x in data]

# compute tfidf
stemmer = SnowballStemmer("english")
tokenizer = RegexpTokenizer("[a-z']+")
tfidf_m, tfidf_d = get_tf(titles, use_idf=True, max_df=0.90, min_df=10)

# k-means clustering
n_topics_ = 10
kmean_m, kmean_d = get_kmeans(tfidf_d, n_topics_, scale=True)
cluster_centers = kmean_m.cluster_centers_

# SVD(LSA)
svd_v, svd_m = get_svd(tfidf_d, 200) # For LSA, a value of 100 is recommended.
variances = svd_v.explained_variance_ # each title's variance is roughly 0.006, which is acceptable
svd_center_v, svd_center_m = get_svd(cluster_centers, 100)

# save file
mat = np.matrix(kmean_d)
with open('kmean_cluster_10.txt','wb') as f:
    for line in mat:
        np.savetxt(f, line, fmt='%d')

mat = np.matrix(svd_m)
with open('svd_tfidf_100.txt','wb') as f:
    for line in mat:
        np.savetxt(f, line, fmt='%f')

# plot k_means clustering results
supressed_data, supressed_results = supress_data(200)
tnse_v, tsne_m = get_tsne(supressed_data, 2, 25)
plot_scatter_2d(tsne_m[:,0], tsne_m[:,1], supressed_results, 'KMeans Clustering of Titles using TFIDF (t-SNE Plot)')

# evalutate the k-means clustering in terms of subreddits
top_10, top_10_ratio = get_top_10_subreddits(kmean_d)
plot_bar_distribution(top_10, top_10_ratio)

# train a Neural Network to predict
X_train, X_test, y_train, y_test = train_test_split(svd_m, scores, test_size=0.5)
from sklearn.neural_network import MLPRegressor
MLP_model = MLPRegressor(hidden_layer_sizes=(30,20,10))
trained_MLP = MLP_model.fit(X_train, y_train)

# test set evaluation
predicted = trained_MLP.predict(X_test)
MSE = 0
for i in range(len(y_test)):
    MSE += (predicted[i] - y_test[i])**2

MSE = MSE/len(y_test)

print(MSE)
