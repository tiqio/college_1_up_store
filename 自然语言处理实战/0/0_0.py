import tensorflow as tf
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  # Dense为全连接层,附带了激活函数的变换
  tf.keras.layers.Dropout(0.2),
  # 减遍化后可以很好的完成泛华
  tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5)
# 以5为周期进行模型的训练
model.evaluate(x_test,  y_test, verbose=1)
# fit中的verbose:0:不输出,1：输出进度条记录,2:每个epoch输出一行记录,默认为1
# evaluate中的verbose:0:不输出,1:输出进度条记录,默认为1