import subprocess
bashCommand = ['curl','--http2','-I','-L','-H','\'Accept: */*\'',
               '-H','\'user-agent: h2-check/1.0.1\'',
               '-H','\'Connection: Upgrade, HTTP2-Settings\'',
               '-H','\'Upgrade: h2c\'','-H','\'HTTP2-Settings: <base64url encoding of HTTP/2 SETTINGS payload\'',
               'google.com']
process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
output, error = process.communicate()

if(str(output).find('HTTP/2')>-1):
    print("HTTP 2 Support")
else:
    print("Not Support")

print(output)