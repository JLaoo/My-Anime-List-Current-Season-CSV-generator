import requests
import re
import numpy as np
import pandas as pd
import time
from lxml import html

mal_page = requests.get('https://myanimelist.net/anime/season')
mal_tree = html.fromstring(mal_page.content)
new_tv_urls = []
continuing_tv_urls = []
ONA_urls = []
OVA_urls = []
movie_urls = []
special_urls = []
urls_lst = [[] for i in range(6)]
names_lst = [[] for i in range(6)]

#scraping new tv series urls
url_count = 2
while True:
    true_count = 0
    for i in np.arange(1,7):
        url_path = '//*[@id="content"]/div[4]/div['+str(i)+']/div['+str(url_count)+']/div[1]/div[1]/p/a/@href'
        name_path = '//*[@id="content"]/div[4]/div['+str(i)+']/div['+str(url_count)+']/div[1]/div[1]/p/a/text()'
        url = mal_tree.xpath(url_path)
        name = mal_tree.xpath(name_path)
        if url != []:
            urls_lst[i-1].append(url[0])
            names_lst[i-1].append(name[0])
            true_count += 1
    url_count += 1
    if true_count == 0:
        break
unrolled_names = []
for names in names_lst:
    for name in names:
        unrolled_names.append(name)
unrolled_urls = []
for urls in urls_lst:
    for url in urls:
        unrolled_urls.append(url)
type_lst = []
for i in np.arange(6):
    for j in np.arange(len(urls_lst[i])):
        if i == 0:
            type_lst.append('TV (New)')
        elif i == 1:
            type_lst.append('TV (Continuing)')
        elif i == 2:
            type_lst.append('ONA')
        elif i == 3:
            type_lst.append('OVA')
        elif i == 4:
            type_lst.append('Movie')
        else:
            type_lst.append('Special')

#scraping info from urls
info = [[] for i in range(5)]
for url in unrolled_urls:
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,und;q=0.8',
        'upgrade-insecure-requests': '1'
    }
    url = str(url)
    anime_page = requests.get(url, headers=headers)
    anime_tree = html.fromstring(anime_page.content)
    score_path = '//*[@id="content"]/table/tr/td[2]/div[1]/table/tr[1]/td/div[1]/div[1]/div[1]/div[1]/div[1]/text()'
    rank_path = '//*[@id="content"]/table/tr/td[2]/div[1]/table/tr[1]/td/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/strong/text()'
    popularity_path = '//*[@id="content"]/table/tr/td[2]/div[1]/table/tr[1]/td/div[1]/div[1]/div[1]/div[1]/div[2]/span[2]/strong/text()'
    members_path = '//*[@id="content"]/table/tr/td[2]/div[1]/table/tr[1]/td/div[1]/div[1]/div[1]/div[1]/div[2]/span[3]/strong/text()'
    info[0].append(anime_tree.xpath(score_path))
    time.sleep(0.5)
    info[1].append(anime_tree.xpath(rank_path))
    time.sleep(0.5)
    info[2].append(anime_tree.xpath(popularity_path))
    time.sleep(0.5)
    info[3].append(anime_tree.xpath(members_path))
    time.sleep(0.5)

#Cleaning data
cleaned_info = [[] for i in range(4)]
for i in np.arange(5):
    for item in info[i]:
        if item == []:
            cleaned_info[i].append('N/A')
        else:
            cleaned_info[i].append(item[0].strip())
data_dct = {
    'Name': unrolled_names,
    'Type': type_lst,
    'Score': cleaned_info[0],
    'Rank': cleaned_info[1],
    'Popularity': cleaned_info[2],
    'Members': cleaned_info[3],
    'URL': unrolled_urls
}
df = pd.DataFrame(data=data_dct)

#Export to CSV
df.to_csv('current_season_anime.csv')

