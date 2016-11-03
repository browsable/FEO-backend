def make(url):
    try:
        split = str(url).split('.')
        splitlength = len(split)
        sitename = ""
        if (splitlength == 1):
            sitename = url
        elif (splitlength == 2):
            sitename = url
        else:
            if (split[0] == 'www'):
                sitename = str(url)[4:]
            else:
                sitename = url
    except Exception:
        print("url error: " + url)

    return sitename