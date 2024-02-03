import typer

from .calculations import calculate_scenario, monte_carlo
from .report import display, display_monte_carlo

app = typer.Typer()


@app.command()
def calculate(starting_balance: int, starting_age: int, starting_distribution: int):
    result = calculate_scenario(starting_balance, starting_age, starting_distribution)
    display(result)


@app.command()
def monte(starting_balance: int, starting_age: int, starting_distribution: int):
    result = monte_carlo(
        starting_balance, starting_age, starting_distribution, count=10_000
    )
    display_monte_carlo(result)


if __name__ == "__main__":
    app()
