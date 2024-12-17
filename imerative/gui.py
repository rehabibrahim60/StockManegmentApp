import tkinter as tk
from tkinter import ttk, messagebox ,PhotoImage
from product import add_product, get_products, delete_product, update_product
from order import create_order , get_orders , delete_order
from reporting import generate_report



def open_product_management():
    product_window = tk.Toplevel()
    product_window.title("Product Management")
    product_window.geometry("800x500")
    
    # Frame for inputs and buttons
    input_frame = tk.Frame(product_window)
    input_frame.pack(fill="x", padx=10, pady=10)

    # Input fields
    tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(input_frame, text="Price:").grid(row=0, column=1, padx=5, pady=5)
    tk.Label(input_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=5)

    name_var = tk.StringVar()
    price_var = tk.StringVar()
    quantity_var = tk.StringVar()

    tk.Entry(input_frame, textvariable=name_var).grid(row=1, column=0, padx=5, pady=5)
    tk.Entry(input_frame, textvariable=price_var).grid(row=1, column=1, padx=5, pady=5)
    tk.Entry(input_frame, textvariable=quantity_var).grid(row=1, column=2, padx=5, pady=5)

    # Buttons for Add, Update, and Delete
    tk.Button(input_frame, text="Add Product", command=lambda: add_product_ui(name_var, price_var, quantity_var, product_tree)).grid(row=1, column=3, padx=5, pady=5)
    tk.Button(input_frame, text="Update Product", command=lambda: update_product_ui(name_var, price_var, quantity_var, product_tree)).grid(row=1, column=4, padx=5, pady=5)

    # Table to display products
    product_tree = ttk.Treeview(product_window, columns=("ID", "Name", "Price", "Quantity"), show="headings")
    product_tree.heading("ID", text="ID")
    product_tree.heading("Name", text="Name")
    product_tree.heading("Price", text="Price")
    product_tree.heading("Quantity", text="Quantity")
    product_tree.bind("<ButtonRelease-1>", lambda event: populate_fields_ui(event, product_tree, name_var, price_var, quantity_var))  # Bind click event
    product_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Delete Product Button
    tk.Button(product_window, text="Delete Product", command=lambda: delete_product_ui(product_tree)).pack(pady=10)

    # Refresh table initially
    refresh_products_ui(product_tree)


# Helper functions
def populate_fields_ui(event, product_tree, name_var, price_var, quantity_var):
    """Populates the input fields with the selected product's data."""
    selected_item = product_tree.focus()
    if selected_item:
        product_data = product_tree.item(selected_item)["values"]
        name_var.set(product_data[1])
        price_var.set(product_data[2])
        quantity_var.set(product_data[3])


def update_product_ui(name_var, price_var, quantity_var, product_tree):
    """Updates the selected product's details."""
    selected_item = product_tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "No product selected!")
        return

    # Get updated data
    product_id = product_tree.item(selected_item)["values"][0]
    name = name_var.get()
    try:
        price = float(price_var.get())
        quantity = int(quantity_var.get())
        update_product(product_id, name, price, quantity)  # Call the update function
        messagebox.showinfo("Success", f"Product '{name}' updated successfully!")
        refresh_products_ui(product_tree)
        name_var.set("")
        price_var.set("")
        quantity_var.set("")
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter valid values for price and quantity.")



# Helper functions for the Product Management Window
def add_product_ui(name_var, price_var, quantity_var, product_tree):
    name = name_var.get()
    try:
        price = float(price_var.get())
        quantity = int(quantity_var.get())
        add_product(name, price, quantity)
        messagebox.showinfo("Success", f"Product '{name}' added successfully!")
        refresh_products_ui(product_tree)
        name_var.set("")
        price_var.set("")
        quantity_var.set("")
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter valid values for price and quantity.")


def refresh_products_ui(product_tree):
    # Clear existing rows
    for row in product_tree.get_children():
        product_tree.delete(row)
    
    # Fetch all products and insert them into the table
    products = get_products()
    for product in products:
        product_tree.insert("", tk.END, values=product)


def delete_product_ui(product_tree):
    selected_item = product_tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "No product selected!")
        return

    # Get the selected product ID
    product_id = product_tree.item(selected_item)["values"][0]
    delete_product(product_id)
    messagebox.showinfo("Success", "Product deleted successfully!")
    refresh_products_ui(product_tree)






def open_order_management():
    order_window = tk.Toplevel()
    order_window.title("Order Management")
    order_window.geometry("800x500")
    
    # Frame for inputs and buttons
    input_frame = tk.Frame(order_window)
    input_frame.pack(fill="x", padx=10, pady=10)

    # Input fields
    tk.Label(input_frame, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(input_frame, text="Quantity:").grid(row=0, column=1, padx=5, pady=5)

    product_name_var = tk.StringVar()
    quantity_var = tk.StringVar()

    tk.Entry(input_frame, textvariable=product_name_var).grid(row=1, column=0, padx=5, pady=5)
    tk.Entry(input_frame, textvariable=quantity_var).grid(row=1, column=1, padx=5, pady=5)

    # Buttons for Create and Delete Order
    tk.Button(input_frame, text="Create Order", command=lambda: create_order_ui(product_name_var, quantity_var, order_tree)).grid(row=1, column=2, padx=5, pady=5)
    tk.Button(input_frame, text="Delete Order", command=lambda: delete_order_ui(order_tree)).grid(row=1, column=3, padx=5, pady=5)

    # Table to display orders
    order_tree = ttk.Treeview(order_window, columns=("Order ID", "Product Name", "Quantity", "Total Cost"), show="headings")
    order_tree.heading("Order ID", text="Order ID")
    order_tree.heading("Product Name", text="Product Name")
    order_tree.heading("Quantity", text="Quantity")
    order_tree.heading("Total Cost", text="Total Cost")
    order_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Refresh table initially
    refresh_orders_ui(order_tree)

# Helper Functions

def create_order_ui(product_name_var, quantity_var, order_tree):
    """Creates a new order using product name."""
    product_name = product_name_var.get()
    quantity = quantity_var.get()

    try:
        quantity = int(quantity)
        create_order(product_name, quantity)  # Call backend create_order
        messagebox.showinfo("Success", "Order created successfully!")
        refresh_orders_ui(order_tree)
        
        product_name_var.set("")
        quantity_var.set("")
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Quantity must be an integer.")
    except Exception as e:
        messagebox.showerror("Error", f"Error creating order: {e}")


def delete_order_ui(order_tree):
    """Deletes the selected order from the table."""
    selected_item = order_tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "No order selected!")
        return

    order_id = order_tree.item(selected_item)["values"][0]
    try:
        delete_order(order_id)  # Calls the backend delete_order function
        messagebox.showinfo("Success", "Order deleted successfully!")
        refresh_orders_ui(order_tree)
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting order: {e}")


def refresh_orders_ui(order_tree):
    """Refreshes the order table with data from the database."""
    for row in order_tree.get_children():
        order_tree.delete(row)

    try:
        orders = get_orders()  # Calls the backend get_orders function
        for order in orders:
            order_tree.insert("", tk.END, values=order)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading orders: {e}")






def open_reporting():
    report_window = tk.Toplevel()
    report_window.title("Reporting")
    report_window.geometry("600x400")
    
    # Frame for report display
    report_frame = tk.Frame(report_window)
    report_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Label for window title
    tk.Label(report_frame, text="Report ", font=("Arial", 14, "bold")).pack(pady=5)
    
    # Scrollable text widget to display the report
    report_text = tk.Text(report_frame, wrap="word", font=("Arial", 12))
    report_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Scrollbar
    scrollbar = tk.Scrollbar(report_text, orient="vertical", command=report_text.yview)
    scrollbar.pack(side="right", fill="y")
    report_text.configure(yscrollcommand=scrollbar.set)
    
    # Generate and display the report
    try:
        report_details = generate_report()  # Calls the backend function to get the report details
        report_text.insert("1.0", report_details)
    except Exception as e:
        report_text.insert("1.0", f"Error generating report: {e}")
    
    # Disable editing of the report text
    report_text.configure(state="disabled")





def main_gui():
    root = tk.Tk()
    root.title("Stock Management System")
    root.geometry("700x700")
    
    #reload images
    order_img =PhotoImage( file ="./order.png")
    product_img = PhotoImage( file ="./pro.png")
    report_img = PhotoImage( file ="./report.png")

    tk.Button(root, text="Product Management",image=product_img, compound="top" , command=open_product_management).pack(pady=10)
    tk.Button(root, text="Order Management",image=order_img,compound="top" , command=open_order_management).pack(pady=10)
    tk.Button(root, text="Reporting",image=report_img, compound="top" , command=open_reporting).pack(pady=10)

    root.mainloop()
