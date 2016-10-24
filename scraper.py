import time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
from pykeyboard import PyKeyboard

def scraper(url):
    try:
        split = str(url).split('.')
        if(len(split)==1):
            sitename = split[0]
        elif(len(split)==2):
            sitename = split[1]
        else:
            sitename = split[1]
    except Exception:
        sitename = split[1]
        print("url error: " + url)
    print("start")
    display = Display(visible=0, size=(800,600))
    display.start()
    browser = webdriver.PhantomJS()
    print("get url")
    browser.get(url)
    time.sleep(2)
    browser.save_screenshot(sitename)
    print("ctrl + s")
    ActionChains(browser).send_keys(Keys.COMMAND, 's').perform()
    time.sleep(3)
    print("enter")
    pyautogui.typewrite(sitename+".html", interval=0.25)
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')
    time.sleep(10) #waiting....enough time
    print("download")
    browser.quit()
    display.stop()

#scraper('http://www.11st.co.kr')