from typing import List, Dict, Callable

# Type definitions for clarity
Product = Dict[str, any]
Order = Dict[str, any]


# Higher-order recursive function to process collections
def process_collection(collection: List, predicate: Callable = None, transformer: Callable = None, result=None):
    if result is None:
        result = []

    if not collection:
        return result

    head, *tail = collection

    # Apply predicate filter
    if predicate and predicate(head):
        result = result + [transformer(head) if transformer else head]
    elif not predicate:
        result = result + [transformer(head) if transformer else head]

    return process_collection(tail, predicate, transformer, result)


# Fetch low stock products using process_collection
def fetch_low_stock(products: List[Product], threshold: int = 10) -> List[Product]:
    return process_collection(products, predicate=lambda p: p["quantity"] < threshold)


# Calculate total value using recursion and higher-order function
def calculate_total(collection: List, value_extractor: Callable[[Dict], int], total: int = 0) -> int:
    if not collection:
        return total

    head, *tail = collection
    return calculate_total(tail, value_extractor, total + value_extractor(head))


# Calculate total sales
def calculate_total_sales(orders: List[Order]) -> int:
    return calculate_total(orders, value_extractor=lambda o: o["total_cost"])


# Calculate inventory value
def calculate_inventory_value(products: List[Product]) -> int:
    return calculate_total(products, value_extractor=lambda p: p["price"] * p["quantity"])


# Generate report using higher-order functions
def generate_report(products: List[Product], orders: List[Order]) -> Dict[str, any]:
    return {
        "low_stock": fetch_low_stock(products),
        "total_sales": calculate_total_sales(orders),
        "inventory_value": calculate_inventory_value(products),
    }
