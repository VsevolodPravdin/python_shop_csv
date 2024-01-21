import csv
import getpass



PRODUCT_FILE = "products.csv"
SELLER_PASSWORD = "sel123"
cart = []

def load_products():
    try:
        with open(PRODUCT_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            products = list(reader)

            # Convert 'quantity' and 'price' values to integers and floats
            for product in products:
                product['quantity'] = int(product['quantity'])
                product['price'] = float(product['price'])

        return products
    except FileNotFoundError:
        print("Product file not found. Please create a product file.")
        return []

def save_products(products):
    try:
        with open(PRODUCT_FILE, 'w', newline='', encoding='utf-8') as file:
            fieldnames = products[0].keys() if products else []
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)
        print("Product list updated successfully.")
    except Exception as e:
        print(f"Error saving product list: {e}")


def authenticate_seller():
    password_attempts = 3

    while password_attempts > 0:
        entered_password = input("Enter seller password: ")

        if entered_password == SELLER_PASSWORD:
            return True

        password_attempts -= 1
        print(f"Incorrect password. {password_attempts} attempts remaining.")

    print("Authentication failed. Returning to main menu.")
    return False


def display_products(products):
    for product in products:
        print(f"{product['name']} - {product['price']} - Quantity: {product['quantity']}")

def add_product(products):
    name = input("Enter the product name: ")

    # Check if the product with the same name already exists
    for product in products:
        if product['name'].lower() == name.lower():
            print(f"Product with the name '{name}' already exists. Cannot add duplicate products.")
            return

    price = float(input("Enter the product price: "))
    quantity = int(input("Enter the product quantity: "))

    products.append({'name': name, 'price': price, 'quantity': quantity})
    print(f"{name} added to the product list.")
    save_products(products)


def remove_product(products):
    name = input("Enter the product name to remove: ")
    products = [product for product in products if product['name'] != name]
    print(f"{name} removed from the product list.")

def update_product(products):
    name = input("Enter the product name to update: ")

    for product in products:
        if product['name'] == name:
            print(f"Current Details for {name}:")
            print(f"Price: {product['price']}, Quantity: {product['quantity']}")

            new_price = float(input("Enter the new price (press Enter to keep the current price): ").strip() or product['price'])
            new_quantity = int(input("Enter the new quantity (press Enter to keep the current quantity): ").strip() or product['quantity'])

            product['price'] = new_price
            product['quantity'] = new_quantity

            print(f"Details for {name} updated successfully.")
            save_products(products)
            return

    print(f"Product {name} not found.")


def buy_product(products):
    display_products(products)
    name = input("Enter the product name to buy: ")
    quantity = int(input("Enter the quantity to buy: "))
    for product in products:
        if product['name'] == name:
            if product['quantity'] >= quantity:
                product['quantity'] -= quantity
                cart.append({'name': name, 'price': product['price'], 'quantity': quantity})
                print(f"{quantity} {name} added to the cart.")
                return True
            else:
                print(f"Insufficient quantity of {name} in stock.")
                return False
    else:
        print(f"Product {name} not found.")
        return False

def process_payment(cart):
    total_cost = sum(float(item['price']) * item['quantity'] for item in cart)
    print(f"Total Cost: {total_cost}")
    payment_method = input("Enter payment method (Credit Card/PayPal): ")

    # Additional payment processing logic can be added here

    print("Payment successful! Thank you for your purchase.")
    return total_cost

def display_cart():
    print("Shopping Cart:")
    for item in cart:
        print(f"{item['name']} - {item['price']} - Quantity: {item['quantity']}")

# ... (previous code remains unchanged)

def sort_products(products, key, reverse=False):
    products.sort(key=lambda x: x[key], reverse=reverse)

# ... (previous code remains unchanged)

def clear_cart():
    cart.clear()
    print("Shopping cart cleared.")

def seller_operations(products):
    if authenticate_seller():
        while True:
            print("\nSeller Operations:")
            print("1. Add Product")
            print("2. Remove Product")
            print("3. update the product")
            print("4. Exit Seller Operations")

            seller_choice = input("Enter seller choice: ")

            if seller_choice == '1':
                add_product(products)
            elif seller_choice == '2':
                remove_product(products)
            elif seller_choice == '3':
                update_product(products)
                save_products(products)
            elif seller_choice == '4':
                save_products(products)
                print("Exiting Seller Operations. Returning to main menu.")
                break
            else:
                print("Invalid seller choice. Please try again.")
    else:
        print("Seller authentication failed.")

def main():
    products = load_products()

    while True:
        print("\n1. Display Products")
        print("2. Buy Product")
        print("3. Sort Products by Price (Expensive to Cheap)")
        print("4. Sort Products by Price (Cheap to Expensive)")
        print("5. Sort Products by Name (A-Z)")
        print("6. Sort Products by Name (Z-A)")
        print("7. Display Cart")
        print("8. Checkout and Pay")
        print("9. Clear Shopping Cart")
        print("10. Seller Operations")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_products(products)
        elif choice == '2':
            success = buy_product(products)
            if success:
                save_products(products)
        elif choice == '3':
            sort_products(products, 'price', reverse=True)
            display_products(products)
        elif choice == '4':
            sort_products(products, 'price')
            display_products(products)
        elif choice == '5':
            sort_products(products, 'name')
            display_products(products)
        elif choice == '6':
            sort_products(products, 'name', reverse=True)
            display_products(products)
        elif choice == '7':
            display_cart()
        elif choice == '8':
            if cart:
                total_cost = process_payment(cart)
                for item in cart:
                    for product in products:
                        if item['name'] == product['name']:
                            product['quantity'] -= item['quantity']
                cart.clear()
                print("Inventory updated after purchase.")
                save_products(products)
            else:
                print("The cart is empty. Please add items before checking out.")
        elif choice == '9':
            clear_cart()
        elif choice == '10':
            seller_operations(products)
        elif choice == '11':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
