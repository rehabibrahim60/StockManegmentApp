from product import update_product
from typing import List, Dict, Callable, Tuple

# Product and Order types
Product = Dict[str, any]
Order = Dict[str, any]

# Orders list
orders = [
    {"id": 1, "product_id": 1, "quantity": 2, "total_cost": 20},
    {"id": 2, "product_id": 2, "quantity": 1, "total_cost": 50},
]

# Get orders with product names using recursion
def get_orders(products: List[Product], orders: List[Order], formatter: Callable[[Order, int], Dict] = None, result=None) -> List[Dict]:
    if result is None:
        result = []

    if not orders:
        return result

    head, *tail = orders
    product_id = head["product_id"]  # Fetch product ID directly

    formatted_order = formatter(head, product_id) if formatter else {
        "order_id": head["id"],
        "product_id": product_id,
        "quantity": head["quantity"],
        "total_cost": head["total_cost"],
    }

    return get_orders(products, tail, formatter, result + [formatted_order])

def find_product_recursive(products: List[Product], product_name:str) -> Product:
    if not products:
        return"Product not found"
    if products[0]["name"] == product_name:
        return products[0]
    return find_product_recursive(products[1:], product_name)

def create_order(products: List[Product], orders: List[Order], product_name: str, quantity: int) -> Tuple[List[Product], List[Order]]:
    product = find_product_recursive(products, product_name)
    print(product)
    if product["quantity"] < quantity:
        return "Insufficient stock try again..."

    updated_products = update_product(
        products,
        product["id"],
        {"quantity": product["quantity"] - quantity}
    )

    new_order = {
        "id": len(orders) + 1,
        "product_id": product["id"],
        "quantity": quantity,
        "total_cost": product["price"] * quantity,
    }

    return updated_products, orders + [new_order]
# Delete an order
def delete_order(products: List[Product], orders: List[Order], order_id: int, updater: Callable[[List[Product], Order], List[Product]] = None, result=None) -> Tuple[List[Product], List[Order]]:
    if result is None:
        result = []

    if not orders:
        return products, result

    head, *tail = orders

    if head["id"] == order_id:
        updated_products = updater(products, head) if updater else update_product(
            products,
            head["product_id"],
            {"quantity": next(p["quantity"] for p in products if p["id"] == head["product_id"]) + head["quantity"]}
        )
        return delete_order(updated_products, tail, order_id, updater, result)

    return delete_order(products, tail, order_id, updater, result + [head])

# Helper function for restoring stock
def default_stock_updater(products: List[Product], order: Order) -> List[Product]:
    return update_product(
        products,
        order["product_id"],
        {"quantity": next(p["quantity"] for p in products if p["id"] == order["product_id"]) + order["quantity"]}
    )
