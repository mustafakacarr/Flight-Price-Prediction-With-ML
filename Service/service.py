#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 01:46:54 2023

@author: mustafa
"""

import streamlit as st
import pickle
import numpy as np
import datetime
import json
try:
    with open('predictionModel.pkl', 'rb') as file:
      model = pickle.load(file)
except FileNotFoundError:
    print("File couldn't find.")
except Exception as e:
    print(f"Error: {e}")

with open('/Users/mustafa/Desktop/Flight Price Prediction/GetAirportsFromWiki/airports.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Get IATA codes
iata_codes = [entry["Airport"] + " (" + entry["IATA"] + ")" for entry in json_data]
iata_dict = {entry["IATA"]: entry["Airport"] for entry in json_data}

st.title('Flight Price Prediction Web Service')


dateInput = st.date_input("Choose day", datetime.datetime.now())

airlineInput = st.selectbox(
    'Choose a airline',
    ('Türk Hava Yolları', 'Sunexpress', 'Anadolujet','Pegasus'))
flightDuration = st.slider('Flight Duration (minute)', 0.0,150.00)
fromInput = st.selectbox(
    'Choose a departure airport',
    iata_codes,    
  
)
selected_iata_from = fromInput.split("(")[-1].replace(")", "").strip()

st.write('You selected IATA code:', selected_iata_from)
toInput = st.selectbox(
    'Choose an arrival airport',
    iata_codes,

)
selected_iata_to = toInput.split("(")[-1].replace(")", "").strip()
st.write('You selected IATA code:', selected_iata_to)


def fromInputToDummy():
   pass
def toInputToDummy():
    pass
def encodeDate():
    pass
def airlineToDummy():
    pass
    


