# -*- coding: utf-8 -*-
import sys
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

import discord

# WEBスクレイピング
def get_web_data(url, el):
    # Seleniumをあらゆる環境で起動させるChromeオプション
    options = Options()
    options.add_argument('--disable-gpu');
    options.add_argument('--disable-extensions');
    options.add_argument('--proxy-server="direct://"');
    options.add_argument('--proxy-bypass-list=*');
    options.add_argument('--start-maximized');

    # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がる）
    options.headless = True

    driver_path = 'chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    driver.get(url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    data = soup.select_one(el).text

    return data

# 今日のコロナ新規感染者数を取得
def get_covid_num():
    yahoo_covid_url = 'https://hazard.yahoo.co.jp/article/covid19'
    num_el = 'dl.dashBoard__main > div:nth-child(2) > dd:nth-child(2)'

    num_tokyo = get_web_data(yahoo_covid_url + 'tokyo', num_el)
    num_chiba = get_web_data(yahoo_covid_url + 'chiba', num_el)
    num_yamanashi = get_web_data(yahoo_covid_url + 'yamanashi', num_el)
    num_aichi = get_web_data(yahoo_covid_url + 'aichi', num_el)

    covid_msg = '```CSS\n'
    covid_msg += '今日の新規感染者数\n'
    covid_msg += '東京：' + num_tokyo + '人\n'
    covid_msg += '千葉：' + num_chiba + '人\n'
    covid_msg += '山梨：' + num_yamanashi + '人\n'
    covid_msg += '愛知：' + num_aichi + '人\n'
    covid_msg += '```'

    return covid_msg

# botを起動
def run_bot():
    client = discord.Client()
    TOKEN = os.environ['TOKEN']
    MAIN_CH_ID = int(os.environ['MAIN_CH_ID']) # 一般ルーム

    @client.event
    # bot起動時の処理
    async def on_ready():
        covid_msg = get_covid_num()

        for channel in client.get_all_channels():
            if channel.id == MAIN_CH_ID:
                await channel.send(covid_msg)

        await client.logout()
        await sys.exit()

    client.run(TOKEN)

def main():
    run_bot()

if __name__ == '__main__':
    main()
