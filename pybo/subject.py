import requests
from datetime import datetime, timedelta
import re
import calendar
import os


def subject(day):
    target_date = (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')

    # Load existing meal data
    if os.path.exists('time_table.txt'):
        with open('time_table.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                date, a1, b1, a3, b3, a, b = line.strip().split('|')
                a1 += 'T'
                b1 += 'T'
                a3 += 'T'
                b3 += 'T'
                a += 'T'
                b += 'T'

                if date == target_date:
                    sub = {
                        '1': [a1, b1],
                        '2': [b1, a1],
                        '3': [a3, b3],
                        '4': [b3, a3],
                        'A': [a, a],
                        'B': [b, b]
                    }
                    return sub
    return {
        '1': "방과후 수업이 없는 날입니다.",
        '2': "방과후 수업이 없는 날입니다.",
        '3': "방과후 수업이 없는 날입니다.",
        '4': "방과후 수업이 없는 날입니다.",
        'A': "방과후 수업이 없는 날입니다.",
        'B': "방과후 수업이 없는 날입니다."
        }

