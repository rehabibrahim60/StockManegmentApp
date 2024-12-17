from DB_connection import get_connection

def generate_report():
    # Establish database connection
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch low stock items
    query_low_stock = "SELECT name, quantity FROM products WHERE quantity < 10"
    cursor.execute(query_low_stock)
    low_stock = cursor.fetchall()

    # Fetch total sales
    query_total_sales = "SELECT SUM(total_cost) FROM orders"
    cursor.execute(query_total_sales)
    total_sales_result = cursor.fetchone()
    total_sales = total_sales_result[0] if total_sales_result else 0

    # Fetch inventory value
    query_inventory_value = "SELECT SUM(price * quantity) FROM products"
    cursor.execute(query_inventory_value)
    inventory_value_result = cursor.fetchone()
    inventory_value = inventory_value_result[0] if inventory_value_result else 0

    # Close resources
    cursor.close()
    connection.close()

    # Construct and return the report
    report = (
        "low_stock: ", low_stock, 
        "\n\n\ntotal_sales: ", total_sales, 
        "\n\n\ninventory_value:", inventory_value
    )
    return report
