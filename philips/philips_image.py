"""
飞利浦官网指定类型产品及其相关产品图片的爬取实现。
"""
import os
import time
import requests
from bs4 import BeautifulSoup

# 全局请求头
HEADERS = {'Authorization': 'Bearer xx0d641857-e140-4e94-af32-ea8fe1063ce8',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/104.0.0.0 Safari/537.36'}

# 全局会话
SEN = requests.Session()
SEN.headers.update(HEADERS)


def is_resp_ok(resp):
    """
    判断请求是否成功，如果失败打印错误信息。
    :param resp: 响应数据
    :return: 是否成功
    """
    code = resp.status_code

    if code == 200:
        return True
    else:
        print(f'请求 {resp.url} 失败,错误代码: {code}')
        return False


def search_products(key):
    """
    搜索飞利浦官网指定产品关键词，获取对应全部产品的Json数据。
    :param key: 关键词
    :return: json数据
    """
    url = 'https://koninklijkephilipsnvproduction2k8xfrmr.org.coveo.com/rest/search/v2'

    data = {'q': key,
            'facets': '[{"field":"commoncontenttypedict", "currentValues":[{"value":"产品","state":"selected"}]}]'}

    print('正在发送请求...')
    resp = SEN.post(url, data=data)

    if is_resp_ok(resp):
        num = resp.json()['totalCount']
        print(f'共 {num} 条数据。')
        if num > 0:
            new_data = data.copy()
            new_data.update({'numberOfResults': num})
            print('正在重发请求...')
            new_resp = SEN.post(url, data=new_data)
            results = new_resp.json()['results']
            print(f'Json数据获取成功。')
            return results


def crawl_picture(data, path, ext):
    """
    通过解析字典数据,爬取指定飞利浦官网产品图片，并保存。
    :param data: 存有产品信息的字典数据
    :param path: 保存图片的文件夹路径
    :param ext: 图片扩展名
    :return:
    """
    resp = SEN.get(data['uri'])
    if not is_resp_ok(resp):
        return

    try:
        name = data['raw']['ps_productid'][0].replace('/', '-')
    except KeyError:
        name = time.strftime("%H_%M_%S", time.localtime())

    print(f'正在处理... {name}')

    save_path = f'{path}/{name}.{ext}'
    if os.path.exists(save_path):
        print(f'{save_path} 已存在。')
        return

    try:
        soup = BeautifulSoup(resp.text, 'html.parser')
        pic = soup.find('picture', class_='p-picture p-normal-view p-is-zoomable')
        if not (pic is None):
            pic = pic.find('source')['srcset'].split(',')[1].replace(' 2x', '')
            print(f'图片路径: {pic}')
            response = SEN.get(pic)
            if is_resp_ok(response):
                with open(save_path, 'wb') as f:
                    f.write(response.content)
    except Exception as e:
        print(f'爬取图像时，发生未知错误: {e}')

    print(f'{name} 处理完成。')


def crawl_pictures(data, path,  ext, freq):
    """
    爬取飞利浦json数据全部图片。
    :param path: 保存图片的文件夹路径
    :param data: 指定json数据
    :param ext: 图片扩展名
    :param freq: 爬取阻塞频率
    :return:
    """
    if not (data is None):
        length = len(data)
        for idx, val in enumerate(data):
            print(f'\n[{idx + 1}/{length}]')
            crawl_picture(val, path, ext)
            time.sleep(freq)


def main(keyword, path='./PhilipsImage', ext='jpg', freq=0.0):
    """
    飞利浦官网爬取某类产品及其相关产品图片的爬虫主函数。
    :param path: 保存图片的文件夹路径
    :param keyword: 产品关键词，可为飞利浦官网能搜到的任意产品类型
    :param ext: 图片扩展名
    :param freq: 爬取阻塞频率
    :return:
    """
    if not os.path.exists(path):
        os.mkdir(path)

    print('图片将保存于: ', os.path.abspath(path))

    search_data = search_products(keyword)
    crawl_pictures(search_data, path, ext, freq)


if __name__ == '__main__':
    main('电视')
