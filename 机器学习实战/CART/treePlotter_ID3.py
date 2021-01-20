import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

# 不定类型的键会自动转化成字符串的形式
decisionNode = dict(boxstyle='sawtooth', fc='0.8')
leafNode = dict(boxstyle='round4', fc='0.8')
# fc指灰度,即背景颜色
arrow_args = dict(arrowstyle='<|-')

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
  # centerPt文本坐标,parentPt箭头指向
  createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
    xytext=centerPt, textcoords='axes fraction',
    # 可以使用xycoords和textcoords（默认为data）指定xy和xytext的坐标系。
    va='center', ha='center', bbox=nodeType, arrowprops=arrow_args
  )
  # 构造添加注解的框架,需要为createPlot这个函数对象添加属性

def createPlot():
  fig = plt.figure(1, facecolor='white')
  # fig.clf()
  # 暂时不知道cla和clf的区别
  createPlot.ax1 = plt.subplot(111, frameon=False)
  # 将子图绑定为函数对象的属性,暂时不知道有什么用
  plotNode('决策叶点', (0.5,0.1), (0.1,0.5), decisionNode)
  plotNode('叶节点', (0.8,0.1), (0.3,0.8), leafNode)
  plt.show()

def getNumLeafs(myTree):
  numLeafs = 0
  firstStr = list(myTree.keys())[0]
  # TypeError: 'dict_keys' object is not subscriptable 可有下标的
  # 注意,使用keys()获取的值是dict_keys类型,需要转化为list类型
  secondDict = myTree[firstStr]
  for key in secondDict.keys():
    if type(secondDict[key]).__name__ == 'dict':
      numLeafs += getNumLeafs(secondDict[key])
    else: 
      numLeafs += 1
  return numLeafs
  
def getTreeDepth(myTree):
  maxDepth = 0
  firstStr = list(myTree.keys())[0]
  secondDict = myTree[firstStr]
  for key in secondDict.keys():
    if type(secondDict[key]).__name__ == 'dict':
      thisDepth = 1 + getTreeDepth(secondDict[key])
    else:
      thisDepth = 1
    if thisDepth > maxDepth: 
      maxDepth = thisDepth
  return maxDepth

def retrieveTree(i):
  listOfTrees = [ {'no surfacing': {0: 'no', 1: {'flippers':
                    {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers':
                    {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                ]
  return listOfTrees[i]

def plotMidText(cntrPt, parentPt, txtString):
  xMid = (parentPt[0] - cntrPt[0])/2.0 + cntrPt[0]
  yMid = (parentPt[1] - cntrPt[1])/2.0 + cntrPt[1]
  createPlot.ax1.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt):
  numLeafs = getNumLeafs(myTree)
  depth = getTreeDepth(myTree)
  firstStr = list(myTree.keys())[0]
  cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
  plotMidText(cntrPt, parentPt, nodeTxt)
  plotNode(firstStr, cntrPt, parentPt, decisionNode)
  secondDict = myTree[firstStr]
  plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
  for key in secondDict.keys():
    if type(secondDict[key]).__name__ == 'dict':
      plotTree(secondDict[key], cntrPt, str(key))
    else:
      plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
      plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff),
        cntrPt, leafNode)
      plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
  plotTree.yOff = plotTree.yOff +1.0/plotTree.totalD

def treeOut(inTree):
  fig = plt.figure(1, facecolor='white')
  fig.clf()
  axprops = dict(xticks=[], yticks=[])
  createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
  plotTree.totalW = float(getNumLeafs(inTree))
  plotTree.totalD = float(getTreeDepth(inTree))
  plotTree.xOff = -0.5/plotTree.totalW
  plotTree.yOff = 1.0
  plotTree(inTree, (0.5,1.0), '')
  plt.show()

