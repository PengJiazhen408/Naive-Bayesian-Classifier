from utils import *


if __name__ == '__main__':
    questions, _ = open_data('data/train.txt')

    load_jieba()
    # 槽值替换
    for i in range(len(questions)):
        questions[i] = synonym_sub(questions[i])

    # 分词
    words = jieba.cut("\n".join(questions), cut_all=False)
    print(words)

    # 统计词频
    word_count = {}
    stopwords = [line.strip() for line in open("data_orig/stopwords.txt", 'r', encoding="utf-8").readlines()]
    for word in words:
        if word not in stopwords:
            if len(word) == 1:
                continue
            word_count[word] = word_count.get(word, 0) + 1

    # for word in words:
    #     if len(word) == 1:
    #         continue
    #     word_count[word] = word_count.get(word, 0) + 1

    items = list(word_count.items())
    items.sort(key=lambda x: x[1], reverse=True)

    single = ['吃', '药', '能', '治', '啥', '病', ]
    with open('data/vocab.txt', 'w', encoding='utf-8') as f:
        for item in items:
            f.write(item[0]+'\n')
        for word in single:
            f.write(word + '\n')



