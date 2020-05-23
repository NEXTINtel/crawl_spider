"""
此页面用于爬取雪球网单支股票数据
Created by CSDN梦栖，2020-05-22
"""

# 导库
import os

from bs4 import BeautifulSoup
import requests
import csv

message = '即将开始处理...'


# 获取源数据
def get_source_data(source_file_path):
    stock_id_list = []
    with open(source_file_path, 'r', encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader)  # 不读取表头信息
        for r in reader:
            try:
                stock_id = r[0]  # 仅获取第一列的股票号即可
                stock_id_list.append(stock_id)
            except:
                continue
    return stock_id_list


def get_source_data_name(source_file_path):
    stock_name_list = []
    with open(source_file_path, 'r', encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader)  # 不读取表头信息
        for r in reader:
            try:
                stock_name = r[1]  # 仅获取第一列的股票名称即可
                stock_name_list.append(stock_name)
            except:
                continue
    return stock_name_list


def http_header():
    # 定制请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77',

        'Referer': 'https://xueqiu.com/k?q=600074'
    }

    return headers


def parse_page(url):
    headers = http_header()

    response = requests.get(url, headers=headers)

    text = response.content.decode('utf-8')

    soup = BeautifulSoup(text, 'lxml')

    tableData = soup.find('table', class_='quote-info')

    data_list = []

    if tableData:
        for table in tableData:
            spans = table.find_all('span')
            for span in spans:
                data_list.append(span.get_text())

    return data_list


def handle_url(stock_id_list, stock_name_list, target_file):
    # 处理股票的id
    new_stock_id_list = []
    for i in stock_id_list:
        stock_id_temp = i
        stock_id_part1 = stock_id_temp[0:-3]
        stock_id_part2 = stock_id_temp[7:9]
        new_stock_id = stock_id_part2 + stock_id_part1
        new_stock_id_list.append(new_stock_id)

    url_origin = 'https://xueqiu.com/S/'  # 原始url

    # 写入csv表头
    headers = ['股票代号', '股票名', '最高', '今开', '涨停', '成交量', '最低', '昨收', '跌停', '成交额', '量比', '换手', '市盈率(动)', '市盈率(TTM)', '委比',
               '振幅', '市盈率(静)',
               '市净率', '每股收益', '股息(TTM)', '总股本', '总市值', '每股净资产', '股息率(TTM)', '流通股', '流通值', '52周最高', '52周最低', '货币单位']

    with open(target_file, 'w', encoding='gbk', newline='') as fp:
        writer = csv.DictWriter(fp, headers)
        writer.writeheader()

    '''headers2 = ['跳过的数据url']
    with open('jumpData.csv', 'w', encoding='utf-8', newline='') as fp:
        writer = csv.DictWriter(fp, headers2)
        writer.writeheader()'''

    # 进行查询与写入处理
    jump_data_url = {}
    for i in range(len(new_stock_id_list)):
        current_stock_id = new_stock_id_list[i]
        current_stock_name = stock_name_list[i]
        url = url_origin + current_stock_id  # 拼接每支股票的url
        global message
        message = "开始第" + str(i) + "支股票爬取...股票id为：" + current_stock_id + "...爬取链接为：" + url
        print("开始第" + str(i) + "支股票爬取...股票id为：" + current_stock_id + "...爬取链接为：" + url)
        data_item = parse_page(url)  # 返回每支股票的详情
        dict_item = {}
        print("股票信息字段大小为：" + str(len(data_item)))
        if len(headers) - 2 == len(data_item):
            dict_item[headers[0]] = current_stock_id
            dict_item[headers[1]] = current_stock_name
            for j in range(2, 2 + len(data_item)):
                dict_item[headers[j]] = data_item[j - 2]
                # target_data.append(dict_item)
            with open(target_file, 'a+', encoding='gbk', newline='') as fp:
                writer = csv.DictWriter(fp, headers)
                writer.writerows([dict_item])
        '''else:
            jump_data_url["跳过的数据url"] = url
            with open('jumpData.csv', 'a+', encoding='gbk', newline='') as fp:
                writer = csv.DictWriter(fp, headers2)
                writer.writerows([jump_data_url])'''

    print("股票数据爬取成功！\n数据文件路径为：" + os.path.realpath(target_file))


def give_message():
    return message


def main():
    source_file_path = 'sourceData.csv'  # 源数据文件路径
    target_file_path = 'targetData2.csv'  # 目的数据文件路径

    stock_id_list = get_source_data(source_file_path)
    stock_name_list = get_source_data_name(source_file_path)
    handle_url(stock_id_list, stock_name_list, target_file_path)

# main()
