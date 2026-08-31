import csv
import json
import os
from datetime import datetime

CSV_FILE = "expenses.csv"
JSON_FILE = "expenses.json"


# Load expenses from JSON file
def load_expenses():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []


# Save expenses to JSON file
def save_to_json(expenses):
    with open(JSON_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


# Save expense to CSV file
def save_to_csv(expense):
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["Date", "Category", "Amount", "Description"]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(expense)


# Add a new expense
def add_expense(expenses):
    print("\n--- Add Expense ---")

    category = input("Enter category: ").strip()

    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                break
        except ValueError:
            print("Please enter a valid amount.")

    description = input("Enter description: ").strip()

    date = datetime.now().strftime("%Y-%m-%d")

    expense = {
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Description": description
    }

    expenses.append(expense)

    save_to_json(expenses)
    save_to_csv(expense)

    print("\nExpense added successfully!")


# View all expenses
def view_expenses(expenses):
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses found.")
        return

    print("-" * 70)
    print(f"{'Date':<15}{'Category':<15}{'Amount':<15}{'Description'}")
    print("-" * 70)

    for expense in expenses:
        print(
            f"{expense['Date']:<15}"
            f"{expense['Category']:<15}"
            f"₹{float(expense['Amount']):<14.2f}"
            f"{expense['Description']}"
        )

    print("-" * 70)


# Calculate total expenses
def show_total(expenses):
    print("\n--- Total Expenses ---")

    if not expenses:
        print("No expenses found.")
        return

    total = sum(float(expense["Amount"]) for expense in expenses)

    print(f"Total amount spent: ₹{total:.2f}")


# Search expenses by category
def search_by_category(expenses):
    print("\n--- Search by Category ---")

    category = input("Enter category: ").strip().lower()

    results = [
        expense
        for expense in expenses
        if expense["Category"].lower() == category
    ]

    if not results:
        print("No expenses found for this category.")
        return

    print("-" * 70)

    for expense in results:
        print(
            f"Date: {expense['Date']} | "
            f"Category: {expense['Category']} | "
            f"Amount: ₹{float(expense['Amount']):.2f} | "
            f"Description: {expense['Description']}"
        )

    print("-" * 70)


# Delete all expenses
def clear_expenses():
    confirmation = input(
        "\nAre you sure you want to delete all expenses? (yes/no): "
    ).lower()

    if confirmation == "yes":
        if os.path.exists(JSON_FILE):
            os.remove(JSON_FILE)

        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)

        print("All expenses deleted successfully!")
    else:
        print("Operation cancelled.")


# Main program
def main():
    expenses = load_expenses()

    while True:
        print("\n================================")
        print("       EXPENSE TRACKER")
        print("================================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Total Expenses")
        print("4. Search by Category")
        print("5. Clear All Expenses")
        print("6. Exit")
        print("================================")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            show_total(expenses)

        elif choice == "4":
            search_by_category(expenses)

        elif choice == "5":
            clear_expenses()
            expenses = []

        elif choice == "6":
            print("\nThank you for using Expense Tracker!")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
