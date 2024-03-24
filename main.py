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
import FeaturesDrivers as Features

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    fetcher = DataFetcher.DataFetcher()

    #fetcher.fetchCircuits()
  #  fetcher.fetchStatus()
   # fetcher.fetchConstructors()
    #fetcher.fetchDrivers()
#    fetcher.fetchSeasons()
 #   fetcher.fetchRaces()
  #  fetcher.fetchQualifying()
   # fetcher.fetchResults()
#    fetcher.fetchSprintResults()
  #  fetcher.fetchConstructorStandings()
  #  fetcher.fetchDriverStandings()
  #  fetcher.fetchLaptimes()
   # fetcher.fetchPitstops()

   # fetcher.fetchAll()

    features = Features.Features()
    test = features.get_driver_name(23)

    print(features.get_front_row_starts(802))
    print(test)

    # Beispielwerte für die Tests
    driver_id = 802
    race_id = 1100
    race_date = '2023-11-19'
    constructor_id = 167
    circuit_id = 70

    # Fahrer-Features testen
    print("Fahrer-Features:")
    print("Alter:", features.get_driver_age(driver_id, race_date))
    print("Jahre in der Formel 1:", features.get_driver_years_in_f1(driver_id, race_date))
    print("Qualifikationszeit-Differenz zur Pole-Position:",
          features.get_qualifying_time_diff_to_pole(race_id, driver_id))
    print("Starts aus der ersten Reihe:", features.get_front_row_starts(driver_id))
    print("Karrieresiege:", features.get_career_wins(driver_id))
    print("Saisonsiege:", features.get_season_wins(driver_id, race_id))
    print("Gestartete Rennen:", features.get_races_started(driver_id))
    print("Beendete Rennen:", features.get_races_finished(driver_id))
    print("Pole-Positionen:", features.get_pole_positions(driver_id))
    print("Gewonnene Fahrertitel:", features.get_driver_championships(driver_id))
    print("Fahrerwertung im letzten Jahr:", features.get_driver_standings_last_year(driver_id, race_id))
    print("Aktuelle Fahrerwertungsposition:", features.get_current_driver_standings(driver_id, race_id))
    print("Gewonnene/Verlorene Positionen in den letzten 5 Rennen:",
          features.get_positions_gained_lost_last_x_races(driver_id, race_id, 5))
    print("Endpositionen in den letzten 5 Rennen:",
          features.get_finishing_positions_last_x_races(driver_id, race_id, 5))
    print("Korrelation zwischen Qualifikations- und Rennergebnissen:",
          features.get_qualifying_race_correlation(driver_id))
    print("Ergebnis des vorherigen Rennens:", features.get_previous_race_result(driver_id, race_id))
    print("Ergebnis des Rennens im Vorjahr:", features.get_previous_year_race_result(driver_id, race_id))
    print("Zeitdifferenz zum Sieger im letzten Rennen:", features.get_time_diff_to_winner_last_race(driver_id, race_id))
    print("Anzahl der Boxenstopps im Rennen des Vorjahres:", features.get_prev_year_race_pit_stops(driver_id, race_id))
    print("Durchschnittliche Rundenzeit im letzten Rennen:", features.get_avg_lap_time_last_race(driver_id, race_id))
    print("Konsistenz der Rundenzeiten im letzten Rennen:",
          features.get_avg_lap_time_consistency_last_race(driver_id, race_id))
    print("Geschwindigkeitsstatistiken im letzten Rennen:", features.get_speed_stats_last_race(driver_id, race_id))
    print("Geschwindigkeitsrang im letzten Rennen:", features.get_speed_rank_last_race(driver_id, race_id))

    # Konstrukteur-Features testen
    print("\nKonstrukteur-Features:")
    print("Konstrukteur-Name:", features.get_constructor_name(constructor_id))
    print("Gewonnene Konstrukteurs-Meisterschaften:", features.get_constructor_championships_won(constructor_id))
    print("Gewonnene Konstrukteurs-Rennen:", features.get_constructor_race_wins(constructor_id))
    print("Saisonsiege des Konstrukteurs:", features.get_constructor_season_wins(constructor_id, race_id))
    print("Gewonnene Konstrukteurs-Meisterschaften in den letzten 5 Jahren:",
          features.get_constructor_championships_last_x_years(constructor_id, race_id, 5))
    print("Konstrukteurs-Meisterschaftsplatzierung im letzten Jahr:",
          features.get_constructor_standings_last_year(constructor_id, race_id))
    print("Aktuelle Position in der Konstrukteurs-Meisterschaft:",
          features.get_current_constructor_standings(constructor_id, race_id))
    print("Beste Qualifying-Position des Teamkollegen:",
          features.get_max_teammate_qualifying_position(constructor_id, driver_id, race_id))
    print("Gewonnene/Verlorene Positionen des Konstrukteurs in den letzten 5 Rennen:",
          features.get_constructor_positions_gained_lost_last_x_races(constructor_id, race_id, 5))
    print("Endpositionen des Konstrukteurs in den letzten 5 Rennen:",
          features.get_constructor_finishing_positions_last_x_races(constructor_id, race_id, 5))
    print("Geschwindigkeitsdifferenz des Konstrukteurs zum Schnellsten im letzten Rennen:",
          features.get_constructor_speed_diff_to_fastest_last_race(constructor_id, race_id))
    print("Anzahl der Ausfälle des Konstrukteurs:", features.get_constructor_retirements(constructor_id))
    print("Anzahl der Ausfälle des Konstrukteurs in den letzten 5 Rennen:",
          features.get_constructor_retirements_last_x_races(constructor_id, race_id, 5))
    print("Geschwindigkeitsstatistiken des Konstrukteurs im letzten Rennen:",
          features.get_constructor_speed_stats_last_race(constructor_id, race_id))
    print("Geschwindigkeitsrang des Konstrukteurs im letzten Rennen:",
          features.get_constructor_speed_rank_last_race(constructor_id, race_id))

    # Rennen-Features testen
    print("\nRennen-Features:")
    print("Streckenname:", features.get_circuit_name(circuit_id))
    print("Runde des Rennens:", features.get_race_round(race_id))
    print("Jahr des Rennens:", features.get_race_year(race_id))
    print("Durchschnittliche Überholmanöver pro Rennen auf der Strecke:",
          features.get_avg_overtakes_per_race(circuit_id))



