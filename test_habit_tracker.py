import pytest
import sqlite3
from habit_tracker import Habit
from datetime import date
from db import HabitTracker
from habit_analyse import HabitAnalyser


@pytest.fixture
def create_habit():
    habit = Habit("Test habit", start_date=date(2020, 1, 1), frequency="daily")
    return habit


class TestHabit:
    def test_init(self):
        habit = Habit("Read", start_date=date(2020, 1, 1), frequency="daily")
        assert habit.name == "Read"
        assert habit.start_date == date(2020, 1, 1)
        assert habit.frequency == "daily"

    def test_mark_complete(self, create_habit):
        create_habit.mark_complete(date(2020, 1, 2))
        assert create_habit.progress == [date(2020, 1, 2)]

        create_habit.mark_complete(date(2020, 1, 3))
        assert create_habit.progress == [date(2020, 1, 2), date(2020, 1, 3)]

        create_habit.mark_complete(date(2020, 1, 5))
        assert create_habit.progress == [date(2020, 1, 2), date(2020, 1, 3), date(2020, 1, 5)]

    def test_check_streak(self, create_habit):
        create_habit.mark_complete(date(2023, 5, 8))
        assert create_habit.check_streak() == True


@pytest.fixture
def reset_db():
    """Drop and recreate the database"""
    print("Resetting database!")
    conn = sqlite3.connect('Test.db')
    conn.execute("DROP TABLE IF EXISTS habits")
    conn.execute("""
        CREATE TABLE habits (
            name text PRIMARY KEY, 
            description text,
            start_date date,
            end_date date, 
            frequency text,
            progress text
        )
    """)
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def tracker(reset_db):
    return HabitTracker(name='Test.db', isolation_level=None)


class TestHabitTracker:
    def test_init(self, tracker):
        assert isinstance(tracker.cursor, sqlite3.Cursor)
        assert tracker.conn.isolation_level is None

    def test_create_habit(self, tracker, reset_db):
        tracker.create_habit("Test 40", "Test habit", date(2020, 1, 1), date(2020, 1, 31), "daily")
        reset_db.commit()
        row = reset_db.execute("SELECT * FROM habits WHERE name='Test 40'")
        assert row.fetchone()

    def test_get_habit(self, tracker, reset_db):
        tracker.create_habit("Test 41", "Test habit", date(2020, 1, 1), date(2020, 1, 31), "daily")
        habit = tracker.get_habit("Test 41")
        assert habit.name == "Test 41"

    def test_get_tracker(self, tracker, reset_db):
        tracker.create_habit("Test 42", "Test habit", date(2020, 1, 1), date(2020, 1, 31), "daily")
        tracker.check_habit("Test 42", date(2020, 1, 5), True)
        row = tracker.get_tracker("Test")
        if row is not None:
            assert row[1] == "Test 42"
            assert row[2] == date(2020, 1, 5)
            assert row[3] == True

    def test_check_habit(self, tracker, reset_db):
        tracker.create_habit("Test 43", "Test habit", date(2020, 1, 1), date(2020, 1, 31), "daily")
        habit = tracker.check_habit("Test 43", date(2020, 1, 5), True)
        if habit is not None:
            assert habit.progress == [date(2020, 1, 5)]

    def test_delete_habit(self, tracker, reset_db):
        tracker.create_habit("Test 44", "Test habit", date(2020, 1, 1), date(2020, 1, 31), "daily")
        tracker.delete_habit("Test 44")
        new_row = reset_db.execute("SELECT * FROM habits WHERE name='Test'")
        assert new_row.fetchone() is None

    def test_update_habit(self, tracker, reset_db):
        tracker.create_habit("Test 45", "Test habit", date(2020, 1, 1), date(2020, 1, 31), "daily")
        reset_db.commit()
        tracker.update_habit("Test 45", "Updated habit", date(2020, 2, 1), date(2020, 2, 28), "weekly")
        reset_db.commit()
        row = reset_db.execute("SELECT * FROM habits WHERE name='Test 35'")
        if row.fetchone():
            result = row.fetchone()
            assert result[1] == "Updated habit"
            assert result[2] == date(2020, 2, 1)
            assert result[3] == date(2020, 2, 28)
            assert result[4] == "weekly"


@pytest.fixture
def habit_analyser(reset_db):
    analyser = HabitAnalyser(name='Test.db', isolation_level=None)
    setup_test_data(reset_db)
    return analyser


def setup_test_data(reset_db):
    reset_db.execute(
        'INSERT INTO habits (name, description, start_date, end_date, frequency, progress) VALUES ("read", "read 30 mins", "2020-01-01", "2020-01-05" , "daily", "[1, 1, 1, 1, 1]")')
    reset_db.commit()
    reset_db.execute(
        'INSERT INTO habits (name, description, start_date, end_date, frequency, progress) VALUES ("gym", "go to gym", "2020-01-06", "2020-02-14", "weekly", "[1, 1, 1, 1, 1]")')
    reset_db.commit()


class TestHabitAnalyser:
    def test_init(self, habit_analyser):
        assert isinstance(habit_analyser.cursor, sqlite3.Cursor)
        assert habit_analyser.conn.isolation_level is None

    def test_get_all_habits(self, habit_analyser):
        assert habit_analyser.get_all_habits() != []

    def test_get_habits_with_periodicity(self, habit_analyser):
        assert habit_analyser.get_habits_with_periodicity('daily') != []

    def test_get_longest_streak(self, habit_analyser):
        assert habit_analyser.get_longest_streak() > 0

    def test_get_longest_streak_for_habit(self, habit_analyser):
        assert habit_analyser.get_longest_streak_for_habit('gym') > 0
