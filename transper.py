import requests, os


def transper ():
    path = os.path.abspath('/Users/browsable/downloads');
    assert os.path.exists (path)
    print("")
    print(path)
    url = 'https://h2test.net/file_receive'
    files = {'file': open(path+'/11st.html', 'rb')}

    r = requests.post(url, files=files)
    print(url)
    print(r.text)


transper()