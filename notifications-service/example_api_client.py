import uvicorn
from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient
import asyncio
import json

app = FastAPI()
PORT = 9002


async def run_client(uri , notif:str) -> object:
    async with WebSocketRpcClient(uri, RpcMethodsBase()) as client:
        print(f"notifi---> {notif}")
        response = await client.other.sendMail(notif=notif)
        return response.result        

@app.get("/rpc")
def send():
    notif = {
            "userName": "Mercadito",# nombre del usuario o vendedor 
            "userAddress": "mauroportilloe@gmail.com", # direccion de correo del usuario o vendedor.
            "action": "venta", # Accion: compra o venta, se usa en el texto de email. 
            "subject": "Venta de mercadito", # asunto del correo. 
            "orderN": "2342134213443434", # nro de orden de compra ejecutada.
            "productName": "Panchos", # nombre del producto
            "quantity": "10", # cantidad de productos 
            "amount": 990 # monto total de compra o venta. 
        }
    notifi = asyncio.run(run_client(f"ws://localhost:{PORT}/ws" ,json.dumps(notif)))

    return notifi

uvicorn.run(app,host="0.0.0.0",port=9000)

