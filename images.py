def getTitlesFrom(String):
    #for that I will need the number of lines
    myfile = open(String,'r+')
    lines = sum(1 for line in myfile)
    myfile.close()
    #to get the list of titles
    myfile = open('MangA.txt','r+')
    titles = []
    for title in range(lines):
        titles.append(myfile.readline().split('\t')[0])
    myfile.close()
    return titles
	
def getHtmlOf(title):
	import urllib2,cookielib
	website = "http://kissmanga.com/Manga/"
	site = website+title
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		   'Accept-Encoding': 'none',
		   'Accept-Language': 'en-US,en;q=0.8',
		   'Connection': 'keep-alive'}

	req = urllib2.Request(site, headers=hdr)
	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()
	page_source = page.read()
	return page_source


def getTitleAsOnWeb(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html)
    Callit = soup.find("a", class_="bigChar").get_text()
    #Callit = Callit.replace('\','')
    Callit = Callit.replace('/','')
    Callit = Callit.replace('?','')
    Callit = Callit.replace(':','')
    Callit = Callit.replace('*','')
    Callit = Callit.replace('"','')
    Callit = Callit.replace('>','')
    Callit = Callit.replace('<','')
    Callit = Callit.replace('|','')
    return Callit
def getImg(page_source):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_source)
    Image = soup.find_all("img")[4].get('src')
    return Image	
def getExtension(url):
	splitted = url.split('/')
	splitted = splitted[len(splitted)-1].split('.')
	extension = splitted[len(splitted)-1]
	return extension
#################################################################	
from time import *
print "Program Start"
titles = getTitlesFrom('MangA.txt')
textFile = ''
for n in range(len(titles)):
	print "downloading Image "+str(titles[n])
	html = getHtmlOf(titles[n])

	Callit = getTitleAsOnWeb(html)
	textFile = textFile + str(Callit) + '\n'
                                
	url = getImg(html)
	extension = getExtension(url)

	filename = str(Callit)+'.'+str(extension)
	import requests
	f = open('thumbs/'+filename,'wb')
	f.write(requests.get(url).content)
	f.close()

myfile = open("thumbs/titles.txt", "w")
myfile.write(textFile)
myfile.close()

print "Program Done"
sleep(30)
##################################################################
