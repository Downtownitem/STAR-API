from Database.MySQL.Control.General import General


class Chunks(General):

    def __init__(self):
        super().__init__()

    def add(self, info) -> int:
        self.execute('INSERT INTO information_chunks (info) VALUES (%s)', (info,))
        return self.cursor.lastrowid

    def get_chunk(self, id: int) -> str:
        return self.execute('SELECT info FROM information_chunks WHERE id = %s', (id,), fetch_all=False)[0]

    def get_id(self, info: str) -> int:
        return self.execute('SELECT id FROM information_chunks WHERE info = %s', (info,), fetch_all=False)[0]

    def delete_by_id(self, id: int):
        self.execute('DELETE FROM information_chunks WHERE id = %s', (id,))

    def delete_by_info(self, info: str):
        self.execute('DELETE FROM information_chunks WHERE info = %s', (info,))
