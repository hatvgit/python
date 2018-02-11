# -- coding: UTF-8 --
import requests
from bs4 import BeautifulSoup
from threading import Lock,Thread
import os
basePath = r"/content/mm"
threadLimit = 10
threadNum = 0
os.chdir(basePath)
# 遍历打印出图片地址
urlPool = ["http://www.meitulu.com/item/{}.html".format(str(i)) for i in range(3465, 5645)]
mutex = Lock()
def downloadImg(url):
    dirname = url.split("/")[-1].split(".")[0]
    print(dirname)
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    ordinal = 1
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"}
    linkPool = []
    while True:
        try:
            resp = requests.get(url, headers=headers).text
            soup = BeautifulSoup(resp, "html.parser")
            links = soup.select("body > div.content > center > img")
            for urlLink in links:
                link = urlLink.get("src")
                linkPool.append(link)
                nextPageUrl = soup.findAll("a", {"class": "a1"})[1].get("href")
                if nextPageUrl == url:
                    break
                else:
                    url = nextPageUrl
        except Exception:
                print("Connection Error, or BeautifulSoup going Wrong, forget it:", url)
                break
    for link in linkPool:
        try:
            content = requests.get(link, headers=headers)
            title = str(ordinal) + ".jpg"
            # 文件就保存在工作目录了
            file = open(dirname + "/" + title, "wb")
            print(dirname + "/" + title)
            file.write(content.content)
            file.close()
            ordinal += 1
        except Exception:
            print("Couldn't Parse!", link)
            break
            print('爬取完成')
class MyThread(Thread):
    def __init__(self, url):
        self.url = url
        Thread.__init__(self)
    def run(self):
        downloadImg(self.url)
        mutex.acquire()
        global threadNum
        threadNum -= 1
        mutex.release()
while urlPool != []:
    if threadNum < threadLimit:
        newUrl = urlPool.pop()
        threadNum += 1
        newThread = MyThread(newUrl)
        newThread.start()