import requests
# 目的 : 用來與網頁取得資源
from bs4 import BeautifulSoup
# 目的 : 用來處理 HTML 文本內的特定標籤或類別等
import re
# 目的 : 正規表達式找出 HTML 中的 href

print('執行 IETF WG 所有 email list 位置連結搜尋')

r = requests.get("https://mailarchive.ietf.org/arch/browse/") 
# 將此頁面的 HTML GET 下來

html_Str = r.text
# 變成 text 形式

soup = BeautifulSoup(html_Str,'html.parser')
# 以 Beautiful Soup 解析 HTML 程式碼

inactive = soup.find_all('div',id='inactive-lists')
# inactive-lists 
active = soup.find_all('div',id='active-lists')
# active-lists 

re_link = re.compile(r'href="([^"]*)"')
# 規則是找出 href 的連結

inactive_list = re_link.findall(str(inactive))
# 找出 inactive 相關的 wg 連結 list
active_list = re_link.findall(str(active))
# 找出 active 相關的 wg 連結 list

print("active wg: ", len(active_list))
print("inactive wg: ", len(inactive_list))

import pandas as pd

re_name = re.compile(r'/arch/browse/([^/]*)/')

active_name = re_name.findall(str(active_list))
# 找出 active 相關的 wg 連結 name
inactive_name = re_name.findall(str(inactive_list))   
# 找出 inactive 相關的 wg 連結 name

status_list = []
for i in range(0,len(active_list)):
    status_list.append('active')
    active_list[i] = "https://mailarchive.ietf.org" + active_list[i]

for i in range(0,len(inactive_list)):
    status_list.append('inactive')
    inactive_list[i] = "https://mailarchive.ietf.org" + inactive_list[i]

link_list = active_list + inactive_list
name_list = active_name + inactive_name

print(len(link_list))

print(len(name_list))

print(len(status_list))

df = pd.DataFrame({'wg': name_list  , 'link' : link_list , 'status' : status_list})

df = df.drop(0 ,axis = 0)
# 刪除 <a class="float-end" href="/arch/browse/static/">Go to Static View</a>

df.to_csv('IETF_WG_Link.csv', encoding='utf-8', index=False)

print('完成存檔')