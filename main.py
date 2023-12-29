# This is a sample Python script.
import psycopg
import pyergast as pyergast
import urllib.request, json
import urllib.request
import json
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import DataFetcher as DataFetcher
import DatabaseConnection
import pandas as pd


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    fetcher = DataFetcher.DataFetcher()

  #  fetcher.fetchCircuits()
   # fetcher.fetchStatus()
    #fetcher.fetchConstructors()
 #   fetcher.fetchDrivers()
   # fetcher.fetchSeasons()
   # fetcher.fetchRaces()

   # fetcher.fetchQualifying()
    fetcher.fetchResults()
