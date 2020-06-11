# generates an Anki deck of the skylines of all cities with more than 10 skyscrapers (>150m)

from bs4 import BeautifulSoup
import csv
import requests

url = 'https://en.wikipedia.org/wiki/List_of_cities_with_the_most_skyscrapers'
source = requests.get(url).text

soup = BeautifulSoup(source, 'lxml')


csv_file = open('CSVs/most_skyscrapers_skylines (cloze).csv',
                'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)


def write_to_csv(rank, city, country_region, number_of_skyscrapers):

    skyline_image = f'<img src=\"{city} - Most Skyscrapers.jpg\"><br>'

    cloze = f'Rank: {{{{c1::{rank}}}}}<br>' + \
        f'City: {{{{c1::{city}}}}}<br>' + \
        f'Country/Region: {{{{c1::{country_region}}}}}<br>' + \
        f'Number of skyscrapers: {{{{c1::{number_of_skyscrapers}}}}}'

    row = skyline_image + cloze

    csv_writer.writerow([row])


def save_empty_image(city):

    with open(f"Images/Skylines/Most Skyscrapers/{city} - Most Skyscrapers.jpg", 'wb') as f:
        f.write(b'')


def save_skyline_image(skyline_image_url, city):

    page = requests.get(skyline_image_url).text
    soup = BeautifulSoup(page, 'lxml')

    image_div = soup.find('div', id='file', class_='fullImageLink')
    image_src = image_div.find('img')
    image_url = 'https:' + image_src['src']

    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(f"Images/Skylines/Most Skyscrapers/{city} - Most Skyscrapers.jpg", 'wb') as f:
            f.write(image_response.content)
            return

    save_empty_image(city)


table = soup.find('table')
body = table.find('tbody')

for row in body.find_all('tr')[1:]:

    entries = row.find_all('td')

    rank = entries[0].text

    city_link = entries[1].find('a')
    city = city_link.text

    country_region_link = entries[2].find('a')
    country_region = country_region_link.text

    number_of_skyscrapers_link = entries[4].find('a')

    if number_of_skyscrapers_link is None:
        number_of_skyscrapers = entries[4].text
    else:
        number_of_skyscrapers = number_of_skyscrapers_link.text

    skyline_image_link = entries[3].find('a')

    if skyline_image_link is None:
        save_empty_image(city)
    else:
        skyline_image_url = 'https://en.wikipedia.org' + \
            skyline_image_link['href']

        save_skyline_image(skyline_image_url, city)

    write_to_csv(rank, city, country_region, number_of_skyscrapers)
