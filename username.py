from load_data import *
from collections import defaultdict
import json
import numpy as np
import matplotlib.pyplot as plt
import os
USER_DIR = 'user_feature'
PIC_DIR = 'pic'
def _load_each_user_profile():
    with open(os.path.join(USER_DIR,'each_user_profile.json'),'r') as f:
        each_user_profile = json.load(f)
    return each_user_profile

def _load_user_stat():
    with open(os.path.join(USER_DIR,'user_stat.json'),'r') as f:
        user_stat = json.load(f)
    return user_stat

def gen_feature(target):
    """
    @param target: target is the prediction feature. It should be either 'number_of_comments' or 'total_votes'
    """
    user_vec = {}
    user_stat = _load_user_stat()
    user_profile = _load_each_user_profile()
    total_avg_comments = user_stat['avg_comments']
    total_std_comments = user_stat['std_comments']
    total_avg_votes = user_stat['avg_votes']
    total_std_votes = user_stat['std_votes']
    
    for user in user_profile:
        user_name = user.get('username')
        avg_comments = user.get('avg_comments')
        # avg_downvotes = user.get('avg_downvotes')
        # avg_upvotes = user.get('avg_upvotes')
        avg_votes = user.get('avg_votes')
        if target == "number_of_comments":        
            user_vec[user_name] = [1,float(avg_votes-total_avg_votes)/total_std_votes]
        elif target == 'total_votes': # target is number of votes
            user_vec[user_name] = [1,float(avg_comments-total_avg_comments)/total_std_comments]
        else:
            print '{0} is undefined.'.format(target)
            break

    with open(os.path.join(USER_DIR,'user_vec_'+target+'.json'),'w') as f:
        json.dump(user_vec,f)

def _username():
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
    std_post_num = np.std(user_post_num.values())

    avg_votes = np.mean(user_vote.values())
    std_votes = np.std(user_vote.values())

    avg_comments = np.mean(user_comment_num.values())
    std_comments = np.std(user_comment_num.values())

    def user_profile(user_name):
        profile = {
            'username':user_name,
            'num_of_post':user_post_num[user_name],
            'avg_comments':float(user_comment_num[user_name])/user_post_num[user_name],
            'avg_downvotes':float(user_down_vote[user_name])/user_post_num[user_name],
            'avg_upvotes':float(user_up_vote[user_name])/user_post_num[user_name],
            'avg_votes':float(user_vote[user_name])/user_post_num[user_name],
        }
        return profile

    each_user_profile = [user_profile(user) for user in user_post_num.keys()]

    result = {
        'top_10':[user_profile(ele[0]) for ele in post_num_list[:10]],
        'bottom_10':[user_profile(ele[0]) for ele in post_num_list[-10:]],
        'avg_post_num':avg_post_num,
        'median_post_num':median_post_num,
        'avg_votes':avg_votes,
        'std_votes':std_votes,
        'avg_comments':avg_comments,
        'std_comments':std_comments
    }

    with open(os.path.join(USER_DIR,'each_user_profile.json'),'w') as f:
        json.dump(each_user_profile,f)

    with open(os.path.join(USER_DIR,'user_stat.json'),'w') as f:
        json.dump(result,f)

    with open(os.path.join(USER_DIR,'all_user_post_num.json'),'w') as f:
        json.dump(dict(user_post_num),f)

def _plot():
    each_user_profile = _load_each_user_profile()
    post_list = []
    comment_list = []
    votes_list = []
    for user in each_user_profile:
        post_list.append(user.get('num_of_post'))
        comment_list.append(user.get('avg_comments'))
        votes_list.append(user.get('avg_votes'))
        
    plt.scatter(x=post_list,y=votes_list,alpha=0.5,color='r',marker='+')
    #plt.scatter(x=comment_list,y=votes_list,alpha=0.5,color='b',marker='o')
    plt.legend(['post_num_vs_votes'])
    plt.savefig(os.path.join(PIC_DIR,'post_num_vs_votes.png'),format='png')

if __name__ == '__main__':
    #_username()
    #_plot()
    gen_feature("number_of_comments")
    gen_feature("total_votes")


    
    

