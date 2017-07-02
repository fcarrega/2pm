import sys
import click

@click.command()
def help():
    with open("2pm/help.txt") as f:
        for line in f:
                print(line, end = '')
