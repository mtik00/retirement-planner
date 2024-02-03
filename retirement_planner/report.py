#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import locale

from .calculations import Iteration, MonteCarloResult

locale.setlocale(locale.LC_ALL, "")


def display(iterations: list[Iteration]):
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

    for iteration in iterations:
        print(
            row.format(
                str(iteration.age),
                locale.currency(iteration.start_of_year_balance, grouping=True),
                locale.currency(iteration.fixed_income, grouping=True),
                locale.currency(iteration.distributions, grouping=True),
                locale.currency(iteration.earnings, grouping=True),
                locale.currency(iteration.total_balance, grouping=True),
            )
        )


def display_monte_carlo(iterations: list[MonteCarloResult]):
    """NOTE: This could use a lot of work."""
    results = sorted(iterations, reverse=True)

    print(results[0])
    print(results[-1])

    # We're only interest in ages.  There will be lots of duplicates, which don't
    # really matter for reporting purposes.  Ditch the duplicates and make
    # assumptions based on that.
    ages = sorted(list(set([x.age for x in results])))

    average_age = int(sum(ages) / len(ages))
    print(f"Average age where money runs out: {average_age}")

    median_age = list(ages)[int(len(ages) / 2)]
    print(f"Median age where money runs out: {median_age}")

    for percentile in range(75, 96, 5):
        index = int((percentile / 100) * len(ages))
        print(
            f"{percentile}th percentile age where money runs out after: {ages[index]}"
        )
