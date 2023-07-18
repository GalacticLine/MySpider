"""
京东图片爬虫
"""
import time
import random
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class JDInfoCrawler:
    def __init__(self, keyword, freq=random.randint(1, 2)):
        """
        京东爬取产品信息 爬虫类
        :param keyword: 关键词
        :param freq: 爬取频率
        """
        self.main_url = 'https://search.jd.com/'
        self.keyword = keyword
        self.freq = freq
        self.browser = webdriver.Chrome()
        self.df = pd.DataFrame(columns=['价格', '店铺', '评论数'])

    def search_products(self):
        """
        搜索产品
        :return: 
        """
        self.browser.get(self.main_url)

        search_box = self.browser.find_element(by=By.ID, value='keyword')
        search_box.clear()

        time.sleep(0.1)
        search_box.send_keys(self.keyword)
        time.sleep(0.1)

        search_box.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(1)

    def next_page(self):
        """
        跳转到下一页
        :return: 
        """
        next_page_button = self.browser.find_element(by=By.CSS_SELECTOR, value='.pn-next')
        next_page_button.click()
        time.sleep(0.5)

    def get_product_info(self, product):
        """
        获取产品信息。
        :param product: 产品
        :return: 
        """
        try:
            name = product.find_element(by=By.CSS_SELECTOR, value='.p-name a em').text.strip()
            price = product.find_element(by=By.CSS_SELECTOR, value='.p-price i').text.strip()
            shop = product.find_element(by=By.CSS_SELECTOR, value='.p-shop span a').text.strip()
            comment = product.find_element(by=By.CSS_SELECTOR, value='.p-commit strong a').text.strip()
            self.df.loc[name] = {'价格': price, '店铺': shop, '评论数': comment}
            time.sleep(self.freq)
            print('商品名称：', name)
        except Exception as e:
            logging.warning(e)
            pass

    def get_products_info(self):
        """
        批量获取产品信息
        :return: 
        """
        total_height = self.browser.execute_script("return document.body.scrollHeight")
        num = 5
        scroll_distance = round(total_height / num)

        for i in range(num):
            start = scroll_distance * i
            end = scroll_distance * (i + 1)
            self.browser.execute_script(f"window.scrollBy({start}, {end});")
            time.sleep(1)

        products = self.browser.find_elements(by=By.CSS_SELECTOR, value='#J_goodsList .gl-item')
        for product in products:
            self.get_product_info(product)

    def main(self, start=0, length=0):
        """
        爬虫主函数
        :param start: 起始页索引 
        :param length: 爬取页数
        :return: 
        """
        self.search_products()
        input('请按任意key继续...')

        if start > 0:
            for _ in range(start):
                self.next_page()

        if length == 0:
            self.get_products_info()
        else:
            for _ in range(length):
                self.get_products_info()
                self.next_page()
        self.browser.quit()
