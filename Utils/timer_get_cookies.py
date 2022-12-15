import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import browsercookie
import requests


def parse_yuntu_json(json_data: json):
    web_package_info = []
    all_packages = json_data['shipments']
    for package in all_packages:
        temp_dict = {
            'number': package['number'],
            'state': package['state'],
            'latest_event': package['shipment']['latest_event'],
            'events': package['shipment']['tracking']['providers'][0]['events']
        }
        web_package_info.append(temp_dict)
    return json.dumps(web_package_info)


def get_cookies():
    print("Get cookies already")


def start_requests(packer_numbers: list):
    data = {
        "data": [],
        "guid": "",
        "timeZoneOffset": -480
    }
    for packer_number in packer_numbers:
        data['data'].append({
            'num': packer_number,
            'fc': '0',
            'sc': '0'
        })
    data = json.dumps(data).replace(" ", "")
    print(len(data))
    headers = {
        "Content-Length": f"{len(data)}",
        "Referer": "https://t.17track.net/zh-cn",
        'Cookie': 'country=CN; _yq_bid=G-7338B1A549F3BCD1; v5_TranslateLang=en; v5_Culture=en; _ga=GA1.2.932552877.1671092442; _gid=GA1.2.1288259628.1671092442; __gads=ID=388306af4f105670:T=1671092442:S=ALNI_MZkdok5ZLCmg709WXXTI0DtKZbzKg; __gpi=UID=00000b9100565ce3:T=1671092442:RT=1671092442:S=ALNI_MZnTu9Ke31QZ6DNNrb1kYE-ZlUy3Q; _gat_cnGa=1; _gat=1; _ati=4001940269729; uid=A31627EFEAE14A14B021B7E9A4B432BB; _yq_rc_=yq.16.2105.en.0.0.409970913657809286G; Last-Event-ID=657572742f3164352f66383735323935313538312f3065312d3a383136356534663065333a3530313834383433383a65736c61663a656469682067736d2d616964656d2d756e656d2d6e776f64706f72642d7179c1302e9cc62128cd9e5'
    }
    r = requests.post('https://t.17track.net/track/restapi', data=data, headers=headers)
    # with open("result.json", 'w+', encoding='U8') as f:
    #     json.dump(r.json(), f, indent=4, ensure_ascii=False)
    return parse_yuntu_json(r.json())


def test_for_get_json():
    r = """
        YT2220621272046565
        YT2222021272078719
        YT2224121225000875
        YT2223921272038985
        YT2223921266009420
        YT2223721272045551
        YT2224121292004552
        YT2224121292005619
        YT2224121292004717
        YT2224121292018871
        YT2224122093000003
        YT2224221225000671
        YT2224221225000672
        YT2224221225000721
        YT2224221225000673
        """
    packer_numbers = [
        item.strip() for item in r.split("\n") if item.strip()
    ]
    print(packer_numbers)
    # start_requests('YT2222021272078719')
    start_requests(packer_numbers[:9])


def use_selenium_to_get_cookie():
    option = Options()
    option.add_argument('--headless')
    br = webdriver.Chrome(options=option)
    br.get('https://t.17track.net/en#nums=YT2220621272046565')
    cookies = br.get_cookies()
    cookie_list = []
    for cookie in cookies:
        name = cookie['name']
        value = cookie['value']
        if name.startswith('Last'):
            cookie_list.append(f"{name}={value}")
    string_cookies = '; '.join(cookie_list)
    print(string_cookies)
    br.close()


if __name__ == '__main__':
    test_for_get_json()
    # use_selenium_to_get_cookie()
    # timer = Timer(10, get_cookies)
    # timer.start()
