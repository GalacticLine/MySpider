"""
爬取飞利浦官网产品图片。
"""
import os
import time
import requests
from bs4 import BeautifulSoup


class PhilipImageCrawler:
    def __init__(self, keyword: str, path: str, ext='.jpg'):
        """
        关键词爬取飞利浦产品图片 爬虫类。
        :param keyword: 关键词
        :param path: 保存路径
        :param ext: 图像文件后缀
        """
        session = requests.session()
        session.headers.update({
            'Authorization': 'Bearer xx0d641857-e140-4e94-af32-ea8fe1063ce8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/104.0.0.0 Safari/537.36'})

        if not os.path.exists(path):
            os.makedirs(path)

        self.keyword = keyword
        self.path = path
        self.session = session
        self.ext = ext

    def search_products(self):
        """
        搜索飞利浦官网指定产品关键词，获取对应全部产品的Json数据。
        :return: json数据
        """
        url = 'https://koninklijkephilipsnvproduction2k8xfrmr.org.coveo.com/rest/search/v2'

        data = {'q': self.keyword,
                'facets': '[{"field":"commoncontenttypedict", "currentValues":[{"value":"产品","state":"selected"}]}]'}

        resp = self.session.post(url, data=data)
        num = resp.json()['totalCount']

        if num > 0:
            new_data = data.copy()
            new_data.update({'numberOfResults': num})
            new_resp = self.session.post(url, data=new_data)
            results = new_resp.json()['results']
            return results

    def craw_image(self, data):
        """
        通过解析数据,爬取指定飞利浦官网产品图片。
        :param data: 存有产品信息的字典数据

        :return:
        """
        resp = self.session.get(data['uri'])

        try:
            name = data['raw']['ps_productid'][0].replace('/', '-')
        except KeyError:
            name = time.strftime("%H_%M_%S", time.localtime())

        save_path = f'{self.path}/{name}.{self.ext}'
        if os.path.exists(save_path):
            print(save_path, '已存在。')
            return

        try:
            soup = BeautifulSoup(resp.text, 'html.parser')
            pic = soup.find('picture', class_='p-picture p-normal-view p-is-zoomable')
            if pic is not None:
                pic = pic.find('source')['srcset'].split(',')[1].replace(' 2x', '')
                response = self.session.get(pic)
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                    print('保存成功：', save_path)
        except Exception as e:
            print(f'爬取图像时，发生未知错误: {e}')

    def craw_images(self):
        """
        爬取飞利浦指定产品全部图片。
        :return:
        """
        data = self.search_products()
        if not (data is None):
            length = len(data)
            for idx, val in enumerate(data):
                print(f'\n[{idx + 1}/{length}]')
                self.craw_image(val)


if __name__ == '__main__':
    crawler = PhilipImageCrawler('电视', './PhilipsImageTV')
    crawler.craw_images()
