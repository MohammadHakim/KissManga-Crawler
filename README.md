# KissManga-Crawler
A couple Python Scripts which use Beautiful Soup to Collect Latest Chapter Number and Series Cover Art


#Hello!#


This project includes two crawler scripts for <https://kissmanga.com>:

1.	notifications.py which checks for latest chapters

2.	images.py which checks for the latest images provided for the series on the website



To run the scripts you need:

1.	Python 2.7

2.	The library Beautiful Soup



To run notifications.py (assumes you already have Python 2.7 and Beautiful Soup installed properly):

1.	Create MangA.txt if not already created.

2.	Go to Kissmanga.com and search for your series.

3.	Copy the last part of the url (e.g. copy The-Breaker-New-Waves from the url http://kissmanga.com/Manga/The-Breaker-New-Waves into the text file).

4.	Provide the latest chapter number you have read following the series name separated by a Tab. An example is provided in MangA.txt. Enter each series on a separate line.

5.	Once you have your list you can run notifications.py by double clicking on run.bat. (Assumes you have MangA.txt, notifications.py and run.bat in the same directory).

6.	To run the images.py file edit the contents of run.bat from python notifications.py to python images.py  and then double click on the file.



__Warnings:__

1.	These scripts have been tested on a Windows 8 environment (I have been personally using them for at least a year)

2.	In the past sometimes the parser in notifications.py stops working. Alternating between xml and html solves the issue.

3.	One logical issue is that the update gets stored in memory and then printed. This is vulnerable to errors that break the program causing memory loss and memory limits in case of very large sizes.

4.	The total number provided is also an estimate, due to fractional chapter numbers (e.g. a sum of 2.002 is rounded to 3 chapters assuming .002 stands for an extra side story chapter. The problem here is .002 might be one chapter or two .001 chapters or any other combination).
