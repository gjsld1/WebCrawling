from libs.crawler import crawl

url="http://www.naver.com"

pageString = crawl(url)
print(pageString)