from typing import List, Dict, Callable

# Product type
Product = Dict[str, any]

products = [
    {"id": 1, "name": "Socks", "price": 10, "quantity": 20},
    {"id": 2, "name": "Shoes", "price": 50, "quantity": 5},
    {"id": 3, "name": "Hats", "price": 15, "quantity": 8},
]

# Add a product
def add_product(products: List[Product], product: Product) -> List[Product]:
    """Returns a new list with the added product."""
    return products + [product]

# Update a product using recursion
def update_product(products: List[Product], product_id: int, updates: Dict[str, any]) -> List[Product]:
    """Returns a new list with the updated product."""
    if not products:
        return []
    head, *tail = products
    updated_head = {**head, **updates} if head["id"] == product_id else head
    return [updated_head] + update_product(tail, product_id, updates)

# Delete a product using recursion
def delete_product(products: List[Product], product_id: int) -> List[Product]:
    """Returns a new list with the product removed."""
    if not products:
        return []
    head, *tail = products
    return delete_product(tail, product_id) if head["id"] == product_id else [head] + delete_product(tail, product_id)


# Recursive implementation of filter
def filter_products(products: List[Product], condition: Callable[[Product], bool]) -> List[Product]:
    """Returns a new list of products filtered by a given condition."""
    if not products:
        return []
    head, *tail = products
    return ([head] if condition(head) else []) + filter_products(tail, condition)

# Retrieve all products (pure function, no side effects)
def get_all_products(products: List[Product]) -> List[Product]:
    """Returns the list of products."""
    return products

