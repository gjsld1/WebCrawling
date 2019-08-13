from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from itertools import count
import time
import re
import pandas as pd

driver = webdriver.Chrome(
                          executable_path="../webdriver/chromedriver"
                          )

url="http://www.ssfshop.com/8seconds/GM0018121103186/good?dspCtgryNo=SFMA41A03&brandShopNo=BDMA07A01&brndShopId=8SBSS&keyword=&leftBrandNM=&utag=ref_cat:SFMA41A03$ref_brn:BDMA07A01$ref_gtp:GNRL_CTGRY$ref_br:8SBSS$set:1$dpos:9"

driver.get(url)
time.sleep(5)

html = driver.page_source

# HTML 소스코드를 파이썬 객체로 변환
soup = BeautifulSoup(html, 'html.parser')

# 성별/옷분류/모델명
sex = driver.find_element_by_xpath('//*[@id="location"]/span[3]/a').text

print(sex)
branch = driver.find_element_by_xpath('//*[@id="location"]/span[4]/a').text
print(branch)
cModel = driver.find_element_by_xpath('//*[@id="content"]/section[2]/div[1]/div[2]/h3/small').text
print(cModel)

# 추가 정보
infos = []
info = []
RESULT_DIRECTORY = '../info/'
# 추가 정보
additionalInfos = soup.select("div.wear > div > dl > dd > em.on")
for additionalInfo in additionalInfos:
    #print(additionalInfo.text)
    strings = list(additionalInfo.strings)
    #print(strings[0])
    info.append(strings[0])
if len(info) > 4:
    for temp in range(1, len(info) - 3):
        info[0] = info[0] + info[temp]
    
    for temp in range(len(info) - 3, len(info)):
        info[temp - 1] = info[temp]

var_0 = re.sub('\t', '', info[0])
var0 = re.sub('\n', '', var_0)
var_1 = re.sub('\t', '', info[1])
var1 = re.sub('\n', '', var_1)
var_2 = re.sub('\t', '', info[2])
var2 = re.sub('\n', '', var_2)
var_3 = re.sub('\t', '', info[3])
var3 = re.sub('\n', '', var_3)

infos.append((cModel, sex, branch, var0, var1, var2, var3))
table = pd.DataFrame(infos, columns=['model', 'sex', 'branch', 'season', 'expansion', 'reflection', 'lining'])
name = '{0}/table_info_' + cModel + '.csv'
table.to_csv(name.format(RESULT_DIRECTORY), encoding="utf-8", mode='w')

reviewCnt = soup.find("em", id="review_size_h3_em").text
pageNum = int(reviewCnt) / 10
temp = int(pageNum)
if (pageNum - temp != 0): pageNum = temp + 1

reviews = []
RESULT_DIRECTORY = '../review/'
for page in count(1):
    
    script = 'getMySizeSet(0, 300, %d)' % page
    if page != 1:
        driver.execute_script(script)  # js실행
    time.sleep(5)

html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    mySizeLists = soup.select("#goodsMySizeList > tbody > tr")
    
    for mySizeList in mySizeLists:
        strings = list(mySizeList.strings)
        print(strings)
        if strings[0] == '해당 범위로 등록된 사이즈 리뷰가 없습니다.':
            continue
        if strings[0] == '키':
            continue
        if strings[0] == " ":
            continue
        if strings[2] == " ":
            continue
        if strings[4] == " ":
            continue
        if strings[6] == " ":
            continue
        if strings[8] == " ":
            continue
        
        height = strings[0]
        weight = strings[2]
        fit = strings[4]
        size = strings[6]
        evaluation = strings[8]
        reviews.append((cModel, height, weight, fit, size, evaluation))
    
    if page == pageNum:
        break

table = pd.DataFrame(reviews, columns=['model', 'height', 'weight', 'fit', 'size', 'evaluation'])
name = '{0}/table_review_' + cModel + '.csv'
table.to_csv(name.format(RESULT_DIRECTORY), encoding="utf-8", mode='w')

driver.close()s
