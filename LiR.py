import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, precision_score, accuracy_score
from FeaturesDrivers import FeaturesDrivers
import numpy as np
import decimal
import matplotlib.pyplot as plt


# Daten vorbereiten
def prepare_data(races, last_race_id):
    features = FeaturesDrivers()
    data = []

    for race_id in races:
        if race_id == last_race_id:
            continue

        driver_ids = features.get_driver_id(race_id)
        for driver_id in driver_ids:
            row = [
                driver_id,
                features.get_driver_age(driver_id, race_id),
                features.get_driver_years_in_f1(driver_id, race_id),
                features.get_qualifying_time_diff_to_pole(race_id, driver_id),
                features.get_front_row_starts(driver_id),
                features.get_career_wins(driver_id),
                features.get_season_wins(driver_id, race_id),
                features.get_races_started(driver_id),
                features.get_races_finished(driver_id),
                features.get_pole_positions(driver_id),
                features.get_driver_championships(driver_id),
                features.get_driver_standings_last_year(driver_id, race_id),
                features.get_current_driver_standings(driver_id, race_id),
                features.get_qualifying_race_correlation(driver_id),
                features.get_time_diff_to_winner_last_race(driver_id, race_id),
                features.get_prev_year_race_pit_stops(driver_id, race_id),
                features.get_avg_lap_time_last_race(driver_id, race_id).total_seconds() if features.get_avg_lap_time_last_race(driver_id, race_id) else None,
                features.get_avg_lap_time_consistency_last_race(driver_id, race_id),
                features.get_speed_rank_last_race(driver_id, race_id),
                features.get_qualifying_position(driver_id, race_id),
                features.get_race_position(driver_id, race_id)
            ]
            data.append(row)

    df = pd.DataFrame(data, columns=[
        'DriverID', 'Age', 'YearsInF1', 'QualifyingTimeDiffToPole', 'FrontRowStarts',
        'CareerWins', 'SeasonWins', 'RacesStarted', 'RacesFinished', 'PolePositions',
        'DriverChampionships', 'LastYearStandings', 'CurrentStandings', 'QualifyingRaceCorrelation',
        'TimeDiffToWinnerLastRace', 'PrevYearRacePitStops', 'AvgLapTimeLastRace',
        'AvgLapTimeConsistencyLastRace', 'SpeedRankLastRace', 'QualifyingPosition', 'RacePosition'
    ])

    # Ersetze fehlende Werte nur in numerischen Spalten durch den Mittelwert
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

    # Ersetze fehlende Werte in nicht-numerischen Spalten durch den häufigsten Wert oder einen Standardwert
    non_numeric_columns = df.columns.difference(numeric_columns)
    for column in non_numeric_columns:
        if df[column].dtype == object:
            most_frequent_value = df[column].mode().iloc[0]
            if isinstance(most_frequent_value, tuple):
                most_frequent_value = most_frequent_value[0]  # Nimm den ersten Wert des Tupels
            df[column] = df[column].fillna(most_frequent_value)
        else:
            df[column] = df[column].fillna(0)  # Oder einen anderen Standardwert verwenden

    return df

# Modell trainieren und evaluieren
def train_and_evaluate_model(data):
    X = data.drop(['DriverID', 'RacePosition'], axis=1)
    y = data['RacePosition']

    # Daten in Trainings- und Testset aufteilen
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Hyperparameter-Optimierung
    model = Ridge()
    param_grid = {'alpha': [0.1, 1.0, 10.0]}
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_absolute_error')
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_

    # Bewertung des besten Modells auf dem Testset
    y_pred = best_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared: {r2:.2f}")
    # Berechne die Precision und Accuracy für Top-10, Top-5 und Top-3
    y_test_top10 = y_test.apply(lambda x: 1 if x <= 10 else 0)
    y_pred_top10 = pd.Series(y_pred).apply(lambda x: 1 if x <= 10 else 0)
    precision_top10 = precision_score(y_test_top10, y_pred_top10)
    accuracy_top10 = accuracy_score(y_test_top10, y_pred_top10)
    print(f"Precision for Top 10: {precision_top10:.2f}")
    print(f"Accuracy for Top 10: {accuracy_top10:.2f}")

    y_test_top5 = y_test.apply(lambda x: 1 if x <= 5 else 0)
    y_pred_top5 = pd.Series(y_pred).apply(lambda x: 1 if x <= 5 else 0)
    precision_top5 = precision_score(y_test_top5, y_pred_top5)
    accuracy_top5 = accuracy_score(y_test_top5, y_pred_top5)
    print(f"Precision for Top 5: {precision_top5:.2f}")
    print(f"Accuracy for Top 5: {accuracy_top5:.2f}")

    y_test_top3 = y_test.apply(lambda x: 1 if x <= 3 else 0)
    y_pred_top3 = pd.Series(y_pred).apply(lambda x: 1 if x <= 3 else 0)
    precision_top3 = precision_score(y_test_top3, y_pred_top3)
    accuracy_top3 = accuracy_score(y_test_top3, y_pred_top3)
    print(f"Precision for Top 3: {precision_top3:.2f}")
    print(f"Accuracy for Top 3: {accuracy_top3:.2f}")

    feature_importance = pd.DataFrame({'Feature': X.columns, 'Importance': best_model.coef_})
    feature_importance = feature_importance.sort_values('Importance', ascending=False)
    print("\nFeature Importance:")
    print(feature_importance)

    return best_model

# Vorhersage für das letzte Rennen
def predict_last_race(model, last_race_id):
    features = FeaturesDrivers()
    driver_ids = features.get_driver_id(last_race_id)
    data = []

    for driver_id in driver_ids:
        row = [
            driver_id,
            features.get_driver_age(driver_id, last_race_id),
            features.get_driver_years_in_f1(driver_id, last_race_id),
            features.get_qualifying_time_diff_to_pole(last_race_id, driver_id),
            features.get_front_row_starts(driver_id),
            features.get_career_wins(driver_id),
            features.get_season_wins(driver_id, last_race_id),
            features.get_races_started(driver_id),
            features.get_races_finished(driver_id),
            features.get_pole_positions(driver_id),
            features.get_driver_championships(driver_id),
            features.get_driver_standings_last_year(driver_id, last_race_id),
            features.get_current_driver_standings(driver_id, last_race_id),
            features.get_qualifying_race_correlation(driver_id),
            features.get_time_diff_to_winner_last_race(driver_id, last_race_id),
            features.get_prev_year_race_pit_stops(driver_id, last_race_id),
            features.get_avg_lap_time_last_race(driver_id, last_race_id).total_seconds() if features.get_avg_lap_time_last_race(driver_id, last_race_id) else None,
            features.get_avg_lap_time_consistency_last_race(driver_id, last_race_id),
            features.get_speed_rank_last_race(driver_id, last_race_id),
            features.get_qualifying_position(driver_id, last_race_id)
        ]
        data.append(row)

    df = pd.DataFrame(data, columns=[
        'DriverID', 'Age', 'YearsInF1', 'QualifyingTimeDiffToPole', 'FrontRowStarts',
        'CareerWins', 'SeasonWins', 'RacesStarted', 'RacesFinished', 'PolePositions',
        'DriverChampionships', 'LastYearStandings', 'CurrentStandings', 'QualifyingRaceCorrelation',
        'TimeDiffToWinnerLastRace', 'PrevYearRacePitStops', 'AvgLapTimeLastRace',
        'AvgLapTimeConsistencyLastRace', 'SpeedRankLastRace', 'QualifyingPosition'
    ])

    X_last_race = df.drop(['DriverID'], axis=1)

    # Konvertiere Timedelta-Werte in Sekunden, wenn sie nicht bereits als Gleitkommazahlen vorliegen
    timedelta_columns = ['AvgLapTimeLastRace', 'AvgLapTimeConsistencyLastRace', 'TimeDiffToWinnerLastRace']
    for column in timedelta_columns:
        if column in X_last_race.columns:
            X_last_race[column] = X_last_race[column].apply(lambda x: float(x.total_seconds()) if pd.notnull(x) and not isinstance(x, (float, decimal.Decimal)) else float(x) if pd.notnull(x) else x)

    # Ersetze fehlende Werte durch den Mittelwert
    X_last_race = X_last_race.fillna(X_last_race.mean())

    y_pred = model.predict(X_last_race)

    results = pd.DataFrame({
        'DriverID': df['DriverID'],
        'PredictedPosition': y_pred
    })

    # Get the actual race positions for each driver in the last race
    actual_positions = []
    for driver_id in results['DriverID']:
        actual_position = features.get_race_position(driver_id, last_race_id)
        actual_positions.append(actual_position)

    results['ActualPosition'] = actual_positions

    driver_names = results['DriverID'].apply(lambda x: features.get_driver_name(x))
    results['Driver'] = driver_names
    results = results.sort_values("ActualPosition")

    print("Predicted Last Race Results:")
    print(results[['Driver', 'PredictedPosition', 'ActualPosition']])

def plot_linear_regression(X_test, y_test, model):
    plt.figure(figsize=(12, 8))

    # Streudiagramm der tatsächlichen Werte
    plt.subplot(2, 2, 1)
    plt.scatter(range(len(y_test)), y_test, color='blue', label='Actual')
    plt.xlabel('Data Points')
    plt.ylabel('Race Position')
    plt.title('Actual Race Positions')
    plt.legend()

    # Streudiagramm der vorhergesagten Werte
    plt.subplot(2, 2, 2)
    plt.scatter(range(len(y_test)), model.predict(X_test), color='red', label='Predicted')
    plt.xlabel('Data Points')
    plt.ylabel('Race Position')
    plt.title('Predicted Race Positions')
    plt.legend()

    # Liniendiagramm der tatsächlichen und vorhergesagten Werte
    plt.subplot(2, 2, 3)
    plt.plot(range(len(y_test)), y_test, color='blue', label='Actual')
    plt.plot(range(len(y_test)), model.predict(X_test), color='red', label='Predicted')
    plt.xlabel('Data Points')
    plt.ylabel('Race Position')
    plt.title('Actual vs Predicted Race Positions')
    plt.legend()

    # Streudiagramm der tatsächlichen gegen die vorhergesagten Werte
    plt.subplot(2, 2, 4)
    plt.scatter(y_test, model.predict(X_test), color='green')
    plt.xlabel('Actual Race Position')
    plt.ylabel('Predicted Race Position')
    plt.title('Actual vs Predicted Race Positions')

    plt.tight_layout()
    plt.show()
# Hauptprogramm
def main():
    # Liste der Rennen der Saison 2023 (angenommene Werte)
    races = [1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075,
             1076, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094,
             1095, 1096, 1097, 1098, 1099, 1099, 1100,1101]
    last_race_id = 1101

    # Daten vorbereiten
    data = prepare_data(races, last_race_id)

    # Modell trainieren und evaluieren
    X = data.drop(['DriverID', 'RacePosition'], axis=1)
    y = data['RacePosition']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_and_evaluate_model(data)

    # Graph mit den Datenpunkten und der linearen Regression erstellen
    plot_linear_regression(X_test, y_test, model)

    # Vorhersage für das letzte Rennen
    predict_last_race(model, last_race_id)


if __name__ == '__main__':
    main()