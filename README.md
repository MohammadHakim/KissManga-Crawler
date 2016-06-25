# KissManga-Crawler
A Python Script which uses Beautiful Soup to Collect Latest Chapter Numbers


#Hello!#


This project includes a crawler script for <https://kissmanga.com>:

1.	notification.py which checks for latest chapters



To run the scripts you need:

1.	[Python 2.7](https://www.python.org/downloads/)

2.	[The library Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

3.	[Nodejs](https://nodejs.org/en/download/)

4.	[The library Cloud Flare Scrape](https://github.com/Anorov/cloudflare-scrape)



To run notification.py (assumes all the above installed properly):

1.	Create MangA.txt if not already created.

2.	Go to Kissmanga.com and search for your series.

3.	Copy the last part of the url (e.g. copy The-Breaker-New-Waves from the url http://kissmanga.com/Manga/The-Breaker-New-Waves into the text file).

4.	Provide the latest chapter number you have read following the series name separated by a Tab. An example is provided in MangA.txt. Enter each series on a separate line.

5.	Once you have your list you can run notification.py by double clicking on run.bat. (Assumes you have MangA.txt, notification.py and run.bat in the same directory).



__Warnings:__

1.	This script has been tested on a Windows 8+10 environments (I have been personally using it for at least a year)

2.	In the past sometimes the parser in notification.py stops working. Alternating between xml and html solves the issue.

3.	One logical issue is that the update gets stored in memory. This makes the program vulnerable to long chapter lists. Although I doubt anyone has a list of chapters long enough to break the program. Anyone with such a list should not use this program as the html parser is actually slow compared to normal text parsers.

4.	The total number provided is also an estimate, due to fractional chapter numbers (e.g. a sum of 2.002 is rounded to 3 chapters assuming .002 stands for an extra side story chapter. The problem here is .002 might be one chapter or two .001 chapters or any other combination).

5.	This algorithm is totally dependent on the sort algorithm of the kissmanga website. It grabs the first entry in the site's list which is almost always the most recent chapter. There has been cases in the past where the most recent chapter is jumbled somewhere in the chapter list (is not the first entry).

6.	This program is dependent on the cloud flare scrape library ability to bypass the security mechanism of kissmanga. If cloud flare updates their protective page from the 5 second counter to something else, this program is futile.
