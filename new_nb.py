from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import pyperclip

driver = webdriver.Chrome("module/chromedriver.exe")
id = "ID"
pw = "PW"

login_err_dic = {
    # xPath
    'Auth2' : '//*[@id="call_success"]/div[1]/label',
    'Capture' : '//*[@id="captcha"]'
}
naverUrl = 'https://nid.naver.com/nidlogin.login'
cafeUrl = 'https://m.cafe.naver.com/ca-fe/web/cafes/카페 고유번호/articles/write'

driver.get(naverUrl)

time.sleep(1)


def clipboard_input(user_input):
    temp_copy = pyperclip.paste()
    pyperclip.copy(user_input)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    pyperclip.copy(temp_copy)

e_id = driver.find_element_by_id('id')
e_pw = driver.find_element_by_id('pw')

e_id.clear()
e_id.click()
clipboard_input(id)

e_pw.clear()
e_pw.click()
clipboard_input(pw)

driver.find_element_by_class_name('btn_global').click()

time.sleep(2)

def has_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False

for i in login_err_dic:
    if has_xpath(login_err_dic[i]):
        print("login_err_chk: {}".format(i))
        exit()

driver.get(cafeUrl)

time.sleep(1)
title = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div/textarea')
title.clear()
title.send_keys("Title")
iframes = driver.find_elements_by_css_selector('iframe')

driver.switch_to.frame(iframes[0])
time.sleep(2)
print(driver.page_source)

content = driver.find_element_by_tag_name('body')
# content.click()
content.send_keys('Content')
content.send_keys(Keys.ENTER)
content.send_keys('Content')

driver.switch_to.default_content()