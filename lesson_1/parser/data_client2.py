from abc import ABC, abstractmethod
import io
import psycopg2
import sqlite3
from sqlite3 import Error
import pandas

# pip install psycopg2
class DataClient(ABC):

    @abstractmethod
    def __get_connection(self):
        pass

    @abstractmethod
    def create_mebel_table(self):
        pass

    @abstractmethod
    def get_items(self,  price_from=0, price_to=1000000):
        pass

    @abstractmethod
    def insert(self,  link, price, description):
        pass

    @abstractmethod
    def select_by_word(self, word):
        pass

    @abstractmethod
    def select_by_word_and_price(self, word, price_from, price_to):
        pass

    def run_test(self):
        self.create_mebel_table()
        items = self.get_items( 10, 30)
        for item in items:
            print(item)

class Postgresclient(DataClient):

    USER = "postgres"
    PASSWORD = "563674AAi"
    HOST = "127.0.0.1"
    PORT = "5432"

    def select_by_word(self, word):
        with self._DataClient__get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM app_1_mebel WHERE description LIKE '%s'", (word, ))
            return cur.fetchall()
    def select_by_word_and_price(self, word, price_from, price_to):
        with self._DataClient__get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM app_1_mebel WHERE description LIKE %s and price >= %s and price <= %s",
                        (f'%{word}%',  price_from, price_to)
                        )
            return cur.fetchall()
    def _DataClient__get_connection(self):
        return psycopg2.connect(
                user=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT
        )

    def create_mebel_table(self):
        with self._DataClient__get_connection() as conn:
            cursor_object = conn.cursor()
            cursor_object.execute(
                """
                    CREATE TABLE IF NOT EXISTS app_1_mebel
                    (
                        id serial PRIMARY KEY ,
                        link text,
                        price integer,
                        description text
                    );
                """
            )


    def get_items(self, price_from = 1000, price_to = 1000000):
        with self._DataClient__get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM app_1_mebel WHERE price >= {price_from} and price <= {price_to}')
            return cur.fetchall()


    def insert(self, link, price, description):
        with self._DataClient__get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT INTO  app_1_mebel (link, price, description) VALUES ('{link}', '{price}', '{description}')")
            conn.commit()


class SQL3client(DataClient):
    DB_NAME = 'kufar.db'

    def select_by_word(self, word):
        with self._DataClient__get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM app_1_mebel WHERE word LIKE '%{word}%'")
            return cur.fetchall()

    def select_by_word_and_price(self, word, price_from, price_to):
        with self._DataClient__get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO  app_1_mebel WHERE word LIKE " % {word} % " and price >= {price_from} and price <= {price_to}")
            conn.commit()
    def _DataClient__get_connection(self):
        return sqlite3.connect(self.DB_NAME)

    def create_mebel_table(self):
        with self._DataClient__get_connection() as conn:
            cursor_object = conn.cursor()
            cursor_object.execute(
                """
                    CREATE TABLE IF NOT EXISTS app_1_mebel 
                    (
                        id integer PRIMARY KEY autoincrement,
                        link text,
                        price integer,
                        description text
                    );
                """
            )



    def get_items(self, price_from=0, price_to=1000000):
        with self._DataClient__get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM app_1_mebel WHERE price >= {price_from} and price <= {price_to}')
            return cur.fetchall()

    def insert(self,  link, price, description):
        with self._DataClient__get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT INTO  app_1_mebel (link, price, description) VALUES ('{link}', '{price}', '{description}')")
            conn.commit()

class CsvClient(DataClient):

    DB_NAME = 'kufar.db'

    def _DataClient__get_connection(self):
        return sqlite3.connect(self.DB_NAME)

    def create_mebel_table(self):
        with self._DataClient__get_connection() as conn:
            cursor_object = conn.cursor()
            cursor_object.execute(
                """
                    CREATE TABLE IF NOT EXISTS app_1_mebel
                    (
                        id serial PRIMARY KEY ,
                        link text,
                        price integer,
                        description text
                    );
                """
            )


    def get_items(self,  price_from = 0, price_to = 1000000):
        with self._DataClient__get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM app_1_mebel WHERE price >= {price_from} and price <= {price_to}')
            return cur.fetchall()


    def insert(self, link, price, description):
        with self._DataClient__get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT INTO  app_1_mebel (link, price, description) VALUES ('{link}', '{price}', '{description}')")
            conn.commit()




# data_client = Postgresclient()
# data_client = SQL3client()
# data_client.run_test()
# data_client.CsvClient()
