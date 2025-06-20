import requests
from bs4 import BeautifulSoup
import psycopg2

def scrape_immobilienscout24():
    url = 'https://www.immobilienscout24.ch'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    properties = []
    for listing in soup.find_all('div', class_='listing'):
        title = listing.find('h2').text
        price = listing.find('span', class_='price').text
        link = listing.find('a')['href']
        properties.append({
            'title': title,
            'price': price,
            'link': link
        })
    
    return properties

def save_to_db(properties):
    conn = psycopg2.connect(
        dbname='yourdbname',
        user='yourdbuser',
        password='yourdbpassword',
        host='yourdbhost'
    )
    cursor = conn.cursor()
    
    for property in properties:
        cursor.execute(
            "INSERT INTO properties (title, price, link) VALUES (%s, %s, %s)",
            (property['title'], property['price'], property['link'])
        )
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    properties = scrape_immobilienscout24()
    save_to_db(properties)