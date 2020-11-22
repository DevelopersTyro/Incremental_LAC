#增量训练
from LAC import LAC
from utils import txt_to_li, get_entity_hallmark, join_txt

class lac_agg():
    def __init__(self, mod):
        self.train_file = "./ner_datasets/MSRA/disposed_msra_train_bio.tsv"
        self.test_file = "./ner_datasets/MSRA/disposed_msra_test_bio.tsv"
        self.save_model_path = './lac_model/'
        self.mod = mod
        if self.mod == None:
            self.lac = LAC()
        else:
            self.lac = LAC(model_path=mod)

    def train_model(self, iter_num=10, thread_num=10):
        # train(self, model_save_dir, train_data, test_data=None, iter_num=10, thread_num=10)
        self.lac.train(model_save_dir=self.save_model_path,
                       train_data=self.train_file,
                       test_data=self.test_file,
                       iter_num=iter_num,
                       thread_num=thread_num)
        self.lac = LAC(model_path=self.save_model_path)

    def test(self, filepath, change_format=True):
        """
        :param filepath:
        :param change_format: True指文件路径对应文件为bio格式
        :return:
        """
        if change_format:
            text = ['B-LOC', 'B-PER', 'B-ORG']
            text_i = ['I-LOC', 'I-PER', 'I-ORG']
            text_lac = ['LOC', 'PER', 'ORG']
            text_li, pos_li = txt_to_li(filepath)
            hallmark_li_0 = get_entity_hallmark(text, text_i, pos_li)
            hallmark_li = []
            for i in range(len(hallmark_li_0)):
                item = hallmark_li_0[i]
                hallmark_item = [item[0], item[1], text_lac[text.index(item[2])]]
                hallmark_li.append(hallmark_item)
            texts = join_txt(text_li)
            lac_result = self.lac.run(texts)
            lac_hallmark_li = []
            lac_text_li = lac_result[0]
            lac_pos_li = lac_result[1]
            for i in range(len(lac_pos_li)):
                if lac_pos_li[i] in text_lac:
                    start_idx = get_len_from_lac(i, lac_result)
                    end_idx = len(lac_text_li[i]) + start_idx
                    lac_hallmark_li.append((start_idx, end_idx, lac_pos_li[i]))
            hallmark_index = 0
            fix_cnt = 0
            hallmark_match_li = []
            for i in range(len(hallmark_li)):
                hallmark = hallmark_li[i]
                start_idx1 = hallmark[0]
                end_idx1 = hallmark[1]
                is_find = False
                for j in range(hallmark_index, len(lac_hallmark_li)-1):
                    start_idx2 = lac_hallmark_li[j][0]
                    end_idx2 = lac_hallmark_li[j][1]
                    if overlap(start_idx1, end_idx1, start_idx2, end_idx2):
                        hallmark_index = j+1
                        fix_cnt += 1
                        is_find = True
                        hallmark_match_li.append([start_idx1, end_idx1, start_idx2, end_idx2])
                        # print("###start_idx1:{} end_idx1:{} start_idx2:{} end_idx2:{}".format(start_idx1, end_idx1, start_idx2, end_idx2))
                        # print("start_idx:{} end_idx1:{} text:{} pos:{}".format(start_idx1, end_idx1, lac_text_li[j], lac_pos_li[j]))
                        break
                if not is_find:
                    print("start_idx:{} end_idx1:{} text:{}".format(start_idx1, end_idx1,
                                                                           texts[start_idx1: end_idx1],))
            print("Get acc of {}".format(fix_cnt/len(hallmark_li)))

    def run(self, text):
        self.lac.run(text)


def get_len_from_lac(index, lac_result):
    lac_text_li = lac_result[0]
    lac_pos_li = lac_result[1]
    words_length = 0

    for i in range(index):
        words_length += len(lac_text_li[i])
    return words_length


def overlap(start_idx1, end_idx1, start_idx2, end_idx2):
    """
    Decide whether 2 intervals overlap.
    :param start_idx1:
    :param end_idx1:
    :param start_idx2:
    :param end_idx2:
    :return: True/False
    """
    head = min(end_idx1, end_idx2)
    tail = max(start_idx1, start_idx2)
    return head >= tail

if __name__ == '__main__':
    # my_lac = lac_agg()
    # my_lac.train_model()
    my_lac = lac_agg('./lac_model/')
    my_lac.test(filepath="./ner_datasets/MSRA/msra_test_bio.txt")
# # 选择使用默认的词法分析模型
# lac = LAC()
#
#
# # 训练和测试数据集，格式一致
# # train_file = "./ner_datasets/MSRA/disposed_msra_train_bio.tsv"
# # test_file = "./ner_datasets/MSRA/disposed_msra_test_bio.tsv"
# # train_file = "./ner_datasets/MSRA/baidu_train_data.tsv"
# # test_file = "./ner_datasets/MSRA/baidu_test_data.tsv"
# train_file = "./ner_datasets/MSRA/disposed_msra_train_bio.tsv"
# test_file = "./ner_datasets/MSRA/disposed_msra_test_bio.tsv"
# # train(self, model_save_dir, train_data, test_data=None, iter_num=10, thread_num=10)
# lac.train(model_save_dir='./lac_model/', train_data=train_file, test_data=test_file)
#
# # 使用自己训练好的模型
# my_lac = LAC(model_path='./lac_model/')

