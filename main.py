import csv
from datetime import date
import os
import statistics as stats
from decimal import ROUND_HALF_UP, Decimal

from consumer import run_consumer
from producer import run_producer
from adjust_count import adjust_count, zero_all_currency


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


def read_currency(prompt):
    while True:
        value = read_required_string(prompt)
        try:
            dollar = value.split(".")[0]
            cent = value.split(".")[1]
            if int(dollar) > 0 or int(cent) > 0:
                return (int(dollar), int(cent))
        except ValueError:
            pass
        print("[ERR] Value must be a positive number.")


def get_total():
    bank = run_consumer("bank")

    coins = bank['bank']
    running_total = 0.0
    for coin, count in coins.items():
        running_total += float(coin) * count

    run_producer("bank", bank)

    return running_total


def insert_money(amount):
    dollars = amount[0]
    cents = amount[1]
    bank = run_consumer("bank")

    # Process dollar amount
    dollar_denominations = [5, 1]
    for bill in dollar_denominations:
        if dollars >= bill:
            count = dollars // bill
            dollars = dollars % bill
            bank['bank'][str(bill)] += count
            # print(
            #     f"  Added {count} * ${bill} bills, ${dollars} dollars remaining")

    # Process cents second
    coin_denominations = [(25, '0.25'), (10, '0.10'), (5, '0.05'), (1, '0.01')]
    for cent_val, denom_key in coin_denominations:
        if cents >= cent_val:
            count = cents // cent_val
            cents = cents % cent_val
            bank['bank'][denom_key] += count
            # print(f"  Added {count} * {cent_val}¢ coins, {cents}¢ remaining")

    run_producer('bank', bank)

    total = sum(Decimal(amount_str) * count
                for amount_str, count in bank['bank'].items())
    print(f"New bank total: ${total}")


def show_items():
    print_header("Items")

    items = run_consumer("inventory")

    for code, item in items.items():
        status = "In Stock" if item["inventory"] > 0 else "Out of Stock"
        print(
            f"{code}: {item['name']} - ${item['price']:.2f} Count: {item['inventory']} ({status})")

    run_producer("inventory", items)


def cancel_and_refund():
    print_header("Refunding inserted money")

    # Get total function
    print(f"Amount refunded: ${get_total():.2f}")

    # run adjust count function, set all money to 0 in bank
    zero_all_currency()


def set_total(total):
    zero_all_currency()
    insert_money(total)


def select_item():
    selection = read_required_string("Enter item code: ").upper()

    items = run_consumer("inventory")
    if selection not in items:
        print("Item does not exist")
        run_producer("inventory", items)
        return

    if items[selection]["inventory"] <= 0:
        print("Item is out of stock")
        run_producer("inventory", items)
        return

    bank_amount = get_total()

    if bank_amount < items[selection]["price"]:
        print("Don't have enough money for item. insert more")
        run_producer("inventory", items)
        return

    items[selection]["inventory"] -= 1
    new_amount = str((Decimal(bank_amount) - Decimal(items[selection]["price"]))
                     .quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)).split(".")

    # split into dollars cents
    set_total((int(new_amount[0]), int(new_amount[1])))
    run_producer("inventory", items)


def start_vending_machine():
    items = {
        'A1': {'name': 'Nerds Gummy Clusters', 'price': 3.95, 'inventory': 10},
        'B2': {'name': 'Dove Dark Chocolate', 'price': 5.75, 'inventory': 5},
        'C3': {'name': 'Quest Protein Chips', 'price': 4.50, 'inventory': 0}
    }
    run_producer("inventory", items)
    bank = {
        'bank': {       # Mimicing structure of items for code reuse in producer.py
            "0.01": 0,
            "0.05": 0,
            "0.10": 0,
            "0.25": 0,
            "1": 0,
            "5": 0
        }}
    run_producer("bank", bank)


def choose_menu():
    print_header("Vending Machine")
    print("1. Insert Money")
    print("2. Show Items")
    print("3. Select Item")
    print("4. Cancel and Refund")

    return read_int("Select [0-4]: ", 0, 4)


def main():

    start_vending_machine()

    choice = choose_menu()
    while choice != 0:
        if choice == 1:
            insert_money(read_currency("Insert amount: $"))
        elif choice == 2:
            show_items()
        elif choice == 3:
            select_item()
        elif choice == 4:
            cancel_and_refund()
        choice = choose_menu()

    print_header("Thank you for shopping with us!")


if __name__ == "__main__":
    main()
