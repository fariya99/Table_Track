from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime
import tkinter as tk
from tkinter import Label
# === Initialize ===
root = Tk()
root.title("Restaurant Management System")
root.geometry("1000x700")
root.configure(bg="white")

# Center the window
def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")

center_window(root, 1000, 700)
# Top bar inside content_frame
top_frame = Frame(root, bg="#222", height=60)
top_frame.pack(side="top", fill="x")
Label(top_frame, text="Table Track", bg="#222", fg="white",
      font=("Arial", 20, "bold")).pack(pady=10)
# Create a frame for the sidebar
sidebar = tk.Frame(root, bg="#333", width=220)
sidebar.pack(side="left", fill="y")

# Create a content frame for the working area
content_frame = Frame(root, bg="white")
content_frame.pack(side="left", fill=BOTH, expand=True)




def show_welcome_screen():
    for widget in content_frame.winfo_children():
        if widget is not top_frame:
            widget.destroy()

    try:
        left_icon = Image.open("image for res.jpg")  # replace with your image path
        right_icon = Image.open("image for res.jpg")
        left_icon = left_icon.resize((50, 50))
        right_icon = right_icon.resize((50, 50))
        left_img = ImageTk.PhotoImage(left_icon)
        right_img = ImageTk.PhotoImage(right_icon)
    except Exception as e:
        print("Error loading image:", e)
        left_img = right_img = None

    center_frame = Frame(content_frame, bg="white")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    inner_frame = Frame(center_frame, bg="white")
    inner_frame.pack()

    # Keep references on label widgets
    if left_img:
        left_label = Label(inner_frame, image=left_img, bg="white")
        left_label.image = left_img
        left_label.pack(side=LEFT, padx=10)

    Label(inner_frame, text="Welcome to Table Track", font=("Helvetica", 28, "bold"),
          bg="white", fg="#27589d").pack(side=LEFT)

    if right_img:
        right_label = Label(inner_frame, image=right_img, bg="white")
        right_label.image = right_img
        right_label.pack(side=LEFT, padx=10)


# === Utils ===
def clear_content():
    for widget in content_frame.winfo_children():
        if widget is not top_frame:
            widget.destroy()

menu_file = "menu.txt"
sales_file = "sales.txt"
orders_file = "orders.txt"  # New file for orders
bills_file = "bill.txt"  # Single bill file
customers_file = "customers.txt"
revenue="revenue.txt"
# === Functions ===
def show_dashboard():
    clear_content()
    show_welcome_screen()
    
def load_menu():
    menu = {}
    if os.path.exists(menu_file):
        with open(menu_file, 'r') as f:
            category = None
            for line in f:
                line = line.strip()
                if line.startswith("[") and line.endswith("]"):
                    category = line[1:-1]
                    menu[category] = []
                elif line and category:
                    name, price = line.split(',')
                    menu[category].append((name.strip(), float(price)))
    return menu

def save_order_to_files(order_items, customer_info):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    total = sum(price * qty for _, price, qty in order_items)

    # Save to orders.txt (in requested format)
    with open(orders_file, 'a') as f:
        f.write(f"Order Time: {timestamp}\n")
        f.write(f"Customer Name: {customer_info.get('Name', '')}\n")
        f.write(f"Contact: {customer_info.get('Contact', '')}\n")
        f.write(f"Address: {customer_info.get('Address', '')}\n")
        for item_name, item_price, item_qty in order_items:
            f.write(f"{item_name} x {item_qty} = Rs{item_price * item_qty:.2f}\n")
        f.write(f"Total: Rs{total:.2f}\n")
        f.write("\n")  # separate orders with a blank line

    # Save to bill.txt (can be overwritten each time)
    with open(bills_file, 'w') as f:
        f.write("Customer Info:\n")
        for key, val in customer_info.items():
            f.write(f"{key}: {val}\n")
        f.write("\nOrder:\n")
        for name, price, qty in order_items:
            f.write(f"{name} x{qty} = Rs{price * qty:.2f}\n")
        f.write(f"\nTotal: Rs{total:.2f}\n")

    # Save simple summary to sales.txt
    with open(sales_file, 'a') as f:
        f.write(f"{timestamp}, Rs{total:.2f}\n")

    # Save to customers.txt (avoid duplicates)
    customer_line = f"{customer_info.get('Name', '')}|{customer_info.get('Contact', '')}|{customer_info.get('Address', '')}"
    with open(customers_file, 'a+') as f:
        f.seek(0)
        existing_customers = f.read().splitlines()
        if customer_line not in existing_customers:
            f.write(customer_line + "\n")


    messagebox.showinfo("Order Placed", f"Order placed successfully!")

def take_order_page():
    clear_content()
    menu = load_menu()

    Label(content_frame, text="Take Order", font=("Arial", 20), bg="white").pack(pady=10)

    # ---------- Top container (customer info + menu side-by-side) ----------
    top_container = Frame(content_frame, bg="white")
    top_container.pack(padx=10, pady=5, fill="both", expand=True)

    # -------- Left: Customer Info Frame --------
    cust_frame = Frame(top_container, bg="white", bd=2, relief=RIDGE)
    cust_frame.pack(side=LEFT, padx=10, pady=5, fill="y")

    Label(cust_frame, text="Customer Info", font=("Arial", 14, "bold"), bg="white").pack(pady=5)

    entries = {}
    for label in ["Name", "Contact", "Address"]:
        row = Frame(cust_frame, bg="white")
        Label(row, text=label + ":", width=10, anchor='w', bg="white").pack(side=LEFT)
        ent = Entry(row, width=25)
        ent.pack(side=LEFT, padx=5, pady=5)
        entries[label] = ent
        row.pack(pady=2)

    # -------- Right: Menu Frame with Scrollbar --------
    menu_frame_container = Frame(top_container, bg="white", bd=2, relief=RIDGE)
    menu_frame_container.pack(side=LEFT, padx=10, pady=5, fill=BOTH, expand=True)

    Label(menu_frame_container, text="Menu", font=("Arial", 14, "bold"), bg="white").pack(pady=5)

    # Scrollable canvas inside container
    canvas = Canvas(menu_frame_container, bg="white")
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(menu_frame_container, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scroll_frame = Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=scroll_frame, anchor='nw')

    check_vars = []

    for cat, items in menu.items():
        Label(scroll_frame, text=f"{cat}", font=("Arial", 12, "bold"), bg="white", fg="#124c9e").pack(anchor='w', padx=10)
        for name, price in items:
            row = Frame(scroll_frame, bg="white")
            var = IntVar()
            chk = Checkbutton(row, text=f"{name} - Rs{price}", variable=var, bg="white")
            chk.pack(side=LEFT)
            qty = Spinbox(row, from_=1, to=10, width=5)
            qty.pack(side=LEFT, padx=10)
            row.pack(anchor='w', padx=20)
            check_vars.append((var, name, price, qty))

    # ---------- Bottom: Place Order Button ----------
    def place_order():
        selected_items = [(name, price, int(qty.get())) for var, name, price, qty in check_vars if var.get() == 1]
        if not selected_items:
            messagebox.showwarning("Empty Order", "Please select at least one item.")
            return

        customer = {key: entry.get().strip() for key, entry in entries.items()}

        # ---- VALIDATION STARTS HERE ----
        if not customer["Name"].replace(" ", "").isalpha():
            messagebox.showwarning("Invalid Name", "Name must contain only letters.")
            return
        if not (customer["Contact"].isdigit() and 7 <= len(customer["Contact"]) <= 15):
            messagebox.showwarning("Invalid Contact", "Contact number must be numeric and 7 to 15 digits long.")
            return

        if len(customer["Address"]) < 5:
            messagebox.showwarning("Invalid Address", "Address is too short.")
            return
        # ---- VALIDATION ENDS HERE ----

        save_order_to_files(selected_items, customer)

        # Reset entries and selections
        for ent in entries.values():
            ent.delete(0, END)
        for var, _, _, qty in check_vars:
            var.set(0)
            qty.delete(0, END)
            qty.insert(0, "1")

    Button(content_frame, text="Place Order", command=place_order, bg="#28a745", fg="white",
           font=("Arial", 12), padx=10, pady=5).pack(pady=10)

def edit_menu_page():
    clear_content()
    Label(content_frame, text="Edit Menu", font=("Arial", 20), bg="white").pack(pady=10)

    # ---------- Scrollable Frame for Menu ----------
    menu_canvas_frame = Frame(content_frame, bg="white")
    menu_canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = Canvas(menu_canvas_frame, bg="white", height=300)
    scrollbar = Scrollbar(menu_canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="white")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    menu = load_menu()
    for cat, items in menu.items():
        Label(scrollable_frame, text=f"[{cat}]", font=("Arial", 14, "bold"), bg="white").pack(anchor='w', padx=10, pady=(5, 0))
        for name, price in items:
            Label(scrollable_frame, text=f"  - {name}: Rs{price:.2f}", font=("Arial", 12), bg="white").pack(anchor='w', padx=30)

    # ---------- Add/Delete Form ----------
    form_frame = Frame(content_frame, bg="white")
    form_frame.pack(pady=15)

    # Labels
    Label(form_frame, text="Category:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    Label(form_frame, text="Item:", font=("Arial", 12), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky='e')
    Label(form_frame, text="Price:", font=("Arial", 12), bg="white").grid(row=0, column=4, padx=5, pady=5, sticky='e')

    # Entry Fields
    category_var = StringVar()
    item_var = StringVar()
    price_var = StringVar()

    Entry(form_frame, textvariable=category_var, width=20, font=("Arial", 12)).grid(row=0, column=1, padx=5, pady=5)
    Entry(form_frame, textvariable=item_var, width=20, font=("Arial", 12)).grid(row=0, column=3, padx=5, pady=5)
    Entry(form_frame, textvariable=price_var, width=10, font=("Arial", 12)).grid(row=0, column=5, padx=5, pady=5)

    # --- Functions ---
    def save_menu(updated_menu):
        with open(menu_file, 'w') as f:
            for cat, items in updated_menu.items():
                f.write(f"[{cat}]\n")
                for name, price in items:
                    f.write(f"{name},{price}\n")

    def add_item():
        cat = category_var.get().strip().upper()
        name = item_var.get().strip().lower()
        price_input = price_var.get().strip()

        # Check for empty fields
        if not (cat and name and price_input):
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        # Validate category and item name
        if not cat.isalpha():
            messagebox.showerror("Invalid Category", "Category must only contain letters.")
            return
        if not name.replace(" ", "").isalpha():
            messagebox.showerror("Invalid Item Name", "Item name must only contain letters and spaces.")
            return

        # Validate price
        try:
            price = float(price_input)
            if price <= 0 and price!=float:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Price", "Price must be a positive number.")
            return

        # Load, update and save menu
        menu = load_menu()
        if cat not in menu:
            menu[cat] = []
        menu[cat].append((name, price))
        save_menu(menu)

        messagebox.showinfo("Success", "Item added to menu.")
        edit_menu_page()


    def delete_item():
        cat = category_var.get().strip().upper()
        name = item_var.get().strip().lower()

        # Check for empty fields
        if not (cat and name):
            messagebox.showwarning("Input Error", "Category and item name are required.")
            return

        # Validate category and item name
        if not cat.isalpha():
            messagebox.showerror("Invalid Category", "Category must only contain letters.")
            return
        if not name.replace(" ", "").isalpha():
            messagebox.showerror("Invalid Item Name", "Item name must only contain letters and spaces.")
            return

        # Load menu and try to delete item
        menu = load_menu()
        if cat in menu:
            new_items = [(n, p) for (n, p) in menu[cat] if n.lower() != name.lower()]
            if len(new_items) < len(menu[cat]):
                menu[cat] = new_items
                save_menu(menu)
                messagebox.showinfo("Success", "Item deleted from menu.")
                edit_menu_page()
            else:
                messagebox.showinfo("Not Found", "Item not found in the given category.")
        else:
            messagebox.showinfo("Not Found", "Category not found.")

    # Buttons
    Button(form_frame, text="Add Item", command=add_item, bg="#28a745", fg="white",
           font=("Arial", 12)).grid(row=1, column=1, columnspan=2, pady=10)

    Button(form_frame, text="Delete Item", command=delete_item, bg="#dc3545", fg="white",
           font=("Arial", 12)).grid(row=1, column=3, columnspan=2, pady=10)

def view_sales_page():
    clear_content()
    Label(content_frame, text="Sales Records", font=("Arial", 20), bg="white").pack(pady=10)

    # Scrollable frame setup
    frame = Frame(content_frame, bg="white")
    frame.pack(fill="both", expand=True)

    canvas = Canvas(frame, bg="white")
    canvas.pack(side=LEFT, fill="both", expand=True)

    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    sales_frame = Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=sales_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    sales_frame.bind("<Configure>", on_configure)

    if os.path.exists(orders_file):
        with open(orders_file, 'r') as f:
            sale_lines = []
            for line in f:
                stripped = line.strip()
                if stripped.startswith("Order Time:"):
                    if sale_lines:
                        Label(sales_frame, text="Sales Record", font=("Arial", 12, "bold"), bg="white", fg="green").pack(anchor='w', padx=10, pady=(10, 0))
                        for entry in sale_lines:
                            Label(sales_frame, text=entry, bg="white", font=("Courier", 10), anchor='w', justify='left').pack(anchor='w', padx=20)
                        sale_lines = []
                    sale_lines.append(stripped)
                elif stripped:
                    sale_lines.append(stripped)
            # Handle last sale
            if sale_lines:
                Label(sales_frame, text="Sales Record", font=("Arial", 12, "bold"), bg="white", fg="green").pack(anchor='w', padx=10, pady=(10, 0))
                for entry in sale_lines:
                    Label(sales_frame, text=entry, bg="white", font=("Courier", 10), anchor='w', justify='left').pack(anchor='w', padx=20)
    else:
        Label(sales_frame, text="No sales records found.", bg="white").pack(anchor='w', padx=10)

def view_bills_page():
    clear_content()
    Label(content_frame, text="Customer's Receipt", font=("Arial", 20), bg="white").pack(pady=10)

    frame = Frame(content_frame, bg="white")
    frame.pack(fill="both", expand=True)

    canvas_tk = Canvas(frame, bg="white")
    canvas_tk.pack(side=LEFT, fill="both", expand=True)

    scrollbar = Scrollbar(frame, orient="vertical", command=canvas_tk.yview)
    scrollbar.pack(side=RIGHT, fill="y")

    canvas_tk.configure(yscrollcommand=scrollbar.set)

    bills_frame = Frame(canvas_tk, bg="white")
    canvas_tk.create_window((0, 0), window=bills_frame, anchor="nw")

    def on_configure(event):
        canvas_tk.configure(scrollregion=canvas_tk.bbox("all"))
    bills_frame.bind("<Configure>", on_configure)

    # Ensure bill.txt exists
    if not os.path.exists(bills_file):
        with open(bills_file, 'w', encoding='utf-8') as f:
            f.write("No bills available.")

    try:
        with open(bills_file, 'r', encoding='utf-8') as f:
            bill_text = f.read()
            Label(bills_frame, text="Receipt", font=("Arial", 14, "bold"), bg="white", fg="blue").pack(anchor="w", padx=10, pady=(10, 0))
            Label(bills_frame, text=bill_text, justify="left", bg="white", font=("Courier", 11)).pack(anchor="w", padx=20)

            # PDF Download Button
            def download_pdf_receipt():
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    initialfile="Customer_Receipt.pdf",
                    filetypes=[("PDF Files", "*.pdf")]
                )
                if save_path:
                    try:
                        c = canvas.Canvas(save_path, pagesize=A4)
                        width, height = A4
                        y = height - 50
                        for line in bill_text.splitlines():
                            c.drawString(50, y, line)
                            y -= 15
                            if y < 50:
                                c.showPage()
                                y = height - 50
                        c.save()
                        messagebox.showinfo("Success", f"PDF Receipt saved:\n{save_path}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to create PDF:\n{e}")

            Button(bills_frame, text="Download PDF Receipt", command=download_pdf_receipt, bg="#2196F3", fg="white").pack(pady=20)

    except Exception as e:
        Label(bills_frame, text=f"Error reading bill.txt: {e}", bg="white", fg="red").pack(anchor="w", padx=10)

def customer_info_page():
    clear_content()
    Label(content_frame, text="Customer Records", font=("Arial", 20), bg="white").pack(pady=10)

    # Search bar
    search_frame = Frame(content_frame, bg="white")
    search_frame.pack(pady=5, padx=10, fill='x')

    Label(search_frame, text="Search Customer:", bg="white", font=("Arial", 12)).pack(side=LEFT, padx=(0,5))
    search_var = StringVar()
    search_entry = Entry(search_frame, textvariable=search_var, font=("Arial", 12))
    search_entry.pack(side=LEFT, fill='x', expand=True)

    # Scrollable frame setup
    frame = Frame(content_frame, bg="white")
    frame.pack(fill="both", expand=True)

    canvas = Canvas(frame, bg="white")
    canvas.pack(side=LEFT, fill="both", expand=True)

    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    customer_frame = Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=customer_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    customer_frame.bind("<Configure>", on_configure)

    customer_records = []
    if os.path.exists(customers_file):
        with open(customers_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    name, contact, address = parts[0], parts[1], parts[2]
                    customer_records.append((name, contact, address))

    def display_customers(records):
        for widget in customer_frame.winfo_children():
            widget.destroy()
        for i, (name, contact, address) in enumerate(records, start=1):
            Label(customer_frame, text=f"Customer Info {i}", font=("Arial", 12, "bold"), bg="white", fg="blue").pack(anchor="w", padx=10, pady=(10, 0))
            Label(customer_frame, text=f"Name    : {name}", bg="white", anchor="w", font=("Arial", 11)).pack(anchor="w", padx=20)
            Label(customer_frame, text=f"Contact : {contact}", bg="white", anchor="w", font=("Arial", 11)).pack(anchor="w", padx=20)
            Label(customer_frame, text=f"Address : {address}", bg="white", anchor="w", font=("Arial", 11)).pack(anchor="w", padx=20)
            Label(customer_frame, text="", bg="white").pack()  # Spacer

    def on_search(*args):
        query = search_var.get().strip().lower()
        if query == "":
            display_customers(customer_records)
            return
        filtered = [rec for rec in customer_records if query in rec[0].lower() or query in rec[1] or query in rec[2].lower()]
        display_customers(filtered)

    search_var.trace_add("write", on_search)

    display_customers(customer_records)



def daily_revenue_page():
    clear_content()
    Label(content_frame, text="Daily Revenue", font=("Arial", 20), bg="white").pack(pady=10)

    today = datetime.now().strftime('%Y-%m-%d')
    total = 0.0

    # Calculate total revenue for today from sales_file
    if os.path.exists(sales_file):
        with open(sales_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith(today):
                    parts = line.split(',')
                    if len(parts) >= 2:
                        amount_str = parts[1].strip()
                        if amount_str.startswith('Rs'):
                            try:
                                amount = float(amount_str.replace('Rs', '').strip())
                                total += amount
                            except ValueError:
                                pass

    # Display today's total revenue
    Label(content_frame, text=f"Total Revenue for {today}: Rs {total:.2f}", bg="white", font=("Arial", 14)).pack(pady=10)

    revenue_line = f"Revenue of {today}\nRs {total:.2f}\n\n"

    # Read existing revenue file lines
    lines = []
    if os.path.exists(revenue):
        with open(revenue, 'r') as f:
            lines = f.readlines()

    # Rewrite file, updating today's revenue if present, else append it
    found = False
    with open(revenue, 'w') as f:
        for line in lines:
            if line.strip().startswith(today):
                f.write(revenue_line)  # Update today's line
                found = True
            else:
                f.write(line)          # Keep old days unchanged
        if not found:
            f.write(revenue_line)      # Append if today's revenue not found



# === Buttons ===
buttons = [
    ("Dashboard", show_dashboard),
    ("Take Order", take_order_page),
    ("Edit Menu", edit_menu_page),
    ("View Sales", view_sales_page),
    ("View Bills", view_bills_page),
    ("Customer Info", customer_info_page),
    ("Daily Revenue",daily_revenue_page),
    ("Log Out", root.quit)
]

btn_font = ("Arial", 12)
for (text, command) in buttons:
    btn = Button(sidebar, text=text, command=command, bg="#444", fg="white",
                 font=btn_font, relief="flat", pady=12)
    btn.pack(fill="x", padx=10, pady=5)
    btn.bind("<Enter>", lambda e: e.widget.config(bg="#555"))
    btn.bind("<Leave>", lambda e: e.widget.config(bg="#444"))


# === Run ===
show_dashboard()
root.mainloop()

