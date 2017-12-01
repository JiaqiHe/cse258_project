##简介
这个文件夹下面包含了与user有关的各种信息

训练集采用'submission.csv'中的前1/3的数据。

- *all_user_post_num.json*: 一个json文件，包含了训练集中所有的user的发布的帖子数
- *each_user_profile.json*: 一个json list，每一个list包含了对于训练集中的一个user的数据分析，包括TA发的帖子数，平均被评论数，平均被vote数等
- *user_stat.json*: 对于整个训练集的统计数据，包括top10和bottom10发布帖子最多的用户信息，以及对整个训练集的vote平均数，vote标准差，comment平均数，comment标准差
- *user_vec_number_of_comments.json*: **IMPORTANT** 当预测数据为comments数时，user对应的向量，两维向量，第一维为1，第二维为标准化后的用户votes数. 如果测试集中用户不在其中，则对应向量为[0,0]
- *user_vec_total_votes.json*: **IMPORTANT** 当预测数据为votes数时，uesr对应的向量，两维向量，第一维为1，第二维为标准化后的用户comment数. 如果测试集中用户不在其中，则对应向量为[0,0]

注意，有**IMPORTANT**标志的文件需要在训练的时候被读取！@[FeiHua Fang](https://github.com/feihuaya)