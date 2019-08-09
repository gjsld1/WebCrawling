from selenium import webdriver
import time
driver = webdriver.Chrome(
    executable_path="../webdriver/chromedriver"
)

url = "https://www.instagram.com/explore/tags/%EB%B0%9C%EB%A0%88/"
driver.get(url) # 주소 입력 후 enter
time.sleep(5)

pageString = driver.page_source
print(pageString)

# 인스타 껍데기
# 인스타 내용 <div class="Nnq7c">

driver.close()
