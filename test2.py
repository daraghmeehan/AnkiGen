from bs4 import BeautifulSoup
import requests

html = requests.get('http://www.nytimes.com/2009/12/21/us/21storm.html').text
soup = BeautifulSoup(html)
print(soup.get_text())
