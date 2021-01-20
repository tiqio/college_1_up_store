import tensorflow as tf

from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Add a channels dimension
# 60000x28x28x1(进行维度的补充)
x_train = x_train[..., tf.newaxis]
x_test = x_test[..., tf.newaxis]
train_ds = tf.data.Dataset.from_tensor_slices(
    (x_train, y_train)).shuffle(10000).batch(32)
# shuffle将数据打乱,数据越大混乱程度越大
# mini-batch每次传入一个高维矩阵进行训练,分批前进行了洗牌
# 带洗牌的mini-batch,在数据多时洗牌比较有效
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)
# 划分batch提高训练速度,测试集不用打乱,只有一次,本身就是乱的

class MyModel(Model):
  def __init__(self):
    super(MyModel, self).__init__()
    # super将MyModel的self通过super转移到父类上,再调用父类的__init__()函数移植
    # 子类继承了父类的所有属性和方法
    self.conv1 = Conv2D(32, 3, activation='relu')
    self.flatten = Flatten()
    # 一层卷积一层池化,都可以带有激活函数
    self.d1 = Dense(128, activation='relu')
    self.d2 = Dense(10, activation='softmax')

  def call(self, x):
    x = self.conv1(x)
    x = self.flatten(x)
    x = self.d1(x)
    return self.d2(x)

model = MyModel()
# model.compile拆开后:
loss_object = tf.keras.losses.SparseCategoricalCrossentropy()
optimizer = tf.keras.optimizers.Adam()
# 融合了动量下降和RMSProp,都用这个就行

# 定义了衡量指标:evals
# 这些指标在epoch上累积值,然后打印出整体结果
train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')
# 这个是evals函数,是个接口,而不是属性,name是泛型的概念

# 使用 tf.GradientTape 来训练模型：
def train_step(images, labels):
  with tf.GradientTape() as tape:
    # 需要一个上下文管理器（context manager）来连接需要计算梯度的函数和变量，梯度计算方针
    # 默认情况下GradientTape的资源在调用gradient函数后就被释放，再次调用就无法计算了
    # RuntimeError: A non-persistent GradientTape can only be used tocompute one set of gradients
    # 设置persistent可以进行多次计算梯度,但要del g  # 删除这个上下文胶带
    # 这个上下文管理器只在调用gradient后被释放,与缩进无关
    predictions = model(images)
    # 将一张图片卷积成一个10x1的向量
    loss = loss_object(labels, predictions)
    # 计算预测值和实际值的误差
  gradients = tape.gradient(loss, model.trainable_variables)
  # 这样即可计算出所有可训练变量的梯度，然后进行下一步的更新。可是这个怎么在外边???
  optimizer.apply_gradients(zip(gradients, model.trainable_variables))
  # 上述进行了映射到模型上的梯度求解,这里用optimizer更新梯度

  train_loss(loss)
  train_accuracy(labels, predictions)
  # 描述了在更新梯度前的训练情况
# ----------

# 测试模型：
def test_step(images, labels):
  predictions = model(images)
  t_loss = loss_object(labels, predictions)

  test_loss(t_loss)
  test_accuracy(labels, predictions)

EPOCHS = 5

for epoch in range(EPOCHS):
  # 在下一个epoch开始时，重置评估指标
  train_loss.reset_states()
  train_accuracy.reset_states()
  test_loss.reset_states()
  test_accuracy.reset_states()

  for images, labels in train_ds:
    train_step(images, labels)

  for test_images, test_labels in test_ds:
    test_step(test_images, test_labels)

  template = 'Epoch {}, Loss: {}, Accuracy: {}, Test Loss: {}, Test Accuracy: {}'
  print (template.format(epoch+1,
                         train_loss.result(),
                         train_accuracy.result()*100,
                         test_loss.result(),
                         test_accuracy.result()*100))
# 每一次EPOCH都有一个指标evals,可以将检测集视为train set和test set
