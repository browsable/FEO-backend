import requests, os, zipfile

def transper ():
    sitename='11st'
    files_path = '/Users/browsable/Downloads/'+sitename+'_files'
    html_path = '/Users/browsable/Downloads/'+sitename+'.html'
    dest_file = 'web/'+sitename+'.zip'

    with zipfile.ZipFile(dest_file, 'w') as zf:
        rootpath = files_path
        for (path, dir, files) in os.walk(files_path):
            for file in files:
                fullpath = os.path.join(path, file)
                relpath = sitename+'_files/'+os.path.relpath(fullpath, rootpath)
                zf.write(fullpath, relpath, zipfile.ZIP_DEFLATED)
                zf.write(fullpath, relpath, zipfile.ZIP_DEFLATED)
        zf.write(html_path, sitename+'.html', zipfile.ZIP_DEFLATED)
        zf.close()

    url = 'https://h2test.net/downloads'
    params = {'sitename': sitename}
    requests.get(url, params=params)

transper()