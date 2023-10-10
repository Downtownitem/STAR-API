import Database.MySQL.Connect as Connect


class General:

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        Connect.close_connection()
        Connect.connect()
        self.conn = Connect.get_connection()
        self.cursor = self.conn.cursor()
        self.cursor.errorhandler = lambda e: print(e)
        self.cursor.messages = lambda e: print(e)

    def execute(self, sql: str, args: tuple = (), fetch_all: bool = True):
        try:
            # Test if the connection is still alive
            self.conn.ping(reconnect=True)
        except Exception as e:
            print(e)
            self.connect()

        self.cursor.execute(sql, args)
        if fetch_all:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def __str__(self):
        return self.conn
