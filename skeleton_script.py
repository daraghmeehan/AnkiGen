# generates an Anki deck of

from bs4 import BeautifulSoup
import csv
import requests

url = ''
source = requests.get(url).text

soup = BeautifulSoup(source, 'lxml')


csv_file = open('CSVs/.csv',
                'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)


def write_to_csv(a, b):

    _image = f'<img src=\"\"><br>'

    cloze = f'Rank: {{{{c1::{a}}}}}<br>' + \
        f'UN 2018 Population Estimate: {{{{c1::{b}}}}}'

    row = None

    csv_writer.writerow([row])


def save_empty_image():

    with open(f"Images/", 'wb') as f:
        f.write(b'')


def save__image(url):

    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')

    # image_div = soup.find('div', id='file', class_='fullImageLink')
    # image_src = image_div.find('img')
    # image_url = 'https:' + image_src['src']

    image_response = requests.get(url)

    attempt = 1
    while attempt < 6:
        if image_response.status_code == 200:
            with open(f"Images/", 'wb') as f:
                f.write(image_response.content)
                return
        attempt += 1

    save_empty_image()


table = soup.find('table')
body = table.find('tbody')


for row in body.find_all('tr')[1:]:

    entries = row.find_all('td')

    image_link = entries[0].find('a')

    if image_link is None:
        save_empty_image()
    else:
        image_url = ''

        save__image(image_url)

    write_to_csv(0, 0)
