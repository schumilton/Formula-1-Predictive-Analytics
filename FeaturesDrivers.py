from DatabaseConnection import DatabaseConnection


class FeaturesDrivers:
    def __init__(self):
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()

    def get_driver_name(self, driver_id):
        query = """
            SELECT forename, surname FROM drivers WHERE driverId = %s;
        """
        self.cur.execute(query, (driver_id,))
        result = self.cur.fetchone()
        return result if result else None

    def get_driver_age(self, driver_id, race_id):
        query = """
            SELECT DATE_PART('year', races.date) - DATE_PART('year', drivers.dob) AS age
            FROM drivers
            JOIN results ON drivers.driverId = results.driverId
            JOIN races ON results.raceId = races.raceId
            WHERE drivers.driverId = %s AND races.raceId = %s;
        """
        self.cur.execute(query, (driver_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_driver_years_in_f1(self, driver_id, race_id):
        query = """
            SELECT COUNT(DISTINCT year) AS years_in_f1
            FROM results
            JOIN races ON results.raceId = races.raceId
            WHERE results.driverId = %s AND races.raceId <= %s;
        """
        self.cur.execute(query, (driver_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_qualifying_time_diff_to_pole(self, race_id, driver_id):
        query = """
            WITH pole_position AS (
                SELECT EXTRACT(EPOCH FROM MIN(q3)) AS pole_time
                FROM qualifying
                WHERE raceId = %s
            )
            SELECT (EXTRACT(EPOCH FROM q3) - pole_time) / pole_time * 100 AS diff_to_pole
            FROM qualifying, pole_position
            WHERE raceId = %s AND driverId = %s;
        """
        self.cur.execute(query, (race_id, race_id, driver_id))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_front_row_starts(self, driver_id):
        query = """
            SELECT COUNT(*) AS front_row_starts
            FROM qualifying
            WHERE driverId = %s AND position <= 2;
        """
        self.cur.execute(query, (driver_id,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_career_wins(self, driver_id):
        query = """
            SELECT COUNT(*) AS career_wins
            FROM results
            WHERE driverId = %s AND position = 1;
        """
        self.cur.execute(query, (driver_id,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_season_wins(self, driver_id, race_id):
        query = """
            SELECT COUNT(*) AS season_wins
            FROM results
            JOIN races ON results.raceId = races.raceId
            WHERE results.driverId = %s 
              AND races.year = (SELECT year FROM races WHERE raceId = %s)
              AND results.position = 1
              AND races.raceId <= %s;
        """
        self.cur.execute(query, (driver_id, race_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_races_started(self, driver_id):
        query = """
            SELECT COUNT(*) AS races_started
            FROM results
            WHERE driverId = %s;
        """
        self.cur.execute(query, (driver_id,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_races_finished(self, driver_id):
        query = """
            SELECT COUNT(*) AS races_finished
            FROM results
            WHERE driverId = %s AND positionText != 'R';
        """
        self.cur.execute(query, (driver_id,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_pole_positions(self, driver_id):
        query = """
            SELECT COUNT(*) AS pole_positions
            FROM qualifying
            WHERE driverId = %s AND position = 1;
        """
        self.cur.execute(query, (driver_id,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_driver_championships(self, driver_id):
        query = """
            SELECT COUNT(*) AS championships 
            FROM driverStandings 
            WHERE driverId = %s AND position = 1;
        """
        self.cur.execute(query, (driver_id,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_driver_standings_last_year(self, driver_id, race_id):
        query = """
            SELECT position AS last_year_position
            FROM driverStandings
            WHERE driverId = %s AND raceId = (
                SELECT raceId 
                FROM races 
                WHERE year = (SELECT year FROM races WHERE raceId = %s) - 1
                ORDER BY round DESC LIMIT 1
            );
        """
        self.cur.execute(query, (driver_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_current_driver_standings(self, driver_id, race_id):
        query = """
            SELECT position AS current_position
            FROM driverStandings
            WHERE driverId = %s AND raceId = (
                SELECT raceId 
                FROM races 
                WHERE year = (SELECT year FROM races WHERE raceId = %s)
                ORDER BY round DESC LIMIT 1
            );
        """
        self.cur.execute(query, (driver_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_positions_gained_lost_last_x_races(self, driver_id, race_id, x):
        query = """
            SELECT
                MAX(position_change) AS max_positions_gained,
                MIN(position_change) AS max_positions_lost,
                AVG(position_change) AS avg_positions_gained_lost
            FROM (
                SELECT
                    results.grid - results.position AS position_change  
                FROM results
                WHERE results.driverId = %s
                  AND results.raceId IN (
                      SELECT raceId 
                      FROM races
                      WHERE year = (SELECT year FROM races WHERE raceId = %s)
                        AND round < (SELECT round FROM races WHERE raceId = %s)
                      ORDER BY round DESC
                      LIMIT %s
                  )
            ) AS position_changes;
        """
        self.cur.execute(query, (driver_id, race_id, race_id, x))
        result = self.cur.fetchone()
        return result if result else (None, None, None)

    def get_finishing_positions_last_x_races(self, driver_id, race_id, x):
        query = """
            SELECT
                MAX(position) AS best_finish,
                MIN(position) AS worst_finish,
                AVG(position) AS avg_finish
            FROM results
            WHERE driverId = %s
              AND raceId IN (
                  SELECT raceId 
                  FROM races
                  WHERE year = (SELECT year FROM races WHERE raceId = %s)
                    AND round < (SELECT round FROM races WHERE raceId = %s)
                  ORDER BY round DESC
                  LIMIT %s
              );
        """
        self.cur.execute(query, (driver_id, race_id, race_id, x))
        result = self.cur.fetchone()
        return result if result else (None, None, None)

    def get_qualifying_race_correlation(self, driver_id):
        query = """
            WITH driver_results AS (
                SELECT
                    qualifying.raceId,
                    qualifying.position AS qualifying_position,
                    results.position AS race_position
                FROM qualifying
                JOIN results ON qualifying.raceId = results.raceId AND qualifying.driverId = results.driverId
                WHERE qualifying.driverId = %s
            )
            SELECT corr(qualifying_position, race_position) AS correlation 
            FROM driver_results;
        """
        self.cur.execute(query, (driver_id,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_previous_race_result(self, driver_id, race_id):
        query = """
            SELECT
                results.position AS prev_race_position,
                qualifying.position AS prev_race_qualifying_position,
                results.grid - results.position AS prev_race_positions_gained
            FROM results
            JOIN qualifying ON results.raceId = qualifying.raceId AND results.driverId = qualifying.driverId
            WHERE results.driverId = %s
              AND results.raceId = (
                  SELECT raceId
                  FROM races
                  WHERE year = (SELECT year FROM races WHERE raceId = %s)
                    AND round < (SELECT round FROM races WHERE raceId = %s)
                  ORDER BY round DESC
                  LIMIT 1
              );
        """
        self.cur.execute(query, (driver_id, race_id, race_id))
        result = self.cur.fetchone()
        return result if result else (None, None, None)

    def get_previous_year_race_result(self, driver_id, race_id):
        query = """
            SELECT
                results.position AS prev_year_race_position,
                qualifying.position AS prev_year_qualifying_position,
                results.grid - results.position AS prev_year_positions_gained
            FROM results
            JOIN qualifying ON results.raceId = qualifying.raceId AND results.driverId = qualifying.driverId
            JOIN races ON results.raceId = races.raceId
            WHERE results.driverId = %s
              AND races.circuitId = (SELECT circuitId FROM races WHERE raceId = %s)
              AND races.year = (SELECT year FROM races WHERE raceId = %s) - 1;
        """
        self.cur.execute(query, (driver_id, race_id, race_id))
        result = self.cur.fetchone()
        return result if result else (None, None, None)

    def get_time_diff_to_winner_last_race(self, driver_id, race_id):
        query = """
            SELECT (EXTRACT(EPOCH FROM driver_time) - EXTRACT(EPOCH FROM winner_time)) / EXTRACT(EPOCH FROM winner_time) * 100 AS time_diff_to_winner
            FROM (
                SELECT r1.time::INTERVAL AS driver_time
                FROM results r1
                WHERE r1.driverId = %s
                  AND r1.raceId = (
                      SELECT raceId
                      FROM races
                      WHERE year = (SELECT year FROM races WHERE raceId = %s)
                        AND round < (SELECT round FROM races WHERE raceId = %s)
                      ORDER BY round DESC
                      LIMIT 1
                  )
            ) AS driver_result,
            (
                SELECT time::INTERVAL AS winner_time
                FROM results
                WHERE position = 1
                  AND raceId = (
                      SELECT raceId
                      FROM races
                      WHERE year = (SELECT year FROM races WHERE raceId = %s)
                        AND round < (SELECT round FROM races WHERE raceId = %s)
                      ORDER BY round DESC
                      LIMIT 1
                  )
            ) AS winner_result;
        """
        self.cur.execute(query, (driver_id, race_id, race_id, race_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_prev_year_race_pit_stops(self, driver_id, race_id):
        query = """
            SELECT COUNT(*) AS prev_year_race_pit_stops
            FROM pitstops
            WHERE driverId = %s
              AND raceId = (
                  SELECT raceId
                  FROM races
                  WHERE circuitId = (SELECT circuitId FROM races WHERE raceId = %s)
                    AND year = (SELECT year FROM races WHERE raceId = %s) - 1
                  ORDER BY round DESC
                  LIMIT 1
              );
        """
        self.cur.execute(query, (driver_id, race_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_avg_lap_time_last_race(self, driver_id, race_id):
        query = """
            SELECT AVG(lap_time) AS avg_lap_time_last_race
            FROM (
                SELECT (time::TIME)::INTERVAL AS lap_time
                FROM laptimes
                WHERE driverId = %s
                  AND raceId = (
                      SELECT raceId
                      FROM races
                      WHERE year = (SELECT year FROM races WHERE raceId = %s)
                        AND round < (SELECT round FROM races WHERE raceId = %s)
                      ORDER BY round DESC
                      LIMIT 1
                  )
            ) AS lap_times;
        """
        self.cur.execute(query, (driver_id, race_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_avg_lap_time_consistency_last_race(self, driver_id, race_id):
        query = """
            SELECT STDDEV(EXTRACT(EPOCH FROM lap_time)) AS lap_time_consistency
            FROM (
                SELECT (time::TIME)::INTERVAL AS lap_time
                FROM laptimes
                WHERE driverId = %s
                  AND raceId = (
                      SELECT raceId
                      FROM races
                      WHERE year = (SELECT year FROM races WHERE raceId = %s)
                        AND round < (SELECT round FROM races WHERE raceId = %s)
                      ORDER BY round DESC
                      LIMIT 1
                  )
            ) AS lap_times;
        """
        self.cur.execute(query, (driver_id, race_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None



    def get_speed_rank_last_race(self, driver_id, race_id):
        query = """
            WITH driver_speeds AS (
                SELECT driverId, unnest(string_to_array(fastestLapSpeed, ' '))::float AS speed 
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
            driver_avg_speeds AS (
                SELECT driverId, AVG(speed) AS avg_speed
        FROM driver_speeds
                       GROUP BY driverId
                   )
                   SELECT RANK() OVER (ORDER BY avg_speed DESC) AS speed_rank
                   FROM driver_avg_speeds  
                   WHERE driverId = %s;
               """
        self.cur.execute(query, (race_id, race_id, driver_id))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_qualifying_position(self, driver_id, race_id):
        query = """
            SELECT position
            FROM qualifying
            WHERE driverId = %s AND raceId = %s;
        """
        self.cur.execute(query, (driver_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None


    def get_race_position(self, driver_id, race_id):
        query = """
            SELECT position
            FROM results
            WHERE driverId = %s AND raceId = %s;
        """
        self.cur.execute(query, (driver_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_driver_id(self, race_id):
        query = """
            SELECT driverid
            FROM results
            WHERE raceid = %s ;
        """
        self.cur.execute(query, (race_id,))
        result = self.cur.fetchall()
        return result if result else None

    def get_constructor_id(self, driver_id, race_id):
        query = """
                   SELECT constructorId 
                   FROM results
                   WHERE driverId = %s AND raceId = %s
                   LIMIT 1;
               """
        self.cur.execute(query, (driver_id, race_id))
        result = self.cur.fetchone()
        return result[0] if result else None
