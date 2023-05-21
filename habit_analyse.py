from habit_tracker import Habit
import sqlite3


class HabitAnalyser:
    def __init__(self, name='main.db', isolation_level=None):
        """
        initialize a habit analyser object
        :param name: name of the database file
        : create a connection to the database
        : create a cursor object to execute SQL commands
        """
        self.conn = sqlite3.connect(name, isolation_level=isolation_level)
        self.cursor = self.conn.cursor()

    def retrieve_habit(self):
        """
        Get all habits from the database
        :return: List of Habit objects
        """
        habits = []
        self.cursor.execute('SELECT * FROM habits')
        rows = self.cursor.fetchall()
        for row in rows:
            name = row[1]
            description = row[2]
            start_date = row[3]
            end_date = row[4]
            frequency = row[5]
            progress = row[6]
            habit = Habit(name, description, start_date, end_date, frequency, progress)
            habits.append(habit)
        return habits

    def get_all_habits(self):
        """
        get all habits from the database
        :return: habit_names
        """
        habits = self.retrieve_habit()
        # Get a list of just the habit names
        habit_names = [h.name for h in habits]
        return habit_names

    def get_habits_with_periodicity(self, frequency):
        """
        get habits with a specific periodicity from the database
        :param frequency: periodicity of the habit
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
        for date in eval(row[5]):
            if date == row[3]:
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
        :return: max_streak
        """
        habits = self.get_all_habits()
        max_streak = 0
        for habit in habits:
            if isinstance(habit, Habit):
                progress = eval(habit.progress)
                current_streak = 0
                for mark in progress:
                    if mark == 1:
                        current_streak += 1
                    else:
                        current_streak = 0
                    max_streak = max(max_streak, current_streak)
            else:
                name = habit[0]
                progress_index = 0
                for i, field in enumerate(habit.split(',')):
                    if field == 'progress':
                        progress_index = i + 1
                        break
                habit = habit.split(',')
                progress = habit[progress_index]
                habit = Habit(name, progress=progress)
                current_streak = 0
                for mark in progress:
                    if mark == 1:
                        current_streak += 1
                    else:
                        current_streak = 0
                    max_streak = max(max_streak, current_streak)
        return max_streak

    def get_longest_streak_for_habit(self, name):
        """
        get the longest streak for a specific habit
        :param name: name of the habit
        :return: max_streak
        """
        habits = self.get_all_habits()
        habits = [h for h in habits if not isinstance(h, str)]
        if not habits:
            return 0
        habit = habits[0]
        progress = eval(habit.progress)

        max_streak = 0
        current_streak = 0
        for mark in progress:
            if mark == 1:
                current_streak += 1
            else:
                current_streak = 0
            max_streak = max(max_streak, current_streak)

        return max_streak

