import requests
from bs4 import BeautifulSoup
import collections
import pandas as pd
import datetime as dt
collections.Callable = collections.abc.Callable

def meal():
    x=dt.datetime.now()
    year = x.year-2000
    month=x.month
    monthstr=""
    if month<10:
      monthstr="0"+str(month)
    else:
      monthstr=str(month)
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo?ATPT_OFCDC_SC_CODE=D10&SD_SCHUL_CODE=7240331&KEY=ed15a9e1057a458b8e2e286da26cf15c&MLSV_YMD=" + "20240329"#+str(year)+monthstr+str(x.day)
    request = requests.get(url)

    soup = BeautifulSoup(request.content, "html.parser")

    dish0=soup.find_all("ddish_nm")

    dish = []

    dish1one=str(dish0[0]).split('[')
    dish1two=dish1one[2].split(']')
    dish1three=dish1two[0].split('<br/>')
    dish1 = []
    for d in dish1three:
      di = d.split(' ')
      dish1.append(di[0])

    dish2one=str(dish0[1]).split('[')
    dish2two=dish2one[2].split(']')
    dish2three=dish2two[0].split('<br/>')
    dish2 = []
    for d in dish2three:
      di = d.split(' ')
      dish2.append(di[0])

    dish3 = []
    if len(dish0) == 3:
      dish3one=str(dish0[2]).split('[')
      dish3two=dish3one[2].split(']')
      dish3three=dish3two[0].split('<br/>')
      for d in dish3three:
        di = d.split(' ')
        dish3.append(di[0])
    else:
        dish3.append("준비된 석식이 없습니다.")

    dish.append(dish1)
    dish.append(dish2)
    dish.append(dish3)
    return dish