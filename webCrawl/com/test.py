from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from itertools import count
import time
import pandas as pd

driver = webdriver.Chrome(
    executable_path="../webdriver/chromedriver"
)

url="http://www.ssfshop.com/8seconds/GM0018120300013/good?dspCtgryNo=SFMA41A04&brandShopNo=BDMA07A01&brndShopId=8SBSS&keyword=&leftBrandNM=&utag=ref_cat:SFMA41A04$ref_brn:BDMA07A01$ref_gtp:GNRL_CTGRY$ref_br:8SBSS$set:1$dpos:25"
driver.get(url)
time.sleep(5)

html = driver.page_source

# HTML 소스코드를 파이썬 객체로 변환
soup = BeautifulSoup(html, 'html.parser')

# 성별/옷분류/모델명
category = soup.select("div.contents > section.flow > span")
sex = category[2].text
branch = category[3].text
print(sex, branch)
cModel = soup.select_one("div.tag > h3.brand > small").text
print(cModel)

# 추가 정보
infos = []
info = []
RESULT_DIRECTORY = '../info/'
additionalInfos = soup.select("div.wear > div > dl > dd > em.on")
for additionalInfo in additionalInfos:
    #print(additionalInfo.text)
    strings = list(additionalInfo.strings)
    print(strings[0])
    if(strings[0]=='\t가을\n\t'): continue
    info.append(strings[0])

infos.append((cModel,sex,branch,info[0],info[1],info[2],info[3]))
table = pd.DataFrame(infos, columns=['model','sex','branch','season','expansion','reflection','lining'])
name = '{0}/table_info_'+cModel+'.csv'
table.to_csv(name.format(RESULT_DIRECTORY), encoding="utf-8", mode='w')

# 실측 사이즈
#clothSizes = soup.select("table.tbl_info[summary='Size'] > tbody > tr")
#for clothSize in clothSizes:
#    print(clothSize.text)


# 고객 사이즈 리뷰
reviewCnt = soup.find("em", id="review_size_h3_em").text
pageNum = int(reviewCnt)/10
temp = int(pageNum)
if(pageNum-temp!=0): pageNum=temp+1

reviews = []
RESULT_DIRECTORY = '../review'
for page in count(1):
    script = 'getMySizeSet(0,%d,2)'%page #js코드
    if page!=1:
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
        reviews.append((cModel,height,weight,fit,size,evaluation))

    if page==pageNum:
        break
    #next = soup.select("#mySizePaging")
    #if next is None:
    #    break

table = pd.DataFrame(reviews, columns=['model','height','weight','fit','size','evaluation'])
name = '{0}/table_review_'+cModel+'.csv'
table.to_csv(name.format(RESULT_DIRECTORY), encoding="utf-8", mode='w')

#results = soup.find_all('table', id='goodsMySizeList')
#print(results)
#for result in results:
#    print(result)

driver.close()