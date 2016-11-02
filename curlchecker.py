# bashCommand = ['curl','--http2','-I','-L','-H','\'Accept: */*\'',
#                '-H','\'user-agent: h2-check/1.0.1\'',
#                '-H','\'Connection: Upgrade, HTTP2-Settings\'',
#                '-H','\'Upgrade: h2c\'','-H','\'HTTP2-Settings: <base64url encoding of HTTP/2 SETTINGS payload\'',
#                'google.com']
def curl(url):
    import subprocess, json
    url = url
    bashCommand = ['curl','https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url='+url+'&key=']

    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()

    if(str(output).find('HTTP/2')>-1):
        print("HTTP 2 Support")
    else:
        print("Not Support")
    output = ' '.join(str(output.decode('utf-8')).replace('\\n','').replace('\'','').split())
    dict = json.loads(output)
    keys = list(dict['formattedResults']['ruleResults'].keys())
    result = []
    for i in keys:
        temp = dict['formattedResults']['ruleResults'][i]['localizedRuleName']+str(dict['formattedResults']['ruleResults'][i]['ruleImpact'])
        result.append(temp)
    return(result)
