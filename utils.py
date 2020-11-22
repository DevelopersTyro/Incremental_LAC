import re
import numpy as np
from LAC import LAC


def txt_to_li(file_path):
    """
    :param file_path:
    :return:  text_li, pos_li
    """
    with open(file_path, "r", encoding="utf-8") as fa:
        tmp = fa.readlines()
        text_li = []
        pos_li = []
        for item in tmp:
            try:
                item_spli = re.split('\t|\n', item.strip())
                # print(item_spli)
                text_li.append(item_spli[0])
                pos_li.append(item_spli[1])
            except IndexError:
                pass
    # zipped_li = list(zip(text_li, pos_li))
    return text_li, pos_li


def str_to_txt(ouput_path, text):
    """
    :param ouput_path:
    :param text:
    :return: txt文本以‘/w’为标志换行写入
    """
    sentences = re.split(r"(/w)", text)
    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]
    with open(ouput_path, 'a', encoding="utf-8") as f:
        f.writelines([line.strip()+'\n' for line in sentences])


def get_index_li(text, li):
    return np.where(np.array(li) == text)[0]


def get_entity_hallmark(text ,text_I, li):
    """
    :param text: ['B-LOC', 'B-PER', 'B-ORG']
    :param text_I: ['I-LOC', 'I-PER', 'I-ORG']
    :param li: pos_li
    :return: hallmark_li
    """
    hallmark_li = []
    for i in range(len(text)):
        name = text[i]
        end_name = text_I[i]
        index_li = get_index_li(name, li)
        end_li = []
        for index in index_li:
            not_find_end = True
            end_index = index
            while not_find_end:
                end_index += 1
                if li[end_index] != end_name:
                    not_find_end = False
            end_li.append(end_index)
        hallmark_li.extend(list(zip(index_li, end_li, [name]*len(index_li))))

    hallmark_li = sorted(hallmark_li, key=lambda x: x[0])

    return hallmark_li


def get_format_from_lac(lac_result):
    """
    :param lac_result: [['百度', '是', '一家', '高科技', '公司'], ['ORG', 'v', 'm', 'n', 'n']]
    :return: ”百度/ORG 是/v 一家/m 高科技/n 公司/n"
    """
    text, pos = lac_result[0], lac_result[1]
    text_result = []
    for i in range(len(text)):
        t = text[i] + '/' + pos[i] + ' '
        text_result.append(t)
    return ''.join(text_result)


def join_txt(text_list):
    text_result = []
    for i in range(len(text_list)):
        t = text_list[i]
        text_result.append(t)
    return ''.join(text_result)


def format_change(text_li, pos_li):
    text = ['B-LOC', 'B-PER', 'B-ORG']
    text_i = ['I-LOC', 'I-PER', 'I-ORG']
    text_lac = ['LOC', 'PER', 'ORG']
    hallmark_li = get_entity_hallmark(text, text_i, pos_li)

    lac = LAC()
    initial_text = ''.join(text_li[0:hallmark_li[0][0]])
    seg_result = lac.run(initial_text)
    formated_text = get_format_from_lac(seg_result)

    for i in range(len(hallmark_li)):
        hallmark = hallmark_li[i]
        targeted_words_0 = ''.join(text_li[hallmark[0]:hallmark[1]])
        disposed_words_0 = targeted_words_0 + '/' + text_lac[text.index(hallmark[2])] + ' '
        if i == len(hallmark_li)-1:
            targeted_words_1 = ''.join(text_li[hallmark[1]:len(text_i)])
        else:
            targeted_words_1 = ''.join(text_li[hallmark[1]:hallmark_li[i+1][0]])
        disposed_words_1 = get_format_from_lac(lac.run(targeted_words_1))
        formated_text += disposed_words_0 + disposed_words_1

    return formated_text


if __name__ == '__main__':
    file_path = './ner_datasets/MSRA/msra_train_bio.txt'
    output_path = 'ner_datasets/MSRA/disposed_msra_train_bio.txt'
    text_li, pos_li = txt_to_li(file_path)
    formated_result = format_change(text_li, pos_li)
    str_to_txt(output_path, formated_result)

