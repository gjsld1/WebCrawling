from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

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

mySizeLists = soup.select("#goodsMySizeList > tbody > tr")
for mySizeList in mySizeLists:
    print(mySizeList.text)


#results = soup.find_all('table', id='goodsMySizeList')
#print(results)
#for result in results:
#    print(result)

driver.close()
