from utils import *
import pandas as pd
import pickle
import os

classes_dir = 'data'
data_dir = 'predict_data'


if __name__ == '__main__':
    # 加载类别和问句
    classes = [line.strip() for line in open(os.path.join(classes_dir, 'class.txt'), 'r', encoding="utf-8").readlines()]
    sentence_csv = pd.read_csv(os.path.join(data_dir, 'question.csv'), sep='\t', names=['title'])
    sentences = sentence_csv['title'].tolist()

    # 加载模型
    if os.path.exists('MultinomialNB.pkl'):
        with open('MultinomialNB.pkl', 'rb') as f:
            model = pickle.load(f)
    else:
        raise Exception("Please run main.py first!")

    # 预测
    x_query = qes2wb(sentences)
    p_query = model.predict(x_query)
    results = [classes[int(p)] for p in p_query]

    # 保存结果
    dataframe = pd.DataFrame({'title': sentences, 'classes': results})
    dataframe.to_csv(os.path.join(data_dir, 'result.csv'), index=False, sep=',')


