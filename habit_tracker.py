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
        if not self.start_date:
            return False

        today = date.today()
        start_date = self.start_date

        # Get the number of days between the start date and today
        num_days = (today - start_date).days + 1

        if len(self.progress) == 0:
            return False

        if self.frequency == 'daily':
            last_completion = self.progress[-1]
            if (today - last_completion).days > 1:
                return False
            return last_completion == today - timedelta(days=len(self.progress) - 1)
        elif self.frequency == 'weekly':
            if len(self.progress) < 7:
                return False
            last_completion = self.progress[-1]
            if (today - last_completion).days > 7:
                return False
            week_start_date = today - timedelta(days=today.weekday())
            week_completion_dates = [d for d in self.progress if d >= week_start_date]
            return len(week_completion_dates) == len(set(week_completion_dates))
        elif self.frequency == 'monthly':
            if len(self.progress) < num_days:
                return False
            last_completion = self.progress[-1]
            if (today - last_completion).days > 30:
                return False
            month_start_date = today.replace(day=1)
            month_completion_dates = [d for d in self.progress if d >= month_start_date]
            return len(month_completion_dates) == len(set(month_completion_dates))
        else:
            raise ValueError("Invalid frequency")
