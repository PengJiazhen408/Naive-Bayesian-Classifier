# 朴素贝叶斯意图分类器

## 分类流程

问句-->槽值替换-->分词-->根据vocab.txt 生成特征向量 --> 模型预测生成标签 --> 标签转换为类别（中文）

如：
问句|槽值替换后|分词后|one-hot 特征词向量|标签|类别|
--|--|--|--|--|--
糖尿病可以吃草莓吗 |[DISEASE]可以吃[FOOD]吗 |[/DISEASE/]/可以/吃/[/FOOD/]/吗 |[1, 0, 0, 0, 0, 0, 0, 0, 1 ....] |2 |饮食  
胰岛素的副作用 |[DRUG]的副作用 |[/DRUG/]/的/副作用 |[0, 0, 0, 1, 0, 0, 0, 0, 0 ....] |5 |用药情况  
糖尿病吃什么药 |[DISEASE]吃什么药 |[/DISEASE/]/吃什么/药 |[1, 0, 0, 0, 0, 0, 0, 0, 0 ....] |3 |用药治疗  
糖尿病高血糖怎么治 |[DISEASE][DISEASE]怎么治 |[/DISEASE/]/[/DISEASE/]/怎么/治 |[2, 0, 0, 0, 0, 0, 0, 1, 0 ....] |0 |治疗  


## 字典(dict)构造：用于jieba分词和槽值替换

### 类别

文件名|内容|例子
--|--|--
category.txt| 食物集合名|如：海鲜，早餐等  
check.txt| 检查项目名|如：测血糖，抽血等  
department.txt| 科室名| 如：内分泌科，儿科等  
disease.txt|疾病名|如：糖尿病，一型糖尿病等  
drug.txt|药物名|如：胰岛素，二甲双胍等  
food.txt|食物和水果|如：苹果，绿豆等  
style.txt|生活方式名|如：运动，跑步，洗澡等  
symptom.txt|症状名|如：头疼，腹泻等  

### 格式

1. 一个词一行

2. 每个文件第一个词是类别名，如[DISEASE],[DRUG] 用于槽值替换


## 数据集构建

1. 训练集(train_data.txt)： 各类50例

2. 测试集(test_data.txt)：  各类5或10例

3. 格式：问句	类别（中文）

4. 注意事项：每个类别要注意包含一些关键词，各个关键词数量均衡，搭配均衡

5. 关键词参考：https://github.com/liuhuanyong/QASystemOnMedicalKG/blob/master/question_classifier.py

## 算法流程

### data_pro.py: 由train_data.txt, test_data.txt生成 class.txt, train.txt, test.txt

1. 加载原始数据集(train_data.txt, test_data.txt)

2. 对类别列表去重，生成class.txt

3. 将每个问句的类别（中文）转换为标签（数字）

4. 打乱数据集，保存在train.txt, test.txt

### extract.py: 由train.txt, stopwords.txt 生成 特征列表 vocab.txt

1. 加载train.txt，提取其所有问句；加载stopwords.txt，生成停用词表

2. 对问句槽值替换，分词，统计各个词词频，按照词频从大到小对词语排序，生成词语列表

3. 词语列表除去停用词表中的词语；除去长度为1的词；加上对分类有用的长度为1的词，如 ‘吃’，‘药’，‘治’等

4. 将词语列表（也即特征列表）保存在vocab.txt

5. 停用词表构造：人工筛选出vocab.txt中对分类无意义的词，加入到stopwords.txt中

6. 参考资料：https://blog.csdn.net/zcmlimi/article/details/90671005

### main.py: 模型训练，测试，预测

1. 加载train.txt, test.txt, class.txt, vocab.txt

2. 模型训练：训练集问句-->槽值替换-->分词-->根据vocab.txt 生成特征向量 -->  (特征向量，标签) 作为模型输入 --> 训练模型

3. 模型测试：测试集问句-->槽值替换-->分词-->根据vocab.txt 生成特征向量 -->  模型预测生成预测标签 --> 预测标签与真实标签比对，计算混淆矩阵与评价指标

4. 参考资料：https://www.cnblogs.com/boom-meal/p/12505174.html ,  https://blog.csdn.net/XianxinMao/article/details/70556031

### 关键函数：槽值替换 输入：问句，输出：槽值替换后的句子

1. 加载dict中的文件，生成同义词表的字典，key：每个词，value：该词所在文件第一个词

2. 问句分词

3. 遍历问句的每个词，用同义词表进行替换

4. 返回替换后的句子

5. 参考资料：https://xiaoshuwen.blog.csdn.net/article/details/101451408
