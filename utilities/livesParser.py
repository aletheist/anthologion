#!/usr/bin/env python
#Copyright (c) 2011, aletheist
#All rights reserved.

#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



import sys
import time
import string
import os
import re
from datetime import date
import urllib2
#http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup

def get_lives(input_date = date.today()):
  now = input_date

  day = now.day
  month = now.month
  year = now.year
  text = ''
  text += '<h2>'
  text += 'Lives of the Saints for ' + str(month) + '-' + str(day) + '-' + str(now.year)
  text += '</h2>'
  text += '<br/>'

  #Number of times to retry
  tries = 0
  maxtries = 3
  #Interval, in seconds, between retries to access the reading
  retryInterval = 300
  tryagain = True

  #Turns out sometimes a page doesn't load the first time. Who knew? Let's retry a few times before giving up.
  while tryagain == True:
    try:
      url = "http://oca.org/saints/all-lives/" + str(year) + "/"  +str(month) + "/" + str(day) + "/"
      page = urllib2.urlopen(url)
      soup = BeautifulSoup(page)
      exists = soup.find('article' )
      if exists == None:
        text += "There has been an unexpected parsing error."
        tryagain = False
    except urllib2.URLError:
      tries += 1
      if tries >= maxtries:
        tryagain = False
      time.sleep(retryInterval)
      continue
    tryagain = False

    #If we've reached the maximum number of retries we have either run out of readings or something is down.
    #Break the loop and record what we have.
    if tries == maxtries:
      break  
   
    all_articles = soup.find_all('article', { "class" :"clearfix" } )
    for article in all_articles:
      for content in article.contents:
        text += str(content)


  bad_characters = {
  
  ord(u'\u2019'): u'\''
  
  }

  s=text.decode('utf8')
  text = s.translate(bad_characters).encode('ascii', 'ignore')
  return text

if __name__ == "__main__":
  print get_lives()
