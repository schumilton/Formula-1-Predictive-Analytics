from DatabaseConnection import DatabaseConnection

class FeaturesConstructor:
    def __init__(self):
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()
    def get_constructor_name(self, constructor_id):
        query = """
                   SELECT name FROM constructors WHERE constructorId = %s;
               """
        self.cur.execute(query, (constructor_id,))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_constructor_championships_won(self, constructor_id):
        query = """
                   SELECT COUNT(*) AS championships_won
                   FROM constructorStandings
                   WHERE constructorId = %s AND position = 1;
               """
        self.cur.execute(query, (constructor_id,))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_constructor_race_wins(self, constructor_id):
        query = """
                   SELECT COUNT(*) AS race_wins
                   FROM results  
                   WHERE constructorId = %s AND position = 1;
               """
        self.cur.execute(query, (constructor_id,))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_constructor_season_wins(self, constructor_id, race_id):
        query = """
                   SELECT COUNT(*) AS season_wins
                   FROM results
                   WHERE constructorId = %s 
                     AND raceId IN (
                         SELECT raceId 
                         FROM races
                         WHERE year = (SELECT year FROM races WHERE raceId = %s)
                           AND raceId <= %s
                     )
                     AND position = 1;
               """
        self.cur.execute(query, (constructor_id, race_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_constructor_championships_last_x_years(self, constructor_id, race_id, x):
        query = """
                   SELECT COUNT(*) AS championships_last_x_years
                   FROM constructorStandings
                   WHERE constructorId = %s
                     AND raceId IN (
                         SELECT raceId
                         FROM races
                         WHERE year >= (SELECT year FROM races WHERE raceId = %s) - %s
                     )
                     AND position = 1;
               """
        self.cur.execute(query, (constructor_id, race_id, x))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_constructor_standings_last_year(self, constructor_id, race_id):
        query = """
                   SELECT position AS constructor_standings_last_year
                   FROM constructorStandings
                   WHERE constructorId = %s
                     AND raceId = (
                         SELECT raceId 
                         FROM races
                         WHERE year = (SELECT year FROM races WHERE raceId = %s) - 1
                         ORDER BY round DESC 
                         LIMIT 1 
                     );
               """
        self.cur.execute(query, (constructor_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_current_constructor_standings(self, constructor_id, race_id):
        query = """
                   SELECT position AS current_constructor_standings
                   FROM constructorStandings
                   WHERE constructorId = %s
                     AND raceId = (
                         SELECT raceId
                         FROM races
                         WHERE year = (SELECT year FROM races WHERE raceId = %s)
                         ORDER BY round DESC
                         LIMIT 1
                     );
               """
        self.cur.execute(query, (constructor_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_max_teammate_qualifying_position(self, constructor_id, driver_id, race_id):
        query = """
                   SELECT MIN(position) AS best_teammate_qualifying
                   FROM qualifying
                   WHERE constructorId = %s 
                     AND driverId != %s
                     AND raceId = %s;
               """
        self.cur.execute(query, (constructor_id, driver_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_constructor_positions_gained_lost_last_x_races(self, constructor_id, race_id, x):
        query = """
                   SELECT
                       MAX(position_change) AS max_positions_gained,
                       MIN(position_change) AS max_positions_lost,
                       AVG(position_change) AS avg_positions_gained_lost
                   FROM (
                       SELECT 
                           results.grid - results.position AS position_change
                       FROM results
                       JOIN races ON results.raceId = races.raceId
                       WHERE results.constructorId = %s
                         AND races.year = (SELECT year FROM races WHERE raceId = %s)
                         AND races.round < (SELECT round FROM races WHERE raceId = %s)
                       ORDER BY races.round DESC
                       LIMIT %s  
                   ) AS position_changes;
               """
        self.cur.execute(query, (constructor_id, race_id, race_id, x))
        result = self.cur.fetchone()
        return result if result else (None, None, None)


    def get_constructor_finishing_positions_last_x_races(self, constructor_id, race_id, x):
        query = """
            SELECT
                MAX(position) AS best_finish,
                MIN(position) AS worst_finish,
                AVG(position) AS avg_finish
            FROM (
                SELECT results.position
                FROM results
                JOIN races ON results.raceId = races.raceId
                WHERE results.constructorId = %s
                  AND races.year = (SELECT year FROM races WHERE raceId = %s)
                  AND races.round < (SELECT round FROM races WHERE raceId = %s)
                ORDER BY races.round DESC
                LIMIT %s
            ) AS positions;
        """
        self.cur.execute(query, (constructor_id, race_id, race_id, x))
        result = self.cur.fetchone()
        return result if result else (None, None, None)


    def get_constructor_speed_diff_to_fastest_last_race(self, constructor_id, race_id):
        query = """
                   WITH constructor_lap AS (
                       SELECT fastestLapSpeed AS speed
                       FROM results
                       WHERE constructorId = %s 
                         AND raceId = (
                             SELECT raceId
                             FROM races
                             WHERE year = (SELECT year FROM races WHERE raceId = %s)
                               AND round < (SELECT round FROM races WHERE raceId = %s) 
                             ORDER BY round DESC
                             LIMIT 1
                         )
                   ),
                   fastest_lap AS (
                       SELECT fastestLapSpeed AS speed
                       FROM results  
                       WHERE raceId = (
                           SELECT raceId
                           FROM races
                           WHERE year = (SELECT year FROM races WHERE raceId = %s)
                             AND round < (SELECT round FROM races WHERE raceId = %s)
                           ORDER BY round DESC
                           LIMIT 1
                       )
                       ORDER BY fastestLapSpeed DESC 
                       LIMIT 1
                   )
                   SELECT 
                       (constructor_lap.speed::float / fastest_lap.speed::float) * 100 AS percentage_of_fastest_lap
                   FROM constructor_lap, fastest_lap;
               """
        self.cur.execute(query, (constructor_id, race_id, race_id, race_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_constructor_retirements(self, constructor_id):
        query = """
                   SELECT COUNT(*) AS retirements
                   FROM results
                   WHERE constructorId = %s 
                     AND statusId != (SELECT statusId FROM status WHERE status = 'Finished');  
               """
        self.cur.execute(query, (constructor_id,))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_constructor_retirements_last_x_races(self, constructor_id, race_id, x):
        query = """
            SELECT COUNT(*) AS retirements_last_x_races
            FROM (
                SELECT results.statusId
                FROM results
                JOIN races ON results.raceId = races.raceId
                WHERE results.constructorId = %s
                  AND races.year = (SELECT year FROM races WHERE raceId = %s)
                  AND races.round < (SELECT round FROM races WHERE raceId = %s)
                  AND results.statusId != (SELECT statusId FROM status WHERE status = 'Finished')
                ORDER BY races.round DESC
                LIMIT %s
            ) AS subquery;
        """
        self.cur.execute(query, (constructor_id, race_id, race_id, x))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_constructor_speed_stats_last_race(self, constructor_id, race_id):
        query = """  
                   WITH constructor_laps AS (
                       SELECT unnest(string_to_array(fastestLapSpeed, ' '))::float AS speed
                       FROM results
                       WHERE constructorId = %s
                         AND raceId = (
                             SELECT raceId 
                             FROM races
                             WHERE year = (SELECT year FROM races WHERE raceId = %s)
                               AND round < (SELECT round FROM races WHERE raceId = %s)
                             ORDER BY round DESC
                             LIMIT 1
                         )
                   )
                   SELECT
                       MAX(speed) AS max_speed,
                       MIN(speed) AS min_speed,  
                       AVG(speed) AS avg_speed
                   FROM constructor_laps;
               """
        self.cur.execute(query, (constructor_id, race_id, race_id))
        result = self.cur.fetchone()
        return result if result else (None, None, None)


    def get_constructor_speed_rank_last_race(self, constructor_id, race_id):
        query = """
                   WITH constructor_laps AS (
                       SELECT constructorId, unnest(string_to_array(fastestLapSpeed, ' '))::float AS speed
                       FROM results  
                       WHERE raceId = (
                           SELECT raceId
                           FROM races
                           WHERE year = (SELECT year FROM races WHERE raceId = %s)
                             AND round < (SELECT round FROM races WHERE raceId = %s)
                           ORDER BY round DESC
                           LIMIT 1  
                       )
                   ),
                   constructor_avg_speeds AS (
                       SELECT constructorId, AVG(speed) AS avg_speed
                       FROM constructor_laps
                       GROUP BY constructorId
                   )
                   SELECT RANK() OVER (ORDER BY avg_speed DESC) AS speed_rank
                   FROM constructor_avg_speeds
                   WHERE constructorId = %s;
               """
        self.cur.execute(query, (race_id, race_id, constructor_id))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_circuit_name(self, circuit_id):
        query = """
                   SELECT name FROM circuits WHERE circuitId = %s;
               """
        self.cur.execute(query, (circuit_id,))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_race_round(self, race_id):
        query = """  
                   SELECT round FROM races WHERE raceId = %s;
               """
        self.cur.execute(query, (race_id,))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_race_year(self, race_id):
        query = """
                   SELECT year FROM races WHERE raceId = %s;  
               """
        self.cur.execute(query, (race_id,))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_avg_overtakes_per_race(self, circuit_id):
        query = """
                   WITH overtakes AS (
                       SELECT
                           results.raceId,
                           SUM(results.grid - results.position) AS overtakes  
                       FROM results
                       JOIN races ON results.raceId = races.raceId
                       WHERE races.circuitId = %s
                       GROUP BY results.raceId  
                   )
                   SELECT AVG(overtakes) AS avg_overtakes_per_race
                   FROM overtakes;
               """
        self.cur.execute(query, (circuit_id,))
        result = self.cur.fetchone()
        return result[0] if result else None




