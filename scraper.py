import time
from pyvirtualdisplay import Display
from selenium import webdriver
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
    # start
    display = Display(visible=0, size=(800,600))
    display.start()
    browser = webdriver.PhantomJS()
    # get url
    browser.get(url)
    time.sleep(2)
    # press ctrl + s
    ActionChains(browser).send_keys(Keys.COMMAND, 's').perform()
    time.sleep(3)
    # press enter
    pyautogui.typewrite(sitename+".html", interval=0.25)
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')
    time.sleep(10) #waiting....enough time
    # download
    browser.quit()
    display.stop()

scraper('http://www.11st.co.kr')