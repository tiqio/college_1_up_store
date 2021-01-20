from numpy import *

def load_data():
  dataMat = []
  labelMat = []
  # file_ = input("请输入贝叶斯训练需要的数据集:")
  # 调试阶段
  file_ = "txt\贝叶斯2020-12-20-16时.txt"
  fr = open(file_, 'r', encoding='utf-8')
  for line in fr.readlines():
    lineArr = line.strip().split()
    # 在特定条件下,split比正则好用
    dataMat.append(lineArr[1])
    labelMat.append(lineArr[0])
  return dataMat[1:], labelMat[1:]


def createVocabList(dataSet):
  vocabSet = set([])
  for document in dataSet:
    vocabSet = vocabSet | set(document)
  return list(vocabSet)


def get_p_ci(labels, labelMat):
  p_ci = []
  cat_dict = {}
  label_num = 0
  for label in labels:
    # n_label = [int(label==i) for i in labelMat]
    # 不知道为什么,这么写容易卡住出问题,先不这么写
    n_label = 0
    cat_dict[label_num] = []
    for k in range(len(labelMat)):
      if labelMat[k] == label:
        cat_dict[label_num].append(k)
        n_label += 1
        # 列表的append方法没有返回值,不会返回添加元素后的列表
        # 这里的index只能返回第一个元素的索引
        # 修改后的这种方法不仅可以获取索引值,还可以统计值的个数
    label_num += 1
    p_label = n_label/len(labelMat)
    p_ci.append(p_label)
  return p_ci, cat_dict


def setOfWords2Vec(vocabList, inputSet):
  returnVec = [0] * len(vocabList)
  for word in inputSet:
    # 这里的inputSet是60*7规格的非扁平化词集,总共要使用60*7次函数
    if word in vocabList:
      returnVec[vocabList.index(word)] = 1
    else:
      print("单词%s并未存储在该词集内" % word)
  return returnVec


def map_(all_dict, class_dict):
  trainMat = []
  for item in class_dict:
    trainMat.append(setOfWords2Vec(all_dict, item))
  return trainMat


def trainNB0(trainMatrix, cat_dict):
  # trainMatrix 420x2091
  # cat_dict 7x60
  numTrainDocs = len(trainMatrix) # 420
  numWords = len(trainMatrix[0])  # 2091
  pNum = ones([len(cat_dict), numWords]) # 7x2091
  pDenom = ones([len(cat_dict), 1])*2 # 7x0
  for key,indexes in cat_dict.items(): # 0,1,~6
    for index in indexes: # 0,1~59
      pNum[key] += trainMatrix[index] # 7x2091
      pDenom[key] += sum(trainMatrix[index]) # 7x1
  pVect = log(pNum/pDenom) # 7x2091
  return pVect


def classifyNB(vec2Classify, pVect, p_ci):
  # vec2Classify 1x2091 这里使用了numpy广播的技术 相乘时转化为7x2091
  # pVect 7x2091
  # p_ci 7x1
  p = sum(vec2Classify*pVect, axis=1) + log(p_ci) # 7x1
  # ndarray和list在维数一致时可以进行运算
  max_index = p.argmax()
  return max_index


def main():
  labels = ['影视', '音乐', '游戏', '动漫', '趣闻', '科学', '软件']
  dataMat,labelMat = load_data()
  myVocabList = createVocabList(dataMat)
  p_ci,cat_dict = get_p_ci(labels, labelMat)
  trainMat = map_(myVocabList, dataMat)
  pVect = trainNB0(trainMat, cat_dict)
  text = input("请输入你需要分类的文段:")
  vec2Classify = setOfWords2Vec(myVocabList, text)
  max_index = classifyNB(vec2Classify, pVect, p_ci)
  print("该文本属于类别:{}".format(labels[max_index]))
  # print(dataMat) 420x?
  # print(trainMat) 420x2091

  
if __name__ == '__main__':
  main()
