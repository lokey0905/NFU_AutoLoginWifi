import requests
from bs4 import BeautifulSoup
import urllib3

#在這邊輸入帳號密碼
userName = "@ctx10.nfu.edu.tw"
passWord = ""
login_page="https://wifi6.nfu.edu.tw/"

print("請選擇網站\n")
print("1. wifi6.nfu.edu.tw\n")
print("2. 192.0.2.1\n")

choice=input()
if choice=='1':
    login_page="http://wifi6.nfu.edu.tw/"
elif choice=='2':
    login_page="http://192.0.2.1/"
else:
    login_page="http://wifi6.nfu.edu.tw/"

print("正在嘗試登入:"+login_page)
#https warning disable
urllib3.disable_warnings()

# 建立會話（Session）以便跨多個 HTTP 請求傳遞 cookies
s = requests.Session()

# 訪問登錄頁面以獲取 cookies 和其他隱藏字段
login_url = login_page
login_page = s.get(login_url, verify=False)

# 解析 HTML 內容以獲取隱藏字段的值
soup = BeautifulSoup(login_page.content, 'html.parser')
hidden_inputs = soup.find_all('input', type='hidden')
payload = {x['name']: x['value'] for x in hidden_inputs}

# 添加您的帳號和密碼到表單資料中
payload['username'] = userName
payload['password'] = passWord

# 使用表單資料和 cookies 發送 POST 請求以登錄
post_url = login_page
post_response = s.post(post_url, data=payload)

print("done. code by lokey0905")
