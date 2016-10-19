import time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pykeyboard import PyKeyboard

def scrapper(url):
    display = Display(visible=0, size=(800,600))
    display.start()
    print('getURL')
    browser = webdriver.Firefox()
    browser.get(url)
    time.sleep(2)
    print('Press CTRL+S')
    ActionChains(browser).send_keys(Keys.CONTROL,'s').perform()
    time.sleep(3)
    ActionChains(browser).send_keys(Keys.CONTROL, 's').perform()
    time.sleep(3)
    print('Press ENTER')
    k = PyKeyboard()
    k.press_key(k.enter_key)
    k.release_key(k.enter_key)
    print('Downloading...')
    time.sleep(10) #waiting....enough time
    print(browser.title)
    browser.quit()
    display.stop()