#!/usr/bin/python

import sys
import urllib
from bs4 import BeautifulSoup

def get_code_links_html(url):
  linksl = []
  reading = urllib.urlopen(url)
  code = reading.code
  if code != 200:
    html = 'Error. HTML cannot be read. %i' %(code)
  else:
    html = reading.read()
    bs = BeautifulSoup(reading, 'lxml')
    links = bs.find_all('a')
    for link in links:
      if str(link).find('href') > 0:
        linksl.append(link['href'])
  return (code, html, linksl)

#def visit_get_html(reading):
#  #Function that visits a URL and returns it's html as string
#  code = reading.code 
#  if code != 200:
#    html = 'Error. HTML cannot be read. %i' %(code)
#  else: 
#    html = reading.read()
#  return html

def verify_depth_go(url, depth):
  decrease_depth()
  code, html, links = get_code_links_html(url)
  return (html, links)

#def get_links(reading, depth):
#  links = []
#  bs = BeautifulSoup(reading, 'lxml')
#  links = bs.find_all('a')
#  for link in links:
#    if str(link).find('href') > 0:
#      links.append((depth, link['href']))
#  return links

def decrease_depth():
  # Function to decrease the global variable "depth" by one
  global depth 
  # Equivalent to "depth = depth -1"
  depth -= 1
  print """********************************************
Value of Depth : %i
**********************""" %(depth)

def usage():
  print """./Web_Spider.py URL num
This program will download all the HTML files it finds in a specific URL. It follow "num" number levels inside the original URL"""

def web_spider(url, depth):
  # First section. Get the first url and html without verifying depth value
#  code, html, links  = get_code_links_html(url)
#  print """##############################################
#URL, Depth, HTML
###############################################
#%s
#%s
#%s""" %(url, depth, html)
  # Now, verify the value of depth and get the links from the html if necessary 
  while (depth >= 0):
    code, html, links  = get_code_links_html(url)
    print """##############################################
URL, Depth, HTML
##############################################
%s
%s
%s""" %(url, depth, html)
    depth -= 1
    for link in links:
      if str(link).find('http') > 0:
        print """++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%s 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++""" %(link)
        web_spider(link, depth)
#    html, links = verify_depth_go(link, depth)
#    print """##############################################
#URL, Depth, HTML en ciclo
##############################################
#%s
#%s
#%s""" %(url, depth, html)
  

def main():
  if len(sys.argv) < 3:
    usage()
  else:
    args = sys.argv[1:]
    url = args[0]
    global depth
    depth = int(args[1])
    web_spider(url, depth)

if __name__ == '__main__':
  main()
