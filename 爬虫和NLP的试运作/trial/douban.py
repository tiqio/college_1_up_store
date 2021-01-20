import requests
import bs4
import re

def open_url(url):
  # 使用代理
  # proxies = {"http": "127.0.0.1:1000", "https": "127.0.0.1:1000"}
  headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.60'}
  # 根据RFC2616，HTTP Method是区分大小写的，而Header是不区分的
  res = requests.get(url, headers=headers)
  # url params headers data都是属性,params以json的""内部格式进行处理
  return res

def find_movies(res):
  soup = bs4.BeautifulSoup(res.text, 'html.parser')
  # txt是文本文件,text是二进制文件,使用响应的二进制文件解析成html(后头是解析格式)
  # 最好先看一下res.text是不是html的形式,不是的话就得用re来提取
  # 方法:1.形成html树 2

  # with open('items.txt', 'w', encoding='utf-8') as file1:
  #   file1.write(res.text)

  # 电影名
  movies = []
  targets = soup.find_all("div", class_="hd")
  # 基于关键字,id被允许,而class不被允许,需要用class_
  # 以列表的形式对解析出来的html进行了获取
  for each in targets:
    movies.append(each.a.span.text)
  # 1. movies mx1

  # 评分
  ranks = []
  targets = soup.find_all("span",  class_="rating_num")
  for each in targets:
    ranks.append('评分: %s' % each.text)
  # 2. ranks mx1

  # 资料
  messages = []
  targets = soup.find_all("div", class_="bd")
  for each in targets:
    try:
      messages.append(each.p.text.split('\n')[1].strip() + each.p.text.split('\n')[2].strip())
      # 仅仅获取前两行的资料
    except:
      continue
  # 3. messages mx1 将两行压缩为一行,加号是没有空隙的,逗号是有空隙的

  result = []
  length = len(movies)
  for i in range(length):
    result.append(movies[i] + ranks[i] + messages[i] + '\n')
  # 将所有结果进行汇总,形成以一行为元素的列表,可以说是一篇文章的逆向,后头有个换行符
  # fr = open(filename)
  # arrayLines = fr.readlines()
  # 模仿txt文件的打开方式,将二进制转化为文本文档
  return result

# 找出一共有多少页面
def find_depth(res):
  soup = bs4.BeautifulSoup(res.text, 'html.parser')
  depth = soup.find('span', class_='next').previous_sibling.previous_sibling.text
  return int(depth)

def main():
  host = "https://movie.douban.com/top250"
  res = open_url(host)
  depth = find_depth(res)


  result = []
  for i in range(depth):
    url = host + '/?start=' + str(25*i)
    res = open_url(host)
    # 返回url对应的响应体,并针对响应体进行处理
    result.extend(find_movies(res))
    # 衔接代表电影信息的每一行

  with open("豆瓣TOP250电影.txt", 'w', encoding='utf-8') as f:
    for each in result:
      f.write(each)
  # 使用上下文管理器可以处理异常,也可以默认释放

if __name__ == '__main__':
  main()
    