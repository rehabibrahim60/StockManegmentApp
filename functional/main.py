from functional.product import products , add_product ,update_product , delete_product , get_all_products
from functional.order import orders , create_order , delete_order , get_orders  , default_stock_updater
from functional.reporting import generate_report

# ======================== Menus ========================
N_products = products
N_orders = orders
def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Order Management")
        print("2. Product Management")
        print("3. Reporting")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            order_management_menu()
        elif choice == "2":
            product_management_menu()
        elif choice == "3":
            print(generate_report(N_products, N_orders))
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def order_management_menu():
    global N_products, N_orders
    while True:
        print("\n--- Order Management ---")
        print("1. Create Order")
        print("2. Delete Order")
        print("3. Show Orders")
        print("4. Back to Main Menu")
        choice = input("Choose an option: ")
        if choice == "1":
            product_name = input("Enter product Name: ")
            quantity = int(input("Enter quantity: "))
            N_products, N_orders = create_order(N_products, N_orders, product_name, quantity)
            print("orders list: " , N_orders)
            print("products after order: " , N_products)
        elif choice == "2":
            order_id = int(input("Enter order ID: "))
            N_products, N_orders = delete_order(N_products, N_orders, order_id , default_stock_updater)
            print("orders list: " , N_orders)
            print("products after deleting order: " , N_products)
        elif choice == "3":
            print("orders: ",get_orders(N_products, N_orders))
            print("original: " , orders)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


def product_management_menu():
    global N_products
    while True:
        print("\n--- Product Management ---")
        print("1. Add Product")
        print("2. Delete Product")
        print("3. Update Product")
        print("4. Show Products")
        print("5. Back to Main Menu")
        choice = input("Choose an option: ")
        if choice == "1":
            new_product = {
                "id": len(N_products) + 1,
                "name": input("Enter product name: "),
                "price": int(input("Enter product price: ")),
                "quantity": int(input("Enter product quantity: ")),
            }
            N_products = add_product(N_products, new_product)
            print("Product added successfully!")
            print("products after adding : ", N_products)
        elif choice == "2":
            product_id = int(input("Enter product ID to delete: "))
            N_products = delete_product(N_products, product_id)
            print("Product deleted successfully!")
            print("products after deleting" , N_products)
        elif choice == "3":
            product_id = int(input("Enter product ID to update: "))
            updates = {}
            if input("Update name? (y/n): ").lower() == "y":
                updates["name"] = input("Enter new name: ")
            if input("Update price? (y/n): ").lower() == "y":
                updates["price"] = int(input("Enter new price: "))
            if input("Update quantity? (y/n): ").lower() == "y":
                updates["quantity"] = int(input("Enter new quantity: "))
            N_products = update_product(N_products, product_id, updates)
            print("Product updated successfully!")
            print("products after updating",N_products)
        elif choice == "4":
            print(get_all_products(N_products))
            print("original" , products)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


# ======================== Main Program ========================
if __name__ == "__main__":
    main_menu()