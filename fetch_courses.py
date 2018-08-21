from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import urllib
from bs4 import BeautifulSoup
from collections import defaultdict
import re



def getCourseInfo(d):
	d.get('https://www.reg.uci.edu/perl/WebSoc')
	m = urllib.urlopen('https://www.reg.uci.edu/perl/WebSoc')
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
		if int(i[:4]) in (curent_year ,curent_year -1, curent_year -2):
			new_year.append(i)
	years = new_year
	#print(years)



	d.get('https://www.reg.uci.edu/perl/WebSoc')
	a = Select(d.find_element_by_name('YearTerm'))
	a.select_by_visible_text('2018 Fall Quarter')
	b = Select(d.find_element_by_name('Dept'))
	b.select_by_value('COMPSCI')
	d.find_element_by_name('YearTerm').send_keys(Keys.RETURN)
	result = interpretDeptPage(BeautifulSoup(d.page_source, 'lxml'))
	#deptdict[dept] = result
	print(result)




	
	# masterclasses = defaultdict(defaultdict)
	# for term in years:
	# 	deptdict = defaultdict()
	# 	for dept in depts:
	# 		d.get('https://www.reg.uci.edu/perl/WebSoc')
	# 		a = Select(d.find_element_by_name('YearTerm'))
	# 		a.select_by_visible_text(term)
	# 		b = Select(d.find_element_by_name('Dept'))
	# 		b.select_by_value(dept)
	# 		d.find_element_by_name('YearTerm').send_keys(Keys.RETURN)
	# 		result = interpretDeptPage(BeautifulSoup(d.page_source))
	# 		deptdict[dept] = result
	# 	masterclasses[term] = dict(deptdict)
	
	return dict(masterclasses)
	#div.send_keys(Keys.RETURN)
	#print(d.page_source)
	#print(div)


def getYearTerm(tags):
	return [str(option.text) for option in tags.find_all('option')]

def getDept(tags):
	return [str(option['value']) for option in tags.find_all('option')]	

def interpretDeptPage(soup):
	# need to decode the text ffs
	print(soup.original_encoding)
	deptclasses = defaultdict(defaultdict)
	body = soup.body
	pattern = re.compile('[0-9][0-9][0-9][0-9][0-9]')
	counter = 0
	newclass = defaultdict()
	key = ''
	code = ''
	for i in body.find_all('td'):
		string = i.get_text()
		if '  ' in string:
			print('Hi')
			a = [i.encode('utf-8') for i in string.split('  ')]
			print(a)
		elif len(string.strip()) == 0:
			print('Fack')

		if string[:2] == '  ':
			print('Asd')
			deptclasses[key] = dict(newclass)
			print(dict(newclass).values)
			newclass = defaultdict(defaultdict)
			string.strip()
			contents = string.split('  ')
			key =  contents[1] + ' ' + contents[2]
			counter = 0
		elif len(string.strip()) == 0:
			continue
		else:
			string = string.strip()
			print('Here')
			if re.match(pattern, string):

				counter += 1
				code = string
				newclass[string] = defaultdict()
			elif counter == 1:
				newclass['Type'] = string
				counter += 1
			elif counter == 2:
				newclass['Section'] = string
				counter += 1
			elif counter == 3:
				newclass['Units'] = string
				counter += 1
			elif counter == 4:
				newclass['Instructor'] = string
				counter += 1
			elif counter == 5:
				newclass['Time'] = string
				counter += 1
			elif counter == 6:
				newclass['Place'] = string
				counter += 1
			elif counter == 7:
				newclass['Final'] = string
				counter += 1
			elif counter == 8:
				newclass['Max'] = string
				counter += 1
			elif counter == 9:
				newclass['Enrolled'] = string
				counter += 1
			elif counter == 10:
				newclass['Wait List'] = string
				counter += 1
			elif counter == 11:
				newclass['Requested'] = string
				counter += 1
			elif counter == 12:
				newclass['Nor'] = string
				counter += 1
			elif counter == 13:
				newclass['Restrictions'] = string
				counter += 1
			elif counter == 14:
				counter += 1
				continue
			elif counter == 15:
				counter += 1
				continue
			else:
				newclass['Status'] = string

		#print(i.text)

	
	return dict(deptclasses)






if __name__ == '__main__':
	op = webdriver.ChromeOptions()
	op.add_argument('headless');
	d = webdriver.Chrome('/users/chaitu65c/Downloads/chromedriver', options = op)
	f = getCourseInfo(d)
	
