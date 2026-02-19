import sqlite3


conn = sqlite3.connect('grocery.db')
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS grocery_items(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL
            )
""")
conn.commit()

def add_product():
    name = input("Enter product name: ")
    price = int(input("Enter product price: "))
    quantity = int(input("Enter product quantiy: "))
    cur.execute("INSERT INTO grocery_items (name, price, quantity) VALUES (?,?,?)",(name,price,quantity))
    conn.commit()
    print("product added successfully")

def view_products():
    cur.execute("SELECT * FROM grocery_items")
    rows = cur.fetchall()
    for r in rows:
        print(f"ID: {r[0]}, Name: {r[1]} | price: {r[2]} | quantity: {r[3]}")
        print()

def update_product():
    product_id = int(input("Enter product ID to update:"))
    new_price = int(input("Enter new price:"))
    new_quantity = int(input("Enter new quantity:"))
    cur.execute("UPDATE grocery_items SET price = ?, quantity = ? WHERE product_id = ?", (new_price, new_quantity, product_id))
    conn.commit()
    print("Product updated successfully")

def delete_product():
    product_id = int(input("Enter product ID to delete:"))
    cur.execute("DELETE FROM grocery_items WHERE product_id = ?", (product_id,))
    conn.commit()
    print("Product deleted successfully")

def create_bill():
    item =[]
    total = 0
    while True:
        pid = int(input("Product ID (0 to stop):"))
        if pid == 0:
            break
        qty = int(input("Quantity:"))

        cur.execute("SELECT name , price , quantity FROM grocery_items WHERE product_id = ?", (pid,))
        product = cur.fetchone()

        if product:
            name, price, stock = product
            if qty > stock:
                print("Insufficient stock")
                continue
            amount = price * qty
            total += amount
            item.append((name, qty, amount))
            cur.execute("UPDATE grocery_items SET quantity = quantity - ? WHERE product_id = ?", (qty, pid))
            conn.commit()

    print("\n-----------BILL-----------")
    for i in item:
        print(f"{i[0]} x {i[1]} = ${i[2]}")
    print("--------------------------")
    print(f"Total Amount: ${total}")

while True:
    print("1. Add Product")
    print("2. View Products")
    print("3. Update Products")
    print("4. Delete Products")
    print("5. Create Bill")
    print("6. Exit")

    choice = int(input("Enter your choice:"))
    if choice == 1:
        add_product()
    elif choice == 2:
        view_products()
    elif choice == 3:
        update_product()
    elif choice == 4:
        delete_product()
    elif choice == 5:
        create_bill()
    elif choice == 6:
        print("Thank you")
        break
    else:
        print("Invalid choice, please try again.")


