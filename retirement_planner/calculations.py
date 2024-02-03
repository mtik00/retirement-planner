#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass


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


@dataclass
class Iteration:
    age: int
    start_of_year_balance: float
    fixed_income: float
    distributions: float
    earnings: float
    total_balance: float


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
    inflation_table: dict[int, float] = INFLATION,
    fixed_income_table: dict[int, int] = FIXED_INCOME,
    yield_table: dict[int, float] = ANNUAL_YIELD,
) -> list[Iteration]:
    """
    The annual calculation is:
        start - (distribution * inflation) - distributions + yield + fixed income.

    The numbers are basic annual calculations with the most pessimistic view.  All
    deductions are taken at the start of the year, earnings are then calculated from
    that amount, then fixed income is added to the total.
    """
    result = []
    total_balance = starting_balance
    distributions = starting_distribution

    for age in range(starting_age, starting_age + max_number_of_years):
        start_of_year_balance = total_balance
        inflation = get_previous(age, inflation_table)
        fixed_income = get_previous(age, fixed_income_table)
        yield_rate = get_previous(age, yield_table)

        # Increase annual distribution amount based on inflation
        distributions = distributions * (1 + inflation)

        # Calculate the yield as if all distributions were taken on day 1 and
        # before fixed income (most pessimistic view).
        left_overs = total_balance - distributions
        earnings = yield_rate * left_overs

        # Add everything together
        total_balance = left_overs + fixed_income + earnings

        result.append(
            Iteration(
                age,
                start_of_year_balance,
                fixed_income,
                distributions,
                earnings,
                total_balance,
            )
        )

        if total_balance < 0:
            break

    return result


def main():
    calculate_scenario(
        starting_balance=10_000_000,
        starting_age=60,
        starting_distribution=100_000,
        max_number_of_years=100,
    )


if __name__ == "__main__":
    main()
