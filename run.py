import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pyperclip
import time
from pyvirtualdisplay import Display

option = Options()
option.add_argument('window-size=1920x1080')
option.add_argument('--headless')
option.add_argument("lang=ko_KR")
option.add_argument("disable-gpu")

# display = Display(visible=0, size=(1920, 1080))
# display.start()

chrome_dir = 'module/chromedriver'
# driver = webdriver.Chrome(executable_path=chrome_dir, chrome_options=option)
driver = webdriver.Chrome(executable_path=chrome_dir)
# driver.implicitly_wait(2)
driver.get('https://www.naver.com/')
driver.get_screenshot_as_file('capture0.png')
def sleep(s=0.5):
    time.sleep(s)
def has_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False

id1 = 'alsrua7222'
pw1 = '******'
url_cafe = 'https://cafe.naver.com/******'
login_err = {
    'Auth2': '//*[@id="call_success"]/div[1]/label',
    'Capture': '//*[@id="captcha"]'
}
login_btn = driver.find_element_by_class_name('link_login')
login_btn.click()
sleep()

tag_id = driver.find_element_by_id('id')
tag_pw = driver.find_element_by_id('pw')
tag_id.clear()

tag_id.click()
pyperclip.copy(id1)
#tag_id.send_keys(pyperclip.paste()) 캡챠 방지 ㅆㅂ
# tag_id.send_keys(Keys.CONTROL, 'v')
ActionChains(driver).key_down(Keys.CONTROL).send_keys('V').key_up(Keys.CONTROL).perform()
sleep()

driver.get_screenshot_as_file('capture11.png')
tag_pw.click()
pyperclip.copy(pw1)
#tag_pw.send_keys(pyperclip.paste()) 캡챠 방지 ㅆㅂ
# tag_pw.send_keys(Keys.CONTROL, 'v')
ActionChains(driver).key_down(Keys.CONTROL).send_keys('V').key_up(Keys.CONTROL).perform()
sleep(3)


login_btn = driver.find_element_by_class_name('btn_global')
login_btn.click()
sleep()
print("Login Before")
if has_xpath(login_err['Auth2']) == True:
    print("2차 인증 걸려있습니다.")
    exit()
if has_xpath(login_err['Capture']) == True:
    print("캡챠 방지 걸려있습니다.")
    exit()

# 카폐에 들어가서 글쓰기 버튼 누르기
# driver.get(url_cafe)
# write_btn = driver.find_element_by_xpath('//*[@id="cafe-info-data"]/div[4]/a')
# write_btn.click()
# sleep()

# 글쓰기 화면 탭으로 전환하기
# last_tap = driver.window_handles[-1]
# driver.switch_to.window(window_name=last_tap)
# #driver.close()
# sleep()

#iframe 값을 전혀 알 수 없음
#출처: https://dejavuqa.tistory.com/198
# iframes = driver.find_elements_by_css_selector('iframe')
# print("iframes: {}".format(len(iframes)))
# for i, iframe in enumerate(iframes):
#     try:
#         print('%d번째 iframe 입니다.' % i)
#         driver.switch_to.frame(iframes[i])
#         print(driver.page_source)
#         driver.switch_to.default_content()
#     except:
#         driver.switch_to.default_content()
#         print('pass by except: iframes[%d' % i)
#         pass
print("Login After")
driver.get('https://cafe.naver.com/******?iframe_url=%2FArticleWrite.nhn%3Fclubid%3D19543191%26m%3Dwrite')
sleep()
driver.get_screenshot_as_file('capture2.png')
# oEditor = driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[1]/div/div/button[2]')
# oEditor.send_keys(Keys.ENTER)
# oEditor_goto = driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[3]/div[6]/div/div/div[2]/div[2]/a')
# oEditor_goto.send_keys(Keys.ENTER)
# sleep()

# 구버전 프레임 번호
print("Access Cafe Write")
print(driver.window_handles)
iframes = driver.find_elements_by_css_selector('iframe')
print("iframes: {}".format(len(iframes)))
for i, iframe in enumerate(iframes):
    try:
        print('%d번째 iframe 입니다.' % i)
        driver.switch_to.frame(iframes[i])
        print(driver.page_source)
        driver.switch_to.default_content()
    except:
        driver.switch_to.default_content()
        print('pass by except: iframes[%d' % i)
        pass
driver.switch_to.frame(driver.find_element_by_id('cafe_main'))
# driver.switch_to.frame('cafe_main')

# 구버전 글쓰기 메뉴 카테고리
print("Category")
menu = Select(driver.find_element_by_id('boardCategory'))
menu.select_by_visible_text('자유 게시판')

# 구버전 글쓰기 제목
print("Title init")
title = driver.find_element_by_xpath('//*[@id="subject"]')
title.clear()
title.send_keys('Hello World')
sleep()

#직접 내용 쓰고 싶으면 써라
def innerHTML(exStr):
    base = "document.getElementsByTagName('body')[0].innerHTML = \'{}\'".format(exStr)
    return base
def image():
    print("ImageButton")
    Image = driver.find_element_by_xpath('//*[@id="iImage"]/a')
    Image.click()
    sleep()
    # driver.get_screenshot_as_file('capture1.png')
    print("windowHandler")
    last_tap = driver.window_handles[-1]
    driver.switch_to.window(window_name=last_tap)
    # driver.get_screenshot_as_file('capture2.png')
    sleep()

    print("urlImg")
    urlimg = "C:\\Usr\\selenium\\images0.png"
    driver.find_element_by_xpath('//*[@id="pc_image_file"]').send_keys(urlimg)
    sleep()

#나는 이미지를 본문에 삽입하기로 함.
image()

driver.find_element_by_xpath('/html/body/div[3]/header/div[2]/button').click()
sleep(2)

# driver.close()
driver.switch_to.window(driver.window_handles[0])
driver.switch_to.frame(driver.find_element_by_id('cafe_main'))
sleep()

# driver.get_screenshot_as_file('capture3.png')
print(driver.window_handles)

driver.find_element_by_xpath('//*[@id="cafewritebtn"]').click()
sleep(1)
driver.close()
driver.quit()

# display.stop()

# driver.switch_to.frame(driver.find_element_by_id('cafe_main'))
# driver.find_element_by_xpath('//*[@id="cafewritebtn"]').click()
# iframes = driver.find_element_by_css_selector('iframe')
# driver.switch_to.frame(iframes)

# content = driver.find_element_by_id('textbox')


# driver.execute_script(innerHTML('Hello World'))


# content = driver.find_element_by_id('textbox')
# pyperclip.copy("Test")
# content.send_keys(Keys.CONTROL, 'V')


# #driver.get_screenshot_as_file('capture.png')
# list_btn = driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/button')
# #드랍다운 메뉴 버튼일 경우, click() 호출하면 안된다.
# #즉, send_keys(Keys.ENTER)로 호출한다.
# #출처: https://wkdtjsgur100.github.io/selenium-does-not-work-to-click/
# list_btn.send_keys(Keys.ENTER)
# sleep()
#
# list_items = driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[2]/ul/li[9]/button')
# list_items.click()
# sleep()
#
# title = driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[1]/div[2]/div/textarea')
# title.send_keys(Keys.ENTER)
# pyperclip.copy('Test')
# title.send_keys(Keys.CONTROL, 'V')
# sleep()
# title.send_keys(Keys.TAB, Keys.CONTROL, 'V')

# driver.switch_to.frame(iframes[4])
# content = driver.find_element_by_xpath('/html/body')
# pyperclip.copy('Hello World')
# driver.execute_script("document.querySelector('div.se-module-text').textContent = 'sdfsadfsadfsfdgsdf'")
# sleep()
# driver.switch_to.default_content()
#driver.switch_to.frame(driver.find_element_by_id('SmartEditor'))



# context = driver.find_element_by_xpath('//*[@id="SE-ee59c2c0-a40e-4ca4-9f63-be316b9f084a"]/div[1]/div/div[1]/div[2]/section/div[1]')
# context.click()
# pyperclip.copy('Python Selenium Test')
# context.send_keys(Keys.CONTROL, 'V')
# sleep()
#
# send_btn = driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[1]/div/a')
# send_btn.click()
# sleep()