from datetime import date
from db import HabitTracker
from habit_analyse import HabitAnalyser
import questionary


def cli():
    tracker = HabitTracker()
    analyser = HabitAnalyser()

    stop = False
    while not stop:
        questionary.print("Welcome to the Habit Tracker!")

        choice = questionary.select(
            "Wat would you like to do?",
            choices=["Add a habit",
                     "Delete a habit",
                     "Update a habit",
                     "Check a habit",
                     "Analyze a habit",
                     "View progress for a habit",
                     "Exit"]).ask()  # ask() returns the user's choice

        if choice == "Add a habit":
            name = questionary.text("Enter the habit name: ").ask()
            description = questionary.text("Enter habit description: ").ask()
            start_date = questionary.text("Enter start date (YYYY-MM-DD): ").ask()
            end_date = questionary.text("Enter end date (YYYY-MM-DD): ").ask()
            frequency = questionary.text("Enter frequency (daily/weekly/monthly): ").ask()
            tracker.create_habit(name, description, start_date, end_date, frequency)
            print(f"Habit '{name}' added.")

        elif choice == "Delete a habit":
            name = questionary.text("Enter habit name: ").ask()
            habit = tracker.get_habit(name)
            if habit is None:
                print(f"No habit found with name '{name}'.")
            tracker.delete_habit(name)
            print(f"Habit '{name}' deleted.")

        elif choice == "Update a habit":
            while True:
                name = questionary.text("Enter habit name: ").ask()
                habit = tracker.get_habit(name)
                if habit is None:
                    print(f"Habit '{name}' not found.")
                else:
                    description = questionary.text("What is the new description of the habit?").ask()
                    start_date = questionary.text("When does the habit start? (YYYY-MM-DD) ").ask()
                    end_date = questionary.text("When does the habit end? (YYYY-MM-DD) ").ask()
                    frequency = questionary.text("Enter frequency (daily/weekly/monthly): ").ask()
                    tracker.update_habit(name, description, start_date, end_date, frequency)
                    print(f"Habit '{name}' updated.")
                break

        elif choice == "Check a habit":
            name = questionary.text("Enter habit name: ").ask()
            event_date = date.today()
            completed = questionary.confirm("Did you complete the habit today?").ask()  # define completed variable
            tracker.check_habit(name, event_date, completed)  # pass completed variable as argument
            print(f"Habit '{name}' checked.")

        elif choice == "Analyze a habit":
            sub_choice = questionary.select(
                "What would you like to do?",
                choices=["Return a list of all currently tracked habits",
                         "Return a list of all habits with the same periodicity",
                         "Return the longest run streak of all defined habits",
                         "Return the longest run streak for a given habit"]).ask()
            if sub_choice == "Return a list of all currently tracked habits":
                habit_names = analyser.get_all_habits()
                if len(habit_names) == 0:
                    print("No habits currently tracked.")
                else:
                    print("Currently tracked habits:")
                    for name in habit_names:
                        print(name)
            elif sub_choice == "Return a list of all habits with the same periodicity":
                frequency = questionary.text("Enter frequency (daily/weekly/monthly): ").ask()
                matching_habits = analyser.get_habits_with_periodicity(frequency)
                if len(matching_habits) == 0:
                    print(f"No habits tracked with frequency '{frequency}'.")
                else:
                    print(f"Habits tracked with frequency '{frequency}':")
                    for habit in matching_habits:
                        print(habit.name)
            elif sub_choice == "Return the longest run streak of all defined habits":
                longest_streak = analyser.get_longest_streak()
                if longest_streak is None:
                    print("No habits currently tracked.")
                else:
                    print(f"Longest streak: {longest_streak}")
            elif sub_choice == "Return the longest run streak for a given habit":
                name = questionary.text("Enter habit name: ").ask()
                longest_streak = analyser.get_longest_streak_for_habit(name)
                if longest_streak is None:
                    print(f"No habit '{name}' currently tracked.")
                else:
                    print(f"Longest streak for habit '{name}': {longest_streak}")

        elif choice == "View progress for a habit":
            name = questionary.text("Enter habit name: ").ask()
            progress = tracker.get_tracker(name)
            if progress is None:
                print(f"No habit '{name}' currently tracked.")
            else:
                print(f"Progress for habit '{name}': {progress}")

        elif choice == "Exit":
            print("Goodbye!")
            stop = True


if __name__ == "__main__":
    cli()
