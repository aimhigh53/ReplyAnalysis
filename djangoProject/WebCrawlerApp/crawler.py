import json
import sys
import os
import time
import requests

from bs4 import BeautifulSoup
# from .models import search

from django.views import View
from django.http import HttpResponse,JsonResponse
from django_pandas.io import read_frame
from django.forms.models import model_to_dict
from django.shortcuts import render
import pandas as pd
import numpy as np

from WebCrawlerApp.chromedriver import generate_chrome
from datetime import datetime, timedelta


PROJECT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = f'{PROJECT_DIR}/src'
driver_path = f'{PROJECT_DIR}/lib/webDriver/'
platform = sys.platform


if platform == 'darwin':
    print('System platform : Darwin')
    driver_path += 'chromedriver'
elif platform == 'linux':
    print('System platform : Linux')
    driver_path += 'chromedriverLinux'
elif platform == 'win32':
    print('System platform : Window')
    driver_path += 'chromedriverWindow'
else:
    print(f'[{sys.platform}] not supported. Check your system platform.')
    raise Exception()

# 크롬 드라이버 인스턴스 생성
chrome = generate_chrome(
    driver_path=driver_path,
    headless=False,
    download_path=DOWNLOAD_DIR)


# 페이지 요청
url = 'https://news.naver.com/main/ranking/popularDay.nhn'
chrome.get(url)
time.sleep(3)

html = chrome.page_source
soup = BeautifulSoup(html, 'lxml')

def loadPage():
    html = chrome.page_source
    soup = BeautifulSoup(html, 'lxml')

def backToMainPage():
    chrome.get(url)


def getTopFive(i):
    loadPage()
    elements=soup.select('#wrap > table > tbody > tr > td.content > div > div:nth-child('+str(i)+') > ol> li')
    titledic={}

    cnt=0
    for element in elements:
        cnt+=1
        title = element.select_one('dl > dt > a').text
        print('[',cnt,']번째 제목',title)

        if element.select_one('dl > dd > span.lede'):
            title=title+element.select_one('dl > dd > span.lede').text
            print(element.select_one('dl > dd > span.lede').text)

        titledic[cnt] = title

    return titledic


#top5 댓글 가져오기

def getReply(i,j):
    replylist=[]
    collecttime = str(datetime.utcnow().replace(microsecond=0) + timedelta(hours=9))[:16]
    clicknews=chrome.find_element_by_xpath('//*[@id="wrap"]/table/tbody/tr/td[2]/div/div['+str(i)+']/ol/li['+str(j)+']/dl/dt/a')
    clicknews.click()
    time.sleep(1)

    loadPage()

    identify=chrome.find_element_by_xpath('//*[@id="cbox_module"]/div/div[6]/div[1]/div/ul/li[1]')
    identify.click()
    time.sleep(1)

    more = chrome.find_element_by_xpath('//*[@id="cbox_module"]/div/div[9]/a/span[1]')
    more.click()
    time.sleep(1)

    contents = chrome.find_elements_by_css_selector('span.u_cbox_contents')
    likes = chrome.find_elements_by_css_selector('em.u_cbox_cnt_recomm')
    hates = chrome.find_elements_by_css_selector('em.u_cbox_cnt_unrecomm')
    cnt = 0

    for content,like,hate in zip(contents,likes,hates):
        cnt += 1
        print('[', cnt, ']번째')
        print(content.text,like.text,hate.text)
        replylist.append(['[', cnt, ']번째',collecttime,content.text,like.text,hate.text])
    return replylist

    # for reply in replys:
    #     replycontent = reply
    #     print(replycontent)

    time.sleep(1)



for i in range(5,10):
    titledic = getTopFive(i)
    replylist=[]
    for j in range(1,6):
        replylist.append(getReply(i,j))
        backToMainPage()

    for index,title,replys in zip(titledic,titledic.values(),replylist):
        print(index,title,replys)

    #5개 top section, 5개 기사의 리플 가져오기









