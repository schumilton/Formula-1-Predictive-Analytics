from FeaturesDrivers import FeaturesDrivers

# Erstelle eine Instanz der FeaturesDrivers-Klasse
features = FeaturesDrivers()

# Beispielwerte für driver_id und race_id
driver_id = 456
race_id = 1100

# Teste verschiedene Funktionen
driver_name = features.get_driver_name(driver_id)
print(f"Fahrername: {driver_name}")

driver_age = features.get_driver_age(driver_id, race_id)
print(f"Alter des Fahrers: {driver_age}")

years_in_f1 = features.get_driver_years_in_f1(driver_id, race_id)
print(f"Jahre in der Formel 1: {years_in_f1}")

qualifying_time_diff = features.get_qualifying_time_diff_to_pole(race_id, driver_id)
print(f"Zeitdifferenz zum Pole-Setter im Qualifying: {qualifying_time_diff}%")

front_row_starts = features.get_front_row_starts(driver_id)
print(f"Starts aus der ersten Reihe: {front_row_starts}")

career_wins = features.get_career_wins(driver_id)
print(f"Karrieresiege: {career_wins}")

season_wins = features.get_season_wins(driver_id, race_id)
print(f"Saisonsiege: {season_wins}")

races_started = features.get_races_started(driver_id)
print(f"Gestartete Rennen: {races_started}")

races_finished = features.get_races_finished(driver_id)
print(f"Beendete Rennen: {races_finished}")

pole_positions = features.get_pole_positions(driver_id)
print(f"Pole-Positionen: {pole_positions}")

driver_championships = features.get_driver_championships(driver_id)
print(f"Gewonnene Meisterschaften: {driver_championships}")

last_year_position = features.get_driver_standings_last_year(driver_id, race_id)
print(f"Position in der letzten Saison: {last_year_position}")

current_position = features.get_current_driver_standings(driver_id, race_id)
print(f"Aktuelle Position: {current_position}")

max_positions_gained, max_positions_lost, avg_positions_gained_lost = features.get_positions_gained_lost_last_x_races(driver_id, race_id, 5)
print(f"Maximale Positionen gewonnen (in den letzten 5 Rennen): {max_positions_gained}")
print(f"Maximale Positionen verloren (in den letzten 5 Rennen): {max_positions_lost}")
print(f"Durchschnittliche Positionsveränderung (in den letzten 5 Rennen): {avg_positions_gained_lost}")

best_finish, worst_finish, avg_finish = features.get_finishing_positions_last_x_races(driver_id, race_id, 5)
print(f"Beste Platzierung (in den letzten 5 Rennen): {best_finish}")
print(f"Schlechteste Platzierung (in den letzten 5 Rennen): {worst_finish}")
print(f"Durchschnittliche Platzierung (in den letzten 5 Rennen): {avg_finish}")

qualifying_race_correlation = features.get_qualifying_race_correlation(driver_id)
print(f"Korrelation zwischen Qualifying- und Rennposition: {qualifying_race_correlation}")

prev_race_position, prev_race_qualifying_position, prev_race_positions_gained = features.get_previous_race_result(driver_id, race_id)
print(f"Position im letzten Rennen: {prev_race_position}")
print(f"Qualifying-Position im letzten Rennen: {prev_race_qualifying_position}")
print(f"Gewonnene Positionen im letzten Rennen: {prev_race_positions_gained}")

prev_year_race_position, prev_year_qualifying_position, prev_year_positions_gained = features.get_previous_year_race_result(driver_id, race_id)
print(f"Position im Vorjahresrennen: {prev_year_race_position}")
print(f"Qualifying-Position im Vorjahresrennen: {prev_year_qualifying_position}")
print(f"Gewonnene Positionen im Vorjahresrennen: {prev_year_positions_gained}")

time_diff_to_winner = features.get_time_diff_to_winner_last_race(driver_id, race_id)
print(f"Zeitdifferenz zum Sieger im letzten Rennen: {time_diff_to_winner}%")

prev_year_race_pit_stops = features.get_prev_year_race_pit_stops(driver_id, race_id)
print(f"Boxenstopps im Vorjahresrennen: {prev_year_race_pit_stops}")

avg_lap_time_last_race = features.get_avg_lap_time_last_race(driver_id, race_id)
print(f"Durchschnittliche Rundenzeit im letzten Rennen: {avg_lap_time_last_race}")

lap_time_consistency = features.get_avg_lap_time_consistency_last_race(driver_id, race_id)
print(f"Rundenzeitkonsistenz im letzten Rennen: {lap_time_consistency}")



speed_rank = features.get_speed_rank_last_race(driver_id, race_id)
print(f"Geschwindigkeitsrang im letzten Rennen: {speed_rank}")

qualifying_position = features.get_qualifying_position(driver_id, race_id)
print(f"Qualifying-Position: {qualifying_position}")

race_position = features.get_race_position(driver_id, race_id)
print(f"Rennposition: {race_position}")