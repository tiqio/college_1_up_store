from numpy import *
import matplotlib.pyplot as plt

def loadDataSet():
  dataMat = []
  labelMat = []
  fr = open('testSet.txt')
  for line in fr.readlines():
    lineArr = line.strip().split()
    # ()默认删除前后的空格(可多个),换行符,制表符,回车符
    # ()默认以空格(可多个),换行符,制表符,回车符为分隔符
    dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
    labelMat.append(int(lineArr[2]))
  return dataMat, labelMat
  # 注意Mat,是以二维数组的形式存在 

def sigmoid(inX):
  return 1.0/(1 + exp(-inX))

def gradAscent(dataMatIn, classLabels):
  # 从这里可以知道reload仅有更新import的成效,因错引入的数据不会消失
  # https://blog.csdn.net/qq_27736687/article/details/87168978 array更清楚一些
  dataMatrix = mat(dataMatIn)
  labelMat = mat(classLabels).transpose()
  m,n = shape(dataMatrix)
  # 数组或元组的直接接受可以省略[]或()
  alpha = 0.001
  maxCycles = 500
  weights = ones((n,1))
  # 用[]和()定义没有什么不同,结果都是array
  
  for k in range(maxCycles):
    h = sigmoid(dataMatrix * weights)
    error = (labelMat - h)
    weights = weights + alpha * dataMatrix.transpose() * error
  return weights

def plotBestFit(weights):
  dataMat, labelMat = loadDataSet()
  dataArr = array(dataMat)
  n = shape(dataArr)[0]
  xcord1 = []
  ycord1 = []
  xcord2 = []
  ycord2 = []
  for i in range(n):
    if int(labelMat[i]) == 1:
      xcord1.append(dataArr[i, 1])
      ycord1.append(dataArr[i, 2])
    else:
      xcord2.append(dataArr[i, 1])
      ycord2.append(dataArr[i, 2])
  # ax = fig.add_suplot(111)
  # AttributeError: 'Figure' object has no attribute 'add_suplot'
  fig,ax = plt.subplots(figsize=(7, 5))
  ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
  ax.scatter(xcord2, ycord2, s=30, c='green')
  x = arange(-3.0, 3.0, 0.1)
  # print(type(x)) # <class 'numpy.ndarray'>
  # x = x[newaxis, :]
  # 从这里看来,plt.plot的绘图功能只对一维数组有效果
  y = (- weights[0] - weights[1]*x)/weights[2]
  # print(type(y)) # <class 'numpy.matrix'>
  y = y.getA()
  y = squeeze(y, 0)
  # 这种操作对matrix没有效果,还是ndarray好用
  plt.plot(x, y)
  plt.xlabel('X1')
  plt.ylabel('X2', rotation='horizontal')
  plt.show()

# cmd:mat.getA() 将自身矩阵变量转化为ndarray类型的变量

def stocGradAscent0(dataMatrix, classLabels):
  m,n = shape(dataMatrix)
  alpha = 0.01
  weights = ones(n)
  for i in range(m):
    h = sigmoid(sum(dataMatrix[i]*weights))
    error = classLabels - h
    weights = weights + alpha * error * dataMatrix[i]
  return weights

