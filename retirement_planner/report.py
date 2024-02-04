#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import locale

from rich.console import Console
from rich.table import Table

from .calculations import Iteration, MonteCarloResult

locale.setlocale(locale.LC_ALL, "")


def display(iterations: list[Iteration]):
    table = Table()
    table.add_column("Age")
    table.add_column("Starting Balance")
    table.add_column("Crash")
    table.add_column("Fixed Income", style="green")
    table.add_column("Inflation", style="red")
    table.add_column("Withdrawl", style="red")
    table.add_column("Earnings", style="green")
    table.add_column("Ending Balance")

    for iteration in iterations:
        table.add_row(
            str(iteration.age),
            locale.currency(iteration.start_of_year_balance, grouping=True),
            f"{iteration.crash}%" if iteration.crash else "",
            locale.currency(iteration.fixed_income, grouping=True),
            str(iteration.inflation_rate) + "%",
            "-" + locale.currency(iteration.distributions, grouping=True),
            locale.currency(iteration.earnings, grouping=True),
            locale.currency(iteration.total_balance, grouping=True),
        )

    Console().print(table)


def display_monte_carlo(iterations: list[MonteCarloResult]):
    """NOTE: This could use a lot of work."""
    results = sorted(iterations, reverse=True)

    print(f"Results after {len(results):,} iterations.")
    print()

    table = Table()
    table.add_column("Scenario")
    table.add_column("Age")
    table.add_column("Ending Balance")
    table.add_column("# Crashes")
    table.add_column("Avg Yield")

    table.add_row(
        "Best Case",
        str(results[0].age),
        locale.currency(results[0].balance, grouping=True),
        str(results[0].num_crashes),
        str(round(results[0].average_yield, 2)),
    )
    table.add_row(
        "Worst Case",
        str(results[-1].age),
        locale.currency(results[-1].balance, grouping=True),
        str(results[-1].num_crashes),
        str(round(results[-1].average_yield, 2)),
    )

    Console().print(table)

    # We're really only interested in ages.
    ages = sorted([x.age for x in results])

    print()
    median_age = ages[int(len(ages) / 2)]
    print(f"Median age where money runs out: {median_age}")
    print()

    table = Table()
    table.add_column("Chance money runs out", justify="center")
    table.add_column("Age")

    for percentile in range(10, 96, 10):
        index = int((percentile / 100) * len(ages))
        bell = percentile if percentile < 50 else 100 - percentile
        if percentile == 50:
            table.add_row("---", "---")

        table.add_row(str(bell) + "%", str(ages[index]))

        if percentile == 50:
            table.add_row("---", "---")

    Console().print(table)
