#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import locale

from .calculations import Iteration

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
