import os
from configparser import ConfigParser

import psycopg2 as pg2


### FILE CONTEXT MANAGER
class MyFileManager:
    def __init__(self, name, mode, encoding='utf-8'):
        self.name = name
        self.mode = mode
        self.file = None
        self.encoding = encoding

    def __enter__(self):
        self.file = open(self.name, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.file.close()


with MyFileManager("context_manager_sample.txt", "r") as file:
    for line in file.readlines():
        print(line, end='')


### DATABASE CONNECTION MANAGER
class PostgresConnectionManager:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def __enter__(self):
        self.connection = pg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.connection.close()


parser = ConfigParser()
cwd = os.path.dirname(os.path.abspath(__file__))
parser.read(os.path.join(cwd, 'secret_config.ini'))

host = parser.get('postgres', 'host')
database = parser.get('postgres', 'database')
user = parser.get('postgres', 'user')
password = parser.get('postgres', 'password')

query = 'SELECT * FROM auth_user'

with PostgresConnectionManager(host, database, user, password) as conn:
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    print(result)

