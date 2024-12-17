from typing import List, Dict, Callable, Mapping
from types import MappingProxyType
from copy import deepcopy

# Product type (Immutable Dict)
Product = Mapping[str, any]

# Helper to make a Product immutable
def make_immutable(product: Dict[str, any]) -> Product:
    """Convert a mutable dictionary into an immutable product."""
    return MappingProxyType(deepcopy(product))

# Add a product
def add_product(products: List[Product], product: Dict[str, any]) -> List[Product]:
    """Returns a new immutable list with the added product."""
    return products + [make_immutable(product)]

# Update a product using recursion
def update_product(products: List[Product], product_id: int, updates: Dict[str, any]) -> List[Product]:
    """Returns a new immutable list with the updated product."""
    if not products:
        return []
    head, *tail = products
    updated_head = (
        make_immutable({**head, **updates}) if head["id"] == product_id else head
    )
    return [updated_head] + update_product(tail, product_id, updates)

# Delete a product using recursion
def delete_product(products: List[Product], product_id: int) -> List[Product]:
    """Returns a new immutable list with the product removed."""
    if not products:
        return []
    head, *tail = products
    return delete_product(tail, product_id) if head["id"] == product_id else [head] + delete_product(tail, product_id)

# Recursive implementation of filter
def filter_products(products: List[Product], condition: Callable[[Product], bool]) -> List[Product]:
    """Returns a new immutable list of products filtered by a given condition."""
    if not products:
        return []
    head, *tail = products
    return ([head] if condition(head) else []) + filter_products(tail, condition)

# Retrieve all products (pure function, no side effects)
def get_all_products(products: List[Product]) -> List[Product]:
    """Returns the immutable list of products."""
    return products

# Example usage
products = [
    make_immutable({"id": 1, "name": "Socks", "price": 10, "quantity": 20}),
    make_immutable({"id": 2, "name": "Shoes", "price": 50, "quantity": 5}),
    make_immutable({"id": 3, "name": "Hats", "price": 15, "quantity": 8}),
]


