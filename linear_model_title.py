# load data
import csv

data = []

label = ['image_id','unixtime','rawtime','title','total_votes','reddit_id','number_of_upvotes',\
'subreddit','number_of_downvotes','localtime','score','number_of_comments','username',\
'undefined1','undefined2', 'undefined3']

with open('submissions.csv', newline='', encoding='utf-8') as csvfile:
    csvReader = csv.reader(csvfile)
    for row in csvReader:
        if row[0] == '#image_id':
            continue
        d = {}
        for i,elem in enumerate(row):
            d[label[i]] = elem
        data.append(d)

# word count (title)
from collections import defaultdict
import string
wordCount = defaultdict(int)
punctuation = set(string.punctuation)

for d in data:
    r = ''.join([c for c in d['title'].lower() if not c in punctuation])
    for w in r.split():
        wordCount[w] += 1

print(len(wordCount))

remove English stopwords
from nltk.corpus import stopwords
for w in stopwords.words("english"):
    if w in wordCount:
        wordCount.pop(w)

print(len(wordCount))
counts = [(wordCount[w], w) for w in wordCount]
counts.sort()
counts.reverse()

# output top 50 frequent words in title
f = open('top50_words_in_title.txt','w')

for x in range(50):
    f.write(counts[x][1] + ': ' + str(counts[x][0]) + '\n')

f.close()

# take top 1000 words to be our targets
words = [x[1] for x in counts[:1000]]
wordId = dict(zip(words, range(len(words))))
wordSet = set(words)

def feature(datum):
    feat = [0]*len(words)
    r = ''.join([c for c in datum['title'].lower() if not c in punctuation])
    for w in r.split():
        if w in words:
            feat[wordId[w]] += 1
    feat.append(1) #offset
    return feat

X = [feature(d) for d in data]
y_upvotes = [d['number_of_upvotes'] for d in data]
y_downvotes = [d['number_of_downvotes'] for d in data]
y_score = [d['score'] for d in data]
data = []

from sklearn import linear_model
clf = linear_model.Ridge(1.0, fit_intercept=False)
clf.fit(X[:5000], y_upvotes[:5000]) # when using all set of data, MEMORY ERROR!!!
theta = clf.coef_

#store word-theta pairs
f = open('theta.txt','w')

for x in range(len(theta)):
    try:
        f.write(words[x] + ': ' + str(theta[x]) + '\n')
    except Exception as e:
        pass

f.close()
