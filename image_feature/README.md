##简介

这个文件夹下面包含了与image有关的各种信息

训练集采用'submission.csv'中的前1/3的数据。

- *each_image_stat.json*: 一个json dict，包含了训练集中每一张图片的数据（以图片id归类,key是id），数据包括图片被发的次数，平均upvote数，平均downvote数，upvote标准差，downvote标准差，comment平均数，comment标准差
- *overall_stat.json*: 一个json dict，包含对于整个训练集的数据的的分析，数据包括，平均upvote数，平均downvote数，upvote标准差，downvote标准差，comment平均数，comment标准差
- *image_vec_number_of_comments.json*: **IMPORTANT** 当预测数据为comments数时，image对应的向量，两维向量，第一维为1，第二维为标准化后的image **upvotes**数. 如果测试集中发现图片id不在其中，则对应向量为[0,0]
- *image_vec_total_votes.json*: **IMPORTANT** 当预测数据为total vote数时，image对应的向量，两维向量，第一维为1，第二维为标准化后的图片收到的comments数. 如果测试集中用户不在其中，则对应向量为[0,0]

注意：标准化为 $f(x)$. 其中 $\mu$是平均数，$\sigma$是标准差，即方差的平方根
$$f(x) = (x-\mu)/\sigma$$

注意，有**IMPORTANT**标志的文件需要在训练的时候被读取！@[FeiHua Fang](https://github.com/feihuaya)