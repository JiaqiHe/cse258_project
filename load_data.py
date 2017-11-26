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

print(len(data))
