#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 15:30:12 2023

@author: mustafa
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time

link = "https://en.wikipedia.org/wiki/List_of_airports_in_Turkey"

driver = webdriver.Chrome() # Make sure to have the ChromeDriver executable in your PATH
driver.get(link)

# Wait for the page to load (you may need to adjust the time depending on your network speed)
driver.implicitly_wait(20)
time.sleep(3)
soup = BeautifulSoup(driver.page_source, "html.parser")

data = []
headers = []

# Extract header data
header_row = soup.find('table', {"class": "wikitable"}).find('thead')
headers.append("City")
headers.append("ICAO")
headers.append("IATA")
headers.append("Airport")
headers.append("UsageType")

# Extract table data
table_rows = soup.find('table', {"class": "wikitable"}).find('tbody').find_all('tr')
for row in table_rows:
    if(row.find('th') is not None):
       if(row.find('th', {"colspan": "7"})):
           break
       pass
    else:
       cells = row.find_all('td')
 
       city = cells[0].text.strip()
       icao = cells[1].text.strip()
       iata = cells[2].text.strip()
       name = cells[3].text.strip()
       usageType = cells[4].text.strip()
            
       data.append({
       headers[0]: city,
       headers[1]: icao,
       headers[2]: iata,
       headers[3]: name,
       headers[4]: usageType,
       })

# Close the Selenium WebDriver
driver.quit()

# Convert data to JSON
json_data = json.dumps(data, indent=2)
f= open("airports.json","w")
f.write(json_data)
f.close()
#print(json_data)
