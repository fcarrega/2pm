import sys
import click

@click.command()
def help():
    with open('doc/help.txt') as f:
        for line in f:
            print(line, end = '')
