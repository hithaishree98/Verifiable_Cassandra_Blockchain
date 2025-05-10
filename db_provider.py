from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class Server:
    def __init__(self, contact_points=['127.0.0.1'], port=9042,
                 username='cassandra', password='cassandra'):
        auth = PlainTextAuthProvider(username=username, password=password)
        self.cluster = Cluster(contact_points, port=port, auth_provider=auth)
        self.session = self.cluster.connect()
        self.keyspace = "project3"
        self.table = "data"

        try:
            self.session.execute(
                f"CREATE KEYSPACE IF NOT EXISTS {self.keyspace} "
                f"WITH REPLICATION = {{'class': 'SimpleStrategy', 'replication_factor': 1}};"
            )
            self.session.set_keyspace(self.keyspace)
            self.session.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table} ("
                f"key text PRIMARY KEY, value text);"
            )
        except Exception as e:
            print("Failed to setup database:", e)
            raise

    def add_data(self, key: str, value: str):
        try:
            q = f"INSERT INTO {self.table} (key, value) VALUES (%s, %s);"
            self.session.execute(q, (key, value))
        except Exception as e:
            print("Error adding data:", e)
            raise

    def get_data(self, key: str) -> str | None:
        try:
            q = f"SELECT value FROM {self.table} WHERE key = %s;"
            rs = self.session.execute(q, (key,))
            row = rs.one()
            return row[0] if row else None
        except Exception as e:
            print("Error retrieving data:", e)
            raise

    def close(self):
        self.session.shutdown()
        self.cluster.shutdown()
