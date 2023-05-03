import sqlite3
from datetime import date, timedelta
import random
import names

DB_LOCATION = "../db/example2.db"

class User:
    def __init__(self, id=None, name=None, birthdate=None):
        self.id = id
        self.name = name
        self.birthdate = birthdate
        self.save()

    @staticmethod
    def create_table():
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            birthdate TEXT
        )
        """)
        
    def save(self):
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()

        if self.id is None:
            # Insert a new record
            cursor.execute("INSERT INTO users (name, birthdate) VALUES (?, ?)", (self.name, self.birthdate))
            self.id = cursor.lastrowid
        else:
            # Update an existing record
            cursor.execute("UPDATE users SET name = ?, birthdate = ? WHERE id = ?", (self.name, self.birthdate, self.id))

        connection.commit()
        connection.close()

    def delete(self):
        if self.id is not None:
            connection = sqlite3.connect(DB_LOCATION)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (self.id,))
            connection.commit()
            connection.close()

    @classmethod
    def get_by_id(cls, id):
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        row = cursor.fetchone()
        connection.close()

        if row is not None:
            return cls(id=row[0], name=row[1], birthdate=row[2])
        else:
            return None
    
User.create_table()


def random_birthdate(start_year=1950, end_year=2000):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)

    days_between_dates = (end_date - start_date).days
    random_number_of_days = random.randrange(days_between_dates)
    birthdate = start_date + timedelta(days=random_number_of_days)
    return birthdate.strftime("%Y-%m-%d")

def create_random_user():
    random_name = names.get_full_name()
    random_date = random_birthdate()

    random_user = User(name=random_name, birthdate=random_date)
    random_user.save()
    return random_user

for _ in range(100):
    create_random_user()

connection = sqlite3.connect(DB_LOCATION)
cursor = connection.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

