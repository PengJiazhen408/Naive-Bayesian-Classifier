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
    jieba.load_userdict('./data_orig/symbol.txt')
    jieba.del_word('糖尿病人')
    jieba.del_word('常用药')
    jieba.del_word('药有')


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