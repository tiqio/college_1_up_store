import glob
import os
from random import shuffle
from nltk.tokenize import TreebankWordTokenizer
from gensim.models import word2vec
# model = word2vec.Word2Vec.load("Word2vec\word2vec.model") # 相对路径
model = word2vec.Word2Vec.load(r"C:\Users\HP\Desktop\AI\nlp_stage_5\Word2vec\word2vec.model")
# 命令行调试阶段
word_vectors = model.wv
if __name__ != '__main__':
  print("该模块已正式发行,请从正面使用")
# 加载由text8训练出来的模型并转化为KeyedVectors格式的word_vectors

# 数据预处理模块
def pre_process_data(filepath):
  # 加载好的和坏的文档并将它们混合
  positive_path = os.path.join(filepath, 'pos')
  negative_path = os.path.join(filepath, 'neg')
  pos_label = 1
  neg_label = 0
  dataset = []
  for filename in glob.glob(os.path.join(positive_path, '*.txt')):
    with open(filename, 'r', encoding='utf-8') as f:
      dataset.append([pos_label, f.read()])
  for filename in glob.glob(os.path.join(negative_path, '*.txt')):
    with open(filename, 'r', encoding='utf-8') as f:
      dataset.append([neg_label, f.read()])
  shuffle(dataset)
  return dataset

# 数据分词和向量化,对带标签文档的文档分析
def tokenize_and_vectorize(dataset):
  tokenizer = TreebankWordTokenizer()
  vectorized_data = []
  for sample in dataset:
    tokens = tokenizer.tokenize(sample[1])
    sample_vecs = []
    for token in tokens:
      try:
        sample_vecs.append(word_vectors[token])
      except KeyError:
        pass
    vectorized_data.append(sample_vecs)
  return vectorized_data

# 目标变量解压缩
def collect_expected(dataset):
  expected = []
  for sample in dataset:
    expected.append(sample[0])
  return expected

# 将每个样本文档的长度统一化(词向量的数目)
def pad_trunc(data, maxlen):
  new_data = []
  zero_vector = []
  for _ in range(len(data[0][0])):
    zero_vector.append(0.0)
  
  for sample in data:
    if len(sample) > maxlen:
      temp = sample[:maxlen]
    elif len(sample) < maxlen:
      temp = sample
      additional_elems = maxlen - len(sample)
      for _ in range(additional_elems):
        temp.append(zero_vector)
    else:
      temp = sample
    new_data.append(temp)
  return new_data
    
# ----- struct split -----

from keras.models import model_from_json
print("有三组模型可供选择:demo/_2th/bi")
print("""对应的属性分别为:
50神经元: loss: 0.5483 - accuracy: 0.7367 - val_loss: 0.7293 - val_accuracy: 0.6640
100神经元: loss: 0.6123 - accuracy: 0.7333 - val_loss: 0.9981 - val_accuracy: 0.6358
双向10神经元: loss: 0.5659 - accuracy: 0.7097 - val_loss: 0.7312 - val_accuracy: 0.6476""")
branch = input("请输入你要载入的json模型(附带权重文档):")
with open(r"C:\Users\HP\Desktop\AI\nlp_stage_5\rnn\{}_simplernn_model.json".format(branch), 'r', encoding='utf-8') as json_file:
  json_string = json_file.read()
model = model_from_json(json_string)
model.load_weights(r"C:\Users\HP\Desktop\AI\nlp_stage_5\rnn\{}_simplernn_model.h5".format(branch))

import numpy as np
maxlen = 400
embedding_dims = 100
sample = input("请输入你需要进行分类的文本:")
vec_list = tokenize_and_vectorize([(1, sample)])
test_vec_list = pad_trunc(vec_list, maxlen)
test_vec = np.reshape(test_vec_list, (len(test_vec_list), maxlen, embedding_dims))
# 其实可以用np.array直接进行转化
if model.predict(test_vec) > 0.5:
  print("该文本属于积极向文本")
else:
  print("该文本属于消极向文本")




