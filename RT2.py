import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_score
from FeaturesDrivers import FeaturesDrivers
from FeaturesConstructor import FeaturesConstructor
import numpy as np
import decimal
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform
from sklearn.model_selection import cross_val_score
# Daten vorbereiten
def prepare_data(races, last_race_id):
    features_drivers = FeaturesDrivers()
    features_constructor = FeaturesConstructor()
    data = []

    for race_id in races:
        if race_id == last_race_id:
            continue

        driver_ids = features_drivers.get_driver_id(race_id)
        for driver_id in driver_ids:
            constructor_id = features_drivers.get_constructor_id(driver_id, race_id)
            row = [
                driver_id,
                constructor_id,
                features_drivers.get_driver_age(driver_id, race_id),
                features_drivers.get_driver_years_in_f1(driver_id, race_id),
                features_drivers.get_qualifying_time_diff_to_pole(race_id, driver_id),
                features_drivers.get_front_row_starts(driver_id),
                features_drivers.get_career_wins(driver_id),
                features_drivers.get_season_wins(driver_id, race_id),
                features_drivers.get_races_started(driver_id),
                features_drivers.get_races_finished(driver_id),
                features_drivers.get_pole_positions(driver_id),
                features_drivers.get_driver_championships(driver_id),
                features_drivers.get_driver_standings_last_year(driver_id, race_id),
                features_drivers.get_current_driver_standings(driver_id, race_id),
                features_drivers.get_qualifying_race_correlation(driver_id),
                features_drivers.get_time_diff_to_winner_last_race(driver_id, race_id),
                features_drivers.get_prev_year_race_pit_stops(driver_id, race_id),
                features_drivers.get_avg_lap_time_last_race(driver_id, race_id).total_seconds() if features_drivers.get_avg_lap_time_last_race(driver_id, race_id) else None,
                features_drivers.get_avg_lap_time_consistency_last_race(driver_id, race_id),
                features_drivers.get_speed_rank_last_race(driver_id, race_id),
                features_drivers.get_qualifying_position(driver_id, race_id),
                features_constructor.get_constructor_championships_won(constructor_id),
                features_constructor.get_constructor_race_wins(constructor_id),
                features_constructor.get_constructor_season_wins(constructor_id, race_id),
                features_constructor.get_constructor_championships_last_x_years(constructor_id, race_id, 5),
                features_constructor.get_constructor_standings_last_year(constructor_id, race_id),
                features_constructor.get_current_constructor_standings(constructor_id, race_id),
                features_constructor.get_max_teammate_qualifying_position(constructor_id, driver_id, race_id),
                *features_constructor.get_constructor_positions_gained_lost_last_x_races(constructor_id, race_id, 5),
                *features_constructor.get_constructor_finishing_positions_last_x_races(constructor_id, race_id, 5),

                features_constructor.get_constructor_retirements(constructor_id),
                features_constructor.get_constructor_retirements_last_x_races(constructor_id, race_id, 5),
                *features_constructor.get_constructor_speed_stats_last_race(constructor_id, race_id),
                features_constructor.get_constructor_speed_rank_last_race(constructor_id, race_id),
                features_drivers.get_race_position(driver_id, race_id)
            ]
            data.append(row)

    df = pd.DataFrame(data, columns=[
        'DriverID', 'ConstructorID', 'Age', 'YearsInF1', 'QualifyingTimeDiffToPole', 'FrontRowStarts',
        'CareerWins', 'SeasonWins', 'RacesStarted', 'RacesFinished', 'PolePositions', 'DriverChampionships',
        'LastYearStandings', 'CurrentStandings', 'QualifyingRaceCorrelation', 'TimeDiffToWinnerLastRace',
        'PrevYearRacePitStops', 'AvgLapTimeLastRace', 'AvgLapTimeConsistencyLastRace', 'SpeedRankLastRace',
        'QualifyingPosition', 'ConstructorChampionshipsWon', 'ConstructorRaceWins', 'ConstructorSeasonWins',
        'ConstructorChampionshipsLast5Years', 'ConstructorStandingsLastYear', 'CurrentConstructorStandings',
        'MaxTeammateQualifyingPosition', 'MaxPositionsGainedLast5Races', 'MaxPositionsLostLast5Races',
        'AvgPositionsGainedLostLast5Races', 'BestFinishLast5Races', 'WorstFinishLast5Races', 'AvgFinishLast5Races',
         'ConstructorRetirements', 'ConstructorRetirementsLast5Races',
        'MaxSpeedLastRace', 'MinSpeedLastRace', 'AvgSpeedLastRace', 'ConstructorSpeedRankLastRace', 'RacePosition'
    ])

    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

    non_numeric_columns = df.columns.difference(numeric_columns)
    for column in non_numeric_columns:
        if df[column].dtype == object:
            mode_values = df[column].mode()
            if not mode_values.empty:
                most_frequent_value = mode_values.iloc[0]
                if isinstance(most_frequent_value, tuple):
                    most_frequent_value = most_frequent_value[0]
                df[column] = df[column].fillna(most_frequent_value)
            else:
                df[column] = df[column].fillna(0)  # Or choose a suitable default value
        else:
            df[column] = df[column].fillna(0)

    return df

# Modell trainieren und evaluieren
def train_and_evaluate_model(data, test_size=0.2, random_state=42):
    X = data.drop(['DriverID', 'ConstructorID', 'RacePosition'], axis=1)
    y = data['RacePosition']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    param_distributions = {
        'n_estimators': randint(50, 500),
        'max_depth': [None] + list(range(5, 50, 5)),
        'min_samples_split': randint(2, 20),
        'min_samples_leaf': randint(1, 10),
        'max_features': ['sqrt', 'log2', None],
        'bootstrap': [True, False]
    }

    rf = RandomForestClassifier(random_state=random_state)
    random_search = RandomizedSearchCV(estimator=rf, param_distributions=param_distributions, n_iter=100, cv=5, n_jobs=-1, verbose=2, random_state=random_state)
    random_search.fit(X_train, y_train)

    print("Best parameters: ", random_search.best_params_)
    print("Best score: ", random_search.best_score_)

    best_model = random_search.best_estimator_
    y_pred = best_model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    # Konfusionsmatrix visualisieren
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.show()

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")
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
        'Importance': best_model.feature_importances_
    })
    feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
    print("Feature Importance:")
    print(feature_importance)

    return best_model
# Vorhersage für das letzte Rennen
def predict_last_race(model, last_race_id):
    features_drivers = FeaturesDrivers()
    features_constructor = FeaturesConstructor()
    driver_ids = features_drivers.get_driver_id(last_race_id)
    data = []

    for driver_id in driver_ids:
        constructor_id = features_drivers.get_constructor_id(driver_id, last_race_id)
        row = [
            driver_id,
            constructor_id,
            features_drivers.get_driver_age(driver_id, last_race_id),
            features_drivers.get_driver_years_in_f1(driver_id, last_race_id),
            features_drivers.get_qualifying_time_diff_to_pole(last_race_id, driver_id),
            features_drivers.get_front_row_starts(driver_id),
            features_drivers.get_career_wins(driver_id),
            features_drivers.get_season_wins(driver_id, last_race_id),
            features_drivers.get_races_started(driver_id),
            features_drivers.get_races_finished(driver_id),
            features_drivers.get_pole_positions(driver_id),
            features_drivers.get_driver_championships(driver_id),
            features_drivers.get_driver_standings_last_year(driver_id, last_race_id),
            features_drivers.get_current_driver_standings(driver_id, last_race_id),
            features_drivers.get_qualifying_race_correlation(driver_id),
            features_drivers.get_time_diff_to_winner_last_race(driver_id, last_race_id),
            features_drivers.get_prev_year_race_pit_stops(driver_id, last_race_id),
            features_drivers.get_avg_lap_time_last_race(driver_id, last_race_id).total_seconds() if features_drivers.get_avg_lap_time_last_race(driver_id, last_race_id) else None,
            features_drivers.get_avg_lap_time_consistency_last_race(driver_id, last_race_id),
            features_drivers.get_speed_rank_last_race(driver_id, last_race_id),
            features_drivers.get_qualifying_position(driver_id, last_race_id),
            features_constructor.get_constructor_championships_won(constructor_id),
            features_constructor.get_constructor_race_wins(constructor_id),
            features_constructor.get_constructor_season_wins(constructor_id, last_race_id),
            features_constructor.get_constructor_championships_last_x_years(constructor_id, last_race_id, 5),
            features_constructor.get_constructor_standings_last_year(constructor_id, last_race_id),
            features_constructor.get_current_constructor_standings(constructor_id, last_race_id),
            features_constructor.get_max_teammate_qualifying_position(constructor_id, driver_id, last_race_id),
            *features_constructor.get_constructor_positions_gained_lost_last_x_races(constructor_id, last_race_id, 5),
            *features_constructor.get_constructor_finishing_positions_last_x_races(constructor_id, last_race_id, 5),
       #     features_constructor.get_constructor_speed_diff_to_fastest_last_race(constructor_id, last_race_id),
            features_constructor.get_constructor_retirements(constructor_id),
            features_constructor.get_constructor_retirements_last_x_races(constructor_id, last_race_id, 5),
            *features_constructor.get_constructor_speed_stats_last_race(constructor_id, last_race_id),
            features_constructor.get_constructor_speed_rank_last_race(constructor_id, last_race_id)
        ]
        data.append(row)

    df = pd.DataFrame(data, columns=[
        'DriverID', 'ConstructorID', 'Age', 'YearsInF1', 'QualifyingTimeDiffToPole', 'FrontRowStarts',
        'CareerWins', 'SeasonWins', 'RacesStarted', 'RacesFinished', 'PolePositions', 'DriverChampionships',
        'LastYearStandings', 'CurrentStandings', 'QualifyingRaceCorrelation', 'TimeDiffToWinnerLastRace',
        'PrevYearRacePitStops', 'AvgLapTimeLastRace', 'AvgLapTimeConsistencyLastRace', 'SpeedRankLastRace',
        'QualifyingPosition', 'ConstructorChampionshipsWon', 'ConstructorRaceWins', 'ConstructorSeasonWins',
        'ConstructorChampionshipsLast5Years', 'ConstructorStandingsLastYear', 'CurrentConstructorStandings',
        'MaxTeammateQualifyingPosition', 'MaxPositionsGainedLast5Races', 'MaxPositionsLostLast5Races',
        'AvgPositionsGainedLostLast5Races', 'BestFinishLast5Races', 'WorstFinishLast5Races', 'AvgFinishLast5Races',
         'ConstructorRetirements', 'ConstructorRetirementsLast5Races',
        'MaxSpeedLastRace', 'MinSpeedLastRace', 'AvgSpeedLastRace', 'ConstructorSpeedRankLastRace'
    ])

    X_last_race = df.drop(['DriverID', 'ConstructorID'], axis=1)
    timedelta_columns = ['AvgLapTimeLastRace', 'AvgLapTimeConsistencyLastRace', 'TimeDiffToWinnerLastRace']
    for column in timedelta_columns:
        if column in X_last_race.columns:
            X_last_race[column] = X_last_race[column].apply(lambda x: float(x.total_seconds()) if pd.notnull(x) and not isinstance(x, (float, decimal.Decimal)) else float(x) if pd.notnull(x) else x)

    X_last_race = X_last_race.fillna(X_last_race.mean())

    y_pred_proba = model.predict_proba(X_last_race)

    results = pd.DataFrame({
        'DriverID': df['DriverID'],
        'ConstructorID': df['ConstructorID'],
        'Probability': y_pred_proba.max(axis=1)
    })
    results['PredictedPosition'] = results['Probability'].rank(method='dense', ascending=False).astype(int)

    # Get the actual race positions for each driver in the last race
    actual_positions = []
    for driver_id in results['DriverID']:
        actual_position = features_drivers.get_race_position(driver_id, last_race_id)
        actual_positions.append(actual_position)

    results['ActualPosition'] = actual_positions

    driver_names = results['DriverID'].apply(lambda x: features_drivers.get_driver_name(x))
    results['Driver'] = driver_names

    constructor_names = results['ConstructorID'].apply(lambda x: features_constructor.get_constructor_name(x))
    results['Constructor'] = constructor_names

    results = results.sort_values("PredictedPosition")

    print("Predicted Last Race Results:")
    print(results[['PredictedPosition', 'ActualPosition', 'Driver',  'Probability']])

# Hauptprogramm
def main():
    races = list(range(1058, 1101))
#


    last_race_id = 1100

    # Daten vorbereiten
    data = prepare_data(races, last_race_id)

    # Modell trainieren und evaluieren
    model = train_and_evaluate_model(data)

    # Vorhersage für das letzte Rennen
    predict_last_race(model, last_race_id)

if __name__ == '__main__':
    main()