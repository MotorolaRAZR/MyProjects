import requests
import random
import time
a,b,c = (random.randint(0,10000) for i in range(3))
cookies = {
    'dl': f'dl=dl.{a}.{b}.{c}',
}

#a
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9',
    'cookie': f'dl=dl.{a}.{b}.{c}',
    'priority': 'u=0, i',
    'referer': 'https://cp.edusite.ru/dl.html?uri=volsch12.edusite.ru/DswMedia/izmras1.pdf',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://cp.edusite.ru/dl_load.html?uri=volsch12.edusite.ru/DswMedia/izmras1.pdf',
    cookies=cookies,
    headers=headers,
)

response = requests.get(
    'https://volsch12.edusite.ru/DswMedia/izmras1.pdf',
    cookies=cookies,
    headers=headers,
)

with open("aaa.pdf",'wb', ) as f:
    f.write(response.content)
