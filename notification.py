#This file hosts code which generates a list of updated manga chapters of interest from KissManga.com
#parts of this code were contributed by programmers on http://stackoverflow.com/
def getOldTitleNChap(String):
    myfile = open(String,'r+')
    titles = []
    old = []
    for line in myfile:
        splitLine = line.split('\t')
        titles.append(splitLine[0])
        old.append(float(splitLine[1]))
    return titles, old
def getHtmlOf(title,scraper):
    website = "http://kissmanga.com/Manga/"
    website = website+title
    page_source = scraper.get(website).content
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
    import re
    try:
        #if the string CH is found (ch., ch, chapter, chap., etc)
        temp = re.findall('ch[\w\s,.]+?\d+', choice, re.IGNORECASE)[-1]
        chapter = re.search('\d+\.\d+|\d+',temp).group(0)
    except (AttributeError, IndexError):
        #if there is a single digit in the chapter string
        remove = title.split()#remove white spaces
        biggie = re.compile('|'.join(map(re.escape,remove)))#remove strings which appear in the title string from the chapter string
        choice = biggie.sub("",choice)
        chapter = re.findall("\d+\.\d+|\d+",choice)#find all the numbers in the chapter string
        chapter = [x for x in chapter if float(x)!=0]#excluding Zeros
        if len(chapter)==1:
            chapter = chapter[0]
        else:
            #otherwise
            chapter = 1000
    return float(chapter)
def CheckNprint(titles,old,textFile):
    try:
        import datetime
        import cfscrape
        from bs4 import BeautifulSoup
        scraper = cfscrape.create_scraper()
        f = open(textFile,'a')
        f.truncate()
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')
        new = []
        n = 0
        total = 0
        while n < len(titles):
            print "Checking "+titles[n]
            page_source = getHtmlOf(titles[n],scraper)
            Chapter,Title = getString(page_source)
            Number = extractChapterNum(Chapter,Title)
            #handle chapter titles with no numbers (1000 indicates an error)
            if Number == 1000:
                soup = BeautifulSoup(page_source)
                listOfChapters = [x for x in soup.find_all('td') if x.a !=None]
                Number = next((i+old[n] for i,x in enumerate(listOfChapters) if extractChapterNum(x.a.get_text(),Title) == old[n]),1000)
            new.append(Number)
            if(Number>old[n]):
                maybe = "New Chapter"+"("+'%5s'+") "+'%5s'+" for"+'%30s'+". You are now on "+ '%5s'     
                f.write(maybe % (str(Number-old[n]),str(Number),str(titles[n]),str(old[n])) + '\n')
                print maybe % (str(Number-old[n]),str(Number),str(titles[n]),str(old[n]))
                total = total + Number-old[n]
                if eval(str(total).split(".")[1]) > 0:
                    total = eval(str(total).split(".")[0]) + 1
            n+=1
        print 4*'\n'
        print "Total: ",total
        print "See ", textFile," for report"
        f.write('\n'+'Total: '+str(total))		
        f.write((4*'\n'))
        f.write("List of titles with updated chapter numbers:\n")
        for n in range(len(titles)):
            f.write(str(titles[n]))
            f.write(str('\t'))
            f.write(str(new[n]))
            f.write(str('\n'))
        f.close()
    except:
        f.write("error")
        f.close()
        raise	
	



####################################################################################
from time import sleep
print "Program Start"

#first step is to read in the titles
titles, old = getOldTitleNChap('MangA.txt')
#Get a list of the new titles from kissmanga.com
CheckNprint(titles,old,'UpdatedManga.txt')

print "Program Done"
sleep(3)
