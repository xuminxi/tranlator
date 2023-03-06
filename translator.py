from pynput import keyboard
import pyperclip
import pymysql
import hashlib
import random
import urllib.parse
import tkinter as tk
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#global var
list = []
"""
A tool to help you translate easily

-single word : local database
-long sentence : Baidu API

"""
def baidu_translate(en_word):

    #Info need to be
    q = en_word
    appid = 'Your appid'
    p_key = 'Your privatekey'
    rand_num = str(random.randint(32768, 65536))

    #make url , refer to https://api.fanyi.baidu.com/api/trans/product/apidoc
    combine_str = appid + q + rand_num + p_key
    sign = hashlib.md5(combine_str.encode(encoding='utf-8')).hexdigest()
    url_template = "http://api.fanyi.baidu.com/api/trans/vip/translate?"
    param = 'q=' +  urllib.parse.quote(en_word) + "&from=en&to=zh&appid=" + appid + "&salt=" + rand_num + "&sign=" + sign
    url = url_template + param
    return url

def show_translate(trans_word,size):
    root = Tk()
    root.title("Translation")
    root.geometry("800x200+600+0")
    root.wm_attributes('-topmost', 1)
    trans = StringVar()
    trans.set(trans_word)
    tk.Label(root, textvariable=trans, font=("Times New Roman", size), justify='left', wraplength=800).place(x=10,
                                                                                                           y=10)
    root.update()
    root.deiconify()
    time.sleep(5)
    root.destroy()


def on_press(key):
    global list
    list.append(key)

    #only add ctrl to record list
    for i in list:
        if i != keyboard.Key.ctrl_r and i!=keyboard.Key.ctrl_l:
            list = []

    #if 3 ctrl was pressed Continuously
    if len(list) == 3:
        #query local database
        conn = pymysql.connect(host='your host',
                               user='your username',
                               password='your password',
                               database='your database')
        cursor = conn.cursor()
        enword = pyperclip.paste()
        re_enword = enword#.replace(' ','').replace('\'','')
        res = 0
        try:
            res = cursor.execute("SELECT translation FROM <your database> WHERE word=\'" + re_enword + "\'")
        except:
            pass
        if res:
            res = cursor.fetchone()[0]
            #toast.show_toast("Transation : ",res)
            print(res)
            show_translate(res,18)

        else:
            url = baidu_translate(enword)
            chrome_driver.execute_script("window.location.href='" + url + "'")
            try:
                out_put = chrome_driver.find_element(By.TAG_NAME, 'pre').text.encode().decode("unicode_escape")
                res = out_put.split("\"dst\":")
                res.remove(res[0])
                middle_str = ""
                for i in res:
                    i = i.split('\"}')[0].replace("\"", "")
                    middle_str = middle_str + i + "\n"
                    print(middle_str)
                show_translate(middle_str,14)
            except:
                pass

        cursor.close()
        conn.close()
        list = []


print("Connecting.........")
option = webdriver.ChromeOptions()
option.add_argument('--headless')
chrome_driver = webdriver.Chrome(chrome_options=option)
chrome_driver.get("http://www.baidu.com")

print("Connected!")

with keyboard.Listener(on_press=on_press) as lsn:
    lsn.join()

