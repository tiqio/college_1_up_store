def ss(d):
  d += 1
  return d
  # 在函数作用域中仅仅是传值并进行处理

a = 2
for i in range(2):
  print(i)
  print(ss(a))
  print(ss(a))