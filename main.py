from utils import *
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import numpy as np
from termcolor import colored
import matplotlib.pyplot as plt
import seaborn as sns


def qes2wb(questions):
    # 加载vocab
    vocab = [line.strip() for line in open('data/vocab.txt', 'r', encoding="utf-8").readlines()]

    # 问句，槽值替换后， 分词，转换为词袋向量
    vecs = []
    load_jieba()
    for question in questions:
        sen = synonym_sub(question)
        words = list(jieba.cut(sen, cut_all=False))
        vec = [words.count(v) for v in vocab]
        vecs.append(vec)
    return vecs


if __name__ == '__main__':
    # 加载训练集 测试集 类别
    q_train, y_train = open_data('data/train.txt')
    q_test, y_test = open_data('data/test.txt')
    q_dev, y_dev = open_data('data/dev.txt')
    q_test = q_test + q_dev
    y_test = y_test + y_dev

    classes = [line.strip() for line in open('data/class.txt', 'r', encoding="utf-8").readlines()]

    # 转为词袋模型
    x_train = qes2wb(q_train)
    x_test = qes2wb(q_test)

    # 建模
    model = MultinomialNB()
    model.fit(x_train, y_train)
    # 测试
    p_test = model.predict(x_test)
    y_test = np.array(y_test)
    p_test = np.array(p_test)

    # 输出模型测试结果
    # print(metrics.classification_report(y_test, p_test, target_names=classes))
    for i, c in enumerate(classes):
        print("%d: %s" % (i, c), end='\t')
    print('\n')
    print(metrics.classification_report(y_test, p_test))

    # 输出错误
    errors = []
    for i in range(len(y_test)):
        if y_test[i] != p_test[i]:
            errors.append((y_test[i], q_test[i], p_test[i]))
    print('---Bad Cases---')
    for y, q, p in sorted(errors):
        row = [classes[int(y)], q, classes[int(p)]]
        print('Truth: %-20s Query: %-30s Predict: %-20s' % (classes[int(y)], q, classes[int(p)]))

    # 混淆矩阵
    # 用来正常显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 用来正常显示负号
    plt.rcParams['axes.unicode_minus'] = False
    # 计算混淆矩阵
    confusion = metrics.confusion_matrix(y_test, p_test)
    plt.clf()
    plt.title('分类混淆矩阵')
    sns.heatmap(confusion, square=True, annot=True, fmt='d', cbar=False,
                xticklabels=classes,
                yticklabels=classes,
                linewidths=0.1, cmap='YlGnBu_r')
    plt.ylabel('观测')
    plt.xlabel('预测')
    plt.xticks(rotation=-13)
    plt.savefig('分类混淆矩阵.png', dpi=100)

    # 预测
    while True:
        query = input(colored('请咨询：', 'green'))
        x_query = qes2wb([query])
        p_query = model.predict(x_query)
        print('意图： ' + classes[int(p_query[0])])



