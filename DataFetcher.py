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
                    self.cur.execute('INSERT INTO circuits (name,location,country,lat, lng,alt, url)'
                                     'VALUES (%s, %s, %s,%s,%s,%s,%s)',
                                     (circuit["circuitName"],
                                      circuit["Location"]["locality"],
                                      circuit["Location"]["country"],
                                      circuit["Location"]["lat"],
                                      circuit["Location"]["lng"],
                                      circuit["Location"]["alt"],
                                      circuit["Location"]["url"]))
                    print("Die Strecke " + circuit["circuitName"] + " wurde hinzugefügt :)")
                    count1 += 1
                    self.conn.commit()
                except:
                    self.conn.rollback()
                    count2 += 1

            print("FetchCircuits:")
            print("Already up-to-date: ", count2)
            print("Added: ", count1)
