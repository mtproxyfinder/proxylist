import requests
import json
import time

def get(json_link):
    response = requests.get(json_link)
    mtproxy_list = json.loads(response.text)
    return mtproxy_list

def checkhost(addr):
    Result_URL =  "https://check-host.net/check-result/"
    Check_URL = "https://check-host.net/check-http"
    # Header for check-host.net 
    headers = {'Accept': 'application/json'}
    # Reaquest to check server
    response = requests.get("https://check-host.net/check-http?host={addr}&node=ir1.node.check-host.net&node=ir2.node.check-host.net&node=ir3.node.check-host.net", headers=headers)
    request_id = json.loads(response.text)["request_id"]
    # load result
    time.sleep(5)
    headers = {'Accept': 'application/json'}
    result = requests.get(Result_URL + request_id, headers=headers)
    result = json.loads(result.text)
    for server in result:
        if result[server][0][2] == 'Connection refused':
            return False
        else:
            return True

def save_mtproxy_list(mtproxy_list, file_name):
    with open(file_name, 'w') as file:
        for mtproxy in mtproxy_list:
            server = mtproxy['query']['server']
            port = mtproxy['query']['port']
            if checkhost(server+":"+port):
                secret = mtproxy['query']['secret']
                mtproxy_url = f"https://t.me/proxy?server={server}&port={port}&secret={secret}"
                file.write(mtproxy_url + '\n')

json_link = "https://raw.githubusercontent.com/yebekhe/MTProtoCollector/main/proxy/mtproto.json"  # Json link
file_name = "list.txt"  # Name of the text file to save the mtproxy list

mtproxy_list = get(json_link)
save_mtproxy_list(mtproxy_list, file_name)
