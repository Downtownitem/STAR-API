import Database.MySQL.Connect as Connect


class General:

    def __init__(self):
        Connect.connect()
        self.conn = Connect.get_connection()
        self.cursor = self.conn.cursor()
        self.cursor.errorhandler = lambda e: print(e)
        self.cursor.messages = lambda e: print(e)

    def execute(self, sql: str, args: tuple = (), fetch_all: bool = True):
        self.cursor.execute(sql, args)
        if fetch_all:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def __str__(self):
        return self.conn
