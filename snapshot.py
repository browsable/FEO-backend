def urlpageshot(url, name):
    from selenium import webdriver
    shot = webdriver.PhantomJS();
    shot.set_window_size(1920,1080)
    shot.get(url)
    imgurl = 'static/images/'+name
    shot.save_screenshot(imgurl)
    shot.quit()
    return 'images/'+name