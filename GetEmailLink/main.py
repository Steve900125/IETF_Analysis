from Subroutine.get_MC import get_message_count
# Get messages number
from Subroutine.get_Infor import get_Information
# Get Subject、From(sender)、Date、Link(mail)
import pandas as pd

tar_link = "https://mailarchive.ietf.org/arch/browse/dance/"
# 把該 WG 的 email 的連結放在此處

mc = get_message_count(tar_link)
# 訊息的實際數量取得
df = get_Information(tar_link)
# 把資料用 pandas 紀錄

print(df.shape[0])
print(df.head())