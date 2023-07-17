"""
爬取第一PPT
"""
import time
import requests
import os.path
from typing import OrderedDict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class FirstPPTCrawler:

    def __init__(self, target: str, path: str, down_line=0, freq=2):
        """
        第一PPT爬虫类
        :param target: 爬取目标板块
        :param path: 保存路径
        :param down_line: 下载线路，0或者1
        :param freq: 爬取频率
        """
        path = os.path.abspath(path)
        if not os.path.exists(path):
            os.makedirs(path)

        options = Options()
        options.add_experimental_option("prefs", {"download.default_directory": path})

        self.main_url = 'https://www.1ppt.com'
        self.download_url = self.main_url + '/xiazai'
        self.target_url = self._get_target_url(target)
        self.browser = webdriver.Chrome(options=options)

        assert down_line == 0 or down_line == 1
        self.down_mode = down_line
        self.freq = freq

    def _get_target_url(self, target):
        resp = requests.get(self.download_url)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, 'html.parser')
        target = soup.select(f'a:-soup-contains("{target}")')[0]['href']
        target = self.main_url + target[:-1]
        return target

    def craw_ppts(self, page_idx=0, start=0, length=1):
        """
        获取多个ppt.
        :param page_idx: 页码
        :param start: 当前页起始ppt索引
        :param length: 获取数量
        :return:
        """
        if page_idx == 0:
            resp = requests.get(self.target_url)
        else:
            target = self.target_url.split('/')[-1]
            resp = requests.get(self.target_url + f'/ppt_{target}_{page_idx}.html')

        soup = BeautifulSoup(resp.text, 'html.parser')

        ul = soup.find('ul', class_='tplist')
        anchors = ul.find_all('a', target='_blank')
        hrefs = [a['href'] for a in anchors]
        hrefs = list(OrderedDict.fromkeys(hrefs))

        for href in hrefs[start:length]:
            self.craw_ppt(href)
            time.sleep(self.freq)
        return hrefs

    def craw_ppt(self, href):
        """
        获取指定ppt.
        :param href: 链接
        :return:
        """
        self.browser.get(self.main_url + href)

        box = self.browser.find_element(by=By.CLASS_NAME, value='downurllist')
        li = box.find_element(by=By.TAG_NAME, value='li')
        li.click()

        window_handles = self.browser.window_handles
        self.browser.switch_to.window(window_handles[-1])

        box = self.browser.find_element(by=By.CLASS_NAME, value='downloadlist')
        if self.down_mode == 0:
            mode = 'c1'
        else:
            mode = 'c2'
        li = box.find_element(by=By.CLASS_NAME, value=mode)
        li.click()

