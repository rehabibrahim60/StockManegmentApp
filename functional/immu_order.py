from typing import List, Callable, Tuple, Mapping
from types import MappingProxyType
from copy import deepcopy
from product import products , update_product

# Product type (Immutable Dict)
Product = Mapping[str, any]

# Order type (Immutable Dict)
Order = Mapping[str, any]

# Helper to make a Product immutable
def make_immutable(data: dict) -> Mapping:
    """Convert a mutable dictionary into an immutable structure."""
    return MappingProxyType(deepcopy(data))


# Recursive function to find a product immutably
def find_product(products: List[Product], product_name: str) -> Product:
    """Find a product by name using recursion."""
    if not products:
        raise ValueError("Product not found")
    if products[0]["name"] == product_name:
        return products[0]
    return find_product(products[1:], product_name)

# Create an order immutably
def create_order(products: List[Product], orders: List[Order], product_name: str, quantity: int) -> Tuple[List[Product], List[Order]]:
    """Creates a new order and returns new immutable lists."""
    product = find_product(products, product_name)
    
    if product["quantity"] < quantity:
        raise ValueError("Insufficient stock, try again...")

    updated_products = update_product(
        products,
        product["id"],
        {"quantity": product["quantity"] - quantity}
    )

    new_order = make_immutable({
        "id": len(orders) + 1,
        "product_id": product["id"],
        "quantity": quantity,
        "total_cost": product["price"] * quantity,
    })

    return updated_products, orders + [new_order]

# Delete an order immutably using recursion
def delete_order(products: List[Product], orders: List[Order], order_id: int, updater: Callable[[List[Product], Order], List[Product]] = None, result=None) -> Tuple[List[Product], List[Order]]:
    """Deletes an order immutably and restores stock."""
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

# Default stock updater for restoring stock immutably
def default_stock_updater(products: List[Product], order: Order) -> List[Product]:
    """Restores product stock immutably when an order is deleted."""
    return update_product(
        products,
        order["product_id"],
        {"quantity": next(p["quantity"] for p in products if p["id"] == order["product_id"]) + order["quantity"]}
    )

# Get orders with product details using recursion
def get_orders(products: List[Product], orders: List[Order], formatter: Callable[[Order, Product], dict] = None, result=None) -> List[dict]:
    """Returns a new immutable list of formatted orders."""
    if result is None:
        result = []

    if not orders:
        return result

    head, *tail = orders
    product = next(p for p in products if p["id"] == head["product_id"])

    formatted_order = formatter(head, product) if formatter else {
        "order_id": head["id"],
        "product_name": product["name"],
        "quantity": head["quantity"],
        "total_cost": head["total_cost"],
    }

    return get_orders(products, tail, formatter, result + [make_immutable(formatted_order)])


orders = [
    make_immutable({"id": 1, "product_id": 1, "quantity": 2, "total_cost": 20}),
    make_immutable({"id": 2, "product_id": 2, "quantity": 1, "total_cost": 50}),
]
