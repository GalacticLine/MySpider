"""
爬取百度图片
"""
import logging
import re
import os
import requests


class BaiduImageCrawler:

    def __init__(self, keyword: str, path: str, ext='.jpg', timeout=5):
        """
        关键词爬取百度图片 爬虫类。
        :param keyword: 关键词
        :param path: 保存路径
        :param ext: 图像文件后缀
        :param timeout: 超时阈值
        """
        session = requests.session()
        session.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.198 Safari/537.36'
        })

        if not os.path.exists(path):
            os.makedirs(path)

        self.keyword = keyword
        self.path = path
        self.session = session
        self.timeout = timeout
        self.ext = ext
        self.main_url = 'http://image.baidu.com'

    def next_html(self, html):
        """
        获取下一页的html.
        :param html: 当前html
        :return: 下一页的html
        """
        url = self.main_url + re.findall('<div id="page">.*<a href="(.*?)" class="n">', html, re.S)[0]
        html = self.session.get(url).text
        return html

    def save_image(self, url, filepath):
        """
        保存单个图像。
        :param url: 图像url
        :param filepath: 保存路径
        :return:
        """
        if os.path.exists(filepath):
            print(filepath, '已经存在。')
            return

        try:
            img = self.session.get(url, timeout=self.timeout).content
            with open(filepath, 'wb') as fp:
                fp.write(img)
                print('保存成功：', filepath)
        except Exception as e:
            logging.warning(e)

    def save_images(self, html, page_idx):
        """
        保存某页的全部图像。
        :param html: html页面
        :param page_idx: 页面索引
        :return:
        """
        print('\n正在处理：第', page_idx, '页。\n')
        urls = re.findall('"objURL":"(.*?)"', html, re.S)
        for idx, url in enumerate(urls):
            name = f'{self.keyword}_{page_idx}_{idx}{self.ext}'
            self.save_image(url, f'{self.path}/{name}')

    def main(self, start=0, length=0):
        """
        根据关键词搜索相关百度图像并爬取。
        :param start: 起始页码
        :param length: 页码范围
        :return:
        """
        url = f'{self.main_url}/search/flip?tn=baiduimage&ie=utf-8&word={self.keyword}&ct=201326592&v=flip'
        html = self.session.get(url).text

        if start == 0:
            self.save_images(html, 1)

        if start > 0:
            for _ in range(start):
                html = self.next_html(html)

        for idx in range(length):
            html = self.next_html(html)
            self.save_images(html, start + idx + 2)


if __name__ == '__main__':
    crawler = BaiduImageCrawler('猫', "./BaiduImageCat")
    crawler.main()
