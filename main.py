import requests
import json
import asyncio
import aiohttp

def get(json_link):
    response = requests.get(json_link)
    return response.json()

def check_broken_pipe(data):
    if isinstance(data, dict):
        return any(check_broken_pipe(val) for val in data.values())
    elif isinstance(data, list):
        return any(check_broken_pipe(item) for item in data)
    return data == 'Broken pipe'

async def checkhost(session, addr):
    Result_URL = "https://check-host.net/check-result/"
    Check_URL = "https://check-host.net/check-http"
    
    headers = {'Accept': 'application/json'}
    async with session.get(f"{Check_URL}?host={addr}&node=ir1.node.check-host.net&node=ir2.node.check-host.net&node=ir3.node.check-host.net&node=ir4.node.check-host.net", headers=headers) as response:
        data = await response.json()
        request_id = data["request_id"]
        
    await asyncio.sleep(5)
    
    async with session.get(Result_URL + request_id, headers=headers) as response:
        result = await response.json()
        
    return check_broken_pipe(result)

async def save_mtproxy_list(mtproxy_list, file_name):
    async with aiohttp.ClientSession() as session:
        with open(file_name, 'w') as file:
            for mtproxy in mtproxy_list:
                server = mtproxy['query']['server']
                port = str(mtproxy['query']['port'])
                addr = server + ":" + port
                
                if await checkhost(session, addr):
                    secret = mtproxy['query']['secret']
                    mtproxy_url = f"https://t.me/proxy?server={server}&port={port}&secret={secret}"
                    file.write(mtproxy_url + '\n')


json_link = "https://raw.githubusercontent.com/yebekhe/MTProtoCollector/main/proxy/mtproto.json"
file_name = "list.txt"

mtproxy_list = get(json_link)
asyncio.run(save_mtproxy_list(mtproxy_list, file_name))
