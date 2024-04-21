import pandas as pd
import requests
import trafilatura
from itertools import chain
from bs4 import BeautifulSoup
import embedder
import logging

logging.warning('Warming up...')

url = "https://finance.yahoo.com/most-active/"
data = pd.read_html(url)
df = data[0]
df = df.drop(columns=['52 Week Range'])

logging.warning('Got the most active stocks')

def flatten_chain(matrix):
     return list(chain.from_iterable(matrix))

companies = flatten_chain(df.Name.str.split(r" |,|Inc.|.com").tolist())
companies = set(companies)
firms = ["stock", "buy", "sell"]
for i in companies:
  if len(i) > 4:
    firms.append(i)

firms = [item.lower() for item in firms]

news_url = ["https://finance.yahoo.com/topic/stock-market-news/", "https://finance.yahoo.com/topic/earnings/", "https://finance.yahoo.com/topic/morning-brief/", "https://finance.yahoo.com/topic/personal-finance-news/", "https://finance.yahoo.com/topic/yahoo-finance-originals/", "https://finance.yahoo.com/live/politics/", "https://finance.yahoo.com/topic/economic-news/", "https://finance.yahoo.com/topic/crypto/"]
infos = []

def get_news_links(site):
  news_links = []
  news = []
  page = requests.get(site)
  bs = BeautifulSoup(page.content, features='lxml')
  for link in bs.findAll('a'):
    news_links.append(link.get('href'))

  for link in news_links:
    for firm in firms:
      if firm in link and ".html" in link:
        if "yahoo" not in link:
          link = "https://finance.yahoo.com" + link
        news.append(link)
  return news

for url in news_url:
  infos += get_news_links(url)

news = list(set(infos))

information = []

def get_content(url):
  downloaded = trafilatura.fetch_url(url)
  return trafilatura.extract(downloaded)

for link in news:
  information.append(get_content(link))

if len(information) > len(df):
  information = information[:len(df)]
elif len(information) < len(df):
  dif = len(df) - len(information)
  for i in range(dif):
    information.append("")

assert len(information) == len(df)

df["News"] = information
df = df.fillna(" ")
df["News_embedding"] = df["News"].apply(embedder.get_embedding)

logging.warning(f'Dataset ready to go! The chatbot will leverage the following information: {information}')

def get_df():
    return df