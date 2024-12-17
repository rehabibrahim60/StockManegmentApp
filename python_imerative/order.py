from DB_connection import get_connection

def create_order(product_name, quantity):
    # Establish database connection
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch product details
    query_fetch_product = "SELECT * FROM products WHERE name = %s"
    cursor.execute(query_fetch_product, (product_name,))
    product = cursor.fetchone()
    print(product)

    # Check if product exists
    if not product:
        raise ValueError("Product not found")

    # Assign product details to variables
    _,_,price, stock = product

    # Check stock availability
    if stock < quantity:
        raise ValueError(f"Insufficient stock! Available: {stock}")

    # Calculate total cost and update stock
    total_cost = price * quantity
    new_quantity = stock - quantity

    # Insert order into database
    query_insert_order = "INSERT INTO orders (product_id, quantity, total_cost) VALUES (%s, %s, %s)"
    values_order = (product[0], quantity, total_cost)
    cursor.execute(query_insert_order, values_order)

    # Update product stock
    query_update_product = "UPDATE products SET quantity = %s WHERE id = %s"
    values_update_stock = (new_quantity, product[0])
    cursor.execute(query_update_product, values_update_stock)

    # Commit changes and close resources
    connection.commit()
    cursor.close()
    connection.close()


def get_orders():
    # Establish database connection
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch all orders with product names
    query_fetch_orders = """
    SELECT 
        orders.id AS order_id,
        products.name AS product_name,
        orders.quantity,
        orders.total_cost
    FROM 
        orders
    JOIN 
        products
    ON 
        orders.product_id = products.id;
    """
    cursor.execute(query_fetch_orders)
    orders = cursor.fetchall()

    # Close resources
    cursor.close()
    connection.close()

    # Return fetched orders
    return orders

def delete_order(order_id):
    # Establish database connection
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch order details
    query_fetch_order = "SELECT product_id, quantity FROM orders WHERE id = %s"
    cursor.execute(query_fetch_order, (order_id,))
    order = cursor.fetchone()

    # Check if order exists
    if not order:
        raise ValueError("Order not found")

    # Assign order details to variables
    product_id, quantity = order

    # Delete order from database
    query_delete_order = "DELETE FROM orders WHERE id = %s"
    cursor.execute(query_delete_order, (order_id,))

    # Fetch current stock of the product
    query_fetch_stock = "SELECT quantity FROM products WHERE id = %s"
    cursor.execute(query_fetch_stock, (product_id,))
    stock = cursor.fetchone()[0]

    # Calculate new stock quantity
    new_quantity = stock + quantity

    # Update product stock
    query_update_stock = "UPDATE products SET quantity = %s WHERE id = %s"
    values_update_stock = (new_quantity, product_id)
    cursor.execute(query_update_stock, values_update_stock)

    # Commit changes and close resources
    connection.commit()
    cursor.close()
    connection.close()
