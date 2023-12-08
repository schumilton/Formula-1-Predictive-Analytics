import psycopg2


class DatabaseConnection:
    def __init__(self):
        self.host = "localhost"
        self.database = "F1"
        self.user = "postgres"
        self.password = "caqzev-javjen-4zAcpo"
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return self.conn
        except psycopg2.Error as e:
            print("Fehler beim Verbinden zur Datenbank:", e)


