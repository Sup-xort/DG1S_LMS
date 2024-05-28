import requests
from bs4 import BeautifulSoup
import collections
import pandas as pd
import datetime as dt
collections.Callable = collections.abc.Callable

def meal():
    x = dt.datetime.now()
    url = ("https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=blBI&pkid=682&os=24929848&qvt=0&query=%EB%8C%80%EA%B5%AC%EC%9D%BC%EA%B3%BC%ED%95%99%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90%20%EA%B8%89%EC%8B%9D%EC%8B%9D%EB%8B%A8")
    request = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(request.content, "html.parser")

    today_menu = []
    title = soup.find_all('div', class_='timeline_box')
    breakfast = [title]
    lunch = ["준비된 식사가 없습니다"]
    dinner = ["준비된 식사가 없습니다"]

    for i in title:
        date = i.find('strong', class_='cm_date')
        t = date.text
        if t[-5:] == "TODAY":
            if "조식" in i.text:
                menus = i.find('ul', class_='item_list')
                breakfast = menus.text.split()
            elif "중식" in i.text:
                menus = i.find('ul', class_='item_list')
                lunch = menus.text.split()
            elif "석식" in i.text:
                menus = i.find('ul', class_='item_list')
                dinner = menus.text.split()
            else:
                continue
    today_menu.append(breakfast)
    today_menu.append(lunch)
    today_menu.append(dinner)
    return today_menu