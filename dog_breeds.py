# instructions for use...

from bs4 import BeautifulSoup
import csv
import requests

url = 'https://en.wikipedia.org/wiki/List_of_dog_breeds'
source = requests.get(url).text

soup = BeautifulSoup(source, 'lxml')

breed_names = []


def write_to_csv(breed_names):

    csv_file = open('CSVs/dog_breeds (basic with image).csv',
                    'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)

    for breed_name in breed_names:
        breed_image = f'<img src=\"{breed_name}.jpg\">'
        csv_writer.writerow([breed_image, breed_name])


# finds...
def save_breed_image(url, breed_name):

    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')

    infobox = soup.find('table', class_='infobox biota')

    # we must replace these photos manually
    if infobox is not None:

        image_link = infobox.find('a', class_='image')

        if image_link is not None:

            image_src = image_link.find('img')
            image_url = 'https:' + image_src['src']

            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                with open(f"Images/Dog Breeds/{breed_name}.jpg", 'wb') as f:
                    f.write(image_response.content)

            return

    with open(f"Images/Dog Breeds/{breed_name}.jpg", 'wb') as f:
        f.write(b'')


content = soup.find('div', class_='mw-parser-output')

# fins...
for subcontent in content.find_all('div', class_='div-col columns column-width')[:4]:

    list_of_breeds = subcontent.find('ul')

    for breed in list_of_breeds.find_all('li'):

        breed_link = breed.find('a')

        breed_name = breed_link.text
        breed_names.append(breed_name)

        breed_url = 'https://en.wikipedia.org' + \
            breed_link['href']

        save_breed_image(breed_url, breed_name)


write_to_csv(breed_names)
