import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from excel import ship_list, max_row, notes
import re
from excel import write_excel

# import folium

start_time = time.time()

y = 0
count = 2
unique_ports = []
unique_portsnew = []
gemiler = []
portlar = {}
options = Options()
options.headless = True
time.sleep(1)

browser = webdriver.Chrome(options=options)
browser.get('https://www.marinetraffic.com/en/ais/home/centerx:54.9/centery:12.1/zoom:2')
time.sleep(3)

button = browser.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
button.click()
time.sleep(3)

while y <= (max_row - 2):
    searchbar = browser.find_element(By.ID, 'searchMarineTraffic')
    searchbar.click()
    time.sleep(3)
    searchbar = ActionChains(browser)
    searchbar.send_keys(ship_list[y])
    searchbar.perform()
    time.sleep(3)

    ship = browser.find_element(By.ID, 'shipShape')
    ship.click()
    time.sleep(3)

    shipment_inf = browser.find_element(By.XPATH,
                                        "//script[contains(text(),'') and contains(@type, 'json')]").get_attribute(
        'text')
    time.sleep(2)

    shipment_inf1 = browser.find_element(By.XPATH,
                                         '//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div/div/div/div[2]/div['
                                         '1]/div/div[2]/a/span/b').get_attribute(
        "innerHTML")
    shipment_inf3 = browser.find_element(By.XPATH, '//*[@id="vesselDetails_voyageInfoSection"]/div['
                                                   '2]/div/div/div/div[2]/div[1]/div/div[2]/a/b').get_attribute(
        "innerHTML")
    shipment_inf2 = shipment_inf1 + shipment_inf3
    time.sleep(2)
    html = shipment_inf
    html = re.sub(";", "", html)
    html = json.loads(html)

    colors = ["red", "blue", "green", "purple", "orange", "darkred",
              "lightred", "beige", "darkblue", "darkgreen", "cadetblue", "darkpurple", "white", "pink", "lightblue",
              "lightgreen", "gray", "black", "lightgray"]

    infos2 = pd.read_json('C:/Users/oğuzhan/PycharmProjects/WebCrawler/ports.json')
    port_name = infos2[shipment_inf2]['name']
    port_latitude = infos2[shipment_inf2]['coordinates'][1]
    port_longitude = infos2[shipment_inf2]['coordinates'][0]

    write_excel(html["latitude"], html["longitude"], html["potentialAction"], shipment_inf2, port_name, port_latitude,
                port_longitude, count)

    sayac = len(unique_portsnew)

    shipDict = {

        'ID': html["name"].replace(" ", ""),
        'NAME': html["name"],
        'ACT': html["potentialAction"],
        'LONG': html["latitude"], 'LATH': html["longitude"],
        'RENK': colors[y],
        'NOTES': notes[y],

        'DEST': {

            'ID': shipment_inf2,
            'NAME': port_name,
            'LONG': port_latitude, 'LATH': port_longitude

        }

    }

    portDict = {

        shipment_inf2: {
            'COUNT': sayac,
            'ID': shipment_inf2,
            'NAME': port_name,
            'LONG': port_latitude, 'LATH': port_longitude,
            'SHIPS': [html["name"]]

        }
    }

    gemiler.append(shipDict)
    unique_ports.append(port_name)
    unique_ports.sort()
    unique_portsnew = list(set(unique_ports))
    unique_portsnew.sort()

    print(unique_ports)
    print(unique_portsnew)

    print(portDict)

    if unique_ports != unique_portsnew:
        unique_ports = unique_portsnew
        portlar[shipment_inf2]['SHIPS'] += [html["name"]]
    elif unique_ports == unique_portsnew:
        portlar.update(portDict)

    print(portlar)

    if y == (max_row - 2):
        with open('C:/Users/oğuzhan/PycharmProjects/WebCrawler/json_data.json', 'w') as f:
            json.dump(gemiler, f, indent=4)
        with open('C:/Users/oğuzhan/PycharmProjects/WebCrawler/json_data2.json', 'w') as f:
            json.dump(portlar, f, indent=4)

    print(html)
    count = count + 1
    y += 1

"""

infos = pd.read_excel('C:/Users/oğuzhan/PycharmProjects/WebCrawler/ships.xlsx')

colors = ["red", "blue", "green", "purple", "orange", "darkred",
          "lightred", "beige", "darkblue", "darkgreen", "cadetblue", "darkpurple", "white", "pink", "lightblue",
          "lightgreen", "gray", "black", "lightgray"]

my_map = folium.Map(location=[13, 16], zoom_start=2)
tile = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google',
    name='Google Satellite',
    overlay=True,
    control=True
).add_to(my_map)



for _, ship_loc, in infos.iterrows():
    folium.Marker(
        location=[ship_loc['Latitude'], ship_loc['Longitude']],
        popup=ship_loc['Ship Name'] + " >>> " + ship_loc['Potential Action'],
        icon=folium.Icon(icon='ship', prefix='fa', color=colors[_])
    ).add_to(my_map)
    folium.Marker(
        location=[ship_loc['Port Latitude'], ship_loc['Port Longitude']],
        popup=ship_loc['Heading Port Name'],
        icon=folium.Icon(icon='anchor', prefix='fa', color=colors[_])
    ).add_to(my_map)

    my_map.save("map.html")

"""

stop_time = time.time()
execute_time = stop_time - start_time
print(execute_time)
browser.close()
