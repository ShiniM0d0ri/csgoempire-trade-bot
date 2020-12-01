import asyncio,time
import websockets
import json,requests
from threading import Thread
from config import config
import webhook

potential_items=[]
min_custom_price=int(input("Enter minimum custom price: "))
min_price=int(input("Enter minimum price: "))
max_price=int(input("Enter maximum price: "))

def check_items(item_dict):
    print(potential_items)
    time.sleep(150)
    if item_dict['assetid'] in potential_items:
        try:
            message=f'found {item_dict["market_name"]} at {item_dict["custom_price"]}% with wear {item_dict["wear"]} at only {item_dict["market_value"]/100} coins'
            webhook.webhook(message)
        except KeyError:
            message=f'found {item_dict["market_name"]} at 0% with wear {item_dict["wear"]} at only {item_dict["market_value"]/100} coins'
            webhook.webhook(message)

def low_custom_price(item_dict):
    try:
        if (item_dict['custom_price']<=min_custom_price and ((item_dict['market_value']/100) in range(min_price,max_price))):
            potential_items.append(item_dict['assetid'])
            t = Thread(target=check_items, args=(item_dict,))
            t.start()
    except KeyError:
        potential_items.append(item_dict['assetid'])
        t = Thread(target=check_items, args=(item_dict,))
        t.start()

async def main():
    uri = "wss://trade.csgoempire.com/socket.io/?EIO=3&transport=websocket"
    async with websockets.connect(uri,extra_headers={'user-agent': config['useragent']}) as socket:
        while(True):
            rec_msg=await socket.recv()
            if type(rec_msg)==bytes:
                continue
            if str(rec_msg)=="40":
                print('\t42["p2p/new-items/subscribe",1]')
                await socket.send('42["p2p/new-items/subscribe",1]')
            if '"p2p_new_item"' in rec_msg:
                new_item=rec_msg.replace("\\","")[19:-2]
                low_custom_price(json.loads(new_item))
            if '"p2p_removed_item"' in rec_msg:
                removed_item=rec_msg.replace("\\","")[27:-2]
                if removed_item in potential_items:
                    potential_items.remove(removed_item)

            await socket.send('42["timesync"]')
        
asyncio.get_event_loop().run_until_complete(main())