#This file hosts code which generates a list of updated manga chapters of interest from KissManga.com
#parts of this code were contributed by programmers on http://stackoverflow.com/
def getHtmlOf(title,scraper):
    website = "http://kissmanga.com/Manga/"
    website = website+title
    page_source = scraper.get(website).content
    return page_source
def getChNTitle(page_source):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_source)
    Chapter = soup.td.a.get_text()
    Title = soup.title.get_text()
    return Chapter,Title
def extractChNum(SiteCh, SiteTitle):
    """This function looks for chapter, ch or numbers in a given choice string
    and utilizes the page title to choose candidate numbers that are assumed to
    be the chapter number"""
    import re
    try:
        #if the string CH is found (ch., ch, chapter, chap., etc)
        temp = re.findall('ch[\w\s,.]+?\d+', SiteCh, re.IGNORECASE)[-1]
        ChNum = re.search('\d+\.\d+|\d+',temp).group(0)
    except (AttributeError, IndexError):
        #if there is a single digit in the chapter string
        remove = SiteTitle.split()#remove white spaces
        temp = re.compile('|'.join(map(re.escape,remove)))#remove strings which appear in the title string from the chapter string
        SiteCh = temp.sub("",SiteCh)
        ChNum = re.findall("\d+\.\d+|\d+",SiteCh)#find all the numbers in the chapter string
        ChNum = [x for x in ChNum if float(x)!=0]#excluding Zeros
        if len(ChNum)==1:
            ChNum = ChNum[0]
        else:
            #otherwise
            ChNum = 1000
    return float(ChNum)
def CheckNprint(InTxt,OutTxt):
    try:
        import datetime
        import cfscrape
        from bs4 import BeautifulSoup
        scraper = cfscrape.create_scraper()
        Ofile = open(OutTxt,'a')
        Ofile.truncate()
        Ofile.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')
        Ifile = open(InTxt,'r+')
        for line in Ifile:
            splitLine = line.split('\t')
            title = splitLine[0]
            oldChNum = float(splitLine[1])        
            print "Checking "+title
            total = 0
            page_source = getHtmlOf(title,scraper)
            Chapter,Title = getChNTitle(page_source)
            Number = extractChNum(Chapter,Title)
            #handle chapter titles with no numbers (1000 indicates an error)
            if Number == 1000:
                soup = BeautifulSoup(page_source)
                lstOCh = [x for x in soup.find_all('td') if x.a !=None]
                Number = next((i+oldChNum for i,x in enumerate(lstOCh) if extractChNum(x.a.get_text(),Title) == oldChNum),1000)
            if(Number>oldChNum):
                maybe = "New Chapter"+"("+'%5s'+") "+'%5s'+" for"+'%30s'+". You are now on "+ '%5s'
                Ofile.write(maybe % (str(Number-oldChNum),str(Number),str(title),str(oldChNum)) + '\n')
                print maybe % (str(Number-oldChNum),str(Number),str(title),str(oldChNum))
                total = total + Number-oldChNum
                if eval(str(total).split(".")[1]) > 0:
                    total = eval(str(total).split(".")[0]) + 1
        print 4*'\n'
        print "Total: ",total
        print "See ", OutTxt," for report"
        Ofile.write('\n'+'Total: '+str(total))
        Ofile.close()
        Ifile.close()
    except:
        Ofile.write("error")
        Ofile.close()
        Ifile.close()
        raise
####################################################################################
from time import sleep
print "Program Start"
#Get a list of the new titles from kissmanga.com
CheckNprint('MangA.txt','UpdatedManga.txt')
print "Program Done"
sleep(3)
