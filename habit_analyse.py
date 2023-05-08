from habit_tracker import Habit
import sqlite3


class HabitAnalyser:
    def __init__(self, name='main.db'):
        """
        initialize a habit analyser object
        :param name: name of the database file
        : create a connection to the database
        : create a cursor object to execute SQL commands
        """
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()

    def retrieve_habit(self):
        """
        Get all habits from the database
        :return: List of Habit objects
        """
        rows = self.cursor.fetchall()
        habits = []
        for row in rows:
            habit = Habit(row[1], row[2], row[3], row[4], row[5])
            habit.progress = eval(row[6])
            habits.append(habit)
        return habits

    def get_all_habits(self):
        """
        get all habits from the database
        :return: habits
        """
        self.cursor.execute('SELECT * FROM habits')
        habits = self.retrieve_habit()
        return habits

    def get_habits_with_periodicity(self, frequency):
        """
        get habits with a specific periodicity from the database
        :param frequency:
        :return: habits
        """
        self.cursor.execute('SELECT * FROM habits WHERE frequency = ?', (frequency,))
        habits = self.retrieve_habit()
        return habits

    def get_streak(self, row, longest_streak):
        """
        Calculate the streak for a habit and update longest streak
        :param row: Habit row from database
        :param longest_streak: Longest streak across all habits
        :return: Updated the longest streak
        """
        streak = 0
        for date in eval(row[6]):
            if date == row[4]:
                streak += 1
        else:
            if streak > longest_streak:
                longest_streak = streak
        streak = 0
        if streak > longest_streak:
            longest_streak = streak
        return longest_streak

    def get_longest_streak(self):
        """
        get the longest streak of all habits
        :return: longest_streak
        """
        self.cursor.execute('SELECT * FROM habits')
        rows = self.cursor.fetchall()
        longest_streak = 0
        for row in rows:
            self.get_streak(row, longest_streak)
        return longest_streak

    def get_longest_streak_for_habit(self, name):
        """
        get the longest streak of a specific habit
        :param name:
        :return: longest_streak
        """
        self.cursor.execute('SELECT * FROM habits WHERE name = ?', (name,))
        row = self.cursor.fetchone()
        if not row:
            return 0
        longest_streak = 0
        self.get_streak(row, longest_streak)
        return longest_streak

