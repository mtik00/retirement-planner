import typer

from .calculations import calculate_scenario
from .report import display

app = typer.Typer()


@app.command()
def calculate(starting_balance: int, starting_age: int, starting_distribution: int):
    result = calculate_scenario(starting_balance, starting_age, starting_distribution)
    display(result)


if __name__ == "__main__":
    app()
