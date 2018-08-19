from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
#from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup


op = webdriver.ChromeOptions()
op.add_argument('headless');
d = webdriver.Chrome('/users/chaitu65c/Downloads/chromedriver', options = op)
d.get('https://www.reg.uci.edu/perl/WebSoc')
m = urllib.urlopen('https://www.reg.uci.edu/perl/WebSoc')
s = BeautifulSoup(m, "html.parser")
main = s.body
div = s.find_all('select')
a = Select(d.find_element_by_name('YearTerm'))
a.select_by_visible_text('2018 Fall Quarter')
b = Select(d.find_element_by_name('Dept'))
b.select_by_value('IN4MATX')
#for i in div:
#    print(i)
d.find_element_by_name('YearTerm').send_keys(Keys.RETURN)
#div.send_keys(Keys.RETURN)
print(d.page_source)
#print(div)
