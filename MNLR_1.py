import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_score, mean_absolute_error
from FeaturesDrivers import FeaturesDrivers
import numpy as np
import decimal
from sklearn.metrics import confusion_matrix
import seaborn as sns
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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=100000000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Konfusionsmatrix berechnen
    cm = confusion_matrix(y_test, y_pred)

    # Konfusionsmatrix visualisieren
    plt.figure(figsize=(10, 10))
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='d', square=True, xticklabels=range(1, len(cm) + 1),
                yticklabels=range(1, len(cm) + 1))
    plt.xlabel('Predicted Position')
    plt.ylabel('Actual Position')
    plt.title('Confusion Matrix')
    plt.show()
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")
    mae = mean_absolute_error(y_test, y_pred)

    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(classification_report(y_test, y_pred, zero_division=1))

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

    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.coef_[0]
    })
    feature_importance['Absolute Importance'] = abs(feature_importance['Importance'])
    feature_importance = feature_importance.sort_values(by='Absolute Importance', ascending=False)

    print("Feature Importance:")
    print(feature_importance)
    return model

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

    y_pred_proba = model.predict_proba(X_last_race)

    results = pd.DataFrame({
        'DriverID': df['DriverID'],
        'Probability': y_pred_proba.max(axis=1)
    })
    results['PredictedPosition'] = results['Probability'].rank(method='dense', ascending=False).astype(int)

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
    print(results[['PredictedPosition', 'ActualPosition', 'Driver', 'Probability']])

# Hauptprogramm
def main():
    # Liste der Rennen der Saison 2023 (angenommene Werte)
    races = list(range(1058, 1102))
    last_race_id = 1101

    # Daten vorbereiten
    data = prepare_data(races, last_race_id)

    # Modell trainieren und evaluieren
    model = train_and_evaluate_model(data)

    # Vorhersage für das letzte Rennen
    predict_last_race(model, last_race_id)

if __name__ == '__main__':
    main()