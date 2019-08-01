from selenium import webdriver


driver = webdriver.Chrome('Downloads/chromedriver')
driver.get("http://www.google.co.kr/maps")
driver.implicitly_wait(3)

#assert "Google" in driver.title
#elem = driver.find_element_by_name("q")
#elem = clear()
#elem.send_keys("selenium")
#elem.submit()

#assert "No results found." not in driver.page_source
#driver.close()

elem = driver.find_element_by_id("searchboxinput")
elem.send_keys("restaurant")

elem = driver.find_element_by_id("searchbox-searchbutton")
elem.click()

e = driver.find_element_by_class_name("widget-pane-content-holder")
e.text
