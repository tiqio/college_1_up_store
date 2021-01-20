import requests
import bs4
import re 
import openpyxl

def open_url(url):
  headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.60"}
  res = requests.get(url, headers=headers)
  return res

def find_data(res):
  data = []
  soup = bs4.BeautifulSoup(res.text, 'html.parser')
  content = soup.find(id="Cnt-Main-Article-QQ")
  # 先锁定html的部分,去除js,find特性是只会返回第一个匹配的文本
  target = content.find_all("p", style="TEXT-INDENT: 2em")
  # 可以通过属性节点获取元素节点,find_all会将所有匹配到的html组合形成列表,进过实验知是可以遍历的
  # <class 'bs4.element.ResultSet'>
  target = iter(target)
  # 可以用iter转化为同内容的可迭代类型
  # <class 'list_iterator'>
  # 是python最强大的功能之一,iter和next是基本的方法,可以调用next方法进行迭代
  for each in target:
    if each.text.isnumeric():
      # 这里的迭代器是根据each的判断进行的(式前加变化
      data.append([
        re.search(r'\[(.+)\]', next(target).text).group(1),
        # group之前是一个匹配对象,调用group得到的是一个匹配的字符串
        re.search(r'\d.*', next(target).text).group(),
        re.search(r'\d.*', next(target).text).group(),
        re.search(r'\d.*', next(target).text).group()
        # 括号代表分组,group可以把匹配的组打印出来,而group括号里如果没有数字就是全部打印
        # 注意打印的下标从1开始
      ])
  return data

def to_excel(data):
  wb = openpyxl.Workbook()
  # 在刚开始使用openpyxl的时候，不需要直接在文件系统中创建一个文件，仅仅需要导入Workbook类并开始使用它
  wb.guess_types = True
  # 通过guess_types判断保存的是数字还是文档
  ws = wb.active
  # 激活传入功能
  ws.append(['城市', '平均房价', '平均工资', '房价工资比'])
  for each in data:
    ws.append(each)
    # 每一个数组都是一行
  wb.save("2017年中国主要城市房价工资比排行榜.xlsx")

def main():
  url = "http://news.house.qq.com/a/20170702/003985.htm"
  res = open_url(url)
  data = find_data(res)
  to_excel(data)

if __name__ == '__main__':
  main()


