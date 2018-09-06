#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
import re, os
from pprint import pprint



def getCourseInfo(d):
	d.get('https://www.reg.uci.edu/perl/WebSoc')
	m = urlopen('https://www.reg.uci.edu/perl/WebSoc')
	s = BeautifulSoup(m, 'lxml')
	main = s.body
	div = s.find_all('select')
	#print(div)
	first_name = ''
	second_name = ''
	for tag in div:
	    string_tag  = str(tag).split('\n')
	    r = string_tag[0]
	    first_name = str(r)[r.find('"')+1 : r.rfind('"')]
	    if first_name not in ('YearTerm', 'Dept'):
	    	continue
	    elif first_name in 'YearTerm':
	    	years = getYearTerm(tag)
	    	#print(years)
	    else:
	    	depts = getDept(tag)
	    	#print(depts)
	new_year = []
	v = years[0]
	curent_year = int(v[:4])
	for i in years:
		if int(i[:4]) == curent_year:
			new_year.append(i)
	years = [years[0]]
	
	masterclasses = defaultdict(defaultdict)
	for term in years:
		deptdict = defaultdict()
		for dept in depts:
			d.get('https://www.reg.uci.edu/perl/WebSoc')
			a = Select(d.find_element_by_name('YearTerm'))
			a.select_by_visible_text(term)
			b = Select(d.find_element_by_name('Dept'))
			b.select_by_value(dept)
			d.find_element_by_name('YearTerm').send_keys(Keys.RETURN)
			result = interpretDeptPage(BeautifulSoup(d.page_source), dept.lower())
			pprint(result)
			masterclasses[dept] = result
		# masterclasses[term] = dict(deptdict)
	
	return dict(masterclasses)
	#div.send_keys(Keys.RETURN)
	#print(d.page_source)
	#print(div)


def getYearTerm(tags):
	return [str(option.text) for option in tags.find_all('option')]

def getDept(tags):
	return [str(option['value']) for option in tags.find_all('option')]	

def interpretDeptPage(soup, dept):
	# need to decode the text ffs
	
	p = re.compile('[A-Za-z]+')
	deptclasses = defaultdict(defaultdict)
	body = soup.body
	
	pattern = re.compile('[0-9][0-9][0-9][0-9][0-9]')
	counter = 0
	newclass = defaultdict()
	key = ''
	code = ''
	details = defaultdict()
	for i in body.find_all('td'):
		string = i.get_text()
		string = string.encode('utf-8')
		string = string.replace('\xc2\xa0', '')
		string = string.strip()
		splitter = string.split('  ')
		if re.match(p, splitter[0]) and splitter[0].lower()  == dept:
			if key != '':
				#print(key)
				if code != '':
					newclass[code] = dict(details)
				if key in deptclasses.keys():
					deptclasses[key].update(dict(newclass))
				else:
					deptclasses[key] = dict(newclass)
			newclass = defaultdict(defaultdict)
			string.strip()
			contents = string.split('  ')
			counter = 0
			key = splitter[0] + ' ' + splitter[1]
			pprint(deptclasses)
		elif len(string.strip()) == 0:
			continue
		else:
			string = string.strip()
			if re.match(pattern, string):
				if counter == 0:
					counter += 1
					code = string
					details = defaultdict()
				else:					
					counter = 0
					counter += 1
					newclass[code] = dict(details)
					code = string
					details = defaultdict()
			elif counter == 1:
				details['Type'] = string
				counter += 1
			elif counter == 2:
				details['Section'] = string
				counter += 1
			elif counter == 3:
				details['Units'] = string
				counter += 1
			elif counter == 4:
				if 'STAFF' in string and string != 'STAFF':
					string = string[:5] + ', ' + string[5:]
				details['Instructor'] = string
				counter += 1
			elif counter == 5:
				details['Time'] = string
				counter += 1
			elif counter == 6:
				details['Place'] = string
				counter += 1
			elif counter == 7:
				if re.match(re.compile('[0-9]+'), string):
					continue
				details['Final'] = string
				counter += 1
			elif counter == 8:
				details['Max'] = string
				counter += 1
			elif counter == 9:
				details['Enrolled'] = string
				counter += 1
			elif counter == 10:
				details['Waitlist'] = string
				counter += 1
			elif counter == 11:
				counter += 1
			elif counter == 12:
				counter += 1
			elif counter == 13:
				details['Restriction'] = string
				counter += 1
			elif counter == 14:
				counter += 1
			elif counter == 15:
				details['Status'] = string
			else:
				if key == '':
					continue
				

		#print(i.text)

	#pprint(deptclasses)
	return dict(deptclasses)






if __name__ == '__main__':
	op = webdriver.ChromeOptions()
	op.add_argument('headless')
	print(os.environ['HOME'])
	d = webdriver.Chrome(os.environ['HOME']+'/Downloads/chromedriver', options = op)
	f = getCourseInfo(d)
	pprint(f)
	
