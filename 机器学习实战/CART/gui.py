from tkinter.constants import END
import numpy as np
import tkinter as gui
import cart
import matplotlib 
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def getInputs():
  try:
    tolN = int(tolNentry.get())
  except:
    tolN = 10
    print("enter Interger for tolN")
    tolNentry.delete(0, END)
    tolNentry.insert(0, '10')
  try: 
    tolS = float(tolSentry.get())
  except:
    tolS = 1.0
    print("enter Float for tolS")
    tolSentry.delete(0, END)
    tolSentry.insert(0, '1.0')
  return tolN, tolS

def reDraw(tolS, tolN):
  reDraw.f.clf()
  reDraw.a = reDraw.f.add_subplot(111)
  # 如果使用add_sunplot,就可以进行axes引领的绘图,而如果是subplots,就省略axes
  if chkBtnVar.get():
    if tolN < 2:
      tolN = 2
      # tolN的最小值是2,在这里进行修正
    myTree = cart.createTree(reDraw.rawDat, cart.modelLeaf, cart.modelErr, (tolS, tolN))
    # 使用reDraw的属性技术作为局部处理变量,但并不在函数中定义
    yHat = cart.createForeCast(myTree, reDraw.testDat, cart.modelTreeEval)
  else:
    myTree = cart.createTree(reDraw.rawDat, ops=(tolS, tolN))
    yHat = cart.createForeCast(myTree, reDraw.testDat)
  reDraw.a.scatter(reDraw.rawDat[:, 0].tolist(), reDraw.rawDat[:, 1].tolist(), s=5)
  reDraw.a.plot(reDraw.testDat.tolist(), yHat.tolist(), linewidth=2.0)
  # 注意如果要绘图,每一个轴只能容纳一维,不能用np.mat来表示(固定二维),但特殊的,如果是列向量,也是可绘图的
  # ValueError: matrix must be 2-dimensional
  reDraw.canvas.draw()

def drawNewTree():
  tolN,tolS = getInputs()
  reDraw(tolN, tolS)

trainData = input("请输入你用来训练的数据集(特征1&标签1):")
print("该图是根据特征的取值进行的plot预测")
root = gui.Tk()
# gui.Label(root, text="Plot Place Holder").grid(row=0, columnspan=3) 占位符
# 如果使用网格进行绘画就是实时响应的,不用pack进行装箱
# 下方将plt与gui进行集成
reDraw.f = Figure(figsize=(5,4), dpi=100)
# 这种方法适用于在tk上绘图,实时显示
reDraw.canvas = FigureCanvasTkAgg(reDraw.f, master=root)
# reDraw.canvas.show() 已被弃用,现在由draw代替
reDraw.canvas.draw()
reDraw.canvas.get_tk_widget().grid(row=0, columnspan=3)
# 以上代码作为画布的方位显示

gui.Label(root, text='tolN').grid(row=1, column=0)
tolNentry = gui.Entry(root)
tolNentry.grid(row=1, column=1)
tolNentry.insert(0, '10')
gui.Label(root, text='tolS').grid(row=2, column=0)
tolSentry = gui.Entry(root)
tolSentry.grid(row=2, column=1)
tolSentry.insert(0, '1.0')
gui.Button(root, text='ReDraw', command=drawNewTree).grid(row=1, column=2, rowspan=3)
chkBtnVar = gui.IntVar()
chkBtn = gui.Checkbutton(root, text="Model Tree", variable=chkBtnVar)
chkBtn.grid(row=3, column=0, columnspan=2)
reDraw.rawDat = cart.loadDataSet(trainData)
reDraw.testDat = np.arange(np.min(reDraw.rawDat[:, 0]), np.max(reDraw.rawDat[:, 0]), 0.01)
reDraw.testDat = np.mat(reDraw.testDat).T
# 改变函数参数的形式,从而完成对函数的适配
drawNewTree()
root.mainloop()

