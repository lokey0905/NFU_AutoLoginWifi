import requests
from bs4 import BeautifulSoup
import getpass
import json
import os
import keyring
import sys

NFU_DOMAIN = "nfu.edu.tw"

def save_credentials(username, password):
    # 安全地保存憑證。
    keyring.set_password(NFU_DOMAIN, username, password)

def load_credentials(username):
    # 從安全存儲中加載憑證。
    return keyring.get_password(NFU_DOMAIN, username)

def get_credentials():
    # 提示用戶輸入並保存憑證。
    print("您尚未儲存資訊\n請輸入您的帳號密碼：")
    username = input("帳號：")
    password = getpass.getpass("密碼：")
    save_credentials(username, password)
    return username, password

def check_need_login_page(login_url):
    try:
        response = requests.get(login_url)
        if "Authentication Successful" in response.text:
            print("已經登入！")
            return False
        else:
            print("尚未登入。")
            return True
    except requests.RequestException as e:
        print("發生錯誤：", e)
        return False

# 檢查是否已經登入
login_url = 'https://wifi6.nfu.edu.tw/login.html'
if check_need_login_page(login_url):
    # 載入或獲取用戶憑證
    userName = input("輸入您的帳號：")
    passWord = load_credentials(userName)

    if passWord is None:
        userName, passWord = get_credentials()

    # 創建一個 Session 以便跨多個 HTTP 請求傳遞 cookies
    s = requests.Session()

    try:
        # 訪問登錄頁面以獲取 cookies 和其他隱藏字段
        login_page = s.get(login_url)

        # 使用 BeautifulSoup 解析 HTML 內容
        soup = BeautifulSoup(login_page.content, 'html.parser')

        # 找到表單元素
        login_form = soup.find('form')

        # 找到所有的 input 元素
        input_elements = login_form.find_all('input')

        # 建立一個字典來存儲表單數據
        payload = {}

        # 遍歷 input 元素，將名稱和值添加到 payload 字典中
        for input_element in input_elements:
            if input_element.get('name') and input_element.get('value'):
                payload[input_element['name']] = input_element['value']

        # 添加您的帳號和密碼到表單資料中
        payload['username'] = userName
        payload['password'] = passWord

        # 使用表單資料和 cookies 發送 POST 請求以登錄
        post_response = s.post(login_url, data=payload)

        # 檢查登錄結果並進行相應的處理
        if "Authentication Successful" in post_response.text:
            print("登入成功！")
        else:
            print("登入失敗！請檢查帳號密碼是否正確。")
    except requests.RequestException as e:
        print("發生錯誤：", e)

print("完成 code by lokey0905\n若有需要移除儲存資訊 可至控制台\所有控制台項目\認證管理員")
input("按 Enter 鍵退出...")
