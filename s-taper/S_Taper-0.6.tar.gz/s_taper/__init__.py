import sqlite3


class Taper(object):
    """
        Main class. Its instances correspond to a single table in the database.
        Use:
        table1 = Taper("table_name", "file.db")
    """
    def __init__(self, table_name: str, file_name: str):
        self._table_name: str = table_name
        self._file_name: str = file_name

    def write(self, values: list | tuple):
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        questions = "?"
        for x in range(len(values) - 1):
            questions += ", ?"
        try:
            cur.execute(f"INSERT or REPLACE into {self._table_name} VALUES({questions});", values)
            conn.commit()
            conn.close()
            return values
        except sqlite3.OperationalError as e:
            print(f"Sorry, you have too many values than your table. T{str(e)[1:]}")
        conn.close()

    def read(self, column_name: str, key: str | int):
        if key.isnumeric():
            key = str(key)
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        cur.execute(f'SELECT * from {self._table_name} WHERE {column_name} = ? ', (key,))
        result = cur.fetchone()
        return result

    def read_all(self):
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        cur.execute(f'SELECT * from {self._table_name}')
        result = cur.fetchall()
        conn.close()
        return result

    def delete_row(self, column_name: str, key: str | int, all_rows: bool):
        """
        Func uses to deleting rows from the table.

        :param column_name: Column name to delete the row in which the key is found in the current column
        :param key: Key which looks in column
        :param all_rows: If True func delete all rows in the table
        """

        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        if all_rows:
            cur.execute(f'DELETE FROM {self._table_name}')
        else:
            cur.execute(f'DELETE FROM {self._table_name} WHERE {column_name} = ?', (key, ))
        conn.commit()
        conn.close()

    def upgrade(self, new_data: list):
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        old_data = list(self.read(column_name, key))
        index = 0  # Номер текущего элемента
        for element in new_data:
            old_data[index] += element
            index += 1
        self.write(old_data)
