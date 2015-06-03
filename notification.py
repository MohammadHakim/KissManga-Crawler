#this file will host my try to notify me of updates Using A web Parser 
#parts of this code were contributed by programmers on http://stackoverflow.com/

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
def getOldCh(String):
    import re
    myfile = open(String,'r+')
    lines = sum(1 for line in myfile)
    myfile.close()
    
    myfile = open(String,'r+')
    old = []
    for title in range(lines):
        old.append(re.search('\d+\.\d+|\d+',myfile.readline().split('\t')[1]).group(0)) 
    myfile.close()
    for title in range(lines):
        old[title] = float(old[title])
    return old
def getHtmlOf(title):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    import urllib2,time,random
    #sleep(random.randint(60,120))
    website = "http://kissmanga.com/Manga/"
    website = website+title
    request = urllib2.Request(website,headers=hdr)
    response = urllib2.urlopen(request)
    page_source = response.read()
    return page_source
def getString(page_source):
	from bs4 import BeautifulSoup
	soup = BeautifulSoup(page_source)
	Chapter = soup.td.a.get_text()
	Title = soup.title.get_text()
	return Chapter,Title
def extractChapterNum(choice, title):
    """This function looks for chapter, ch or numbers in a given choice string
    and utilizes the page title to choose candidate numbers that are assumed to
    be the chapter number"""
    ###I need to create a way to find the chapter numbers
    ##chapter1 ='Yamada-kun to 7-nin no Majo Yamada-kun to 007-nin no Majo 090'
    ##title1 = 'Yamada-kun to 7-nin no Majo manga | Read Yamada-kun to 7-nin no Majo manga online in high quality'
    ##chapter2 = 'Trump (LEE Chae-Eun) Ch.029: The 073rd Cabinet (019)'
    ##title2 = 'Trump (LEE Chae-Eun) manga | Read Trump (LEE Chae-Eun) manga online in high quality'
    ##chapter3 = 'Magician Vol.002.029 Ch.127: Long Night (006)'
    ##title3 = 'Magician manga | Read Magician manga online in high quality'
    ##chapter4 ='Otoyomegatari Vol.006 Ch.034: Shield at Your Back'
    ##title4 ='Otoyomegatari manga | Read Otoyomegatari manga online in high quality'

    #the easiest way to find the chapter number is to look for the two variations ch and chapter
    import re
    #first convert the string to all lower case to avoid the need to account to variations
    choice = choice.lower()
    title = title.lower()
    #make sure you remove any strings appearing in title from choice
    remove = title.split()
    biggie = re.compile('|'.join(map(re.escape,remove)))
    choice = biggie.sub("",choice)
    #before that however try to see if the title has onle one number, that number is probably the chapter number
    chapter = re.findall("\d+\.\d+|\d+",choice)
    #make sure you don't have zeroes in the list
    chapter = [x for x in chapter if float(x)!=0]
    if len(chapter)==1:
        chapter = chapter[0]
    else:
        #first try to find the word chapter in the title
        chapter = choice.split('ch')
        #print chapter[0]
        if len(chapter)>1:
            #If you fall here then the word chapter was found, search in the 1st term for the chapter number
            for n in range(1,len(chapter)):
                #print chapter[n]
                try:
                    chapter = re.search("\d+|\d+\.\d+",chapter[n]).group(0)
                    break
                except:
                    chapter = 1000#meaning there is a problem
        else:
            #If you fall here then chapter was not found try ch instead
            chapter = choice.split('chapter');#print chapter;#CH IN TITLE PROBLEM
            if len(chapter)>1:
                #if you fall here then ch was found, search for the chapter number
                for n in range(1,len(chapter)):
                    try:
                        chapter = re.search("\d+\.\d+|\d+",chapter[n]).group(0);#print chapter
                        break
                    except:
                        continue
            else:
                #if you fall here then neither chapter nor ch were found look for all the numbers in the chapter
                chapter = choice
                chapter = re.findall("\d+\.\d+|\d+",chapter)
                #discard any numbers which appear in the title to do this
                title = re.findall("\d+\.\d+|\d+",title)
                title = list(set(title))
                newchapter = []
                for number in chapter:
                    for occurance in title:
                        #print number,occurance,float(number)!= float(occurance)
                        if(float(number)== float(occurance)):
                            break
                        else:
                            if occurance == (title[len(title)-1]):
                                newchapter.append(number)
                #print newchapter
                if(len(newchapter)==1):
                    chapter = newchapter[0]
                elif(len(newchapter)==0):
                    chapter = chapter[0]
                else:
                    chapter = 1000#meaning there is a problem
    chapter = float(chapter)
    return chapter
def listNewChapters(titles):
	new = []
	for title in titles:
		print "Checking "+title
		Chapter,Title = getString(getHtmlOf(title))
		#cool Now I need to strip the string to get only the numbers
		Number = extractChapterNum(Chapter,Title)
		new.append(Number)
	return new
def textNprint(titles,old,new):
	import datetime
	ToSave = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n'
	total = 0
	for n in range(len(old)):
		if(new[n]>old[n]):
			maybe = "New Chapter"+"("+'%5s'+") "+'%5s'+" for"+'%30s'+". You are now on "+ '%5s'      
			ToSave=ToSave+maybe % (str(new[n]-old[n]),str(new[n]),str(titles[n]),str(old[n])) + '\n'
			#print "New Chapter","(",new[n]-old[n],")",new[n],"for",titles[n],". You are now on", old[n]
			print maybe % (str(new[n]-old[n]),str(new[n]),str(titles[n]),str(old[n]))
			total = total + new[n]-old[n]
			if eval(str(total).split(".")[1]) > 0:
				total = eval(str(total).split(".")[0]) + 1
	print "Total: ",total
	ToSave=ToSave+'\n'+'Total: '+str(total)		
	ToSave=ToSave+(4*'\n')
	for n in range(len(titles)):
		ToSave=ToSave+str(titles[n])
		ToSave=ToSave+str('\t')
		ToSave=ToSave+str(new[n])
		ToSave=ToSave+str('\n')   
	f = open('UpdatedManga.txt','w')
	f.write(ToSave)
	f.close()
	
	



####################################################################################
#first step is to read in the titles

from time import *
print "Program Start"

titles = getTitlesFrom('MangA.txt')
old = getOldCh('MangA.txt')
#now let me try to get a list of the new titles from kissmanga.com
new = listNewChapters(titles)
print 4*'\n'
textNprint(titles,old,new)

print "Program Done"
sleep(20)
