import sqlite3
from datetime import date
from habit_tracker import Habit


class HabitTracker:
    def __init__(self, name='main.db', isolation_level=None):
        """
        initialize a habit tracker object
        :param name: name of the database file
        : create a connection to the database
        : create a cursor object to execute SQL commands
        : create tables if they don't exist
        """
        self.conn = sqlite3.connect(name, isolation_level=isolation_level)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                name TEXT NOT NULL PRIMARY KEY,
                description TEXT,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                frequency TEXT NOT NULL,
                progress TEXT)''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracker (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_name TEXT NOT NULL,
                event_date DATE NOT NULL,
                completed BOOLEAN NOT NULL,
                FOREIGN KEY (habit_name) REFERENCES habits(name)
            )''')

        # self.cursor.execute("DELETE FROM habits")
        # self.cursor.execute("DELETE FROM tracker")

        self.conn.commit()

    def create_habit(self, name, description, start_date, end_date, frequency):
        """
        create a habit object and insert it into the database
        :param name: name of the habit
        :param description: description of the habit
        :param start_date: start date of the habit
        :param end_date: end date of the habit
        :param frequency: frequency of the habit
        """
        habit = Habit(name, description, start_date, end_date, frequency)
        self.cursor.execute('''
            INSERT INTO habits(name, description, start_date, end_date, frequency, progress)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (habit.name, habit.description, habit.start_date, habit.end_date, habit.frequency, str(habit.progress)))
        self.conn.commit()

    def predefined_habits(self):
        """
        create a few predefined habits
        :return: habit_names
        """
        habit_1 = Habit("Exercise", "Workout for 30 minutes", date(2020, 1, 1), date(2020, 1, 28), "daily")
        habit_2 = Habit("Meditate", "Meditate for 10 minutes", date(2020, 1, 1), date(2020, 1, 28), "weekly")
        habit_3 = Habit("Journal", "Write in journal for 5 minutes", date(2020, 1, 1), date(2020, 1, 28), "daily")
        habit_4 = Habit("Read", "Read for 15 minutes", date(2020, 1, 1), date(2020, 1, 28), "weekly")
        habit_5 = Habit("Drink Water", "Drink 8 glasses of water", date(2020, 1, 1), date(2020, 1, 28), "daily")

        habit_names = [h.name for h in [habit_1, habit_2, habit_3, habit_4, habit_5]]
        return habit_names

    def get_habit(self, habit_name):
        """
        get a habit object from the database
        :param habit_name: name of the habit
        :return: ‘Habit’ object
        """
        self.cursor.execute('SELECT * FROM habits WHERE name = ?', (str(habit_name),))
        row = self.cursor.fetchone()
        if row is None:
            return None
        name, description, start_date, end_date, frequency, progress, *extra_values = row
        return Habit(name, description, start_date, end_date, frequency, progress=progress)

    def get_tracker(self, habit_name):
        """
        get a habit tracker object from the database
        :param habit_name: name of the habit
        :return: ‘HabitTracker’ object
        """
        self.cursor.execute(
            'SELECT habit_name, event_date, completed FROM tracker WHERE habit_name = ?',
            (habit_name,))
        rows = self.cursor.fetchone()
        return rows

    def check_habit(self, habit_name, event_date, completed):
        """
        check if a habit was completed on a given date
        :param habit_name: name of the habit
        :param event_date: date of the event
        :param completed: boolean value
        :return: ‘Habit’ object
        """
        habit_completed = Habit(habit_name, end_date=event_date)
        self.cursor.execute('''
                    INSERT INTO tracker(habit_name, event_date, completed)
                    VALUES (?, ?, ?)
                ''', (habit_name, event_date, completed))
        self.conn.commit()
        rows = self.cursor.fetchone()
        if rows is None:
            return None
        habit_completed.mark_complete(event_date)
        return habit_completed

    def delete_habit(self, name):
        """
        delete a habit from the database
        :param name: name of the habit
        """
        habit = Habit(name)
        self.cursor.execute('DELETE FROM habits WHERE name = ?', (habit.name,))
        self.conn.commit()

    def update_habit(self, name, description, start_date, end_date, frequency):
        """
        update a habit in the database
        :param name: name of the habit
        :param description: description of the habit
        :param start_date: start date of the habit
        :param end_date: end date of the habit
        :param frequency: frequency of the habit
        """
        habit = Habit(name, description, start_date, end_date, frequency)
        self.cursor.execute('''
            UPDATE habits
            SET description = ?, start_date = ?, end_date = ?, frequency = ?, progress = ?
            WHERE name = ?
        ''', (habit.description, habit.start_date, habit.end_date, habit.frequency, str(habit.progress), habit.name))
        self.conn.commit()

    def close(self):
        self.conn.close()

        
