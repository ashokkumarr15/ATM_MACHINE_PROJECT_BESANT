Source code

import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="atm_db"
)
cursor = db.cursor()

# Function to check account balance
def check_balance(account_number, pin):
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s AND pin = %s", (account_number, pin))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

# Function to deposit money
def deposit(account_number, amount):
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (amount, account_number))
    db.commit()

# Function to withdraw money
def withdraw(account_number, pin, amount):
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s AND pin = %s", (account_number, pin))
    result = cursor.fetchone()
    if result and result[0] >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_number = %s", (amount, account_number))
        db.commit()
        return True
    else:
        return False

# Function to add a new account
def add_account(account_number, account_holder, pin, initial_balance):
    cursor.execute("INSERT INTO accounts (account_number, account_holder, pin, balance) VALUES (%s, %s, %s, %s)",
                   (account_number, account_holder, pin, initial_balance))
    db.commit()

# Main ATM loop
while True:
    print("\nATM Menu:")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        account_number = int(input("Enter your account number: "))
        pin = int(input("Enter your PIN: "))
        balance = check_balance(account_number, pin)
        if balance is not None:
            print(f"Your balance is ${balance:.2f}")
        else:
            print("Invalid account number or PIN.")

    elif choice == "2":
        account_number = int(input("Enter your account number: "))
        amount = float(input("Enter the amount to deposit: "))
        deposit(account_number, amount)
        print(f"${amount:.2f} deposited successfully.")

    elif choice == "3":
        account_number = int(input("Enter your account number: "))
        pin = int(input("Enter your PIN: "))
        amount = float(input("Enter the amount to withdraw: "))
        if withdraw(account_number, pin, amount):
            print(f"${amount:.2f} withdrawn successfully.")
        else:
            print("Insufficient funds or invalid account number/PIN.")

    elif choice == "4":
        break

    else:
        print("Invalid choice. Please try again.")

# Close the database connection
db.close()
