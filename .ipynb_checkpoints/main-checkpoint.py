# This is a sample Python script.
import psycopg
import pyergast as pyergast

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import DataFetcher
import DatabaseConnection
import pandas as pd


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    print(pyergast.query_driver("raikkonen"))
    pyergast.get_drivers()
    pyergast.get_race_result()
    pyergast.get_schedule()

