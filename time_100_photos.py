# generates an Anki deck of TIME's 100 most influential photos of all time

from bs4 import BeautifulSoup
import csv
import requests

url = 'http://100photos.time.com'
source = requests.get(url).text

soup = BeautifulSoup(source, 'lxml')


csv_file = open('CSVs/time_100_photos (cloze).csv',
                'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)


def write_to_csv(title, photographer, year):

    image = f'<img src=\"{title} - {photographer}.jpg\"><br>'

    cloze = f'Photo Name: {{{{c1::{title}}}}}<br>' + \
        f'Photographer: {{{{c1::{photographer}}}}}<br>' + \
            f'Year: {{{{c1::{year}}}}}'

    row = image + cloze

    csv_writer.writerow([row])


def save_empty_image(title, photographer):

    with open(f"Images/TIME 100 Photos/{title} - {photographer}.jpg", 'wb') as f:
        f.write(b'')


def save_image(photo_url, title, photographer):

    image_response = requests.get(photo_url)

    attempt = 1
    while attempt < 6:
        if image_response.status_code == 200:
            with open(f"Images/TIME 100 Photos/{title} - {photographer}.jpg", 'wb') as f:
                f.write(image_response.content)
                return
        attempt += 1

    save_empty_image(title, photographer)


div = soup.find('div', class_='main')
photo_links = div.find_all('a', class_='collection__link')

for photo_link in photo_links:

    photo_url = url + photo_link['href']

    photo_page = requests.get(photo_url).text
    photo_soup = BeautifulSoup(photo_page, 'lxml')

    title_header = photo_soup.find('h1', class_='photograph__title')
    title = title_header.text

    photographer_elem = photo_soup.find(
        'li', class_='photograph__photographer')
    photographer = photographer_elem.text

    year_elem = photo_soup.find('li', class_='photograph__year')
    year = year_elem.text

    photo_img = photo_soup.find('img', id='photograph-image')

    if photo_img is None:
        save_empty_image(title, photographer)
    else:
        photo_url = photo_img['src']
        save_image(photo_url, title, photographer)

    write_to_csv(title, photographer, year)
