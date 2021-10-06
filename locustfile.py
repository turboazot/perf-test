from locust import FastHttpUser, task
import json
import random

class HelloWorldUser(FastHttpUser):
    @task
    def basic_scenario(self):
        print("===================================")
        users_r = self.client.get('/api/v1/users').json()
        users_page = random.randrange(users_r["meta"]["page"], users_r["meta"]["pages"])
        users_item_number = random.randrange(0, users_r["meta"]["per_page"] - 1)

        current_user_r = self.client.get(f"/api/v1/users?page={users_page}").json()
        current_user = current_user_r["data"][users_item_number]
        
        current_order_r = self.client.post(f"/api/v1/users/{current_user['id']}/orders", json={"status": "pending"})
        
        current_order = current_order_r.json()

        products_r = self.client.get("/api/v1/products").json()
        for _ in range(random.randrange(1, 5)):
            products_page = random.randrange(products_r["meta"]["page"], products_r["meta"]["pages"])
            products_item_number = random.randrange(0, products_r["meta"]["per_page"] - 1)
            current_product_r = self.client.get(f"/api/v1/products?page={products_page}").json()
            current_product = current_product_r["data"][products_item_number]
            self.client.post(f"/api/v1/users/{current_user['id']}/orders/{current_order['id']}/order-items", json={
                "product_id": current_product["id"],
                "quantity": random.randrange(1, 100)
            })
        order_items = self.client.get(f"/api/v1/users/{current_user['id']}/orders/{current_order['id']}/order-items").json()
        print(order_items)
        self.client.patch(f"/api/v1/users/{current_user['id']}/orders/{current_order['id']}", json={"status": "finished"}).json()
    
        print("===================================")
