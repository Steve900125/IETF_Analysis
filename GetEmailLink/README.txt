此專案包含了1個主程式2個副程式

架構
GetEmailLink
d-----       chromedriver_win32
d-----       Subroutine
            d-----       __pycache__
            -a----       get_Infor.py (副程式)
            -a----       get_MC.py (副程式)
d-----       __pycache__
-a----       main.py (主程式)
-a----       README.txt
-a----        __init__.py

主程式
main.py : 
    用來取得特定 WG 內的所有 email 連結，包括主題、寄件者、日期、信件連結

副程式
get_Infor.py :
    回傳帶有 WG 內的所有 email 連結，包括主題、寄件者、日期、信件連結的 df
    方法為 get_Information()

get_MC.py :
    回傳 WG 內的 Message 實際數量
    方法為 get_message_count()
