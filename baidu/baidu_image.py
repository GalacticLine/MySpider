import time
import logging
import os.path
import urllib.request
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def scroll_refresh(browser, wait_time=1):
    """
    滑动底部，并等待网页刷新，图像加载。
    :param browser: 浏览器对象
    :param wait_time: 等待时间
    :return:
    """
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(wait_time)


def save_image(url, save_path):
    """
    保存单张图片
    :param url: 图像url
    :param save_path: 保存路径
    :return:
    """

    img = urllib.request.urlopen(url)
    img = Image.open(img)
    save_path = f'{save_path}/img{int(time.time())}'
    try:
        img.save(save_path + '.jpg')
        print('保存成功：', url)
    except OSError:
        img.save(save_path + '.png')
        print('保存成功：', url)
    except Exception as e:
        logging.warning(f'保存失败：{url}，错误：{e}')


def save_images(browser, save_path):
    """
    保存当前滚动页面全部图片
    :param browser: 浏览器对象
    :param save_path: 保存路径
    :return:
    """
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('img', class_='main_img img-hover')

    for img in images:
        save_image(img['src'], save_path)

    scroll_refresh(browser, wait_time=2)


def craw_image(keyword: str, start=0, length=2, save_path='./Image'):
    """
    爬取百度图片实现
    :param keyword: 图片搜索关键字
    :param start: 起始滚动位置
    :param length: 爬取滚动页面长度
    :param save_path: 保存路径
    :return:
    """
    url = 'https://www.baidu.com/'

    browser = webdriver.Chrome()
    browser.get(url)

    input_box = browser.find_element(by=By.CLASS_NAME, value='s_ipt')
    input_box.send_keys(keyword)
    input_box.submit()

    scroll_refresh(browser)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    href = soup.select('a[href*="http://image.baidu.com/i"]')[0]['href']
    browser.get(href)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if start > 0:
        for _ in range(start):
            scroll_refresh(browser)

    for _ in range(length):
        save_images(browser, save_path)

    browser.quit()


if __name__ == '__main__':
    craw_image("猫")
    
