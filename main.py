import requests
import json
import time

def get(json_link):
    response = requests.get(json_link)
    mtproxy_list = json.loads(response.text)
    return mtproxy_list

def check_broken_pipe(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if check_broken_pipe(value):
                return True
    elif isinstance(data, list):
        for item in data:
            if check_broken_pipe(item):
                return True
    elif data == 'Broken pipe':
        return True

    return False
def checkhost(addr):
    Result_URL =  "https://check-host.net/check-result/"
    Check_URL = "https://check-host.net/check-http"
    # Header for check-host.net 
    headers = {'Accept': 'application/json'}
    # Reaquest to check server
    response = requests.get(f"https://check-host.net/check-http?host={addr}&node=ir1.node.check-host.net&node=ir2.node.check-host.net&node=ir3.node.check-host.net&node=ir4.node.check-host.net", headers=headers)
    request_id = json.loads(response.text)["request_id"]
    # load result
    time.sleep(10)
    headers = {'Accept': 'application/json'}
    result = requests.get(Result_URL + request_id, headers=headers)
    result = json.loads(result.text)
    return check_broken_pipe(result)

def save_mtproxy_list(mtproxy_list, file_name):
    with open(file_name, 'w') as file:
        for mtproxy in mtproxy_list:
            server = mtproxy['host']
            port = str(mtproxy['port'])
            print(server+":"+port)
            if checkhost(server+":"+port):
                print("conected")
                secret = mtproxy['secret']
                mtproxy_url = f"https://t.me/proxy?server={server}&port={port}&secret={secret}"
                file.write(mtproxy_url + '\n')
            else:
                print("not conected")

json_link = "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/mtproto.json"  # Json link
file_name = "list.txt"  # Name of the text file to save the mtproxy list

mtproxy_list = get(json_link)
save_mtproxy_list(mtproxy_list, file_name)
