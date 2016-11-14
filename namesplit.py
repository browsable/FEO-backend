import re
def make(url):
    try:
        sitename = re.sub(u'(.*?//|www.)', "", url)
        sitename = re.sub(u'(/.*)', "", sitename)
    except Exception:
        print("url error: " + url)
    return sitename