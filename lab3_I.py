#-*- coding: utf8 -*-
import urllib
import urllib2
import re
import os


mainDir = os.getcwd()
numbPages = 15
maxLenUrlsList = numbPages * 10
extensions = ['gif', 'bmp', 'jpg', 'jpeg', 'png', 'js', 'css', 'html', 'ico']


def CorrectAddress(url, mainUrl):
    if url.find('http') < 0:
        correctUrl = mainUrl + url
    else:
        correctUrl = url
    if (url.find('@') > 0) or (url.find('#') > 0) or (url =='/rss'):
        return False
    else:
        return correctUrl

def CreateResourcesList(url):
    content = urllib2.urlopen(url).read()
    img_urls = re.findall('img.*?src="(.*?)"', content)
    img_urls1 = re.findall('href="(.*?)"', content)
    js_urls = re.findall('script.*?src=\"(.*?.js)\"', content)
    js_urls1 = re.findall('link.*?href=\"(.*?.js)\"', content)
    css_urls = re.findall('link.*?href=\"(.*?.css)\"',content)
    urls = img_urls + js_urls + css_urls + js_urls1 + img_urls1
    return urls


def SaveRecourcesUrl(mainUrl, url, count, mainDir):
    extraContent = ''
    newDir = mainDir + '\\' + str(count)
    os.mkdir(newDir)
    os.chdir(newDir)
    correctUrl = CorrectAddress(url, mainUrl)
    content = urllib2.urlopen(correctUrl).read()
    urlsList = CreateResourcesList(correctUrl)
    for i in range(len(urlsList)):
        address = urlsList[i]
        if address[address.rfind('.') + 1 : ] in extensions:
            name = address[address.rfind('/') + 1 : ]
            index = content.find(address)
            extraContent = content[ : index] + './' + name + content[index + len(address):]
            content = extraContent
            extraContent = ''
            if address.find('http') < 0:
                address = mainUrl + address
            if address.find('http') > 0:
                address = address[address.find('http') : ]
            urllib.urlretrieve(address, name)
    fout = open(str(count) + '.html', 'w')
    fout.write(content)
    fout.close()


savedPages = []
count = 1
i = 0
correctUrl = ''
urlsList = []
mainUrl = 'http://lenta.ru'
word = 'книга'
#mainUrl = raw_input(u'Введите адрес URL: ')
#word = raw_input(u'Введите слово, которое будем искать: ')
urlsList.append(mainUrl)

while (i < len(urlsList)) and (len(savedPages) <= numbPages):
    url = urlsList[i]
    correctUrl = CorrectAddress(url, mainUrl)
    if (correctUrl == False):
        urlsList.pop(i)
    else:
        content = urllib2.urlopen(correctUrl).read()
        if (content.find(word) > 0) and (correctUrl not in savedPages) and (len(savedPages) <= numbPages):
            SaveRecourcesUrl(mainUrl, url, count, mainDir)
            os.chdir(mainDir)
            print count
            count += 1
            savedPages.append(correctUrl)
        urlsList += re.findall('a.*?href="(.*?)"',content)
        urlsList.pop(i)
print '.'      
