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
from datetime import timedelta
import urllib2
#http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup

from psalmParser import psalm_of_today
from hymnParser import get_hymns
from livesParser import get_lives

day_names = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]

def get_scripture( day_to_fetch = date.today(), max_retries = 3, max_readings = 20):
  text = ""
  #Interval, in seconds, between retries to access the reading
  retryInterval = 300

  #Important note: This script uses the fact that on an invalid reading URL, an exception is thrown.
  #This is a potentially unsafe assumption that could cause a blowup if the way oca.org handles a 404 or database
  #lookup failure changes. To mitigate against this, I chose a to stop the loop at 20 readings because I don't
  #think we ever have that many, and it prevents an infinite loop.
  numReadings = max_readings
  readingNum = 0
  while readingNum < numReadings:
    tries = 0
    tryagain = True
    #Turns out sometimes a page doesn't load the first time. Who knew? Let's retry a few times before giving up.
    while tryagain == True:
      try:
        url = "http://oca.org/readings/daily/" + str(year) + "/"  +str(month) + "/" + str(day) + "/" + str(readingNum)
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        exists = soup.find("dl", { "class" :"reading" } )
        if exists == None:
          tries = max_retries
      except urllib2.URLError:
        tries += 1
        if tries == max_retries:
          tryagain = False
        time.sleep(retryInterval)
        continue
      tryagain = False

    #If we've reached the maximum number of retries we have either run out of readings or something is down.
    #Break the loop and record what we have.
    if tries == max_retries:
      break  
   
    headings = soup('h2');
    scriptureReference = ''  
    for partial in headings[1].contents:
      scriptureReference += str(partial)
    text += '<h2>\n'
    text += scriptureReference + '\n'
    text += '</h2>\n'
  
    text += '<div>\n'
    text += '<dl>\n'
    reading = soup.find("dl", { "class" :"reading" } )
    if reading == None:
      break
    for verse in reading.findAll("dd"):
      text += str(verse)
    #for verse in verses:
    #  text += verse.contents[0] + '\n'
    #text += '</div>\n'
    readingNum += 1
    text += '</dl>\n'
    text += '</div>\n'

  return text

text = '<html>\n'
text += '<body>\n'

now = date.today() + timedelta(days=1)

day = now.day
month = now.month
year = now.year

outFile = 'Scripture Reading for Liturgical ' + day_names[now.weekday()] + ' ' + str(month) + '-' + str(day) + '-' + str(now.year)
text += '<h2>'
text += outFile
text += '</h2>'
text += '<br/>'

readingNum = 1

text += '<h3>'
text += 'A Prayer Before Reading the Holy Scripture'
text += '</h3>'
text += 'Illumine our hearts, O Master Who lovest mankind, with the pure light of Thy divine knowledge. Open the eyes of our mind to the understanding of Thy gospel teachings. Implant also in us the fear of Thy blessed commandments, that trampling down all carnal desires, we may enter upon a spiritual manner of living, both thinking and doing such things as are well-pleasing unto Thee. For Thou art the illumination of our souls and bodies, O Christ our God, and unto Thee we ascribe glory, together with Thy Father, Who is from everlasting, and Thine all-holy, good, and life-creating Spirit, now and ever and unto ages of ages. Amen.'
text += '<mbp:pagebreak />'

text += psalm_of_today()
text += '<mbp:pagebreak />'

text += get_scripture(now)

text += '<mbp:pagebreak />'


text += get_hymns(now)
text += '<mbp:pagebreak />'

text += get_lives(now)
text += '<mbp:pagebreak />'

text += '</body>\n'
text += '</html>\n'

bad_characters = {

ord(u'\u2019'): u'\''

}



s=text.decode('utf8')
text = s.translate(bad_characters).encode('ascii', 'ignore')

#write the HTML out someplace temporary for emailing by my shell script.
#TODO: Add generality by specifying an output location as an argument
#FILE = open('/tmp/' + outFile + '.html', "w")
#FILE.writelines(text)
#FILE.close()
print text
