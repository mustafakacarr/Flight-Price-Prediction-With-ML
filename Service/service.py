#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 01:46:54 2023

@author: mustafa
"""

import streamlit as st
import pickle
import datetime
import json
import pandas as pd
import os

app_dir = os.path.dirname(__file__)
base_dir = os.path.abspath(os.path.join(app_dir, '..'))

# Dosya yollarını oluştur
model_path = os.path.join(base_dir, 'Service','predictionModel.pkl')
airports_json_path = os.path.join(base_dir, 'GetAirportsFromWiki', 'airports.json')
data_train_path = os.path.join(base_dir, 'datasets', 'data_train.xlsx')


with open(model_path, 'rb') as file:
   model = pickle.load(file)


with open(airports_json_path, 'r', encoding='utf-8') as file:
   json_data = json.load(file)

def inputsToDummy(df):
   df = pd.get_dummies(df, columns=["Airline","From","To"], dtype=int)
   return df
def encodeDate(df):
    df['Flight Date'] = pd.to_datetime(df['Flight Date'], format='%d.%m.%Y', dayfirst=True)
    df['DayOfWeek']=df['Flight Date'].dt.dayofweek
    df.drop('Flight Date',axis=1,inplace=True)
    df = pd.get_dummies(df, columns=["DayOfWeek"], dtype=int)
    return df

# Get IATA codes
iata_codes = [entry["Airport"] + " (" + entry["IATA"] + ")" for entry in json_data]
iata_dict = {entry["IATA"]: entry["Airport"] for entry in json_data}

st.title('Flight Price Prediction Web Service')


dateInput = st.date_input("Choose date", datetime.datetime.now())

airlineInput = st.selectbox(
    'Choose a airline',
    ('Türk Hava Yolları', 'Sunexpress', 'Anadolujet','Pegasus'))
flightDuration = st.slider('Flight Duration (minute)', 0,150)
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


flight_data = {
    'Flight Date': [dateInput.strftime('%d.%m.%Y')],
    'Airline': [airlineInput],
    'From': [selected_iata_from],
    'To': [selected_iata_to],
    'Flight Duration (min)': [flightDuration]
}

df = pd.DataFrame(flight_data)

df=inputsToDummy(df)
df=encodeDate(df)

data_train = pd.read_excel(data_train_path)
expected_columns_order = data_train.columns

# Reorder columns in df to match the expected order
df = df.reindex(columns=expected_columns_order, fill_value=0)


prediction = model.predict(df)
prediction=round(prediction[0],2)
st.write(f"Predicted price: {prediction} TL")
