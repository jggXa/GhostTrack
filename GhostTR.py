# 导入模块

import json
import requests
import time
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr
from functools import wraps

Bl = '\033[30m'  # 颜色变量
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'


# 工具函数

# 装饰器：在函数执行前显示 banner
def is_option(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        run_banner()
        return func(*args, **kwargs)
    return wrapper


# 菜单功能函数
@is_option
def IP_Track():
    ip = input(f"{Wh}\n 输入目标 IP : {Gr}").strip()
    if not ip:
        print(f"{Re}IP 不能为空")
        return
    print()
    print(f' {Wh}============= {Gr}显示 IP 地址信息 {Wh}=============')
    try:
        req_api = requests.get(f"https://ipwho.is/{ip}", timeout=10)
        ip_data = req_api.json()
        if not ip_data.get("success", True):
            print(f"{Re}查询失败：{ip_data.get('message', '未知错误')}")
            return
        time.sleep(2)
        print(f"{Wh}\n 目标 IP         :{Gr}", ip)
        print(f"{Wh} IP 类型         :{Gr}", ip_data["type"])
        print(f"{Wh} 国家            :{Gr}", ip_data["country"])
        print(f"{Wh} 国家代码        :{Gr}", ip_data["country_code"])
        print(f"{Wh} 城市            :{Gr}", ip_data["city"])
        print(f"{Wh} 大洲            :{Gr}", ip_data["continent"])
        print(f"{Wh} 大洲代码        :{Gr}", ip_data["continent_code"])
        print(f"{Wh} 地区            :{Gr}", ip_data["region"])
        print(f"{Wh} 地区代码        :{Gr}", ip_data["region_code"])
        print(f"{Wh} 纬度            :{Gr}", ip_data["latitude"])
        print(f"{Wh} 经度            :{Gr}", ip_data["longitude"])
        lat = float(ip_data['latitude'])
        lon = float(ip_data['longitude'])
        print(f"{Wh} 地图            :{Gr}", f"https://www.google.com/maps/@{lat},{lon},8z")
        print(f"{Wh} 欧盟            :{Gr}", ip_data["is_eu"])
        print(f"{Wh} 邮政编码        :{Gr}", ip_data["postal"])
        print(f"{Wh} 国际区号        :{Gr}", ip_data["calling_code"])
        print(f"{Wh} 首都            :{Gr}", ip_data["capital"])
        print(f"{Wh} 边境            :{Gr}", ip_data["borders"])
        print(f"{Wh} 国旗            :{Gr}", ip_data["flag"]["emoji"])
        print(f"{Wh} ASN             :{Gr}", ip_data["connection"]["asn"])
        print(f"{Wh} 组织            :{Gr}", ip_data["connection"]["org"])
        print(f"{Wh} ISP             :{Gr}", ip_data["connection"]["isp"])
        print(f"{Wh} 域名            :{Gr}", ip_data["connection"]["domain"])
        print(f"{Wh} 时区 ID         :{Gr}", ip_data["timezone"]["id"])
        print(f"{Wh} 缩写            :{Gr}", ip_data["timezone"]["abbr"])
        print(f"{Wh} 夏令时          :{Gr}", ip_data["timezone"]["is_dst"])
        print(f"{Wh} 偏移            :{Gr}", ip_data["timezone"]["offset"])
        print(f"{Wh} UTC             :{Gr}", ip_data["timezone"]["utc"])
        print(f"{Wh} 当前时间        :{Gr}", ip_data["timezone"]["current_time"])
    except requests.RequestException as e:
        print(f"{Re}网络错误：{e}")
    except (KeyError, TypeError, ValueError) as e:
        print(f"{Re}数据解析错误：{e}")


@is_option
def phoneGW():
    User_phone = input(
        f"\n {Wh}输入目标电话号码 {Gr}例如 [+6281xxxxxxxxx] {Wh}: {Gr}").strip()
    if not User_phone:
        print(f"{Re}电话号码不能为空")
        return
    default_region = "ID"  # 默认国家：印度尼西亚

    try:
        parsed_number = phonenumbers.parse(User_phone, default_region)
        region_code = phonenumbers.region_code_for_number(parsed_number)
        jenis_provider = carrier.name_for_number(parsed_number, "en")  # 运营商保留英文
        location = geocoder.description_for_number(parsed_number, "id")
        is_valid_number = phonenumbers.is_valid_number(parsed_number)
        is_possible_number = phonenumbers.is_possible_number(parsed_number)
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        formatted_number_for_mobile = phonenumbers.format_number_for_mobile_dialing(parsed_number, default_region,
                                                                                    with_formatting=True)
        number_type = phonenumbers.number_type(parsed_number)
        timezone1 = timezone.time_zones_for_number(parsed_number)
        timezoneF = ', '.join(timezone1)
    except Exception as e:
        print(f"{Re}号码解析失败：{e}")
        return

    print(f"\n {Wh}========== {Gr}显示电话号码信息 {Wh}==========")
    print(f"\n {Wh}位置             :{Gr} {location}")
    print(f" {Wh}地区代码         :{Gr} {region_code}")
    print(f" {Wh}时区             :{Gr} {timezoneF}")
    print(f" {Wh}运营商           :{Gr} {jenis_provider}")
    print(f" {Wh}有效号码         :{Gr} {is_valid_number}")
    print(f" {Wh}可能号码         :{Gr} {is_possible_number}")
    print(f" {Wh}国际格式         :{Gr} {formatted_number}")
    print(f" {Wh}手机格式         :{Gr} {formatted_number_for_mobile}")
    print(f" {Wh}原始号码         :{Gr} {parsed_number.national_number}")
    print(
        f" {Wh}E.164 格式       :{Gr} {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}")
    print(f" {Wh}国家代码         :{Gr} {parsed_number.country_code}")
    print(f" {Wh}本地号码         :{Gr} {parsed_number.national_number}")
    if number_type == phonenumbers.PhoneNumberType.MOBILE:
        print(f" {Wh}类型             :{Gr} 这是手机号码")
    elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
        print(f" {Wh}类型             :{Gr} 这是固定电话")
    else:
        print(f" {Wh}类型             :{Gr} 这是其他类型号码")


@is_option
def TrackLu():
    username = input(f"\n {Wh}输入用户名 : {Gr}").strip()
    if not username:
        print(f"{Re}用户名不能为空")
        return
    results = {}
    social_media = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
        {"url": "https://www.github.com/{}", "name": "GitHub"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
        {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
        {"url": "https://www.youtube.com/{}", "name": "Youtube"},
        {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
        {"url": "https://www.behance.net/{}", "name": "Behance"},
        {"url": "https://www.medium.com/@{}", "name": "Medium"},
        {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
        {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
        {"url": "https://www.periscope.tv/{}", "name": "Periscope"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
        {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
        {"url": "https://www.stumbleupon.com/stumbler/{}", "name": "StumbleUpon"},
        {"url": "https://www.ello.co/{}", "name": "Ello"},
        {"url": "https://www.producthunt.com/@{}", "name": "Product Hunt"},
        {"url": "https://www.telegram.me/{}", "name": "Telegram"},
        {"url": "https://www.weheartit.com/{}", "name": "We Heart It"}
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    for site in social_media:
        url = site['url'].format(username)
        try:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                results[site['name']] = url
            else:
                results[site['name']] = None
        except requests.RequestException:
            results[site['name']] = None

    print(f"\n {Wh}========== {Gr}显示用户名信息 {Wh}==========")
    print()
    for site, url in results.items():
        if url:
            print(f" {Wh}[ {Gr}+ {Wh}] {site} : {Gr}{url}")
        else:
            print(f" {Wh}[ {Re}- {Wh}] {site} : {Re}未找到用户名")


@is_option
def showIP():
    try:
        response = requests.get('https://api.ipify.org/', timeout=10)
        Show_IP = response.text
    except requests.RequestException as e:
        print(f"{Re}获取 IP 失败：{e}")
        return

    print(f"\n {Wh}========== {Gr}显示你的 IP 信息 {Wh}==========")
    print(f"\n {Wh}[{Gr} + {Wh}] 你的 IP 地址 : {Gr}{Show_IP}")
    print(f"\n {Wh}==============================================")


# 选项
options = [
    {
        'num': 1,
        'text': 'IP 追踪',
        'func': IP_Track
    },
    {
        'num': 2,
        'text': '显示你的 IP',
        'func': showIP
    },
    {
        'num': 3,
        'text': '电话号码追踪',
        'func': phoneGW
    },
    {
        'num': 4,
        'text': '用户名追踪',
        'func': TrackLu
    },
    {
        'num': 0,
        'text': '退出',
        'func': exit
    }
]


def clear():
    # Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # macOS / Linux
    else:
        _ = os.system('clear')


def call_option(opt):
    if not is_in_options(opt):
        raise ValueError('选项不存在')
    for opt_item in options:
        if opt_item['num'] == opt:
            if 'func' in opt_item:
                opt_item['func']()
            else:
                print('未检测到函数')


def execute_option(opt):
    try:
        call_option(opt)
    except ValueError as e:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}{e}')
        time.sleep(2)
        main()
        return
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}退出')
        time.sleep(2)
        exit()
    input(f'\n{Wh}[ {Gr}+ {Wh}] {Gr}按回车继续')
    main()


def option_text():
    text = ''
    for opt in options:
        text += f'{Wh}[ {opt["num"]} ] {Gr}{opt["text"]}\n'
    return text


def is_in_options(num):
    for opt in options:
        if opt['num'] == num:
            return True
    return False


def option():
    # 工具 banner
    clear()
    stderr.writelines(f"""
       ________               __      ______                __  
      / ____/ /_  ____  _____/ /_    /_  __/________ ______/ /__
     / / __/ __ \\/ __ \\/ ___/ __/_____/ / / ___/ __ `/ ___/ //_/
    / /_/ / / / / /_/ (__  ) /_/_____/ / / /  / /_/ / /__/ ,<   
    \\____/_/ /_/\\____/____/\\__/     /_/ /_/   \\__,_/\\___/_/|_| 

              {Wh}[ + ]  C O D E   B Y  H U N X  [ + ]
    """)

    stderr.writelines(f"\n\n\n{option_text()}")


def run_banner():
    clear()
    time.sleep(1)
    stderr.writelines(f"""{Wh}
         .-.
       .'   `.          {Wh}--------------------------------
       :g g   :         {Wh}| {Gr}GHOST - TRACKER - IP ADDRESS {Wh}|
       : o    `.        {Wh}|       {Gr}@CODE BY HUNXBYTS      {Wh}|
      :         ``.     {Wh}--------------------------------
     :             `.
    :  :         .   `.
    :   :          ` . `.
     `.. :            `. ``;
        `:;             `:'
           :              `.
            `.              `.     .
              `'`'`'`---..,___`;.-'
        """)
    time.sleep(0.5)


def main():
    clear()
    option()
    time.sleep(1)
    try:
        opt = int(input(f"{Wh}\n [ + ] {Gr}选择选项 : {Wh}"))
        execute_option(opt)
    except ValueError:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}请输入数字')
        time.sleep(2)
        main()
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}退出')
        time.sleep(2)
        exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}退出')
        time.sleep(2)
        exit()