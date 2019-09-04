#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import requests
import json
import os
def parse_result(s:str):
    pattern = re.compile('<li>.*?list_num.*?(\d+).*?src=\"(.*?jpg).*?title=\"(.*?)\".*?class="tuijian">(.*?)<.*?title="(.*?)".*?五星评分.*?(\d+次).*?price_n">&yen;(\d+.\d+).*?</li>', re.S)
    items = re.findall(pattern, s)
    for item in items:
        yield {
            'range': item[0],
            'iamge': item[1],
            'title': item[2],
            'recommend': item[3],
            'author': item[4],
            'times': item[5],
            'price': item[6]
        }

def dangdang_request(url:str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def write_to_txt(item, path):
    print('开始写入===>', str(item))
    with open(path, 'a', encoding='UTF-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
        f.close()

def main():
    for i in range(25):
        url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(i)
        html = dangdang_request(url)
        items = parse_result(html)
        for item in items:
            write_to_txt(item, 'C:\\Users\\pp517\\Desktop\\dangdang_500book.txt')

if __name__ == '__main__':
    main()


