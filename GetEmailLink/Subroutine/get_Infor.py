from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# INPUT : "tar_link" => IETF Email Target link
# OUTPUT : df (Subject、From(sender)、Date、Link(mail)) 

def get_Information( tar_link):
    # 利用 selenium 對網頁進行捲動取得而外資料
    Chrome_driver = webdriver.Chrome('\chromedriver_win32\chromedriver.exe')
    #指定你的 webdriver 路徑 

    Chrome_driver.get(tar_link) 
    # 打開網址

    Chrome_driver.implicitly_wait(3)
    # 等待開啟時間 3 秒避免開啟失敗

    source = Chrome_driver.find_element(By.ID, "msg-list")
    # 找到我要捲動的網頁區塊的 ID

    before_height = 0
    # 用來紀錄上一次 element 的高度

    while True:
        Chrome_driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", source)
        # 捲動指定元素
        last_height = Chrome_driver.execute_script("return arguments[0].scrollHeight",source)
        # 回傳當前高度
        print("Height : ",last_height)
        # 顯示當前高度
        if before_height == last_height:
            break
            # 如果當前高度與前一次高度相同代表沒有新的資訊終止捲動
        else:
            before_height = last_height
        time.sleep( 1 )
    
    print("Scroll END")

    html_Str = Chrome_driver.page_source
    # 網頁資料取得 

    soup = BeautifulSoup(html_Str,"html.parser")
    #以 Beautiful Soup 解析 HTML 程式碼

    # <-------------------取出連結--------------------->
    email_list = soup.find_all('a', class_='msg-detail')
    # 找出 email 連結 <a> class = 'msg-detail'

    re_link = re.compile(r'href="([^"]*)"')
    # 規則是找出 href 的連結

    link_list = re_link.findall(str(email_list))
    # 取出 email list

    for i in range(0,len(link_list)):
        link_list[i] = "https://mailarchive.ietf.org" + link_list[i]
        # 完整連結組合

    # <-------------------取出主題--------------------->
    re_subject = re.compile(r'>([^><]*)</a>')
    # 規則是找出 subject 名稱

    subject_list = re_subject.findall(str(email_list))
    # 取出 subject list

    # <-------------------取出日期--------------------->
    date_list_raw = soup.find_all('div', class_='xtd date-col')
    # 找出日期 div 位置

    re_date = re.compile(r'>([^><]*)</div>')
    # 規則是找出日期資料

    date_list = re_date.findall(str(date_list_raw))
    # 取出日期

    # <-------------------取出寄件者--------------------->
    from_list_raw = soup.find_all('div', class_='xtd from-col')
    # 找出寄件人(from) div 位置

    re_from = re.compile(r'>([^><]*)</div>')
    # 規則是找出寄件人資料

    from_list = re_from.findall(str(from_list_raw))
    # 取出寄件人

    df = pd.DataFrame({'Subject': subject_list  , 'From' : from_list , 'Date' : date_list , 'Link' : link_list})

    Chrome_driver.close()

    return df






