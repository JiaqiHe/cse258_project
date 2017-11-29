from load_data import *
from collections import defaultdict
import json
import numpy as np
import matplotlib.pyplot as plt


def username():
    data = load_data()
    data = data[:len(data)/3]
    user_post_num = defaultdict(int)
    user_down_vote = defaultdict(int)
    user_up_vote = defaultdict(int)
    user_vote = defaultdict(int)
    user_comment_num = defaultdict(int)

    for record in data:
        user_name = record.get('username')
        user_post_num[user_name] += 1
        user_comment_num[user_name] += int(record.get('number_of_comments'))
        user_down_vote[user_name] += int(record.get('number_of_downvotes'))
        user_up_vote[user_name] += int(record.get('number_of_upvotes'))
        user_vote[user_name] += int(record.get('total_votes'))

    post_num_list = sorted(user_post_num.items(),key=lambda item:item[1], reverse=True)
    # max_post = max(post_num_list, key=lambda item:item[1])
    # min_post = min(post_num_list, key=lambda item:item[1])
    avg_post_num = np.mean(user_post_num.values())
    median_post_num = np.median(user_post_num.values())

    def user_profile(user_name):
        profile = {
            'username':user_name,
            'num_of_post':user_post_num[user_name],
            'avg_comments':float(user_comment_num[user_name])/user_post_num[user_name],
            'avg_downvotes':float(user_down_vote[user_name])/user_post_num[user_name],
            'avg_upvotes':float(user_up_vote[user_name])/user_post_num[user_name],
            'avg_votes':float(user_vote[user_name])/user_post_num[user_name]
        }
        return profile

    all_user_profile = [user_profile(user) for user in user_post_num.keys()]

    result = {
        'top_10':[user_profile(ele[0]) for ele in post_num_list[:10]],
        'bottom_10':[user_profile(ele[0]) for ele in post_num_list[-10:]],
        'avg_post_num':avg_post_num,
        'median_post_num':median_post_num
    }

    with open('all_user_profile.json','w') as f:
        json.dump(all_user_profile,f)

    with open('user_post_stat.json','w') as f:
        json.dump(result,f)

    with open('all_user_post_num','w') as f:
        json.dump(dict(user_post_num),f)

def plot():
    with open('all_user_profile.json','r') as f:
        all_user_profile = json.load(f)
    post_list = []
    comment_list = []
    votes_list = []
    for user in all_user_profile:
        post_list.append(user.get('num_of_post'))
        comment_list.append(user.get('avg_comments'))
        votes_list.append(user.get('avg_votes'))
        
    plt.scatter(x=post_list,y=votes_list,alpha=0.5,color='r',marker='+')
    #plt.scatter(x=comment_list,y=votes_list,alpha=0.5,color='b',marker='o')
    plt.legend(['post_num_vs_votes'])
    plt.savefig('post_num_vs_votes.png',format='png')

if __name__ == '__main__':
    #username()
    plot()


    
    

