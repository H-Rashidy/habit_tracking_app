from datetime import date, timedelta


class Habit:
    def __init__(self, name: str, description: str = None, start_date: date = None, end_date: date = None,
                 frequency: str = None, progress: list = None):
        """
        initialize a habit object

        :param name: name of the habit
        :param description: description of the habit
        :param start_date: date the habit was started
        :param end_date: date the habit was ended
        :param frequency: frequency of the habit (daily, weekly, monthly)
        :param progress: list of dates the habit was completed
        """
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.progress = []

    def mark_complete(self, check_date: date):
        """
        mark a habit as complete on a given date
        :param check_date: date the habit was completed
        :return: None
        """
        if check_date not in self.progress:
            self.progress.append(check_date)
            self.progress.sort()  # sort the progress list in chronological order
            if self.check_streak():
                print("Streak!")
            else:
                print("Habit Breaker")

    def check_streak(self):
        """
        check if the habit is currently on a streak
        :return: True if the habit is on a streak, False otherwise
        """
        today = date.today()
        if self.frequency == 'daily' and today == self.progress[-1] + timedelta(days=1):
            return True
        elif self.frequency == 'weekly' and today == self.progress[-1] + timedelta(weeks=1):
            return True
        elif self.frequency == 'monthly' and today == self.progress[-1] + timedelta(months=1):
            return True
        return False
