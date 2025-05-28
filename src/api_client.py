import asyncio
from zero import AsyncZeroClient
import json

zero_client = AsyncZeroClient("localhost", 5559)

async def echo():
    resp = await zero_client.call("echo", "Hi there!")
    print(resp)

async def hello():
    resp = await zero_client.call("hello_world", None)
    print(resp)

async def email():
        notif = {
            "userName": "Mercadito",
            "userAddress": "mauroportilloe@gmail.com",
            "action": "venta",
            "subject": "Venta de mercadito",
            "orderN": "2342134213443434",
            "productName": "Panchos",
            "quantity": "10",
            "amount": 990
        }
        resp = await zero_client.call("sendMail", json.dumps(notif))
        print(f' status {resp}')
        

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(echo())
    loop.run_until_complete(email())