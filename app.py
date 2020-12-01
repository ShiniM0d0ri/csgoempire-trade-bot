import asyncio
import websockets
import requests,json
from config import config

mainCookie=config['mainCookie']
useragent=config['useragent']

mainHeaders = {
    'user-agent': useragent,
    'Referer': 'https://csgoempire.com/withdraw',
    'Accept': '/',
    'Connection': 'keep-alive'
}

def requestMetaModel():
    headers={'cookie': mainCookie}
    headers.update(mainHeaders)
    response = requests.get('https://csgoempire.com/api/v2/metadata', headers=headers)
    return response.text
    
data=json.loads(requestMetaModel())
print("\trequesting metadata for user",json.dumps(data["user"]["id"]))
#authorisation message
auth_msg=f'42["identify","uid":{json.dumps(data["user"]["id"])},"model":{json.dumps(data["user"])},"authorizationToken":{json.dumps(data["socket_token"])},"signature":{json.dumps(data["socket_signature"])}]'


async def main():
    Flag=True
    uri = "wss://roulette.csgoempire.com/s/?EIO=3&transport=websocket"
    async with websockets.connect(uri,extra_headers={'user-agent': useragent}) as socket:
        while(Flag):
            rec_msg=await socket.recv()
            if type(rec_msg)==bytes:
                continue
            else:
                print(rec_msg)
            if str(rec_msg)=="40":
                print('\t42["p2p/new-items/subscribe",1]')
                await socket.send('42["p2p/new-items/subscribe",1]')
            # if '"authenticated":false' in rec_msg:
            #     print("\tauthenticating..")
            #     await socket.send(auth_msg)
            # if '"authenticated":true' in rec_msg:
            #     print("\tauthenticated!")
            # if '"p2p_removed_item"' in rec_msg:
            #     print(rec_msg)
            await socket.send('42["timesync"]')
        

asyncio.get_event_loop().run_until_complete(main())