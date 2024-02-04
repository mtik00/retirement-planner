#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from secrets import SystemRandom

random = SystemRandom()

INFLATION_RATE = {
    1: 3.0,
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

ANNUAL_YIELD_RATE = {
    55: 7.0,
    65: 6.0,
    75: 5.0,
    85: 4.0,
}


@dataclass
class Iteration:
    age: int
    start_of_year_balance: float
    fixed_income: float
    distributions: float
    earnings: float
    total_balance: float
    yield_rate: float
    inflation_rate: float
    crash: float


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
    inflation_table: dict[int, float] = INFLATION_RATE,
    fixed_income_table: dict[int, int] = FIXED_INCOME,
    yield_table: dict[int, float] = ANNUAL_YIELD_RATE,
    crash_rate: float = 5.0,
    crash_adjustment_rate: float = 30.0,
) -> list[Iteration]:
    """
    The annual calculation is:
        start - (distribution * inflation) + yield + fixed income.

    The numbers are basic annual calculations with the most pessimistic view.  All
    deductions are taken at the start of the year, earnings are then calculated from
    that amount, then fixed income is added to the total.

    If a market crash were to happen, it would be applied to your balance at the
    start of the calculation.
    """
    result = []
    total_balance = starting_balance
    distributions = starting_distribution

    for age in range(starting_age, starting_age + max_number_of_years):
        crash = 0.0
        if random.random() <= crash_rate / 100.0:
            # print("Crash at age:", age, "of", f"{crash_adjustment_rate:.1f}%")
            total_balance = int((1 - crash_adjustment_rate / 100) * total_balance)
            crash = crash_adjustment_rate

        start_of_year_balance = total_balance

        inflation_rate = get_previous(age, inflation_table)
        fixed_income = get_previous(age, fixed_income_table)
        yield_rate = get_previous(age, yield_table)

        # Increase annual distribution amount based on inflation
        distributions = distributions * (1 + inflation_rate / 100)

        # Calculate the yield as if all distributions were taken on day 1 and
        # before fixed income (most pessimistic view).
        left_overs = total_balance - distributions
        earnings = (yield_rate / 100) * left_overs

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
                yield_rate=yield_rate,
                inflation_rate=inflation_rate,
                crash=crash,
            )
        )

        if total_balance < 0:
            break

    return result


@dataclass
class MonteCarloResult:
    age: int
    inflation: float
    average_yield: float
    balance: float
    num_crashes: int

    def __eq__(self, other) -> bool:
        return (self.age, self.balance) == (other.age, other.balance)

    def __lt__(self, other) -> bool:
        return (self.age, self.balance) < (other.age, other.balance)


def monte_carlo(
    starting_balance: int,
    starting_age: int,
    starting_distribution,
    max_number_of_years=100,
    fixed_income_table: dict[int, int] = FIXED_INCOME,
    count: int = 10,
    inflation_range: tuple[float, float] = (-0.05, 5),
    yield_range: tuple[float, float] = (-2.0, 8),
) -> list[MonteCarloResult]:
    result: list[MonteCarloResult] = []

    for _ in range(count):
        # adjust inflation
        inflation = random.uniform(*inflation_range)
        inflation_table = {1: inflation}

        # adjust yield
        yield_rate = random.uniform(*yield_range)
        yield_table = {1: yield_rate}

        sim_result = calculate_scenario(
            starting_balance,
            starting_age,
            starting_distribution,
            max_number_of_years,
            inflation_table,
            fixed_income_table,
            yield_table,
        )

        result.append(
            MonteCarloResult(
                age=sim_result[-1].age,
                inflation=inflation,
                average_yield=sum(yield_table.values()) / len(yield_table),
                balance=sim_result[-1].total_balance,
                num_crashes=sum([1 if x.crash else 0 for x in sim_result]),
            )
        )

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
