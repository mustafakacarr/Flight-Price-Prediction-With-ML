#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 9 17:06:59 2023
@author: mustafa
"""

import itertools
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import re
from datetime import datetime, timedelta
from selenium.common.exceptions import WebDriverException

driver = webdriver.Chrome() 

#input("type arrival code f.e: DLM")
start_date = datetime.strptime("20.12.2023", "%d.%m.%Y")
end_date = datetime.strptime("26.12.2023", "%d.%m.%Y")

isNonStop = "on"


start_time=time.time()
def parse_time(input_time):
    # Extract hours and minutes values
    match = re.match(r'(\d+)sa(?: (\d+)dk)?', input_time)
    if match:
        groups = match.groups()
        hours = int(groups[0])
        minutes = int(groups[1]) if groups[1] is not None else 0
        total_minutes = hours * 60 + minutes
        return total_minutes
    else:
        return None

with open('GetAirportsFromWiki/airports.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Get IATA codes
iata_codes = [entry["IATA"] for entry in json_data]

# Combine IATA codes pairwise
combinations = list(itertools.combinations(iata_codes, 2))

csv_file_path = 'flight_dataset.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Flight Date', 'Airline', 'From', 'To', 'Flight Duration (min)', 'Price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    i = 0

    current_date = start_date
    while current_date <= end_date:
        for combo in combinations:
            i += 1
            if(i % 50 == 0):
                time.sleep(10)

            print(f"i: '{i}' current_date: '{current_date}'  combination -> '{combo}'\n")
            elapsed_time = time.time() - start_time;
            print(f"Elapsed time -> '{elapsed_time}'\n")
            departureCode = combo[0]
            arrivalCode = combo[1]

            formatted_date = current_date.strftime("%d.%m.%Y")
            
            driver.get("https://www.ucuzabilet.com/ic-hat-arama-sonuc?from="+departureCode+"&to="+arrivalCode+"&ddate="+formatted_date+"&adult=1&directflightsonly=on")
            time.sleep(4)
            soup = BeautifulSoup(driver.page_source, "html.parser")
           
            cards = soup.find_all('tr', {"class": "flight-item"})

            if len(cards) != 0:
                airline_counter = {}

                for card in cards:
                    airline_info = card.find('div', class_='airline')
                    flight_date = formatted_date
                    duration_info = card.find('span', class_='flight-duration')
                    price_info = card.find('span', class_='currencyChangeArea')

                    airline = airline_info.text.strip() if airline_info else None
                    flight_duration = parse_time(duration_info.text.strip()) if duration_info else None
                    price = price_info.text.strip().replace("TRY", "") if price_info else None

                    # Update counter for the airline
                    if airline not in airline_counter:
                        airline_counter[airline] = 1
                    else:
                        airline_counter[airline] += 1

                    # Write to the CSV file
                    if airline_counter[airline] < 3:
                        writer.writerow({
                            'Flight Date': flight_date,
                            'Airline': airline,
                            'From': departureCode,
                            'To': arrivalCode,
                            'Flight Duration (min)': flight_duration,
                            'Price': price
                        })

        current_date += timedelta(days=1)

driver.quit()
