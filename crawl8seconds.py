from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from itertools import count
import time
import pandas as pd

driver = webdriver.Chrome(
                          executable_path="../webdriver/chromedriver"
                          )

url="http://www.ssfshop.com/8seconds/GM0018120501196/good?dspCtgryNo=SFMA41A02&brandShopNo=BDMA07A01&brndShopId=8SBSS&keyword=&leftBrandNM=&utag=ref_cat:SFMA41A02$ref_brn:BDMA07A01$ref_gtp:GNRL_CTGRY$ref_br:8SBSS$set:1$dpos:1"
driver.get(url)
time.sleep(5)

html = driver.page_source

# HTML 소스코드를 파이썬 객체로 변환
soup = BeautifulSoup(html, 'html.parser')

additionalInfos = soup.select("div.wear > div > dl")
for additionalInfo in additionalInfos:
    print(additionalInfo.text)

clothSizes = soup.select("table.tbl_info[summary='Size'] > tbody > tr")
for clothSize in clothSizes:
    print(clothSize.text)


reviewCnt = soup.find("em", id="review_size_h3_em").text
pageNum = int(reviewCnt)/10
temp = int(pageNum)
if(pageNum-temp!=0): pageNum=temp+1

results = []
RESULT_DIRECTORY = '..'
for page in count(1):
    script = 'getMySizeSet(0,%d,2)'%page #js코드
    driver.execute_script(script) #js실행
    time.sleep(5)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    mySizeLists = soup.select("#goodsMySizeList > tbody > tr")
    for mySizeList in mySizeLists:
        strings = list(mySizeList.strings)
        print(strings)
        if strings[0]=='해당 범위로 등록된 사이즈 리뷰가 없습니다.':
            continue
        if strings[0]=='키':
            continue
        height = strings[0]
        weight = strings[2]
        fit = strings[4]
        size = strings[6]
        evaluation = strings[8]
        results.append((height,weight,fit,size,evaluation))
    
    if page==10:
        break
    next = soup.select("#mySizePaging")
    if next is None:
        break

table = pd.DataFrame(results, columns=['height','weight','fit','size','evaluation'])
table.to_csv('{0}/table_review.csv'.format(RESULT_DIRECTORY), encoding="utf-8", mode='w')

#results = soup.find_all('table', id='goodsMySizeList')
#print(results)
#for result in results:
#    print(result)

driver.close()
