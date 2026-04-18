import tkinter as tk
from tkinter import messagebox
import csv

file_name = "inventory.csv"
inventory = {}

# Load data
def load_data():
    try:
        with open(file_name, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                name, quantity, price = row
                inventory[name] = {"quantity": quantity, "price": price}
    except:
        pass

# Save data
def save_data():
    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file)
        for name, details in inventory.items():
            writer.writerow([name, details["quantity"], details["price"]])

# Add product
def add_product():
    name = entry_name.get()
    quantity = entry_quantity.get()
    price = entry_price.get()

    if name and quantity and price:
        inventory[name] = {"quantity": quantity, "price": price}
        save_data()
        update_listbox()
        clear_entries()
    else:
        messagebox.showerror("Error", "Fill all fields")

# Delete product
def delete_product():
    selected = listbox.get(tk.ACTIVE)
    if selected:
        name = selected.split(" - ")[0]
        del inventory[name]
        save_data()
        update_listbox()

# Update list
def update_listbox():
    listbox.delete(0, tk.END)
    for name, details in inventory.items():
        listbox.insert(tk.END, f"{name} - Qty: {details['quantity']} - Price: {details['price']}")

# Clear inputs
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)

# Search product 

def search_product():
    search = entry_name.get().strip().lower()

    if not search:
        messagebox.showwarning("Warning", "Enter product name to search")
        return

    listbox.delete(0, tk.END)

    found = False
    for name, details in inventory.items():
        if search in name.lower():
            listbox.insert(tk.END, f"{name} - Qty: {details['quantity']} - Price: {details['price']}")
            found = True

    if not found:
        messagebox.showinfo("Search", "Product not found")

# Reset list 
def show_all():
    update_listbox()

# Total inventory value

def total_value():
    total = 0
    for details in inventory.values():
        total += int(details["quantity"]) * float(details["price"])

    messagebox.showinfo("Total Value", f"Total Inventory Value = ₹{total}")

# Export to csv

def export_data():
    with open("export_inventory.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Product", "Quantity", "Price"])

        for name, details in inventory.items():
            writer.writerow([name, details["quantity"], details["price"]])

    messagebox.showinfo("Export", "Data exported to export_inventory.csv")

# GUI
# GUI START
root = tk.Tk()
root.title("Inventory System")
root.geometry("400x450")
root.configure(bg="#f0f8ff")

# Title
tk.Label(root, text="Inventory System", font=("Arial", 18, "bold"), bg="#f0f8ff").pack(pady=10)

# Frame (NEW)
main_frame = tk.Frame(root, bg="#e6f2ff", bd=2, relief="ridge")
main_frame.pack(pady=20)

# Inputs inside frame
tk.Label(main_frame, text="Product Name", bg="#e6f2ff").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(main_frame)
entry_name.grid(row=0, column=1)

tk.Label(main_frame, text="Quantity", bg="#e6f2ff").grid(row=1, column=0, padx=10, pady=5)
entry_quantity = tk.Entry(main_frame)
entry_quantity.grid(row=1, column=1)

tk.Label(main_frame, text="Price", bg="#e6f2ff").grid(row=2, column=0, padx=10, pady=5)
entry_price = tk.Entry(main_frame)
entry_price.grid(row=2, column=1)

btn_frame = tk.Frame(root, bg="#f0f8ff")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", width=12, bg="#4CAF50", fg="white", command=add_product).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Delete", width=12, bg="#f44336", fg="white", command=delete_product).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Search", width=12, bg="#2196F3", fg="white", command=search_product).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Total", width=12, bg="#9C27B0", fg="white", command=total_value).grid(row=1, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Export", width=25, bg="#ff9800", command=export_data).grid(row=2, column=0, columnspan=2, pady=5)
tk.Button(root, text="Show All", command=show_all, bg="gray", fg="white").pack(pady=5)

# Listbox with scrollbar
frame_list = tk.Frame(root)
frame_list.pack(pady=10)

scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame_list, width=50, height=10, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT)

scrollbar.config(command=listbox.yview)

# Load existing data before running
load_data()
update_listbox()

root.mainloop()