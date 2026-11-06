import math


def parse_application(text):
    if not isinstance(text, str):
        return "", 0

    parts = text.split(':')
    if len(parts) != 2:
        return "", 0

    visa, entries = parts

    try:
        entries = int(entries.strip())
    except (ValueError, TypeError):
        return "", 0

    if not visa.strip():
        return "", 0

    return visa.strip().title(), entries


def processing_average(days_csv):
    if not isinstance(days_csv, str) or not days_csv.strip():
        return 0

    try:
        values = [int(r.strip()) for r in days_csv.split(',')]
    except (ValueError, TypeError):
        return 0

    if not values:
        return 0

    return sum(values) // len(values)


def payable_fee(text):
    if not isinstance(text, str):
        return 0.0

    parts = text.split('|')
    if len(parts) != 2:
        return 0.0

    fee, discount = parts

    try:
        fee = float(fee.strip())
        discount = float(discount.strip())
    except (ValueError, TypeError):
        return 0.0

    if not math.isfinite(fee) or not math.isfinite(discount):
        return 0.0

    if fee < 0 or discount < 0:
        return 0.0

    total = fee * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    result = parse_application(user_input)
    print("Visa Type and Entries:", result)

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    result = processing_average(user_input)
    print("Average Processing Days:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()