from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris

iris = load_iris()
features = iris.data
labels = iris.target
# 随机抽取33%的数据作为测试集,其余为训练集
# random_state：是随机数的种子。
train_features,test_features,train_labels,test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)
clf = DecisionTreeClassifier(criterion='gini')
# 在python中如果想要查看属性,可以使用vars()(但一定要有__dict__),如果要查看方法,用dir([])
# [i for i in dir(tree) if i not in dir([dir])] 找到不在dir([dir])中的dir(dir)中的元素
clf = clf.fit(train_features, train_labels)
test_predict = clf.predict(test_features)
score = accuracy_score(test_labels, test_predict)
print("CART分类树准确率 %.4lf" % score)
# 暂时认为只有ID3和C4.5有明确的分类功能和绘图的可能性

