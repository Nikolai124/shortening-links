import argparse
from dotenv import load_dotenv
import os
import requests 
from urllib.parse import urlparse

def shorten_link(token, url):
    url_vk = 'https://api.vk.ru/method/utils.getShortLink' 
    params = { 
        'v': 5.236,
        'access_token': token,
        'url': url,
        'private': 0
    } 
    response = requests.get(url_vk, params=params) 
    response.raise_for_status() 
    short_link = response.json()['response']['short_url'] 
    return short_link 


def count_clicks(token, short_link): 
    url_vk = 'https://api.vk.ru/method/utils.getLinkStats'
    short_link_parts = urlparse(short_link) 
    path = short_link_parts.path.replace("/", "") 
    params = { 
        'v': 5.236,
        'access_token': token,
        'key': path
    }
    response = requests.get(url_vk, params=params) 
    count_clicks = response.json()['response']['stats'][0]['views'] 
    return count_clicks 


def is_shorten_link(token, url):
    url_template = 'https://api.vk.ru/method/utils.getLinkStats'
    url_parts = urlparse(url)
    path = url_parts.path.replace("/", "")
    params = { 
        'v': 5.236,
        'access_token': token,
        'key': path
    }
    response = requests.get(url_template, params=params) 
    response.raise_for_status()
    return "response" in response.json() 


def main():
    load_dotenv() 
    parser = argparse.ArgumentParser(
        description='сокращение ссылки и подсчёт кликов по ссылке'
    )
    parser.add_argument('url', help='ссылка')
    args = parser.parse_args()
    token = os.environ['VK_TOKEN'] 
    if is_shorten_link(token, args.url): 
        try: 
            print("Количество переходов по ссылке", count_clicks(token, args.url)) 
        except IndexError: 
            print("Переходов по ссылке не было")
        
    else: 
        try:
            short_link = shorten_link(token, args.url) 
            print("Сокращенная ссылка:", short_link) 
        except KeyError:
            print("Неправельно введена ссылка!") 
    
    

if __name__ == '__main__':
    main()     


