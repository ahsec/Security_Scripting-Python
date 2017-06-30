### Module 4

* HTML_Scraper.py

  Gets 'relevant information about a URL.
Including: Titles of images and links, Titles of videos and links and text
included in the HTML file
This script is highly dependant on the target site's configuration.

  Tested and validated against the following

    [47 motor bikes](http://www.joquz.com/2427/ronin-motor-works-limited-release-of-47-bikes)

  [La Jornada, Noticias](http://www.jornada.unam.mx/ultimas)

* Retrieve_File_progress.py

  Linux's wget implementation on Python.
It shows the progress and validates that the file exists before attempting to
retrieve it.

* SQLinj_Mechanize.py

  SQL Injection exploitation automation using Mechanize
This PoC is created taking BadStore as vulnerable app (192.168.1.4)
(Badstore official Web Page)[http://badstore.net/]

  Automates SQL injection on forms.
Tested against the Login/Register form.

  Link is: http://192.168.1.4/cgi-bin/badstore.cgi?action=loginregister

* Web_Spider.py

  Web Crawler that writes the output to a Database.
This program will download all the HTML files it finds in a specific URL.
It will follow "num" number of links inside the original URL; where num is
configurable.

* XSS_Mechanize.py

  XSS exploitation automation using Mechanize.
This PoC is created taking BadStore as vulnerable app (192.168.1.4)
[Badstore official Web Page](http://badstore.net/)

 Tested against the "Sign our Guestbook! " section.

 Link is: http://192.168.1.4/cgi-bin/badstore.cgi?action=guestbook
