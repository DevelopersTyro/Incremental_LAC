from LAC import LAC
from utils import txt_to_li, get_entity_hallmark, join_txt
# 选择使用默认的词法分析模型
lac = LAC()
# 训练和测试数据集，格式一致
# train_file = "./ner_datasets/MSRA/disposed_msra_train_bio.tsv"
# test_file = "./ner_datasets/MSRA/disposed_msra_test_bio.tsv"
# train_file = "./ner_datasets/MSRA/baidu_train_data.tsv"
# test_file = "./ner_datasets/MSRA/baidu_test_data.tsv"
train_file = "./ner_datasets/MSRA/disposed_msra_train_bio.tsv"
test_file = "./ner_datasets/MSRA/disposed_msra_test_bio.tsv"
# train(self, model_save_dir, train_data, test_data=None, iter_num=10, thread_num=10)
# lac.train(model_save_dir='./lac_model/', train_data=train_file, test_data=test_file)

# 使用自己训练好的模型
filepath="./ner_datasets/MSRA/msra_test_bio.txt"
my_lac = LAC()
text_li, _ = txt_to_li(filepath)
texts = join_txt(text_li)
result = my_lac.run(texts)
print("successul")