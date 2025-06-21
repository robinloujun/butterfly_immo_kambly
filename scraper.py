import requests
from bs4 import BeautifulSoup
import uuid

def scrape_immobilienscout24():
    url = 'https://www.immobilienscout24.ch'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    properties = []
    for listing in soup.find_all('div', class_='listing'):
        property_uuid = str(uuid.uuid4())  # Generate a unique UUID for each property
        name = listing.find('h2').text.strip()
        price = listing.find('span', class_='price').text.strip()
        area_size = listing.find('span', class_='area').text.strip()
        address = listing.find('span', class_='address').text.strip()
        type = 'apartment' if 'apartment' in listing.text.lower() else 'house'
        build_year = listing.find('span', class_='build-year').text.strip() if listing.find('span', class_='build-year') else None
        availability = listing.find('span', class_='availability').text.strip() if listing.find('span', class_='availability') else None
        number_of_rooms = listing.find('span', class_='rooms').text.strip() if listing.find('span', class_='rooms') else None
        number_of_bathrooms = listing.find('span', class_='bathrooms').text.strip() if listing.find('span', class_='bathrooms') else None
        floor = listing.find('span', class_='floor').text.strip() if listing.find('span', class_='floor') else None
        lift = True if listing.find('span', class_='lift') else False
        online_link = listing.find('a')['href']
        
        property_data = {
            'uuid': property_uuid,
            'name': name,
            'price': price,
            'area_size': area_size,
            'address': address,
            'type': type,
            'build_year': build_year,
            'availability': availability,
            'number_of_rooms': number_of_rooms,
            'number_of_bathrooms': number_of_bathrooms,
            'floor': floor,
            'lift': lift,
            'online_link': online_link
        }
        
        properties.append(property_data)
    
    return properties

def save_to_db(properties):
    conn = sqlite3.connect('immodb.db')
    cursor = conn.cursor()
    
    for property in properties:
        cursor.execute(
            """
            INSERT INTO properties (uuid, name, price, area_size, address, type, build_year, availability, number_of_rooms, number_of_bathrooms, online_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (property['uuid'], property['name'], property['price'], property['area_size'], property['address'], property['type'], property['build_year'], property['availability'], property['number_of_rooms'], property['number_of_bathrooms'], property['online_link'])
        )
        if property['type'] == 'apartment':
            cursor.execute(
                """
                INSERT INTO apartments (uuid, floor, lift)
                VALUES (?, ?, ?)
                """,
                (property['uuid'], property['floor'], property['lift'])
            )
        elif property['type'] == 'house':
            cursor.execute(
                """
                INSERT INTO houses (uuid)
                VALUES (?)
                """,
                (property['uuid'],)
            )
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    properties = scrape_immobilienscout24()
    save_to_db(properties)