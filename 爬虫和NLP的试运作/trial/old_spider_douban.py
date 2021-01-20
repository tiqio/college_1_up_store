# -*- codeing = utf-8 -*-
# @Time : 2020/8/18 18:19
# @Author : 全鹏
# @File : spider_douban.py
# @Software: PyCharm

from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import xlwt
import sqlite3


def main():
    # baseurl = "https://movie.douban.com/top250?start="
    baseurl = "https://movie.douban.com/top250?start="
    # 1. 爬取网页
    datalist = geData(baseurl)
    savepath = ".\\豆瓣电影Top250.xls"
    # 3. 保存数据
    # saveData(datalist, savepath)

    # askURL("https://movie.douban.com/top250?start=0")


# 创建正则表达式对象，表示规则（字符串的模式）
findLink = re.compile(r'<a href="(.*?)">')

# 影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S让换行符包含在字符中

# 影片的片名
findTitle = re.compile(r'<span class="title">(.*)</span>')

# 影片的评分
finkReting = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')

# 影片评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')

# 影片的概况
findInq = re.compile(r'<span class="inq">(.*)</span>')

# 找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 2. 爬取网页
def geData(baseurl):
    datalist = []
    # 调用获取页面信息的函数. 10次
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        # 保存获取到的网页源码
        html = askURL(url)

    # 逐个解析数据
    soup = BeautifulSoup(html, "html.parser")
    # 查找符合要求的字符串，形成列表
    for item in soup.find_all('div', class_="item"):
        # 测试：查看item全部信息
        # print(item)

        # 保存一部电影的所有信息
        data = []
        item = str(item)

        # re库来通过正则表达式查找指定的字符串
        link = re.findall(findLink, item)[0]
        data.append(link)  # 添加链接

        imgSrc = re.findall(findImgSrc, item)[0]
        data.append(imgSrc)  # 添加图片

        titles = re.findall(findTitle, item)  # 片名可能只有一个中文名，没有英文名
        if(len(titles) == 2):
            ctitle = titles[0]   # 添加中文名
            data.append(ctitle)
            otitle = titles[1].replace("/", "")  # 去掉无关的符号
            data.append(otitle)  # 添加外国名

        else:
            data.append(titles[0])
            data.append(' ')  # 外文名留空

        reting = re.findall(finkReting, item)[0]
        data.append(reting)   # 添加评分

        judgeNum = re.findall(findJudge, item)[0]
        data.append(judgeNum)  # 添加评价人数

        inq = re.findall(findInq, item)
        if len(inq) != 0:
            inq = inq[0].replace("。", "")  # 去掉句号
            data.append(inq)   # 添加概述
        else:
            data.append(" ")   # 留空

        bd = re.findall(findBd, item)[0]
        bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)  # 去掉<br/>
        bd = re.sub('/', "", bd)  # 替换/
        data.append(bd.strip())  # 去掉前后的空格

        datalist.append(data)  # 处理好的一部电影信息放入datalist中

    print(datalist)

    return datalist


# 得到指定一个URL的网页内容
def askURL(url):
    head = {     # 模拟浏览器头部信息，项豆瓣服务器发送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
    }     # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


# 3. 保存数据
def saveData(datalist,savepath):
    print("save...")
    # book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    # sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
    # col = ("电影详情链接", "图片链接", "影片的中文名", "影片的外国名", "评分", "评价数", "概况", "相关信息")
    # for i in range(0, 8):
    #     sheet.write(0, i, col[i])
    # for i in range(len(datalist)):
    #     print("第%d条"%(i+1))
    #     data = datalist[i]
    #     for j in range(0, 8):
    #         sheet.write(i+1, j, data[j])
    #
    # book.save(savepath)



if __name__=="__main__":

    main()
    print("爬取完毕 !")
