from utils import open_data
from random import shuffle
import os


def pro_data(x, c, str):
    y = [class_dict[i] for i in c]
    all_data = list(zip(x, y))
    shuffle(all_data)
    x[:], y[:] = zip(*all_data)
    folder = 'data/'
    save_sample(folder, str, x, y)
    return x, y


def save_sample(data_folder, str, x, y):
    path = data_folder + str + '.txt'
    with open(path, 'w', encoding='utf-8') as f:
        for i in range(len(x)):
            content = x[i] + '\t' + y[i] + '\n'
            f.write(content)


if __name__ == '__main__':
    # # “每个类别一个文件” 的 版本
    # questions, classes = open_data('data_orig/train_data.txt')
    # for i in range(len(questions)):
    #     c = classes[i]
    #     with open('data/'+c+'.txt', 'a', encoding='utf-8') as f:
    #         f.write(questions[i] + '\n')

    # 加载原始数据
    x_train, c_train = open_data('data_orig/train_data.txt')
    x_test, c_test = open_data('data_orig/test_data.txt')

    # 识别所有类，生成类别列表和字典，并保存类别列表
    if not os.path.exists('data'):
        os.mkdir('data')
    class_list = list(set(c_train))
    with open('data/class.txt', 'w', encoding='utf-8') as f:
        f.writelines(content+'\n' for content in class_list)
    class_dict = {}
    for i, item in enumerate(class_list):
        class_dict[item] = str(i)

    # 类别转换为标签, 打乱顺序， 保存
    x_train, y_train = pro_data(x_train, c_train, 'train')
    x_test, y_test = pro_data(x_test, c_test, 'test')
