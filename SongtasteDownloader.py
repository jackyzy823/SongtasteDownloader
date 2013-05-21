from urllib import urlopen, urlretrieve, urlencode
import re
from base64 import decodestring
# TODO: a javascript version ready to be finished





def search(name):
    try:
        from bs4 import BeautifulSoup
    except:
        print "Sorry,we need module called BeautifulSoup"
        exit()
    u = urlopen('http://www.songtaste.com/search.php?' + urlencode({'keyword': name})).read()
    soup = BeautifulSoup(u)
    m = soup.findAll('td', {"class": "singer"})
    for item in m:
        print item.text
        print getSize(Media(item.a['href'].split('/')[-2]))

    '''
    for item in m:
        print item.text
        print "-----------------------------------"
    '''


def getSize(info):
    import httplib
    import urlparse
    up = urlparse.urlparse(info[0])
    httpCon = httplib.HTTPConnection(up[1])
    httpCon.request('GET', up[2])
    response = httpCon.getresponse()
    if response.status == 200:
        size = int(response.getheader('content-length')) / 1024.0 / 1024.0
    else:
        size = 0
    httpCon.close()
    return size


def rayfileProcess(url):
    # Example:http://224.cachefile10.rayfile.com/f0ba/zh-cn/download/0b98dfb0622566204ccbf8774a4b23a5/preview.mp3
    pg = urlopen('http://www.rayfile.com/files/' + url.split('/')[-2]).read()
    pa1 = re.compile('var vid = "([0-9\-a-zA-Z]*)"')
    pa2 = re.compile('var vkey = "([0-9A-Za-z]*)"')
    u1 = pa1.search(pg).groups()[0]
    u2 = pa2.search(pg).groups()[0]
    referurl = 'http://www.rayfile.com/zh-cn/files/' + u1 + '/' + u2 + '/'
    pg2 = urlopen(referurl).read()
    pa3 = re.compile("var downloads_url = \['(http://[A-Za-z0-9\./\-\%]*)'\]")
    res = pa3.search(pg2)
    # Nees http-headers
    downloadUrl = res.groups()[0]
    return (downloadUrl,referurl)


def Media(songid):
    IsRayfile=0
    mediadown = 'http://huodong.duomi.com/songtaste/?songid=' + songid
    mediapage = urlopen(mediadown).read()
    pattern = re.compile(r'http://[0-9A-Za-z/\-\.]*\.(mp3|MP3)')
    downloadURL = pattern.search(mediapage).group()
    try:
        pattern2 = re.compile('var songname = "([A-Za-z0-9\+/=]*)"')
        filename = decodestring(pattern2.search(mediapage).groups()[0])
    except:
        print "Pattern1 failed"
        filename = decodestring(mediapage[mediapage.index('var songname') + 16:mediapage.index('var url') - 16])
    filetype = downloadURL.split('.')[-1]
    Info = (downloadURL, filetype, filename,IsRayfile)
    if "rayfile"in Info[0]:
        print "Try to download from rayfile"
        IsRayfile=1
        Info = (rayfileProcess(Info[0]), filetype, filename,IsRayfile) #rayfileProcess is a tuple ,so Info =((,),,,)
    return Info


def cbk(a, b, c):
    # print process
    '''
    @a: Downloaded Data block
    @b: size of a block
    @c: total Size
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%.2f%%' % per
    # ready to do:os.system('cls')
    # TODO: x.x /total Size


def download(info, path):
    # if "rayfile" in info[0]:
    #    print "Sorry,We can't get song from rayfile"
    #    return 0
    print '%s is ready to be downloaded' % info[2] + '\n'
    filepath = path + '%s' % info[2] + '.' + info[1]
    # a, b = urlretrieve(info[0], filepath,cbk)  #print process
    if info[3]==0:
        a, b = urlretrieve(info[0], filepath)
    else:
        import urllib2
        refer=info[0][1]
        print info
        req=urllib2.Request(info[0][0],headers={'Refer':refer,'Cookie':'ROXCDNKEY=b651; rayfile_weibo=no; __utma=115050116.932316634.1363494912.1363494912.1363494912.1; __utmb=115050116; __utmc=115050116; __utmz=115050116.1363494912.1.1.utmccn=(referral)|utmcsr=douban.com|utmcct=/note/56600784/|utmcmd=referral'})
        content=urllib2.urlopen(req).read()
        with open(filepath,'w') as f:
            f.write(content)
        b=content.headers
    print '%s.%s' % (info[2], info[1]) + ' has been downloaded successfully in ' + path + '\n'
    print 'FileSize: %.2f MB' % (int(dict(b)['content-length']) / 1024.0 / 1024.0) + '\n'


def main():
    URL = raw_input('URL:')
    if URL.isdigit():
        songid = URL
    else:
        songid = URL.split('/')[URL.split('/').index('song') + 1]
    path = 'D:/My Music/'
    download(Media(songid), path)


def test():
    name = raw_input('name:')
    search(name)
    pass

if __name__ == '__main__':
    while True:
        # test()
        main()
        # input('Method')
