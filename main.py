import csv
from datetime import date
import os
import statistics as stats

cash_register = dict()


def print_header(header):
    print()
    print(header)
    print("=" * len(header))


def read_required_string(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("[ERR] Value is required.")


def read_int(prompt, min, max):
    while True:
        value = read_required_string(prompt)
        if value.isdigit():
            value = int(value)
            if min <= value <= max:
                return value
        print(f"[ERR] Value must be between {min} and {max}.")


def read_positive_float(prompt):
    while True:
        value = read_required_string(prompt)
        try:
            value = float(value)
            if value > 0:
                return value
        except ValueError:
            pass
        print("[ERR] Value must be a positive number.")


def choose_menu():
    print_header("Vending Machine")
    print("1. Insert Money")
    print("2. Show Items")
    print("3. Select Item")
    print("4. Cancel and Refund")

    return read_int("Select [0-4]: ", 0, 4)


# Accepted coins/bills
accepted_denominations = [0.01, 0.05, 0.10, 0.25, 1, 5]

# Initialize cash register with counts of each denomination
cash_register = {denom: 0 for denom in accepted_denominations}


def insert_money():
    while True:
        amount = read_positive_float("Insert amount: $")
        if amount in accepted_denominations:
            cash_register[amount] += 1
            total_balance = sum(denom * count for denom,
                                count in cash_register.items())
            print(f"[INFO] Current balance: ${total_balance:.2f}")
            break
        else:
            print(
                f"[ERR] Invalid denomination. Accepted: {accepted_denominations}")


def show_items():
    print_header("Available Items")
    for code, item in items.items():
        status = "In Stock" if item["inventory"] > 0 else "Out of Stock"
        print(f"{code}: {item['name']} - ${item['price']:.2f} ({status})")


def select_item():
    code = read_required_string("Enter item code: ").upper()
    if code in items:
        item = items[code]
        if item["inventory"] > 0:
            if cash_register.get("balance", 0) >= item["price"]:
                item["inventory"] -= 1
                cash_register["balance"] -= item["price"]
                print(
                    f"[INFO] Dispensing {item['name']}. Remaining balance: ${cash_register['balance']:.2f}")
                producer.send("inventory", value={code: item})
                producer.send("shipping", value={
                              "name": item["name"], "status": "Preparing"})
            else:
                print("[ERR] Insufficient balance.")
        else:
            print("[ERR] Item out of stock.")
    else:
        print("[ERR] Invalid item code.")


def cancel_and_refund():
    refund = cash_register.get("balance", 0)
    if refund > 0:
        print(f"[INFO] Refunding ${refund:.2f}")
        cash_register["balance"] = 0
    else:
        print("[INFO] No balance to refund.")


def main():
    choice = choose_menu()
    while choice != 0:
        if choice == 1:
            insert_money()
        elif choice == 2:
            show_items()
        elif choice == 3:
            select_item()
        elif choice == 4:
            cancel_and_refund()
        choice = choose_menu()

    print_header("Goodbye")


if __name__ == "__main__":
    main()
