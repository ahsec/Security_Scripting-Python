#!/usr/bin/python
import urllib
import sys
from bs4 import BeautifulSoup

###########################################################
# SPSE Module 4. Lesson 3. Ex 1.
# Create a script that gets 'relevant information about a URL. 
# Including: Titles of images and links, Titles of videos and links and text included in the HTML file
# This script is highly dependant on the site queried. Works for some but no for others.
# Created using http://www.joquz.com/2427/ronin-motor-works-limited-release-of-47-bikes as a model

# Tested against: http://www.joquz.com/2427/ronin-motor-works-limited-release-of-47-bikes
# Tested against: http://www.jornada.unam.mx/ultimas
# Tested against: http://www.cnn.com/ 		<- Doesn't Work 
###########################################################


def open_url(url):
  reading = urllib.urlopen(url)
  code = reading.code
  return (reading, code)

def get_videos_info(bs):
  videos_list = []
  iframes = bs.find_all('iframe')
  for iframe in iframes:
    videos_list.append(iframe['src'])
  return videos_list

def get_links_titles(bs):
  title_link = []
  links = bs.find_all('a')
  for link in links:
    title = link.text
    url_link = link['href']
    title_link.append((title, url_link))
  return title_link

def get_txt(bs):
  txt = bs.get_text()
  return txt

def get_html_info(url):
  (reading, code) = open_url(url)
  if code != 200:
    print 'The website at the URL %s cannot be retrieved, please verify your URL and try again' %(url)
    return -1
    exit
  else:
    bs = BeautifulSoup(reading, 'lxml')
    txt = get_txt(bs)
    title_link = get_links_titles(bs)
    videos_list = get_videos_info(bs)
    if len(txt) > 0:
      print """############################################################################################
TXT Content
############################################################################################
%s""" %(txt)
    if len(title_link) > 0:
      print """############################################################################################
Link Content
############################################################################################"""
      for entry in title_link:
        print 'Title: %s <-> Link: %s' %(entry[0], entry[1])
    if len(videos_list) > 0:
      print """############################################################################################
Video Content
############################################################################################"""
      for video in videos_list:
        print video

def usage():
  print """./HTML_Scraper.py URL
This script gets 'relevant information about a URL. Including: Titles of images and links, Titles of videos and links and text included in the HTML file"""

def main():
  if len(sys.argv) < 2:
    usage()
  else:
    url = sys.argv[1]
    url = url.strip()
    get_html_info(url)

if __name__ == '__main__':
  main()
