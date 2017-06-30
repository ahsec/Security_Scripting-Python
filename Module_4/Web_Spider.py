#!/usr/bin/python

import sys
import urllib
from bs4 import BeautifulSoup
'''
##########################################
# SPSE Module 4. Lesson 7. Ex 1
# A Web Crawler that writes the output to a DB
# This code writes the output to a List of objects calle list_final_data
# This program will download all the HTML files it finds in a specific URL.
# It will follow "num" number of links inside the original URL
##########################################
'''
list_final_data = []
url_to_visit = []

def get_code_links_html(url):
  '''
  This function will return the html code and all the links (href)
  found in it
  This will be used later to visit the links found and retrieve more html code.
  '''
  linksl = []
  reading = urllib.urlopen(url)
  code = reading.code
  if code != 200:
    html = 'Error. HTML cannot be read. %i' %(code)
  else:
    bs = BeautifulSoup(reading, 'lxml')
    html = bs
    links = bs.find_all('a')
    for link in links:
      if str(link).find('http') > 0:
        linksl.append(link['href'])
  return (code, html, linksl)

def usage():
  print """./Web_Spider.py URL num
        This program will download all the HTML files found in a specific URL.
        It will follow "num" number of links inside the original URL
        """
def web_spider(url, num_links):
  # Main part of the program
  global list_final_data
  global url_to_visit

  # While we haven't visited enough number of links
  # (specified by command line) the program will call itself
  while len(list_final_data) <= num_links:
    # Get HTML code and links from URL
    (code, html, linksl) = get_code_links_html(url)
    # Add results to the "list_final_data" list.
    # Which is the main results list
    list_final_data.append((url, html))
	###### Temporary - Verification pourpuses only
    print '*' * 30 + 'Len List_Final_Data %i : \n ' %(len(list_final_data))
    for element in list_final_data :
      print element
      print '*' * 30
	###### Temporary - Verification pourpuses only
    for element in linksl :
      # From the elements in the links list retrieved from the HTML code
      # Will add each element to the beginning of the url_to_visit and then
      # will visit each site from that list (until reach the maximum number
      # of links to visit)
      url_to_visit.insert(0,element)
      web_spider(url_to_visit.pop(), num_links)

def main():
  if len(sys.argv) < 3:
    usage()
  else:
    # Get URL and number of links to follow
    args = sys.argv[1:]
    url = args[0]
    global num_links
    num_links = int(args[1])
    web_spider(url, num_links)

if __name__ == '__main__':
  main()
