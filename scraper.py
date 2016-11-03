import time, namesplit
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
# 서버용 from pykeyboard import PyKeyboard

def scraper(url):
    sitename = namesplit.make(url)
    print("start")
    display = Display(visible=0, size=(800,600))
    display.start()
    browser = webdriver.Firefox()
    print("get url")
    browser.get(url)
    time.sleep(2)
    print("ctrl + s")
    # 서버용
    # ActionChains(browser).send_keys(Keys.CONTROL, 's').perform()
    ActionChains(browser).send_keys(Keys.COMMAND, 's').perform()
    time.sleep(3)
    print("enter")
    # 서버용
    # k = PyKeyboard()
    # k.type_string(sitename, interval=0.25)ㅜㅁㅍㄷㄱㅗ싀

    # k.press_key(k.enter_key)
    # k.release_key(k.enter_key)
    # 맥 로컬용
    pyautogui.typewrite(sitename+".html", interval=0.25)
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')
    time.sleep(10) #waiting....enough time
    print("download")
    browser.quit()
    display.stop()