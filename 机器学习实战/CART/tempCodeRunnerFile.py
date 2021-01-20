
# def getInputs():
#   try:
#     tolN = int(tolNentry.get())
#   except:
#     tolN = 10
#     print("enter Interger for tolN")
#     tolNentry.delete(0, END)
#     tolNentry.insert(0, '10')
#   try: 
#     tolS = float(tolSentry.get())
#   except:
#     tolS = 1.0
#     print("enter Float for tolS")
#     tolSentry.delete(0, END)
#     tolSentry.insert(0, '1.0')
#   return tolN, tolS

# def reDraw(tolS, tolN):
#   reDraw.f.clf()
#   reDraw.a = reDraw.f.subplots(111)
#   if chkBtnVar.get():
#     if tolN < 2:
#       tolN = 2
#       myTree = cart.createTree(reDraw.rawDat, cart.modelLeaf, cart.modelErr, (tolS, tolN))
#       yHat = cart.createForeCast(myTree, reDraw.testDat, cart.modelTreeEval)
#     else:
#       myTree = cart.createTree(reDraw.rawDat, ops=(tolS, tolN))
#       yHat = cart.createForeCast(myTree, reDraw.testDat)
#     reDraw.a.scatter(reDraw.rawDat[:, 0], reDraw.rawDat[:, 1], s=5)
#     reDraw.a.plot(reDraw.testDat, yHat, linewidth=2.0)
#     reDraw.canvas.show()

# def drawNewTree():
#   tolN,tolS = getInputs()
#   reDraw(tolN, tolS)
