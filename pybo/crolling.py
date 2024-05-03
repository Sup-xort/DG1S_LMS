import requests
from bs4 import BeautifulSoup
import collections
import pandas as pd
import datetime as dt
collections.Callable = collections.abc.Callable

def meal():
    x = dt.datetime.now()
    year = str(x.year - 2000)
    month = ('0' + str(x.month))[-2:]
    day = ('0' + str(x.day if x.hour <= 20 else x.day + 1))[-2:]

    url = "https://open.neis.go.kr/hub/mealServiceDietInfo?ATPT_OFCDC_SC_CODE=D10&SD_SCHUL_CODE=7240331&KEY=ed15a9e1057a458b8e2e286da26cf15c&MLSV_YMD=" + year + month + day
    request = requests.get(url)

    soup = BeautifulSoup(request.content, "html.parser")

    dish0=soup.find_all("ddish_nm")
    dish = []
    for i in range(3):
      if len(dish0) >= i + 1:
        dish2one=str(dish0[i]).split('[')
        dish2two=dish2one[2].split(']')
        dish2three=dish2two[0].split('<br/>')
        dish2 = []
        for d in dish2three:
          di = d.split(' ')
          dish2.append(di[0])
        dish.append(dish2)
      else:
        dish.append([f"준비된 {['조식', '중식', '석식'][i]}이 없습니다."])
    return dish