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
    55: 10000,  # Spouse will continue to work
    59: 20000,  # Pension
    67: 50000,  # Pension plus Social Security
}

ANNUAL_YIELD = {
    55: 0.07,
    65: 0.06,
    75: 0.05,
    85: 0.03,
}


def get_previous(value, lookup: dict):
    """Search a dictionary for a value < the key."""
    keys = sorted(lookup.keys())

    for index, key in enumerate(keys[1:]):
        if value < key:
            return lookup[keys[index]]
    else:
        return lookup[keys[-1]]


def calculate_scenario(
    starting_balance: int,
    starting_age: int,
    starting_distribution,
    max_number_of_years=100,
):
    """
    The annual calculation is:
        start - (distribution * inflation) - distributions + yield + fixed income.

    The numbers are basic annual calculations with the most pessimistic view.  All
    deductions are taken at the start of the year, earnings are then calculated from
    that amount, then fixed income is added to the total.
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
            "earnings",
            "ending balance",
        )
    )

    for age in range(starting_age, starting_age + max_number_of_years):
        starting_balance = total_balance
        inflation = get_previous(age, INFLATION)
        fixed_income = get_previous(age, FIXED_INCOME)
        yield_rate = get_previous(age, ANNUAL_YIELD)

        # Increase annual distribution amount based on inflation
        distributions = distributions * (1 + inflation)

        # Calculate the yield as if all distributions were taken on day 1 and
        # before fixed income (most pessimistic view).
        left_overs = starting_balance - distributions
        earnings = yield_rate * left_overs

        # Add everything together
        total_balance = left_overs + fixed_income + earnings

        print(
            row.format(
                str(age),
                locale.currency(starting_balance, grouping=True),
                locale.currency(fixed_income, grouping=True),
                locale.currency(distributions, grouping=True),
                locale.currency(earnings, grouping=True),
                locale.currency(total_balance, grouping=True),
            )
        )

        if total_balance < 0:
            print(f"You're broke at {age}")
            break


def main():
    calculate_scenario(
        starting_balance=1_000_000,
        starting_age=60,
        starting_distribution=100_000,
        max_number_of_years=100,
    )


if __name__ == "__main__":
    main()
