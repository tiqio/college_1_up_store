import lightgbm as lgb
import joblib
from sklearn.metrics import mean_squared_error
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split

boston = load_boston()
# 有13个特征,结果用离散值的形式表示
data = boston.data
target = boston.target
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2)
# 将0.2比例的数据划分成测试集

# 转化成lgb库自带的格式, xgb和lgb都喜欢把特征和标签放到一起
lgb_train = lgb.Dataset(X_train, y_train)
lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)
# ???eval是评估的意思,转化为评估模式是用reference吗,有什么用

params = {
  # 提升器参数和目标任务参数
  'task': 'train',
  'objective': 'regression', # 目标函数

  'boosting_type': 'gbdt', # 选择提升类型
  'metric': {'12', 'auc'}, # 评估函数,后方参数不可更改,前方可以
  'learning_rate': 0.05,

  'num_leaves': 31, # 叶子结点树
  'feature_fraction': 0.9, # 建树的特征选择比例
  'bagging_fraction': 0.8, # 建树的样本采集比例
  'bagging_freq': 5, # k意味着每k次迭代执行bagging
  'verbose': 1 # <0显示致命的,=0显示错误(警告),>0显示信息  
}

# 训练cv和train
gbm = lgb.train(params, lgb_train, num_boost_round=20, valid_sets=lgb_eval, early_stopping_rounds=5)
# 方法一:gbm.save_model('model.txt')
# 可以将训练好的模型以文本的方式保存下来
# 方法二:joblib.dump(gbm, './model/lgb.pkl') # dump来保存,load来加载

y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)
# SSE和方差,MSE均方差,RMSE均方根
