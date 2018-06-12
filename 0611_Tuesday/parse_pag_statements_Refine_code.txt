#parse-pag-statements.py

# Code to be used in transforming ESTC pagination statements in Open Refine. (Use Jython.)

import re
roman = re.compile('[xvi]')
plates = re.compile('\d+\splates')
range = re.compile('-')
ie = re.compile('\d+\\[i\\.?e\\.?\d+')
pt = re.compile('\d+pt')
vol = re.compile('v\.\d+')

# This code from http://stackoverflow.com/questions/10093618/convert-a-string-containing-a-roman-numeral-to-integer-equivalent
numeral_map = zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
)

def roman_to_int(n):
    n = unicode(n).upper()

    i = result = 0
    for integer, numeral in numeral_map:
        while n[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)
    return str(result)

if roman.findall(value) :
  value = re.sub('\\b([mcldxvi]+)[^][\.,e-]',lambda x: roman_to_int(x.group()),value)
else :
  value = value
  

dumbNums = [int(s) for s in re.findall(r'\d+',value)]
dumbTotal = sum(dumbNums)
total = dumbTotal

if plates.findall(value) :
  plateCount = re.findall('\d+\splates?',value)
  plateNum = int(re.findall('\d+',plateCount[0])[0])
  total = total - plateNum

if range.findall(value) :
  ranges = re.findall('\\d+-\\d+',value)
  pagesInRanges = 0
  removePages = []
  for range in ranges :
    pageNums = re.findall('\d+',range)
    removePages.extend(pageNums)
    pages = int(pageNums[1]) - int(pageNums[0]) + 1
    pagesInRanges += pages
  removePagesInts = [int(i) for i in removePages]
  pagesToRemove = sum(removePagesInts)
  total = dumbTotal - pagesToRemove + pagesInRanges

if ie.findall(value) :
  caveat = re.findall('\d+\\[\\i\\.?e\\.?\d+',value)
  for instance in caveat :
    pageNums = re.findall('\d+',instance)
    subtract = int(pageNums[0])
  total = total - subtract

if pt.findall(value) :
  total = int(re.findall('\d+',re.findall('\d+p\\.',value)[0])[0])

if vol.findall(value) :
  vols = int(re.findall('\d+',re.findall('v\.\d+',value)[0])[0])
  total = total - vols

if not re.findall('p\.',value) :
  total = 0

return total