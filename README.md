# cse258_project
CSE 258 final project @ UCSD

### Overall
In this project, we use [Reddit submissions](http://snap.stanford.edu/data/web-Reddit.html) as our dataset. We are going to do some predictions and analysis on that. 

### Group memebers
- [FeiHua Fang](https://github.com/feihuaya)
- [JiaQi He](https://github.com/JiaqiHe)
- [JiaZhuo Qin](https://github.com/pooh2713)
- [Yifan Qin](https://github.com/IvanQin/)

### Task distribution

**任务总述：（菲华）**

- 预测 number_of_comments, number_of_upvotes,number_of_downvotes 通过如下regression：
predict = f(title information, user information, time,...)

**细节：（佳琪，嘉卓）**
- 分析title information
-  对title进行聚类，分析出label
- 将title所属的subreddit作为title information的一个feature
- 对title进行降维，得到一系列关键词以作为 “is word xxx in title?” 的二进制feature
- ...(待续)

**分析user information （一帆）**
 
- 对user的权重值分析（是否为大V?) 并作为一个feature (用户分组)
-对user进行聚类分析出user_label
-...(待续)