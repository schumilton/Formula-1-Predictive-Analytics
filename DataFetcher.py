import urllib.request, json
import urllib.request
import json
from DatabaseConnection import DatabaseConnection


class DataFetcher:
    def __init__(self):

        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()

    def fetchCircuits(self):
        with urllib.request.urlopen("http://ergast.com/api/f1/circuits.json?limit=1000") as url:
            data = json.load(url)
            count1 = 0
            count2 = 0

            for circuit in data["MRData"]["CircuitTable"]["Circuits"]:
                try:
                    with urllib.request.urlopen(
                            "https://api.open-elevation.com/api/v1/lookup?locations=" + circuit["Location"][
                                "lat"] + "," +
                            circuit["Location"]["long"]) as ref:
                        elevation = json.load(ref)["results"][0]["elevation"]

                        self.cur.execute('INSERT INTO circuits (name,location,country,lat, lng,alt, url)'
                                         'VALUES (%s, %s, %s,%s,%s,%s,%s)',
                                         (circuit["circuitName"],
                                          circuit["Location"]["locality"],
                                          circuit["Location"]["country"],
                                          circuit["Location"]["lat"],
                                          circuit["Location"]["long"],
                                          elevation,
                                          circuit["url"]))
                        print("Die Strecke " + circuit["circuitName"] + " wurde hinzugefügt :)")
                        count1 += 1
                        self.conn.commit()

                except Exception as err:
                    print(err)
                    self.conn.rollback()
                    count2 += 1

        print("FetchCircuits:")
        print("Already up-to-date: ", count2)
        print("Added: ", count1)

    def fetchStatus(self):
        with urllib.request.urlopen("http://ergast.com/api/f1/status.json?limit=1000") as url:
            data = json.load(url)
            count1 = 0
            count2 = 0
            for stat in data["MRData"]["StatusTable"]["Status"]:
                try:

                    self.cur.execute('INSERT INTO status (statusId, status)'
                                     'VALUES (%s, %s)',
                                     (stat["statusId"],
                                      stat["status"]))

                    print(stat["status"])
                    count1 += 1
                    self.conn.commit()


                except Exception as err:
                    print(err)
                    self.conn.rollback()
                    count2 += 1

            print("FetchCircuits:")
            print("Already up-to-date: ", count2)
            print("Added: ", count1)

    def fetchConstructors(self):
        with urllib.request.urlopen("http://ergast.com/api/f1/constructors.json?limit=1000") as url:
            data = json.load(url)
            count1 = 0
            count2 = 0
            for constructor in data["MRData"]["ConstructorTable"]["Constructors"]:
                try:

                    self.cur.execute('INSERT INTO constructors (name, nationality,url)'
                                     ' VALUES (%s, %s, %s)',
                                     (constructor["name"],
                                      constructor["nationality"],
                                      constructor["url"]))

                    print(constructor["name"])
                    count1 += 1
                    self.conn.commit()


                except Exception as err:

                    self.conn.rollback()
                    print(err)
                    count2 += 1

            print("FetchConstructors:")
            print("Already up-to-date: ", count2)
            print("Added: ", count1)

    def fetchDrivers(self):
        with urllib.request.urlopen("http://ergast.com/api/f1/drivers.json?limit=2000") as url:
            data = json.load(url)
            count1 = 0
            count2 = 0
            for driver in data["MRData"]["DriverTable"]["Drivers"]:
                try:

                    self.cur.execute('INSERT INTO drivers (forename,surname,dob,nationality,url)'
                                     ' VALUES (%s,%s,%s,%s,%s)',
                                     (driver["givenName"],
                                      driver["familyName"],
                                      driver["dateOfBirth"],
                                      driver["nationality"],
                                      driver["url"]))

                    print(driver["givenName"])
                    count1 += 1
                    self.conn.commit()


                except Exception as err:

                    self.conn.rollback()
                    print(err)
                    count2 += 1

            print("FetchDriver:")
            print("Already up-to-date: ", count2)
            print("Added: ", count1)

    def fetchSeasons(self):
        with urllib.request.urlopen("http://ergast.com/api/f1/seasons.json?limit=2000") as url:
            data = json.load(url)
            count1 = 0
            count2 = 0
            for season in data["MRData"]["SeasonTable"]["Seasons"]:
                try:

                    self.cur.execute('INSERT INTO Seasons (year,url)'
                                     ' VALUES (%s,%s)',
                                     (season["season"],
                                      season["url"]))
                    print(season["season"])
                    count1 += 1
                    self.conn.commit()

                except Exception as err:

                    self.conn.rollback()
                    print(err)
                    count2 += 1

            print("Fetched Seasons:")
            print("Already up-to-date: ", count2)
            print("Added: ", count1)

    def fetchRaces(self):
        self.cur.execute("Select DISTINCT year from Seasons ORDER BY year ASC")

        years = self.cur.fetchall()
        print(years[0][0])
        for year in years:
            print(year)
            with urllib.request.urlopen("http://ergast.com/api/f1/" + str(year[0]) + "/races.json?limit=2000") as url:
                data = json.load(url)
                count1 = 0
                count2 = 0
                for race in data["MRData"]["RaceTable"]["Races"]:
                    try:
                        self.cur.execute("SELECT circuitid FROM circuits where circuits.name = %s ",
                                         (str(race["Circuit"]["circuitName"]),))

                        circuit_id = self.cur.fetchone()[0]
                        print(circuit_id)
                        print()

                        self.cur.execute(
                            'INSERT INTO races (year, round, circuitid, name, date, url)'
                            ' VALUES (%s,%s,%s,%s,%s,%s)',
                            (race["season"], race["round"], circuit_id, race["raceName"], race["date"],
                             race["url"])
                        )

                        print(race["raceName"])
                        count1 += 1
                        self.conn.commit()


                    except Exception as err:

                        self.conn.rollback()
                        print(err)
                        count2 += 1

        print("FetchDriver:")
        print("Already up-to-date: ", count2)
        print("Added: ", count1)

    def fetchQualifying(self):
        self.cur.execute("Select DISTINCT year from Seasons ORDER BY year ASC")

        years = self.cur.fetchall()
        print(years[0][0])
        for year in years:

            with urllib.request.urlopen(
                    "http://ergast.com/api/f1/" + str(year[0]) + "/qualifying.json?limit=2000") as url:
                data = json.load(url)
                count1 = 0
                count2 = 0
                for race in data["MRData"]["RaceTable"]["Races"]:
                    try:

                        self.cur.execute("SELECT raceid FROM races where races.name = %s AND races.year = %s ",
                                         (str(race["raceName"]), race["season"]))
                        print
                        race_id = self.cur.fetchone()

                        print(race_id)
                        for driver in race["QualifyingResults"]:
                            print(driver["Driver"]["url"])

                            self.cur.execute("SELECT driverid FROM drivers where drivers.url = %s  ",
                                             (str(driver["Driver"]["url"]),))

                            driver_id = self.cur.fetchone()[0]
                            print(driver_id)

                            self.cur.execute(
                                "SELECT constructorid FROM constructors where constructors.url = %s AND constructors.name = %s ",
                                (str(driver["Constructor"]["url"]), str(driver["Constructor"]["name"])))

                            constructor_id = self.cur.fetchone()[0]
                            q2_value = driver.get("Q2", " ")
                            q3_value = driver.get("Q3", " ")


                            self.cur.execute("INSERT INTO qualifying(raceid,driverid,constructorid,number,position,"
                                             "q1,q2,q3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (
                                race_id, driver_id, constructor_id, driver["number"], driver["position"], driver["Q1"],
                                q2_value, q3_value))
                            count1 += 1

                            print(race["raceName"] + " " + driver["Driver"]["givenName"])

                            self.conn.commit()


                    except Exception as err:
                        self.conn.rollback()
                        print(err)
                        count2 += 1

        print("FetchDriver:")
        print("Already up-to-date: ", count2)
        print("Added: ", count1)
