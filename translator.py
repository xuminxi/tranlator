import hashlib
import random
import urllib.parse
import requests
from tkinter import *
import time
import tkinter as tk
from pynput import keyboard
import pyperclip

def baidu_translate(en_word):
    q = en_word

    with open("user_config.txt", 'r', encoding="UTF-8") as user_config:
        appid = user_config.readline().split("=")[1].lstrip().rstrip()
        p_key = user_config.readline().split("=")[1].lstrip().rstrip()

    rand_num = str(random.randint(32768, 65536))

    combine_str = appid + q + rand_num + p_key
    sign = hashlib.md5(combine_str.encode(encoding='utf-8')).hexdigest()
    url_template = "http://api.fanyi.baidu.com/api/trans/vip/translate?"
    param = 'q=' +  urllib.parse.quote(en_word) + "&from=en&to=zh&appid=" + appid + "&salt=" + rand_num + "&sign=" + sign
    url = url_template + param
    return url


def request_option():
    option_list = {}
    data = {}
    headers = {}
    proxies={}
    try:
        with open("proxies.txt", 'r',encoding='UTF-8') as config:
            proxy = config.read()
            proxies['http'] = proxy
            proxies['https'] = proxy
    except:
        option_list['proxies'] = {}

    option_list['data'] = data
    option_list['headers'] = headers
    option_list['proxies'] = proxies

    return option_list

def show_translate(trans_word,size,duration):
    root = Tk()
    root.title("Translation")
    root.geometry("800x200+600+0")
    root.wm_attributes('-topmost', 1)
    trans = StringVar()
    trans.set(trans_word)
    tk.Label(root, textvariable=trans, font=("Times New Roman", size), justify='left', wraplength=750).place(x=10,
                                                                                                           y=10)
    root.update()
    root.deiconify()
    time.sleep(duration)
    root.destroy()

def main_opreation(en_word):
    url = baidu_translate(en_word)
    req_option = request_option()
    trans_res = requests.request("GET", url, headers=req_option['headers'], data=req_option['data'], proxies=req_option['proxies'])
    out_put = trans_res.text.encode().decode("unicode_escape")
    show_info = out_put.split("\"dst\":")
    show_info.remove(show_info[0])
    middle_str = ""
    for i in show_info:
        i = i.split('\"}')[0].replace("\"", "")
        middle_str = middle_str + i + "\n"
    with open("display.txt", 'r', encoding="UTF-8") as display:
        size = int(display.readline().rstrip().lstrip())
        duration = int(display.readline().rstrip().lstrip())
        show_translate(middle_str, size, duration)


def on_press(key):
    global list
    list.append(key)

    for i in list:
        if i != keyboard.Key.ctrl_r and i!=keyboard.Key.ctrl_l:
            list = []

    if len(list) == 3:
        enword = pyperclip.paste()
        main_opreation(enword)
        list = []

list = []
show_translate("程序开始运行。。。请复制需要翻译的单词，然后敲击三次Ctrl键翻译",25,5)
with keyboard.Listener(on_release=on_press) as lsn:
    lsn.join()
