import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import io
import matplotlib.pyplot as plt
import csv
import os


url_series_poblacion = "https://www.ine.es/dynt3/inebase/index.htm?padre=6235&capsel=6692"
domain = "https://www.ine.es"
response = requests.get(url_series_poblacion)
content_web = BeautifulSoup(response.text, 'html.parser')
code_csv = "36969"
link = content_web.find('a', href=lambda s: '36969' in s).attrs['href']

url_link = "{}{}".format(domain, link)
download_page = requests.get(url_link)
content_down_web = BeautifulSoup(download_page.text, 'html.parser')
data_url = content_down_web.find(title="CSV: separado por ;").attrs['href']
link_data = "{}/jaxiT3/{}".format(domain, data_url)

data = requests.get(link_data)
decode_data = data.content.decode('utf-8')
decode_data = decode_data.replace("\r", "")
df = pd.read_csv(io.StringIO(decode_data[1:]), sep=';')

# PARSEOOOOOO
dd = df.rename(columns={'Comunidades y provincias':'Lugar', 'País de nacimiento':'Nacimiento', 'Edad (hasta 100 y más)': 'Edad'})
dd['Total'] = dd['Total'].astype('str')
dd['Total'] = dd['Total'].str.replace('.', '')
dd['Total'] = dd['Total'].astype('int')
names = dd.keys().tolist()

# los datos van de 2015 - 2020
dd.loc[dd['Periodo'] == "1 de enero de 2015", 'Periodo'] = 2015
dd.loc[dd['Periodo'] == "1 de enero de 2016", 'Periodo'] = 2016
dd.loc[dd['Periodo'] == "1 de enero de 2017", 'Periodo'] = 2017
dd.loc[dd['Periodo'] == "1 de enero de 2018", 'Periodo'] = 2018
dd.loc[dd['Periodo'] == "1 de enero de 2019", 'Periodo'] = 2019
dd.loc[dd['Periodo'] == "1 de enero de 2020", 'Periodo'] = 2020

currentDir = os.path.dirname(__file__)
filename = "population_spain_dataset.csv"
filePath = os.path.join(currentDir, filename)

dd.to_csv(filePath, index=False)
