from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import re

class Naver():
    def __init__(self, mode = False):
        option = Options()
        if mode:
            option.add_argument('--headless')
        option.add_argument('window-size=1920x1080')
        option.add_argument("lang=ko_KR")
        option.add_argument("disable-gpu")
        # if mode:
        #     self.add_argument('--headless')
        # self.add_argument('window-size=1920x1080')
        # self.add_argument("lang=ko_KR")
        # self.add_argument("disable-gpu")

        driver_dlr = 'module/chromedriver'
        self.driver = webdriver.Chrome(executable_path=driver_dlr, chrome_options=option)
        self.n_id = ""
        self.n_pw = ""
        self.title = ""
        self.content = ""
        self.sleep_sec = 0.5
        # 19543191 = lol kor
        self.cafeID = 19543191
        # 2 = 자유 게시판
        self.menuID = 2
        self.HeadlessMode = mode
        self.BTime = ""
        self.imgUrl = ""
        self.writerUrl = 'https://cafe.naver.com/ArticleWrite.nhn?m=write&clubid={0}&menuid={1}'
        self.login_err_dic = {
            # xPath
            'Auth2' : '//*[@id="call_success"]/div[1]/label',
            'Capture' : '//*[@id="captcha"]'
        }
        self.old_editor_iframe = 'cafe_main'

    # def __del__(self):
    #     self.driver.close()
    #     self.driver.quit()

    def run(self, func):
        def wrapper(*args, **kwargs):
            try:
                print("Log: %s Started" % func.__name__)
                func(*args, **kwargs)
            except:
                print("Log: %s Error" % func.__name__)
            finally:
                self.sleep()
        return wrapper

    def sleep(self):
        time.sleep(self.sleep_sec)

    def has_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
            return True
        except:
            return False

    def login_err_chk(self):
        for i in self.login_err_dic:
            if self.has_xpath(self.login_err_dic[i]):
                print("login_err_chk: {}".format(i))
                exit()

    def login(self):
        self.driver.get('https://nid.naver.com/nidlogin.login')
        self.sleep()
        e_id = self.driver.find_element_by_id('id')
        e_pw = self.driver.find_element_by_id('pw')
        e_id.clear()
        e_pw.clear()
        if self.HeadlessMode:
            # Headless Mode - 유료, 배포 전용
            print("Headless mode 지원 불가")
            exit()
        else:
            # Not Headless Mode - 무료, 오픈 소스 전용
            e_id.click()
            self.clipboard_input(self.n_id)
            e_pw.click()
            self.clipboard_input(self.n_pw)
            self.driver.find_element_by_class_name('btn_global').click()
        self.login_err_chk()

    def write(self):
        # 메인으로 작용할 함수.
        # 접속하려는 url에 cafeID와 menuID 포맷.
        url = 'https://cafe.naver.com/ArticleWrite.nhn?m=write&clubid={0}&menuid={1}'.format(self.cafeID, self.menuID)
        self.driver.get(url)
        self.sleep()

        # cafe_main iframe를 찾고 제목, 콘텐트를 설정한다.
        # self.driver.switch_to.frame(self.driver.find_element_by_id('cafe_main'))
        o_title = self.driver.find_element_by_id('subject')
        o_title.clear()
        o_title.send_keys(self.title)

        # How to use it?
        # 1. Smart Editor 2.0으로 만든 content(HTML)를 불러온다.
        # 2. innerHTML에 content를 넣어 추가한다.
        # 3. 대표 이미지를 설정하고 싶다면 사진 업로드를 추가해야 한다.
        self.driver.execute_script(self.innerHTML(self.content))
        self.driver.switch_to.default_content()
        self.insertRPimg()
        self.Timer()
        self.submit()

    def submit(self):
        self.driver.switch_to.default_content()
        # self.driver.switch_to.frame(self.driver.find_element_by_id('cafe_main'))
        self.driver.find_element_by_id('cafewritebtn').click()

    def getIframes2Pagesource(self):
        iframes = self.driver.find_elements_by_css_selector('iframe')
        for i, iframe in enumerate(iframes):
            try:
                self.driver.switch_to.frame(iframes[i])
                print("iframes[%d]'s has data" % i)
                print(self.driver.page_source)
                self.driver.switch_to.default_content()
            except:
                self.driver.switch_to.default_content()
                print("iframes[%d]'s None" % i)
                pass

    def clipboard_input(self, user_input):
        temp_copy = pyperclip.paste()
        pyperclip.copy(user_input)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        pyperclip.copy(temp_copy)
    # @run
    # def S2C(self, content = "Hello World"):
    #     # String to Content(HTML)
    #     tmp = ""
    #     return tmp

    def innerHTML(self, content: str):
        iframe = self.driver.find_element_by_css_selector('iframe')
        self.Check_iframe()
        self.driver.switch_to.frame(iframe)
        time.sleep(1) # 평균 1초로 잡아줌.
        base = "document.getElementsByTagName('body')[0].innerHTML = \'{}\'".format(content)
        return base

    def insertRPimg(self):
        if not self.imgUrl:
            return
        self.driver.find_element_by_xpath('//*[@id="iImage"]/a').click()
        self.sleep()

        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.sleep()

        self.driver.find_element_by_xpath('//*[@id="pc_image_file"]').send_keys(self.imgUrl)
        self.sleep()

        self.driver.find_element_by_xpath('/html/body/div[3]/header/div[2]/button').click()
        time.sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[0])
    def Timer(self):
        if not self.BTime:
            return
        option = Options()
        if self.HeadlessMode:
            option.add_argument('--headless')
        option.add_argument('window-size=1920x1080')
        option.add_argument("lang=ko_KR")
        option.add_argument("disable-gpu")
        driver_time = webdriver.Chrome("module/chromedriver.exe", chrome_options=option)
        driver_time.get("https://time.navyism.com/?host=www.naver.com")

        spl = self.BTime.split(':')
        while True:
            a = driver_time.find_element_by_id('time_area').text

            time = re.findall("[0-9]+", a)
            print(time)
            if time[3] == spl[0] and time[4] == spl[1] and time[5] == spl[2]:
                break
        driver_time.quit()

    def Check_iframe(self):
        iframes = self.driver.find_elements_by_css_selector('iframe')
        for i, iframe in enumerate(iframes):
            try:
                print('%d번째 iframe 입니다.' % i)
                self.driver.switch_to.frame(iframes[i])
                print(self.driver.page_source)
                self.driver.switch_to.default_content()
            except:
                self.driver.switch_to.default_content()
                print('pass by except: iframes[%d' % i)
                pass
    def main(self):
        self.login()
        self.driver.get_screenshot_as_file("capture.png")
        self.write()
        time.sleep(1)
        # self.run(self.login)
        # self.run(self.write)