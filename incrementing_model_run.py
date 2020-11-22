from LAC import LAC

# 使用自己训练好的模型
my_lac = LAC()
texts = u"百度是一家高科技公司"
lac_result = my_lac.run(texts)
print(lac_result)