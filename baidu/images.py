"""
爬取百度图片
"""
import re
import os
import time
import logging
import requests


class BaiduImageCrawler:

    def __init__(self, keyword: str, path: str, ext='.jpg', timeout=5, freq=1):
        """
        关键词爬取百度图片 爬虫类。
        :param keyword: 关键词
        :param path: 保存路径
        :param ext: 图像文件后缀
        :param timeout: 超时阈值
        :param freq: 爬取频率
        """
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/104.0.0.0 Safari/537.36'
        })

        if not os.path.exists(path):
            os.makedirs(path)

        self.keyword = keyword
        self.path = path
        self.session = session
        self.timeout = timeout
        self.ext = ext
        self.main_url = 'http://image.baidu.com'
        self.freq = freq

    def next_html(self, html):
        """
        获取下一页的html.
        :param html: 当前html
        :return: 下一页的html
        """
        url = self.main_url + re.findall('<div id="page">.*<a href="(.*?)" class="n">', html, re.S)[0]
        html = self.session.get(url).text
        return html

    def craw_image(self, url, filepath):
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

    def craw_images(self, html, page_idx):
        """
        保存某页的全部图像。
        :param html: html页面
        :param page_idx: 页面索引
        :return:
        """
        print('\n正在处理：第', page_idx, '页。\n')
        urls = re.findall('"objURL":"(.*?)"', html, re.S)

        length = len(urls)
        for idx, url in enumerate(urls):
            print(f'\n[{idx + 1}/{length}]')
            name = f'{self.keyword}_{page_idx}_{idx}{self.ext}'
            self.craw_image(url, f'{self.path}/{name}')
            time.sleep(self.freq)

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
            self.craw_images(html, 1)

        if start > 0:
            for _ in range(start):
                html = self.next_html(html)
                time.sleep(self.freq)

        for idx in range(length):
            html = self.next_html(html)
            self.craw_images(html, start + idx + 2)
