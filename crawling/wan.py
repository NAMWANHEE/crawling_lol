import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

os.environ.setdefault("DJANGO_SETTINGS_MODULE","crawling.settings")
import django
django.setup()
from opgg.models import *
# from crawling.opgg.models import *
from django.utils import timezone
def opgg_crawl():
    chromedriver = 'C:/chromedriver_win32/chromedriver'
    driver = webdriver.Chrome(chromedriver)
    rank = []
    tier = []
    points = []
    win = []
    lose = []
    win_ratio = []
    most1 = []
    most2 = []
    most3 = []

    cha_name = []
    data = []
    number = int(input("검색할 아이디 개수: "))
    for i in range(number):
        name = input('아이디: ')
        cha_name.append(name)
        driver.get('https://op.gg')
        a = driver.find_element_by_name('userName')
        a.send_keys(name)
        a.submit()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        rank.append(soup.select('span.ranking')[0].text)
        tier.append(soup.select('div.TierRank')[0].text)

        lp = soup.select('span.LeaguePoints')[0].text
        lp = lp.split(" ")[0]
        lp = lp.replace('\t', '').replace('\n', '').replace(',', '')
        points.append(int(lp))
        win.append(soup.select('span.wins')[0].text)
        lose.append(soup.select('span.losses')[0].text)
        win_ratio.append(soup.select('span.winratio')[0].text.split(" ")[1])
        most1.append(soup.select('div.ChampionName > a')[0].text.replace('\n', '').replace('\t', ''))
        most2.append(soup.select('div.ChampionName > a')[1].text.replace('\n', '').replace('\t', ''))
        most3.append(soup.select('div.ChampionName > a')[2].text.replace('\n', '').replace('\t', ''))
    data = [rank, tier, points, win, lose, win_ratio, most1, most2, most3]
    data1 = np.transpose(data)
    df = pd.DataFrame(data1, index=cha_name, columns=['랭킹', '티어', '점수', '승리', '패배', '승률', '모스트1', '모스트2', '모스트3'])
    df['랭킹'] = df['랭킹'].str.replace(',', '').astype('int64')
    df = df.sort_values('랭킹')

    return df



if __name__=='__main__':
    df = opgg_crawl()
    name=[]
    for j in Lol.objects.all():
        name.append(j.cha_name)
    for i in range(len(df)):
        if df.index[i] in name:
            Lol.objects.filter(cha_name = df.index[i]).update(rank=df['랭킹'][i],tier=df['티어'][i],points=df['점수'][i],win=df['승리'][i],lose=df['패배'][i],win_ratio=df['승률'][i],most1=df['모스트1'][i],most2=df['모스트2'][i],most3=df['모스트3'][i],update_time=timezone.now())

        else:
            a = Lol(cha_name=df.index[i],rank=df['랭킹'][i],tier=df['티어'][i],points=df['점수'][i],win=df['승리'][i],lose=df['패배'][i],win_ratio=df['승률'][i],most1=df['모스트1'][i],most2=df['모스트2'][i],most3=df['모스트3'][i])
            a.save()
