import requests
from bs4 import BeautifulSoup
import xlwt

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('豆瓣电影TOP250', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '图片')
sheet.write(0, 2, '排名')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '作者')
sheet.write(0, 5, '简介')
n = 1

def parse_result(s:str):
    soup = BeautifulSoup(s, 'lxml')
    l = soup.find(class_="grid_view").find_all('li')
    for item in l:
        item_name = item.find(class_='title').string
        item_image = item.find('a').find('img').get('src')
        item_rank = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text.strip()
        if item.find(class_='inq'):
            item_intro = item.find(class_='inq').string
        global n
        sheet.write(n, 0, item_name)
        sheet.write(n, 1, item_image)
        sheet.write(n, 2, item_rank)
        sheet.write(n, 3, item_score)
        sheet.write(n, 4, item_author)
        sheet.write(n, 5, item_intro)
        n += 1
        print('爬取电影：' + item_rank + ' | ' + item_name + ' | ' + item_score + ' | ' + item_intro)

def douban_request(url:str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def main(page):
    url = 'https://movie.douban.com/top250?start='+str(page*25)+'&filter='
    html = douban_request(url)
    parse_result(html)

if __name__ == '__main__':
    for i in range(25):
        main(i)

book.save(u'豆瓣最受欢迎的250部电影.xlsx')

