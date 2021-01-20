import requests
import bs4
import re
import openpyxl
import time

def mix(data):
  array_all = re.findall(r'\w+', data)
  # 使用\w*将每个空格纳入考虑范围,用\w+则不是
  mix = ''
  for i in array_all:
    mix += i
  return mix

def get_data_bayes():
  bayes = input("请确定是否使用贝叶斯模式(yes|no):")

  if (bayes == 'yes'):
    urls = ["https://www.cnbeta.com/category/movie.htm",
            "https://www.cnbeta.com/category/music.htm",
            "https://www.cnbeta.com/category/game.htm",
            "https://www.cnbeta.com/category/comic.htm",
            "https://www.cnbeta.com/category/funny.htm",
            "https://www.cnbeta.com/category/science.htm",
            "https://www.cnbeta.com/category/soft.htm"
            ]
    headers = {
      "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    res_all = ''
    for url in urls:
      res = requests.get(url, headers=headers)
      res.encoding = 'utf-8'
      res_all += res.text 
    data = []
    soup = bs4.BeautifulSoup(res_all, 'html.parser')
    items = soup.find_all(class_='cnbeta-update-list category-update')
    for item in items:
      targets = item.find_all('div', class_='item')
      for target in targets:
        # 注意,并不是所有的item都是一个数据格式,需要去除异常
        if (hasattr(target.div, 'label') and hasattr(target.dl, 'dd') and target.div.ul.li.next_sibling.next_sibling.a.attrs['href']):
          row = []
          row.append(target.div.label.text)
          row.append(target.dl.dd.p.text)
          row.append(target.div.ul.li.next_sibling.next_sibling.a.attrs['href'])
          data.append(row)
    t = time.localtime()
    time_fix = time.strftime("%Y-%m-%d-%H时",t)
    with open(r"C:\Users\HP\Desktop\AI\crawler_stage_3\cnBeta\txt\{}{}.txt".format('贝叶斯', time_fix), 'w', encoding='utf-8') as f:
      # 经实验可知,在文件名相同时,文件是以覆盖的方式写入,所以没有必要去用os库来判断文件是否存在
      f.write("文章出处  文章内容  文章链接\n")
      for each in data:
        record = each[0] + '  ' + mix(each[1]) + '  ' + each[2] + '\n'
        # 有些each[1]是由两个字符串相隔而来的,并不是一个字符串,从html也可以看出来
        f.write(record)
    return 1

  elif (bayes == 'no'):
    print("您已经进入单通道模式")
  else: 
    print("请输入你所选择形式的正确书写格式")
    get_data_bayes()


def get_data(url):
  headers = {
      "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
  }
  res = requests.get(url, headers=headers)
  res.encoding = 'utf-8'
  return res


def get_data_all(url, pnum):
  headers = {
      "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
  }
  res_all = requests.get(url, headers=headers)

  for i in range(2, pnum+1):
    headers = {
      "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    params = {
      'type': 'catid|8',
      'page': '{}'.format(i),
      '_csrf': 'hJGqIsW92j9gZIb5GDBKqB4QtzcrCzUahzjR9aTjR3zb_el9s4WXZgIM9LJZaXjsK3znA144bVvQWoa44tIUKg==',
      '_': '1608381362242'
    }
    # douban的事实证明requests的params是可行的
    # 从cnBeta猜想:如果缺少关键参数,params不行但不会报错-------------------------------------?
    res = requests.get(url, params=params, headers=headers)
    res_all += res
  res_all.encoding = 'utf-8'
  return res_all


def to_excel(data):
  wb = openpyxl.Workbook()
  wb.guess_types = True
  ws = wb.active 
  ws.append(['文章出处', '文章内容', '文章链接'])
  for item in data:
    ws.append(item)
  t = time.localtime()
  time_fix = time.strftime("%Y-%m-%d-%H时",t)
  wb.save(r"C:\Users\HP\Desktop\AI\crawler_stage_3\cnBeta\xlsx\{}{}.xlsx".format(data[0][0], time_fix))


def to_txt(data):
  t = time.localtime()
  time_fix = time.strftime("%Y-%m-%d-%H时",t)
  with open(r"C:\Users\HP\Desktop\AI\crawler_stage_3\cnBeta\txt\{}{}.txt".format(data[0][0], time_fix), 'w', encoding='utf-8') as f:
    f.write("文章出处  文章内容  文章链接\n")
    for item in data:
      row = item[0] + '  ' + item[1] + '  ' + item[2] + '\n'
      f.write(row)


def choose(data):
  form = input("请输入你要导入的格式(excel|txt):")
  if (form == 'excel'):
    to_excel(data)
  elif (form == 'txt'):
    to_txt(data)
  else:
    print("请输入你所选择形式的正确书写格式")
    choose(data)


def main():
  # 获取数据(如果想获取更多的数据,就要使用Ajax的技术)
  # 以XMLHttpRequest的对象作为载体,通过XML或json与服务器进行交互,jquery中的ajax就是对xhr的封装
  status = get_data_bayes()
  if (status == 1):
    print("您已经成功完成贝叶斯爬取")
    return 0

  url = input("请输入你要爬取的网址:")
  try:
    res = get_data(url)
  except Exception as e:
    print("您爬取的网址不适配该爬虫")
    return 0
  # pnum = input("请输入你要爬取的批数:")
  # res = get_data_all(url, pnum)
 
  # 处理数据
  data = []
  soup = bs4.BeautifulSoup(res.text, 'html.parser')
  content = soup.find(class_='cnbeta-update-list category-update')
  targets = content.find_all('div', class_='item')
  for item in targets:
    # 注意,并不是所有的item都是一个数据格式,需要去除异常
    if (hasattr(item.div, 'label') and hasattr(item.dl, 'dd') and item.div.ul.li.next_sibling.next_sibling.a.attrs['href']):
      row = []
      row.append(item.div.label.text)
      row.append(item.dl.dd.p.text)
      row.append(item.div.ul.li.next_sibling.next_sibling.a.attrs['href'])
      data.append(row)

  choose(data)

if __name__ == '__main__':
  main()
  
    

