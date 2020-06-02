from bs4 import BeautifulSoup
import csv
import requests
import re

url = 'https://en.wikipedia.org/wiki/Counties_of_Ireland'
source = requests.get(url).text

soup = BeautifulSoup(source, 'lxml')

dict = {}


def write_to_csv(dict):

    csv_file = open('CSVs/county_towns (cloze).csv',
                    'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)

    for key in dict.keys():
        county = key
        county_town = dict[key]
        row = f'The county town of {{{{c1::{county}}}}} is {{{{c2::{county_town}}}}}'
        csv_writer.writerow([row])


table = soup.find('table', class_='wikitable')
body = table.find('tbody')

for row in body.find_all('tr')[1:]:

    entries = row.find_all('td')

    if len(entries) == 8:
        county_entry = entries[0]
        county_town_entry = entries[3]
    else:  # if len == 9
        county_entry = entries[1]
        county_town_entry = entries[4]

    county_text = county_entry.find('a').text
    county_text = re.sub('Londond', 'D', county_text)
    county_town_text = county_town_entry.find('a').text

    dict[county_text] = county_town_text

write_to_csv(dict)
