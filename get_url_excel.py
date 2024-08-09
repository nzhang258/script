import requests
import re
from bs4 import BeautifulSoup
import csv
import time
import urllib.parse



def url2dict(url, target_string):
    # 目标网页URL
    #url = 'https://www.hotelaah.com/liren/anhui_wuhu.html'

    # 发送HTTP请求，获取网页内容
    response = requests.get(url)
    # 尝试使用utf-8解码，如果失败，尝试gbk
    try:
        web_content = response.content.decode('utf-8')
    except UnicodeDecodeError:
        web_content = response.content.decode('gbk', errors='ignore')  # Using 'ignore' to skip problematic characters

    # web_content = response.content.decode('utf-8') or response.content.decode('gbk')

    # 使用BeautifulSoup解析网页
    soup = BeautifulSoup(web_content, 'html.parser')

    # 由于网页可能存在乱码，我们使用正则表达式来查找表格
    from re import findall
    table_pattern = r'<table.*?>(.*?)</table>'
    tables_html = findall(table_pattern, web_content, re.DOTALL)

    # 初始化存储结果的列表
    # secretaries = []  # 市委书记信息
    # mayors = []       # 市长信息
    res = []
    # 遍历所有找到的表格
    for table_html in tables_html:
        # 使用BeautifulSoup解析每个表格
        table_soup = BeautifulSoup(table_html, 'html.parser')
        # 找到表格中的每一行
        for row in table_soup.find_all('tr')[1:]:  # 跳过标题行
            cols = row.find_all('td')
            if len(cols) == 2:  # 确保行中只有两列数据
                term = cols[0].text.strip()
                name = cols[1].text.strip()
                # 打印市委书记和市长信息
                if target_string in table_html:
                    res.append((term, name))
                # elif '市长' in table_html:
                #     mayors.append((term, name))
    return res

def remove_illegal_spaces(text):
    # 正则表达式匹配全角空格（\u3000）以及其他非法空白字符
    pattern = re.compile(r'[\u3000\s]+')
    return pattern.sub(' ', text)


def main():
    ### 
    #  输入网页html， 提取关键字 “市长”/“市委书记”，把相关信息表格保存在csv
    ###
    # Define the base URL of the website
    base_url = 'https://www.hotelaah.com/liren/'

    # URL of the main page
    main_url = f'{base_url}/index.html'

    # Send a GET request to the main page
    response = requests.get(main_url)
    response.encoding = 'utf-8'  # Ensure proper encoding

    # Parse the main page content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Create a CSV file to save the data

        # Find all the city links containing "市" in the text
    for link in soup.find_all('a', href=True):
        
        if "市" in link.text and "区" not in link.text:

            city_name = link.text.strip()
            city_href = link['href']

            if not city_href.startswith('http'):
                city_url = urllib.parse.urljoin(base_url, city_href)
            else:
                city_url = city_href
            print(f'processing {city_name}.... url is {city_url}')

            res1 = url2dict(city_url, "市委书记")
            with open('city_leaders_书记.csv', 'a', newline='', encoding='utf-8') as csvfile1:
                csvwriter1 = csv.writer(csvfile1)
                for term, name in res1:
                    if term=='任期' or term=='':
                        continue
                    term = remove_illegal_spaces(term)
                    name = remove_illegal_spaces(name)
                    csvwriter1.writerow([city_name, term, name])
            
            res2 = url2dict(city_url, "市长")
            with open('city_leaders_市长.csv', 'a', newline='', encoding='utf-8') as csvfile2:
                csvwriter2 = csv.writer(csvfile2)
                for term, name in res2:
                    if term=='任期' or term=='':
                        continue
                    term = remove_illegal_spaces(term)
                    name = remove_illegal_spaces(name)
                    csvwriter2.writerow([city_name, term, name])


if __name__ == '__main__':
    main()

