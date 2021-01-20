from numpy import *

def loadDataSet():
  postingList = [['my','dog','has','flea','problems','help','please'],
                  ['maybe','not','take','him','to','dog','park','stupid'],
                  ['my','dalmation','is','so','cute','I','love','him'],
                  ['stop','posting','stupid','worthless','garbage'],
                  ['mr','licks','ate','my','steak','how','to','stop','him'],
                  ['quit','buying','worthless','dog','food','stupid']
                ]
  classVec = [0,1,0,1,0,1]
  return postingList, classVec

def createVocabList(dataSet):
  vocabSet = set([])
  for document in dataSet:
    vocabSet = vocabSet | set(document)
    # 在集合运算中求并集不能用or,应该用|
  return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
  returnVec = [0] * len(vocabList)
  for word in inputSet:
    if word in vocabList:
      returnVec[vocabList.index(word)] = 1
      # set/list.index(value)可以找到第一个值的索引,缺点是一句话中可能有多个相同的词
      # 没有大问题,但是损失了整体下应有的信息,不够准确
    else:
      print("the word: %s is not in my vocabulary!"% word)
  return returnVec

def trainNB0(trainMatrix, trainCategory):
  numTrainDocs = len(trainMatrix)
  numWords = len(trainMatrix[0])
  pAbusive = sum(trainCategory)/float(numTrainDocs)
  p0Num = ones(numWords)
  p1Num = ones(numWords)
  p0Demon = 2.0
  p1Demon = 2.0
  for i in range(numTrainDocs):
    if trainCategory[i] == 1:
      p1Num += trainMatrix[i]
      p1Demon += sum(trainMatrix[i])
    else:
      p0Num += trainMatrix[i]
      p0Demon += sum(trainMatrix[i])
  p1Vect = log(p1Num/p1Demon) # [1,32]
  p0Vect = log(p0Num/p0Demon) # [1,32]
  # math.log()只能对标量(scalar)计算,而numpy.log()可以对数组计算
  return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
  p1 = sum(vec2Classify * p1Vec) + log(pClass1)
  p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
  if p1 > p0:
    return 1
  else:
    return 0

def testingNB():
  listOPost, listClasses = loadDataSet()
  myVocabList = createVocabList(listOPost)
  trainMat = []
  for postinDoc in listOPost:
    trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
  p0V,p1V,pAb = trainNB0(array(trainMat), array(listClasses))
  # 仅仅是中介的作用,感觉可以不将其转化为numpy
  testEntry = ['love', 'my', 'dalmation']
  thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
  print(testEntry,'classified as',classifyNB(thisDoc, p0V, p1V, pAb))
  testEntry = ['stupid', 'garbage']
  thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
  print(testEntry,'classified as',classifyNB(thisDoc, p0V, p1V, pAb))
  # 经过简单的修饰后可以通过训练集得到分类

def bagOfWords2VecMN(vocabList):
  returnVec = [0] * len(vocabList)
  for word in inputSet:
    if word in vocabList:
      returnVec[vocabList.index(word)] += 1
  return returnVec

# ----------

# 测试算法:使用朴素贝叶斯进行交叉验证
def textParse(bigString):
  import re 
  listOfTokens = re.split(r'\W+', bigString)
  return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
  docList = []
  classList = []
  fullText = []
  for i in range(26):
    wordList = textParse(open('email/spam/%d.txt' % i).read())
    docList.append(wordList)
    fullText.append(wordList)
    classList.append(1)
    wordList = textParse(open('email/ham/%d.txt' % i).read())
    docList.append(wordList)
    fullText.append(wordList)
    classList.append(0)
  vocabList = createVocabList(docList)
  trainingSet = list(range(50))
  # python3中range返回的是range对象,不返回数组对象
  testSet = []
  for i in range(10):
    randIndex = int(random.uniform(0, len(trainingSet)))
    testSet.append(trainingSet[randIndex])
    del(trainingSet[randIndex])

  trainMat = []
  trainClasses = []
  for docIndex in trainingSet:
    trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
    trainClasses.append(classList[docIndex])
  p0V,p1V,pSpam = trainNB0(array(trainMat), array(trainClasses))

  errorCount = 0
  for docIndex in testSet:
    wordVector = setOfWords2Vec(vocabList, docList[docIndex])
    if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
      errorCount += 1
  print("the error rate is:", float(errorCount)/len(testSet))

# ----------

# 示例:使用朴素贝叶斯分类器从个人广告中获取区域倾向
def calcMostFreq(vocabList, fullText):
  import operator
  freqDict = {}
  for token in vocabList:
    freqDict[token] = fullText.count(token)
  sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True)
  return sortedFreq[:30]

def localWords(feed1, feed0):
  import feedparser
  docList = []
  classList = []
  fuulText = []
  minLen = min(len(feed1['entries']), len(feed0['entries']))
  for i in range(minLen):
    wordList = textParse(feed1['entries'][i]['summary'])
    docList.append(wordList)
    fullText.extend(wordlist)
    classList.append(1)
    wordList = textParse(feed0['entries'][i]['summary'])
    docList.append(wordList)
    fullText.extend(wordList)
    classList.append(0)
  vocabList = createVocabList(docList)
  top30Words = calcMostFreq(vocabList, fullText)
  for pairW in top30Words:
    if pairW[0] in vocabList:
      vocabList.remove(pairW[0])
  trainingSet = range(2*minLen)
  testSet = []
  for i in range(20):
    randIndex = int(random.uniform(0, len(trainingSet)))
    testSet.append(trainingSet[randIndex])
    del(trainingSet[randIndex])
    trainMat = []
    trainingClasses = []
  for docIndex in trainingSet:
    trainMat.append(bagOfWords2VecMN(vocabList, docList))
    trainClasses.append(classList[docIndex])
  p0V,p1V,pSpam = trainNB0(array(trainMat), array(trainClasses))
  errorCount = 0
  for docIndex in testSet:
    wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
    if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docList]:
      errorCount += 1
  print("the error rate is:",float(errorCount)/len(testSet))
  return vocabList,p0V,p1V

