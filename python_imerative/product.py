from DB_connection import get_connection

query = ""

def add_product(name, price, quantity):
    # Establish database connection
    connection = get_connection()
    cursor = connection.cursor()

    # Assign values to query variables
    global query
    query = "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)"
    values = (name, price, quantity)

    # Execute query to add the product
    cursor.execute(query, values)
    connection.commit()

    # Close resources
    cursor.close()
    connection.close()


def get_products():
    # Establish database connection
    connection = get_connection()
    cursor = connection.cursor()

    # Execute query to fetch products
    global query
    query = "SELECT * FROM products"
    cursor.execute(query)
    
    # Retrieve products from the database
    products = cursor.fetchall()

    # Close resources
    cursor.close()
    connection.close()

    # Return fetched products
    return products


def update_product(product_id, name=None, price=None, quantity=None):
    # Establish database connection
    connection = get_connection()
    cursor = connection.cursor()

    # Initialize query components
    updates = []  # List of update clauses
    values = []   # Values to bind to the query

    # Check and prepare updates for each field
    if name is not None:
        updates.append("name = %s")
        values.append(name)
    if price is not None:
        updates.append("price = %s")
        values.append(price)
    if quantity is not None:
        updates.append("quantity = %s")
        values.append(quantity)

    # Execute the update query only if there are fields to update
    global query
    if updates:
        query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
        values.append(product_id)  # Add the product_id to the values

        # Execute the constructed query
        cursor.execute(query, values)
        connection.commit()

    # Close resources
    cursor.close()
    connection.close()

    # Print confirmation
    print(f"Product {product_id} updated successfully.")


def delete_product(product_id):
    # Establish database connection
    connection = get_connection()
    cursor = connection.cursor()

    # Prepare the delete query
    global query
    query = "DELETE FROM products WHERE id = %s"
    values = (product_id,)

    # Execute the query
    cursor.execute(query, values)
    connection.commit()

    # Close resources
    cursor.close()
    connection.close()

    # Print confirmation
    print(f"Product {product_id} deleted successfully.")
