# generates an Anki deck of the skylines of all cities with more than 10 skyscrapers (>150m)

from bs4 import BeautifulSoup
import csv
import requests

url = 'https://en.wikipedia.org/wiki/List_of_largest_cities'
source = requests.get(url).text

soup = BeautifulSoup(source, 'lxml')


csv_file = open('CSVs/largest_cities_skylines (cloze).csv',
                'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)


def write_to_csv(rank, city, country, pop_estimate):

    skyline_image = f'<img src=\"{city} - Largest Cities.jpg\"><br>'

    cloze = f'Rank: {{{{c1::{rank}}}}}<br>' + \
        f'City: {{{{c1::{city}}}}}<br>' + \
        f'Country: {{{{c1::{country}}}}}<br>' + \
        f'UN 2018 Population Estimate: {{{{c1::{pop_estimate}}}}}'

    row = skyline_image + cloze

    csv_writer.writerow([row])


def save_empty_image(city):

    with open(f"Images/Skylines/Largest Cities/{city} - Largest Cities.jpg", 'wb') as f:
        f.write(b'')


def save_skyline_image(skyline_image_url, city):

    page = requests.get(skyline_image_url).text
    soup = BeautifulSoup(page, 'lxml')

    image_div = soup.find('div', id='file', class_='fullImageLink')
    image_src = image_div.find('img')
    image_url = 'https:' + image_src['src']

    image_response = requests.get(image_url)
    # could retry a few times if failed
    if image_response.status_code == 200:
        with open(f"Images/Skylines/Largest Cities/{city} - Largest Cities.jpg", 'wb') as f:
            f.write(image_response.content)
            return

    save_empty_image(city)


city_table = soup.find('table', id='cities')
body = city_table.find('tbody')

# population rank of city
rank = 0

for row in body.find_all('tr')[2:]:

    rank += 1

    entries = row.find_all('td')

    city_link = entries[0].find('a')
    city = city_link.text

    country_link = entries[1].find_all('a')[-1]
    country = country_link.text

    pop_estimate_span = entries[3].find('span')
    pop_estimate = pop_estimate_span.text

    skyline_image_link = entries[2].find('a')

    if skyline_image_link is None:
        save_empty_image(city)
    else:
        skyline_image_url = 'https://en.wikipedia.org' + \
            skyline_image_link['href']

        save_skyline_image(skyline_image_url, city)

    write_to_csv(rank, city, country, pop_estimate)
