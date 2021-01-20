# from numpy import *
# 当用*进行全引用时无法使用mat,而使用np来间接引用可以解决
from math import inf
import numpy as np

times = 0
# 理论上也可以用面向对象的方式进行阐释
class treeNode():
  def __init__(self, feat, val, right, left):
    self.featureToSplitOn = feat
    self.valueOfSplit = val
    self.rightBranch = right
    self.leftBranch = left

def loadDataSet(filename):
  dataMat = []
  fr = open(filename)
  for line in fr.readlines():
    curLine = line.strip().split('\t')
    fitLine = [float(i) for i in curLine]
    dataMat.append(fitLine)
  dataMat = np.mat(dataMat)
  return dataMat

def binSplitDataSet(dataSet, feature, value):
  mat0 = dataSet[np.nonzero(dataSet[:, feature] > value)[0], :]
  mat1 = dataSet[np.nonzero(dataSet[:, feature] <= value)[0], :]
  # 同时还可以去除无效点,但只是执行了查找,特征的数目没有变
  return mat0, mat1

# ----------

# 回归树的模型构建
def regLeaf(dataSet):
  return np.mean(dataSet[:,-1])
  
def regErr(dataSet):
  return np.var(dataSet[:,-1]) * np.shape(dataSet)[0]
  # 这是回归树的误差处理方式

def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
  global times
  tolS = ops[0]
  tolN = ops[1]
  if len(set(dataSet[:,-1].T.tolist()[0])) == 1:
    print('分组之前的标签一致')
    times += 1
    print('该叶节点的标记为:', times)
    return None, leafType(dataSet)
  m,n = np.shape(dataSet)
  S = errType(dataSet)
  # 获取标签的重分布方差,而不是特征
  bestS = inf
  bestIndex = 0
  bestValue = 0
  for featIndex in range(n-1):
    # 遍历所有的特征
    for splitVal in set(dataSet[:, featIndex].T.tolist()[0]):
      # 遍历该特征的所有取值,但注意,因为在格式变化中的数据类型必然是可哈希的,[[]]或[{}]是不行的
      mat0,mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
      # 用该特征的每一取值进行分组并返回矩阵
      if (np.shape(mat0)[0] < tolN) or (np.shape(mat1)[0] < tolN):
        continue
      # 超过某一限度就认为是不平衡分组,直接去除
      newS = errType(mat0) + errType(mat1)
      if newS < bestS:
        bestIndex = featIndex
        bestValue = splitVal
        bestS = newS
      # 遍历了所有的可能性,找到了使newS最小的特征和数据划分
  if (S - bestS) < tolS:
    # 这时bestS是最小的误差了,如果减少的不大说明不需要继续了
    # print('ΔS(误差)过小而分组不明显')
    # 如果函数作用域想要使用全局变量,需要声明
    times += 1
    # print('该叶节点的标记为:', times)
    # 大多数都是这个原因,可以先暂停对节点个数的统计
    return None, leafType(dataSet)
  mat0,mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
  if (np.shape(mat1)[0] < tolN) or (np.shape(mat1)[0] < tolN):
    # 如果切分出的数据集很小就退出,不知道这个临界条件怎么来的,可能与公式有关
    print('划分出的两组不平衡')
    print('mat0的样本数:', np.shape(mat0)[0])
    print('mat1的样本数:', np.shape(mat1)[0])
    times += 1
    print('该叶节点的标记为:', times)
    return None, leafType(dataSet)
  return bestIndex, bestValue


# 模型树的模型构建
def linearSolve(dataSet):
  m,n = np.shape(dataSet)
  X = np.mat(np.ones([m,n]))
  Y = np.mat(np.ones([m,1]))
  X[:, 1:n] = dataSet[:, 0:n-1]
  # n个权重,其中第一个是偏置单元
  Y = dataSet[:, -1]
  xTx = X.T * X
  if np.linalg.det(xTx) == 0:
    raise NameError("This matrix is singular, cannot do inverse,\n\
      try increasing the second value of ops")
  ws = xTx.I * (X.T * Y)
  # ws是拟合所需的权重
  return ws, X, Y

def modelLeaf(dataSet):
  ws,X,Y = linearSolve(dataSet)
  return ws

def modelErr(dataSet):
  ws,X,Y = linearSolve(dataSet)
  yHat = X * ws
  return sum(np.power(Y - yHat, 2))

# ----------

def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
  feat,val = chooseBestSplit(dataSet, leafType, errType, ops)
  if feat == None:
    return val
  retTree = {}
  retTree['spInd'] = feat
  retTree['spVal'] = val
  lSet,rSet = binSplitDataSet(dataSet, feat, val)
  retTree['left'] = createTree(lSet, leafType, errType, ops)
  retTree['right'] = createTree(rSet, leafType, errType, ops)
  # 注意并没有消耗特征
  return retTree

# ----------

# 回归树后剪枝操作
def isTree(obj):
  return (type(obj).__name__ == 'dict')

def getMean(tree):
  if isTree(tree['left']): 
    tree['left'] = getMean(tree['left'])
  if isTree(tree['right']):
    tree['right'] = getMean(tree['right'])
  return (tree['left'] + tree['right'])/2

def prune(tree, testData):
  if np.shape(testData)[0] == 0:
    return getMean(tree)
  if (isTree(tree['right'])) or (isTree(tree['left'])):
    lSet,rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
  if isTree(tree['left']):
    tree['left'] = prune(tree['left'], lSet)
  if isTree(tree['right']):
    tree['right'] = prune(tree['right'], rSet)
  if not isTree(tree['left']) and not isTree(tree['right']):
    lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
    errorNoMerge = sum(np.power(lSet[:, -1] - tree['left'], 2)) + sum(np.power(rSet[:, -1] - tree['right'], 2))
    treeMean = (tree['left'] + tree['right']/2)
    errorMerge = sum(np.power(testData[:, -1] - treeMean, 2))
    if errorMerge < errorNoMerge:
      print('merging')
      return treeMean
    else:
      return tree
  else:
    return tree
    
def reSetTimes():
  times = 0

# ----------

# 用回归树进行预测
def regTreeEval(model, inDat):
  return float(model)

def modelTreeEval(model, inDat):
  n = np.shape(inDat)[1]
  X = np.mat(np.ones([1, n+1]))
  X[:, 1: n+1] = inDat
  return float(X * model)

def treeForeCast(tree, inData, modelEval=regTreeEval):
  if not isTree(tree):
    return modelEval(tree, inData)
  # print("inData[tree['spInd']] = " + str(inData[tree['spInd']]))
  # print("tree['spVal'] = "+ str(tree['spVal']))
  # print("inData[tree['spInd']] > tree['spVal'] = " + str(inData[tree['spInd']] > tree['spVal']))
  if float(inData[0, tree['spInd']]) > tree['spVal']:
    # https://blog.csdn.net/xieshimao/article/details/54973198 坑爹代码改正,但这个不是那个问题,并且modelEval也没有问题
    # if inData[tree['spInd']] > tree['spVal']: IndexError: invalid index to scalar variable. 注意索引index
    # 注意:一个矩阵无法和一个数值进行比较,需要用矩阵any或all方法进行适配,但存在一个值时是例外
    # 在一个值的时候甚至可以与一个数值进行真值比较
    if isTree(tree['left']):
      return treeForeCast(tree['left'], inData, modelEval)
    else:
      return modelEval(tree['left'], inData)
  else:
    if isTree(tree['right']):
      return treeForeCast(tree['right'], inData, modelEval)
    else:
      return modelEval(tree['right'], inData)

def createForeCast(tree, testData, modelEval=regTreeEval):
  m = len(testData)
  yHat = np.mat(np.zeros([m,1]))
  for i in range(m):
    yHat[i,0] = treeForeCast(tree, testData[i], modelEval)
  return yHat





