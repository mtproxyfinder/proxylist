import requests
import json

def get_mtproxy_list(json_link):
    response = requests.get(json_link)
    mtproxy_list = json.loads(response.text)
    return mtproxy_list

def save_mtproxy_list(mtproxy_list, file_name):
    with open(file_name, 'w') as file:
        for mtproxy in mtproxy_list:
            server = mtproxy['query']['server']
            port = mtproxy['query']['port']
            secret = mtproxy['query']['secret']
            mtproxy_url = f"https://t.me/proxy?server={server}&port={port}&secret={secret}"
            file.write(mtproxy_url + '\n')

json_link = "https://raw.githubusercontent.com/yebekhe/MTProtoCollector/main/proxy/mtproto.json"  # Json link
file_name = "list.txt"  # Name of the text file to save the mtproxy list

mtproxy_list = get_mtproxy_list(json_link)
save_mtproxy_list(mtproxy_list, file_name)
