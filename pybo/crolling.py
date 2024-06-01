import requests
from bs4 import BeautifulSoup
import collections
import pandas as pd
from datetime import *
import re
collections.Callable = collections.abc.Callable

def meal(day):
    x = datetime.now()
    if x.hour >= 20:
        x = x + timedelta(days=day) + timedelta(days=1)
    else:
        x = x + timedelta(days=day)
    today = "%4d%02d%02d"%(x.year, x.month, x.day)
    
    url = 'https://open.neis.go.kr/hub/mealServiceDietInfo?ATPT_OFCDC_SC_CODE=D10&SD_SCHUL_CODE=7240331&KEY=ed15a9e1057a458b8e2e286da26cf15c&MLSV_YMD='+str(today)
    xmlfile = requests.get(url)
    
    soup = BeautifulSoup(xmlfile.content, "html.parser")
    
    menu = soup.find_all('row')
    
    today_menu = []
    breakfast = ["준비된 식사가 없습니다"]
    lunch=["준비된 식사가 없습니다"]
    dinner = ["준비된 식사가 없습니다"]
    
    for i in menu:
        types = i.find('mmeal_sc_nm')
        if types.text == "중식":
            menus = i.find('ddish_nm')
            lunch = menus.text.split('<br/>')
        elif types.text == "조식":
            menus = i.find('ddish_nm')
            breakfast = menus.text.split('<br/>')
        elif types.text == "석식":
            menus = i.find('ddish_nm')
            dinner = menus.text.split('<br/>')
        else:
            continue
    
    today_menu.append(breakfast)
    today_menu.append(lunch)
    today_menu.append(dinner)
    
    pattern = r'\([^)]*\)'
    for i in range(len(today_menu)):
        for j in range(len(today_menu[i])):
            today_menu[i][j] = re.sub(pattern=pattern, repl='', string= today_menu[i][j])
    today_menu.append("%4d-%02d-%02d"%(x.year, x.month, x.day))
    return today_menu
