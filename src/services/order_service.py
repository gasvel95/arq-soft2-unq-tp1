from domain.order import Order
from domain.order_repository_interface import OrderRepository
from domain.product import Product
from domain.user import User
from domain.product_repository_interface import ProductRepository
from domain.seller_repository_interface import SellerRepository
from domain.user_repository_interface import UserRepository
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient
import asyncio
import json
from domain.seller import Seller
from fastapi_websocket_rpc.logger import logging_config, LoggingModes


PORT = 9002

class OrderService:
    def __init__(self, user_repo: UserRepository, product_repo: ProductRepository, order_repo: OrderRepository, seller_repo:SellerRepository):
        self.user_repo = user_repo
        self.product_repo = product_repo
        self.order_repo = order_repo
        self.seller_repo = seller_repo
        
    def get_order(self, id: str) -> Order:
        try:
            return self.order_repo.get(id)
        except:
            raise ValueError('Order not found')
    def  process_order(self, user_:User, order: Order) -> Order:
        user = self.user_repo.get(order.buyer_id)
        #user = json.loads(user_)
        if user is None: raise ValueError("User not found")
        print(f"user ===>>>>> {user_}")
        product = Product(**self.product_repo.get(order.product_id))
        if product is None: raise ValueError("Product not found")
        product.reduce_stock(order.quantity)
        self.product_repo.update(product)
        order.calculate_total(product.price)
        self.order_repo.add(order)

        ## envio de notificaciones al vendedor.
        seller  =  self.seller_repo.get(product.seller_id)
        notif = self.util_notification_obj(name=seller['company_name'], email=seller['email'], action="Venta",subject="Venta de producto", orderId=order.id, productName=product.name, quantity=order.quantity, amount=order.total.amount, curr=order.total.currency)
        notifi_seller = asyncio.run(self.run_client(f"ws://localhost:{PORT}/ws", json.dumps(notif)))
        
        ## envio de notificacion cliente.
        notif = self.util_notification_obj(name=user['first_name'], email=user['email'], action="Compra",subject="Compra de producto", orderId=order.id, productName=product.name, quantity=order.quantity, amount=order.total.amount, curr=order.total.currency)
        notifi_buyer = asyncio.run(self.run_client(f"ws://localhost:{PORT}/ws", json.dumps(notif)))
        return order
    
    async def run_client(self, uri , notif:str)->object:
        async with WebSocketRpcClient(uri, RpcMethodsBase()) as client:
            print(f"notifi---> {notif}")
            response = await client.other.sendMail(notif=notif)
            return response.result
        
    def util_notification_obj(self, name:str, email:str, action:str,subject:str, orderId:str, productName:str,quantity:int,amount:int,curr:str)->dict :  
        return {
            "userName":name, 
            "userAddress":email, 
            "action": action, 
            "subject": subject,
            "orderN": orderId,
            "productName": productName,
            "quantity": quantity, 
            "amount": f"{amount}  {curr} "  
        } 