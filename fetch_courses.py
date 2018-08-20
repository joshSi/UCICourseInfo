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
	s = BeautifulSoup(m)
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
	result = interpretDeptPage(BeautifulSoup(d.page_source))
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
	deptclasses = defaultdict(defaultdict)
	body = soup.body
	pattern = re.compile('[0-9][0-9][0-9][0-9][0-9]')
	counter = 0
	newclass = defaultdict()
	for i in body.find_all('td'):
		string = i.text
		string 
		if string[:2] == '  ':
			newclass = defaultdict(defaultdict)
			string.strip()
			contents = string.split('  ')
			key =  contents[1] + ' ' + contents[2]
			counter = 0
		elif len(string.strip()) == 0:
			continue
		else:
			string = string.strip()
			if re.match(pattern, string):
				counter += 1
				newclass[string] = defaultdict()
			elif counter == 1:
				asd
			elif counter == 2:
				asd
			elif counter == 3:
				asd
			elif counter == 4:
				asd
			elif counter == 5:
				asd
			elif counter == 6:
				asd
			elif counter == 7:
				asd
			elif counter == 8:
				asd
			elif counter == 9:
				asd
			elif counter == 10:
				asd
			elif counter == 11:
				asd
			elif counter == 12:
				asd
			elif counter == 13:
				counter += 1
				
			elif counter == 14:
				counter += 1
				continue
			elif counter == 15:
				counter += 1
				continue
			else:
				#refer to columns for each course and adjust


		print(i.text)

	
	return defaultdict()






if __name__ == '__main__':
	op = webdriver.ChromeOptions()
	op.add_argument('headless');
	d = webdriver.Chrome('/users/chaitu65c/Downloads/chromedriver', options = op)
	f = getCourseInfo(d)
	
