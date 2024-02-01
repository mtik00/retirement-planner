#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import locale


locale.setlocale(locale.LC_ALL, "")

INFLATION = {
    1: 0.03,
    # 55: 0.04,
    # 59: 0.04,
    # 67: 0.04,
    # 80: 0.04,
    # 90: 0.04,
}

FIXED_INCOME = {
    1: 0,
    55: 10000,  # NTSOC
    59: 20000,  # PERA
    67: 60000,  # PERA + SS
}

ANNUAL_YIELD = {
    55: 0.08,
    65: 0.08,
    75: 0.06,
    85: 0.03,
}


def get_closest(value, lookup: dict):
    keys = sorted(lookup.keys())

    for index, key in enumerate(keys[1:]):
        if value < key:
            return lookup[keys[index]]
    else:
        return lookup[keys[-1]]


def create_table(
    starting_balance: int, starting_age: int, starting_distribution, number_of_years=100
):
    """
    The annual calculation is:
        start + (distribution * inflation) - distributions + yield + fixed income.
    """
    total_balance = starting_balance
    distributions = starting_distribution

    row = "{:5s} {:20s} {:20s} {:20s} {:20s} {:20s}"
    print(
        row.format(
            "age",
            "starting balance",
            "fixed income",
            "withdrawal",
            "yield",
            "ending balance",
        )
    )

    for age in range(starting_age, starting_age + number_of_years):
        starting_balance = total_balance
        inflation = get_closest(age, INFLATION)
        fixed_income = get_closest(age, FIXED_INCOME)
        yield_rate = get_closest(age, ANNUAL_YIELD)
        yield_ = yield_rate * (total_balance - (distributions - fixed_income))
        distributions = distributions * (1 + inflation)

        total_balance = total_balance - distributions + fixed_income + yield_

        print(
            row.format(
                str(age),
                locale.currency(starting_balance, grouping=True),
                locale.currency(fixed_income, grouping=True),
                locale.currency(distributions, grouping=True),
                locale.currency(yield_, grouping=True),
                locale.currency(total_balance, grouping=True),
            )
        )

        if total_balance < 0:
            print(f"You're broke at {age}")
            break


def main():
    create_table(2_500_000, 52, 100_000, number_of_years=100)


if __name__ == "__main__":
    main()
