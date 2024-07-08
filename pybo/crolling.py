import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import calendar
import os

def fetch_meal_info(date):
    base_url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
    params = {
        'ATPT_OFCDC_SC_CODE': 'D10',
        'SD_SCHUL_CODE': '7240331',
        'KEY': 'ed15a9e1057a458b8e2e286da26cf15c',
        'MLSV_YMD': date.strftime('%Y%m%d')
    }

    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    menu = soup.find_all('row')

    date_meal = {
        'date': date.strftime('%Y-%m-%d'),
        'breakfast': "준비된 식사가 없습니다",
        'lunch': "준비된 식사가 없습니다",
        'dinner': "준비된 식사가 없습니다"
    }

    for item in menu:
        meal_type = item.find('mmeal_sc_nm').text
        dishes = item.find('ddish_nm').text.split('<br/>')
        dishes = [re.sub(r'\([^)]*\)', '', dish).strip() for dish in dishes]

        if meal_type == '조식':
            date_meal['breakfast'] = ', '.join(dishes)
        elif meal_type == '중식':
            date_meal['lunch'] = ', '.join(dishes)
        elif meal_type == '석식':
            date_meal['dinner'] = ', '.join(dishes)

    return date_meal

def meal(day):
    target_date = (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')
    meal_data = {}
    print(target_date)

    # Load existing meal data
    if os.path.exists('meal_info.txt'):
        with open('meal_info.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                date, breakfast, lunch, dinner = line.strip().split('|')
                if date == target_date:
                    meal_data = {
                        'breakfast': breakfast,
                        'lunch': lunch,
                        'dinner': dinner,
                        'date': target_date
                    }
                    return meal_data


    new_meal_info = fetch_meal_info(datetime.now() + timedelta(days=day))
    with open('meal_info.txt', 'a', encoding='utf-8') as file:
        file.write(f"{new_meal_info['date']}|{new_meal_info['breakfast']}|{new_meal_info['lunch']}|{new_meal_info['dinner']}\n")
    new_meal_info['date'] = target_date
    return new_meal_info


def remove_duplicate_dates():
    if not os.path.exists('meal_info.txt'):
        print("파일이 존재하지 않습니다.")
        return

    meal_data = {}

    # Read existing meal data
    with open('meal_info.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            date, breakfast, lunch, dinner = line.strip().split('|')
            meal_data[date] = {
                'breakfast': breakfast,
                'lunch': lunch,
                'dinner': dinner
            }

    # Sort meal data by date and remove duplicates
    sorted_meal_data = dict(sorted(meal_data.items()))

    # Write updated meal data back to file
    with open('meal_info.txt', 'w', encoding='utf-8') as file:
        for date, meals in sorted_meal_data.items():
            file.write(f"{date}|{meals['breakfast']}|{meals['lunch']}|{meals['dinner']}\n")

def update_meal(s, e):
    for i in range(s, e + 1):
        meal(i)
    remove_duplicate_dates()
