import jieba
import os


def open_data(path):
    contents, labels = [], []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            lin = line.strip()
            if not lin:
                continue
            content, label = lin.split('\t')
            contents.append(content)
            labels.append(label)
    return contents, labels


def load_jieba():
    # jieba加载词典
    for _, _, filenames in os.walk('dict'):
        for filename in filenames:
            jieba.load_userdict(os.path.join('dict', filename))
    del_words = ['糖尿病人', '常用药', '药有', '感冒药', '特效药', '止疼药', '中成药', '中药', '止痛药', '降糖药', '单药', '喝啤酒',
                 '西药', '怎样才能', '要测', '要验', '能测', '能验', '喝酒', '喝奶', '吃糖', '喝牛奶', '吃肉', '茶好', '吃水果']
    add_words = ['DISEASE', 'SYMPTOM', 'CHECK', 'FOOD', 'STYLE', 'CATEGORY', '会不会', '能不能', '可不可以', '是不是', '要不要',
                 '应不应该', '啥用', '什么用', '吃什么', '喝什么']
    for word in del_words:
        jieba.del_word(word)
    for word in add_words:
        jieba.add_word(word)


def synonym_sub(question):
    # dict文件夹中的每个文件是一个同义词表
    # 1读取同义词表：并生成一个字典。
    combine_dict = {}
    for _, _, filenames in os.walk('dict'):
        for filename in filenames:
            fpath = os.path.join('dict', filename)
            # 加载同义词
            synonyms = []
            with open(fpath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    synonyms.append(line.strip())
            for i in range(1, len(synonyms)):
                combine_dict[synonyms[i]] = synonyms[0]
    # with open('synonym.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(combine_dict))

    # 2将语句切分
    seg_list = jieba.cut(question, cut_all=False)
    temp = "/".join(seg_list)
    # print(temp)

    # 3
    final_sentence = ""
    for word in temp.split("/"):
        if word in combine_dict:
            word = combine_dict[word]
            final_sentence += word
        else:
            final_sentence += word
    # print(final_sentence)
    return final_sentence


def qes2wb(questions):
    # 加载vocab
    data_folder = 'data/'
    vocab = [line.strip() for line in open(data_folder+'vocab.txt', 'r', encoding="utf-8").readlines()]

    # 问句，槽值替换后， 分词，转换为词袋向量
    vecs = []
    load_jieba()
    for question in questions:
        sen = synonym_sub(question)
        # print(sen)
        words = list(jieba.cut(sen, cut_all=False))
        # print('/'.join(words))
        vec = [words.count(v) for v in vocab]
        vecs.append(vec)
    return vecs