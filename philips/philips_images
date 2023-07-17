"""
飞利浦官网产品图片的爬取实现。
"""
import os
import time
import requests
from bs4 import BeautifulSoup

SEN = requests.Session()
SEN.headers.update({'Authorization': 'Bearer xx0d641857-e140-4e94-af32-ea8fe1063ce8',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/104.0.0.0 Safari/537.36'})


def search_products(keyword):
    """
    搜索飞利浦官网指定产品关键词，获取对应全部产品的Json数据。
    :param keyword: 关键词
    :return: json数据
    """
    url = 'https://koninklijkephilipsnvproduction2k8xfrmr.org.coveo.com/rest/search/v2'

    data = {'q': keyword,
            'facets': '[{"field":"commoncontenttypedict", "currentValues":[{"value":"产品","state":"selected"}]}]'}

    print('正在发送请求...')
    resp = SEN.post(url, data=data)

    num = resp.json()['totalCount']
    print(f'共 {num} 条数据。')

    if num > 0:
        new_data = data.copy()
        new_data.update({'numberOfResults': num})
        new_resp = SEN.post(url, data=new_data)
        results = new_resp.json()['results']
        print(f'Json数据获取成功。')

        return results


def craw_image(data, path, ext):
    """
    通过解析数据,爬取指定飞利浦官网产品图片。
    :param data: 存有产品信息的字典数据
    :param path: 保存图片的文件夹路径
    :param ext: 图片扩展名
    :return:
    """
    resp = SEN.get(data['uri'])

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
        if pic is not None:
            pic = pic.find('source')['srcset'].split(',')[1].replace(' 2x', '')
            print(f'图片路径: {pic}')
            response = SEN.get(pic)
            with open(save_path, 'wb') as f:
                f.write(response.content)
    except Exception as e:
        print(f'爬取图像时，发生未知错误: {e}')

    print(f'{name} 处理完成。')


def craw_images(keyword, path='./PhilipsImage', ext='jpg', freq=0.0):
    """
    爬取飞利浦指定产品全部图片。
    :param keyword: 搜索关键词
    :param path: 保存路径
    :param ext: 图片扩展名
    :param freq: 爬取频率
    :return:
    """
    if not os.path.exists(path):
        os.mkdir(path)

    print('图片将保存于: ', os.path.abspath(path))

    data = search_products(keyword)
    if not (data is None):
        length = len(data)
        for idx, val in enumerate(data):
            print(f'\n[{idx + 1}/{length}]')
            craw_image(val, path, ext)
            time.sleep(freq)


if __name__ == '__main__':
    craw_images('电视')
