#/bin/python
import datetime
import re
from bs4 import BeautifulSoup

def get_antiphon(number, numbering = "LXX"):
  antiphon_filepath = "../resources/antiphons"
  hantiphons = open(antiphon_filepath)
  antiphon = "ANTIPHON"
  for line in hantiphons.readlines():
    anti_info = line.split("::")
    if line.strip()[0] == "#":
      continue
    if numbering == "LXX":
      if int(anti_info[0]) == int(number):
        antiphon = anti_info[2]
    else:
      if int(anti_info[1]) == int(number):
        antiphon = anti_info[2]
  return antiphon.strip()

#Get psalm by
def get_psalm(number, numbering = "LXX", antiphons = False):
  text = ""
  day_of_year = datetime.date.today().strftime("%j")
  psalm_number = number
  psalter_filepath = "../resources/pomog_psalter.htm"

  soup = BeautifulSoup(open(psalter_filepath))
  found_psalm=None
  psalm_headings = soup.findAll('h2')
  for heading in psalm_headings:
    heading_text = heading.contents[0].strip()
    if heading_text == ("Psalm " + str(psalm_number).strip()):
      found_psalm = heading
      text += str(found_psalm)


  psalm_body = found_psalm.find_next(re.compile("h4|p"))
  lineno = 0
  antiphon = ""
  if antiphons: 
    antiphon += "\n<p><i>" + get_antiphon(psalm_number) + "</i><p>\n"
  
  while psalm_body.name != "h2":
    try:
      verse_numbers = psalm_body.find_all("small")
      for number in verse_numbers:
        number.extract()
      italics = psalm_body.find_all("i")
      for italic in italics:
        italic.unwrap()
      if "<p>" in str(psalm_body):
        text += antiphon
      text += str(psalm_body)
      psalm_body = psalm_body.find_next(re.compile("h2|h4|p"))
    except AttributeError:
      continue
  text += antiphon
  return text


#This function has no relation to any liturgical calculations. It is purely
#arbitrary.
def psalm_of_today():
  text = ""
  day_of_year = datetime.date.today().strftime("%j")
  psalm_number = int(day_of_year) % 151
  return get_psalm(psalm_of_today, antiphons = True)


